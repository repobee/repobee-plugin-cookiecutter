import re
import sys


def check_plugin_name(plugin_name):
    plugname_regex = r"^[a-zA-Z][a-zA-Z0-9]*$"

    if not re.match(plugname_regex, plugin_name):
        return [
            "ERROR: {} is not a valid plugin name. Please use a "
            "name starting with an alphabetical character, followed "
            "by any amount of alphanumerical characters.".format(plugin_name)
        ]
    return []


def check_not_duplicate_task(basic_task, advanced_task):
    if basic_task == advanced_task == "yes":
        return [
            "ERROR: You can either generate a basic task or an advanced "
            "task, not both!"
        ]
    return []


def check_not_duplicate_extension(basic_extension, advanced_extension):
    if basic_extension == advanced_extension == "yes":
        return [
            "ERROR: You can either generate a basic extension command or an "
            "advanced extension command, not both!"
        ]
    return []


def main():
    plugin_name = "{{ cookiecutter.plugin_name }}"
    basic_task = "{{ cookiecutter.generate_basic_task }}"
    advanced_task = "{{ cookiecutter.generate_advanced_task }}"
    basic_extension = "{{ cookiecutter.generate_basic_extension_command }}"
    advanced_extension = "{{ cookiecutter.generate_advanced_extension_command }}"

    errors = []
    errors += check_plugin_name(plugin_name)
    errors += check_not_duplicate_task(basic_task, advanced_task)
    errors += check_not_duplicate_extension(basic_extension, advanced_extension)

    if errors:
        print("\n".join(errors))
        sys.exit(1)


if __name__ == "__main__":
    main()
