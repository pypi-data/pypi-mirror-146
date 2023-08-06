# -*- coding: utf-8 -*-
import os
import logging
from typing import Any
from collections.abc import Callable
from importlib.machinery import SourceFileLoader
from importlib.util import spec_from_loader, module_from_spec

import jinja2
from benedict import benedict

from .template_config import load_config, unified_loop_config, unified_rename_config, template_path, WrongConfigException


logger = logging.getLogger(__name__)

def template_string(
    str_: str,
    context: dict[str, Any]                   = None,
    filters: dict[str, Callable[[Any], Any]]  = None,
    tests:   dict[str, Callable[[Any], bool]] = None
) -> str:
    """This function templates a given string using jinja2 engine.

    Args:
        str_: The string to template.
        context: A dict with the context of the template.
        filters: A dict with filters to add to the template engine. Names as keys, functions as values.
        tests: A dict of tests to add to the template engine. Names as keys, functions as values.

    Returns:
        The templated string

    Examples:
       >>> from sonotoria import jinja
       >>> jinja.template_string('my {{ name }} is rich', context={'name': 'tailor'})
       my tailor is rich
    """
    context = context or {}

    # Somehow trailing line feed are removed by jinja2 readding them
    add_trail = '\n' if str_.endswith('\n') else ''

    env = jinja2.Environment()
    for name, filter_ in (filters or {}).items():
        env.filters[name] = filter_
    for name, test in (tests or {}).items():
        env.tests[name] = test
    try:
        return env.from_string(str_).render(**context) + add_trail
    except TypeError: # Yaml Objects
        return env.from_string(str_).render(**context.__dict__) + add_trail

def template_file(
    src: str,
    dest: str,
    context: dict[str, Any]                   = None,
    filters: dict[str, Callable[[Any], Any]]  = None,
    tests:   dict[str, Callable[[Any], bool]] = None
) -> str:
    """This function templates a given file using jinja2 engine.

    Args:
        src: The path to the file to template.
        dest: The path where to create the resulting templated file.
        context: A dict with the context of the template.
        filters: A dict with filters to add to the template engine. Names as keys, functions as values.
        tests: A dict of tests to add to the template engine. Names as keys, functions as values.

    Returns:
        Nothing

    Examples:
       >>> from sonotoria import jinja
       >>> jinja.template_file('mytemplate', 'templated', context={'name': 'tailor'})
    """
    with open(src, 'r', encoding='utf-8') as src_f:
        content = template_string(src_f.read(), context, filters, tests)

    with open(dest, 'w', encoding='utf-8') as dest_f:
        dest_f.write(content)

def template_folder(
    src: str,
    dest: str,
    context: dict[str, Any]                   = None,
    filters: dict[str, Callable[[Any], Any]]  = None,
    tests:   dict[str, Callable[[Any], bool]] = None
) -> str:
    """This function templates a given folder using jinja2 engine and configuration provided in this folder. Examples found in README.

    Args:
        src: The path to the folder to template.
        dest: The path where to create the resulting templated folder.
        context: A dict with the context of the template.
        filters: A dict with filters to add to the template engine. Names as keys, functions as values.
        tests: A dict of tests to add to the template engine. Names as keys, functions as values.

    Returns:
        Nothing

    Examples:
       >>> from sonotoria import jinja
       >>> jinja.template_folder('mytemplate', 'templated', context={'name': 'tailor'})
    """
    if not os.path.exists(f'{src}/.template'):
        raise WrongConfigException('No `.template` folder found.')

    default_context, config = load_config(src)

    context = { **default_context, **(context or {}) }

    filters = load_filters(src, filters, context)
    tests = load_tests(src, tests, context)

    excluded = config.get('exclude', []) + ['.template']
    env = {
        'context': context,
        'filters': filters,
        'tests': tests,
        'excluded': excluded,
        'excluded_paths': [f'{src}/{excluded_path}' for excluded_path in excluded]
    }

    if 'template' not in config:
        logger.warning('No template config found.')
    else:
        handle_node(config['template'], src, dest, env)

def without_excluded(env):
    return {
        'context': env['context'],
        'filters': env['filters'],
        'tests': env['tests']
    }

