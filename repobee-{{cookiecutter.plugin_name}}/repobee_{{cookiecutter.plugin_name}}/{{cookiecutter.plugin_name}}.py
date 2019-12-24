"""Write your plugin in here!

.. module:: {{cookiecutter.plugin_name}}
    :synopsis: {{cookiecutter.short_description}}

.. moduleauthor:: {{cookiecutter.author}}
"""

import pathlib
import os

{% if cookiecutter.generate_advanced_task == "yes" %}import argparse
import configparser
import re{% endif %}
{% if cookiecutter.generate_advanced_extension_command == "yes" or cookiecutter.generate_basic_extension_command == "yes" %}import argparse
import configparser
from typing import List, Mapping, Optional{% endif %}

import repobee_plug as plug

PLUGIN_NAME = "{{cookiecutter.plugin_name}}"

{% if cookiecutter.generate_basic_task == "yes" %}# Basic Task plugin start
def act(path: pathlib.Path, api: plug.API):
    """List all files in the repository at path.

    Args:
        path: Path to a repo.
        api: An instance of :py:class:`repobee_plug.API`.
    Returns:
        a plug.HookResult specifying the outcome.
    """
    filepaths = [
        str(p) for p in path.resolve().rglob("*") if ".git" not in str(p).split(os.sep)
    ]
    output = os.linesep.join(filepaths)
    return plug.HookResult(hook=PLUGIN_NAME, status=plug.Status.SUCCESS, msg=output,)


# As listing files is not dependent on the type of the repo, we can add it both
# as a clone task and as a setup task.
@plug.repobee_hook
def clone_task() -> plug.Task:
    """The clone_task hook executes after a student repository has been cloned,
    and the path to the student repo is passed to the ``act`` callback.

    Returns:
        A RepoBee Task to execute on cloned repos.
    """
    return plug.Task(act=act)


@plug.repobee_hook
def setup_task() -> plug.Task:
    """The setup_task hook executes on master repos before they are pushed to
    student repos in the ``setup`` and ``update`` commands.

    Returns:
        A RepoBee Task to execute on master repos before pushing to student
        repos.
    """
    return plug.Task(act=act)
# Basic Task plugin end
{% endif %}

{% if cookiecutter.generate_advanced_task == "yes" %}class AdvancedExamplePlugin(plug.Plugin):
    """An advanced example Task plugin that in addition to acting on a
    repository also adds command line options and uses the config file.
    """

    def __init__(self):
        """Set default values for configuration options."""
        self._pattern = None

    def clone_task(self) -> plug.Task:
        """The clone_task hook executes after a student repository has been cloned,
        and the path to the student repo is passed to the ``act`` callback.

        Returns:
            A RepoBee Task to execute on cloned repos.
        """
        return self._create_task()

    def setup_task(self) -> plug.Task:
        """The setup_task hook executes on master repos before they are pushed to
        student repos in the ``setup`` and ``update`` commands.

        Returns:
            A RepoBee Task to execute on master repos before pushing to student
            repos.
        """
        return self._create_task()

    def config_hook(self, config_parser: configparser.ConfigParser) -> None:
        """Handle the config file. The config hook is always invoked before any
        of the Task hooks are invoked, so the side effects from this hook can
        be used in e.g. the ``add_option`` callback.

        Args:
            config_parser: The parsed config file.
        """
        if PLUGIN_NAME not in config_parser:
            return

        self._pattern = config_parser.get(
            PLUGIN_NAME, "pattern", fallback=self._pattern
        )

    def _create_task(self):
        return plug.Task(
            act=self._act,
            add_option=self._add_option,
            handle_args=self._handle_args,
        )

    def _act(self, path: pathlib.Path, api: plug.API) -> plug.HookResult:
        """List all files in the repository at path.

        Args:
            path: Path to a repo.
            api: An instance of :py:class:`repobee_plug.API`.
        Returns:
            a plug.HookResult specifying the outcome.
        """
        filepaths = [
            str(p)
            for p in path.resolve().rglob("*")
            if ".git" not in str(p).split(os.sep)
            and (self._pattern is None or re.match(self._pattern, p.name))
        ]
        output = os.linesep.join(filepaths)
        return plug.HookResult(
            hook=PLUGIN_NAME,
            status=plug.Status.SUCCESS,
            msg=output,
            # the data attribute is optional, it is included in the data
            # that's saved in the hook results JSON file if you provide the
            # option `--hook-results-file PATH`
            data={"paths": filepaths},
        )

    def _add_option(self, parser: argparse.ArgumentParser) -> None:
        """Add the `--{{cookiecutter.plugin_name}}-pattern` command line option.

        Args:
            parser: An argument parser.
        """
        # note that options that are added to an existing parser should always
        # be prefixed with the name of the plugin
        parser.add_argument(
            "--{{cookiecutter.plugin_name}}-pattern",
            help="A regex pattern to match against filenames. Only filenames "
            "that match this pattern will be displayed.",
            type=str,
            required=self._pattern is None, # required if not configured
            default=self._pattern,
        )

    def _handle_args(self, args: argparse.Namespace) -> None:
        """Handle parsed command line arguments.

        Args:
            args: Command line arguments that have been parsed and processed by
                RepoBee's CLI.
        """
        self._pattern = args.{{cookiecutter.plugin_name}}_pattern
{% endif %}

