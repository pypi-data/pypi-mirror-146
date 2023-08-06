# -*- coding: utf-8 -*-
import os
import logging

import yaml

logger = logging.getLogger(__name__)


class WrongConfigException(Exception):
    pass

template_path = lambda src: f'{src}/.template'
config_path = lambda src: f'{template_path(src)}/config.yaml'
default_path = lambda src: f'{template_path(src)}/default.yaml'

def load_config(src):
    if not os.path.exists(template_path(src)):
        logger.warning('No `.template` folder found, using empty config.')
        return {}

    if not os.path.exists(config_path(src)):
        logger.warning('No config file found, using empty config.')
        return {}

    with open(config_path(src), encoding='utf-8') as config_f:
        config = yaml.safe_load(config_f)
    config_default = config.get('default', {})

    if not os.path.exists(default_path(src)):
        logger.warning('No default file found.')
        default_values = config_default
    else:
        with open(default_path(src), encoding='utf-8') as defaults_f:
            default_values = yaml.safe_load(defaults_f)
        default_values.update(config_default)

    if default_values == {}:
        logger.warning('No default values provided.')

    return default_values, config

def unified_loop_config(config):
    ensure_folder_or_file(config)

    type_, path = get_type_and_path(config)

    if 'var' not in config:
        raise WrongConfigException('A `var` parameter is required for a loop config.')

    if 'item' not in config:
        if not config['var'].endswith('s'):
            raise WrongConfigException('The `var` parameter should end with an `s` if no `item` name is provided.')
        item = config['var'][:-1]
    else:
        item = config['item']

    transform = get_transform(path, config, item)

    return {
        'type': type_,
        'path': path,
        'transform': transform,
        'var': config['var'],
        'item': item,
        'excluded_values': config.get('exclude_values', []),
        'filters': config.get('filters', []),
        'tests': config.get('when', []),
        'loop': config.get('loop', []),
        'rename': config.get('rename', [])
    }

def unified_rename_config(config):
    ensure_folder_or_file(config)

    type_, path = get_type_and_path(config)

    if 'var' not in config and 'transform' not in config:
        logger.warning(f'Neither `var` nor `transform` were provided. No transformation to {type_} at {path}.')

    if 'var' in config and 'transform' in config:
        logger.warning('A `var` was provided together with a `transform` in a rename config. Only the latter will be used.')

    transform = get_transform(path, config, config.get('var', None))

    common_config = {
        'type': type_,
        'path': path,
        'transform': transform
    }

    return common_config if type_ == 'file' else { **common_config,
        'loop': config.get('loop', []),
        'rename': config.get('rename', [])
    }

def ensure_folder_or_file(config):
    if 'folder' in config and 'file' in config:
        raise WrongConfigException('A config cannot have both a `folder` or `file`.')
    if 'folder' not in config and 'file' not in config:
        raise WrongConfigException('A config cannot have neither a `folder` nor `file`.')

def get_type_and_path(config):
    type_ = 'folder' if 'folder' in config else 'file'
    path = config[type_]

    if type_ == 'file' and ('rename' in config or 'loop' in config):
        raise WrongConfigException(f'A file loop config cannot have a nested rename or loop (@ {path}).')

    return type_, path

def get_transform(path, config, var):
    transform = config.get('transform', path.split('/')[-1])
    if 'var' in config and 'transform' not in config:
        ext = '.'.join(transform.split('.')[1:])
        if len(ext) > 0:
            ext = '.' + ext
        transform = '{{ ' + var + ' }}' + ext
    return transform