def handle_node(node_config, src, dest, env):
    handled_paths = []
    if 'loop' in node_config:
        for loop in node_config['loop']:
            handled_paths += handle_loop(loop, src, dest, env)
    if 'rename' in node_config:
        for rename in node_config['rename']:
            handled_paths += handle_rename(rename, src, dest, env)

    paths_to_handle = unhandled_paths(src, handled_paths, env['excluded_paths'])
    for path in paths_to_handle:
        path_dest = path.replace(src, dest)
        if os.path.isdir(path):
            os.mkdir(path_dest)
        if os.path.isfile(path):
            template_file(path, path_dest, **without_excluded(env))
        handled_paths.append(path)

    return handled_paths

def unhandled_paths(root, handled_paths, excluded_paths):
    paths = []
    for rootdir, dirs, files in os.walk(root):
        for file_ in files:
            paths.append(os.path.join(rootdir, file_))
        for subdir in dirs:
            paths.append(os.path.join(rootdir, subdir))

    return [path for path in paths if is_unhandled(path, paths, handled_paths, excluded_paths)]

def is_unhandled(path, paths, handled_paths, excluded_paths):
    return not any(otherpath.startswith(path) and otherpath != path for otherpath in paths)\
           and not any(path.startswith(excluded_path) for excluded_path in excluded_paths)\
           and path not in handled_paths

def handle_rename(rename, src, dest, env):
    config = unified_rename_config(rename)
    handled_paths = [config['path']]

    folder_path = '/'.join(config['path'].split('/')[:-1])

    src_path = f'{src}/{config["path"]}'
    dest_path = '/'.join((dest, folder_path, template_string(config['transform'], **without_excluded(env))))

    if src_path not in env['excluded']:

        if config['type'] == 'file':
            template_file(src_path, dest_path, **without_excluded(env))
            handled_paths.append(src_path)
        if config['type'] == 'folder':
            os.mkdir(dest_path)
            handled_paths.append(src_path)
            handled_paths += handle_node(config, src_path, dest_path, env)

    return handled_paths

def handle_loop(loop, src, dest, env):
    config = unified_loop_config(loop)
    handled_paths = [config['path']]

    context = benedict(env['context'])

    if config['var'] not in context:
        raise WrongConfigException(f'The variable {config["var"]} does not exist in the context.')

    src_path = f'{src}/{config["path"]}'
    local_env = lambda item: {
        'context': {config['item']: item, **env['context']},
        'filters': env['filters'],
        'tests': env['tests']
    }
    dest_path = lambda item: '/'.join((
        dest,
        '/'.join(config['path'].split('/')[:-1]),
        template_string(config['transform'], **local_env(item))
    ))

    if src_path not in env['excluded']:

        items = context[config['var']]
        for test in config['tests']:
            items = [item for item in items if env['tests'][test](item)]
        items = [item for item in items if item not in config['excluded_values']]
        for filter_ in config['filters']:
            items = env['filters'][filter_](items)

        if config['type'] == 'file':
            for item in items:
                template_file(src_path, dest_path(item), **local_env(item))
                handled_paths.append(src_path)
        if config['type'] == 'folder':
            for item in items:
                local_dest = dest_path(item)
                os.mkdir(local_dest)
                handled_paths.append(src_path)
                handled_paths += handle_node(config, src_path, local_dest, {**env, **local_env(item)})

    return handled_paths

def load_filters(src, filters, context):
    module = load_funcs_module(src, 'filters')
    filters = { **module.get_filters(context), **(filters or {}) }
    if len(filters) == 0:
        logger.warning('No filters loaded.')
    return filters

def load_tests(src, tests, context):
    module = load_funcs_module(src, 'tests')
    tests = { **module.get_tests(context), **(tests or {}) }
    if len(tests) == 0:
        logger.warning('No tests loaded.')
    return tests

def load_funcs_module(src, type_):
    path_to_funcs = f'{template_path(src)}/{type_}.py'
    module_name = f'{type_}_specs'

    if not os.path.exists(path_to_funcs):
        logger.warning(f'No {type_} file found.')

    loader = SourceFileLoader(module_name, path_to_funcs)
    spec = spec_from_loader(module_name, loader)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