{% if cookiecutter.generate_basic_extension_command == "yes" %}
def callback(
    args: argparse.Namespace, api: Optional[plug.API]
) -> Optional[Mapping[str, List[plug.Result]]]:
    """A hello world callback function.

    Args:
        args: Parsed and processed args from the RepoBee CLI.
        api: A platform API instance (but expected to be None here).
    Returns:
        A mapping (str -> List[plug.Result]) that RepoBee's CLI can use for
        output.
    """
    # do whatever you want to do!
    return {
        PLUGIN_NAME: [plug.Result(
            name=PLUGIN_NAME, status=plug.Status.SUCCESS, msg="Hello, world!"
        )]
    }

@plug.repobee_hook
def create_extension_command() -> plug.ExtensionCommand:
    """Create an extension command with no arguments.

    Returns:
        The extension command to add to the RepoBee CLI.
    """
    return plug.ExtensionCommand(
        parser=plug.ExtensionParser(), # empty parser
        name="example-command",
        help="An example command.",
        description="An example extension command.",
        callback=callback,
    )
{% endif %}

{% if cookiecutter.generate_advanced_extension_command == "yes" %}
class AdvancedExtensionCommand(plug.Plugin):
    """An advanced extension command with all of the features, including
    command line options and configuration file options.

    The command can be configured by adding the [{{cookiecutter.plugin_name}}]
    section to the config file, and using the "name" and "age" options. For
    example:

    .. code-block:: none

        [{{cookiecutter.plugin_name}}]
        name = Some cool name
        age = 38
    """

    def __init__(self):
        self._name = None
        self._age = None

    def _callback(
        self, args: argparse.Namespace, api: plug.API
    ) -> Optional[Mapping[str, List[plug.Result]]]:
        """A callback function that does nothing useful.

        Args:
            args: Parsed and processed args from the RepoBee CLI.
            api: A platform API instance.
        Returns:
            A mapping (str -> List[plug.Result]) that RepoBee's CLI can use for
            output.
        """
        # do whatever you want to do!
        return {
            PLUGIN_NAME: [plug.Result(
                name=PLUGIN_NAME, status=plug.Status.SUCCESS, msg=str(args)
            )]
        }

    def config_hook(self, config_parser: configparser.ConfigParser) -> None:
        """Hook into the configuration file parsing.

        Args:
            config_parser: A configuration parser.
        """
        if PLUGIN_NAME not in config_parser:
            return

        self._name = config_parser.get(PLUGIN_NAME, "name", fallback=self._name)
        self._age = config_parser.get(PLUGIN_NAME, "age", fallback=self._age)

    def create_extension_command(self) -> plug.ExtensionCommand:
        """Create an extension command.

        Returns:
            The extension command to add to the RepoBee CLI.
        """
        parser = plug.ExtensionParser()
        parser.add_argument(
            "-n",
            "--name",
            help="Your name.",
            type=str,
            required=self._name is None,
            default=self._name
        )
        parser.add_argument(
            "-a",
            "--age",
            help="Your age.",
            type=int,
            default=self._age,
        )
        return plug.ExtensionCommand(
            parser=parser,
            name="example-command",
            help="An example command.",
            description="An example extension command.",
            callback=self._callback,
            requires_api=True,
            requires_base_parsers=[
                plug.BaseParser.REPO_NAMES,
                plug.BaseParser.STUDENTS,
            ],
        )
{% endif %}
