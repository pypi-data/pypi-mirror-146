import argparse
import os
import re
import sys
import subprocess
from datetime import datetime


if sys.version_info[0] < 3:
    input_ = raw_input  # Python2.7
elif sys.version_info[0] < 4:
    input_ = input  # Python3.+


__TEMPLATE_DIR__ = 'templates'
RESOURCES_OF_TEMPLATE_PROJECT, _ = os.path.split(os.path.abspath(__file__))
__REMOVED_FILES__ = ['empty']
__IGNORE_FILES_TEMPLATE__ = ['.+\.json$', '^mobio_exception.+']
__DEPENDENCIES_FILE__ = 'requirements.txt'


def _camel_to_snake(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def _snake_to_camel(name):
    name = ''.join(word.title() for word in name.split('_'))
    return name


def _camel_to_kebab(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1-\2', name).lower()


def _is_yes(user_input):
    return user_input.lower() in ('yes', 'y')


def _get_input(key, regex=None, requirements=None):
    user_input = input_('%s: ' % key) or ''
    if regex:
        match = re.match(regex, user_input)
        if not match or match.group(0) != user_input:
            print('Invalid input. %s' % requirements)
            print('')
            return _get_input(key, regex, requirements)
    return user_input


def _get_user_inputs():

    name = _get_input('project_name(CapitalizeWord, ex: JourneyBuilder)')
    description = _get_input('project_description')
    port = _get_input('project_port(default: 11000)')
    if not port:
        port = '11000'

    print('')
    print('Setup overview')
    print('--------------')
    print('Project name: %s' % name)
    print('Description: %s' % description)
    print('Port: %s' % port)
    print('')
    correct = _is_yes(_get_input('Is this correct?(y/n)'))
    if not correct:
        print()
        return _get_user_inputs()
    return name, description, port


def _setup(name, description, port, args=argparse.Namespace()):
    project_name_camel = name
    project_name_snake_lowercase = _camel_to_snake(name)
    project_name_snake_uppercase = project_name_snake_lowercase.upper()
    project_name_kebab_lowercase = _camel_to_kebab(name)
    project_name_kebab_uppercase = project_name_kebab_lowercase.upper()
    date_created = datetime.now().strftime("%Y/%m/%d")
    project_path = os.path.join(os.getcwd(), project_name_camel)

    replace_options = {
        '{#PROJECT_NAME_CAMEL#}': project_name_camel,
        '{#PROJECT_DESC#}': description,
        '{#PROJECT_PORT#}': port,
        '{#DATE_CREATED#}': date_created,
        '{#PROJECT_NAME_SNAKE_LOWERCASE#}': project_name_snake_lowercase,
        '{#PROJECT_NAME_SNAKE_UPPERCASE#}': project_name_snake_uppercase,
        '{#PROJECT_PATH#}': project_path,
        '{pymobio}': 'py',
        '{#PROJECT_NAME_KEBAB_LOWERCASE#}': project_name_kebab_lowercase,
        '{#PROJECT_NAME_KEBAB_UPPERCASE#}': project_name_kebab_uppercase,
        '{#EMPTY#}': '{}',
    }

    dest_dir = project_path
    os.makedirs(dest_dir, exist_ok=True)
    source_dir = os.path.join(RESOURCES_OF_TEMPLATE_PROJECT, __TEMPLATE_DIR__)

    for (path, directories, filenames) in os.walk(source_dir):
        relative_path = path[len(source_dir + '/'):]
        os.makedirs(os.path.join(dest_dir, relative_path), exist_ok=True)
        for filename in filenames:
            source = os.path.join(path, filename)
            # print('-------------')
            # print(filename)
            _process_file(source, relative_path, filename, dest_dir, replace_options)

    python_path = sys.executable
    create_venv = _get_input("create venv?(y/n)")
    if create_venv == 'y' or create_venv == 'Y':
        venv_path = os.path.join(project_path, 'venv')
        subprocess.run([python_path, '-m', 'venv', venv_path])
        subprocess.run([os.path.join(venv_path, 'bin', 'pip'),
                        'install', '-r',
                        os.path.join(project_path, __DEPENDENCIES_FILE__)])


def _process_file(source, relative_path, filename, dest_dir, replace_options):
    if filename in __REMOVED_FILES__:
        return

    with open(source, 'rt') as fin:
        source_code = fin.read()

    filename = _replace(filename, replace_options)
    dest = os.path.join(dest_dir, relative_path, filename)

    is_ignore = False
    for pattern in __IGNORE_FILES_TEMPLATE__:
        if re.match(pattern, filename):
            is_ignore = True
            break

    if not is_ignore:
        # print('=====')
        # print('source_code: %s' % source_code)
        source_code = _replace(source_code, replace_options)

    with open(dest, 'w') as fout:
        fout.write(source_code)


def _replace(text, options):
    for k,v in options.items():
        text = text.replace(k, v)
    return text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-y', '--yes', action='store_true',
                        help="Say 'yes' to all prompts")
    parser.add_argument('-f', '--force', action='store_true',
                        help="Force remove exist directory")
    args = parser.parse_known_args()[0]

    defaults = ('JourneyBuilder', 'desc', '11000')
    inputs = defaults if args.yes else _get_user_inputs()
    _setup(*inputs, args=args)


if __name__ == '__main__':
    main()
