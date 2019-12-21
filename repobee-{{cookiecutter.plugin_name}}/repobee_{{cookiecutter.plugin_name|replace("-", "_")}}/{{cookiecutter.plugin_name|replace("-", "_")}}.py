"""Write your plugin in here!

.. module:: {{cookiecutter.plugin_name}}
    :synopsis: {{cookiecutter.short_description}}

.. moduleauthor:: {{cookiecutter.author}}
"""

import pathlib
import os

{% if cookiecutter.generate_advanced_task == "yes" %}import argparse
import configparser
import re
{% endif %}

import repobee_plug as plug

PLUGIN_NAME = "{{cookiecutter.plugin_name}}"
# CONFIG_SECTION is the same as PLUGIN_NAME, but with - characters replaced with _
# if PLUGIN_NAMES does not contain any - characters, CONFIG_SECTION is not needed
CONFIG_SECTION = "{{cookiecutter.plugin_name|replace("-", "_")}}" 

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

    @plug.repobee_hook
    def clone_task(self) -> plug.Task:
        """The clone_task hook executes after a student repository has been cloned,
        and the path to the student repo is passed to the ``act`` callback.

        Returns:
            A RepoBee Task to execute on cloned repos.
        """
        return self._create_task()


    @plug.repobee_hook
    def setup_task(self) -> plug.Task:
        """The setup_task hook executes on master repos before they are pushed to
        student repos in the ``setup`` and ``update`` commands.

        Returns:
            A RepoBee Task to execute on master repos before pushing to student
            repos.
        """
        return self._create_task()

    def _create_task(self):
        return plug.Task(
            act=self._act,
            add_option=self._add_option,
            handle_args=self._handle_args,
            handle_config=self._handle_config,
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
            "--{{cookiecutter.plugin_name|replace("-", "_")}}-pattern",
            help="A regex pattern to match against filenames. Only filenames "
            "that match this pattern will be displayed.",
            type=str,
            default=None,
        )

    def _handle_args(self, args: argparse.Namespace) -> None:
        """Handle parsed command line arguments.

        Args:
            args: Command line arguments that have been parsed and processed by
                RepoBee's CLI.
        """
        pattern_arg = args.{{cookiecutter.plugin_name|replace("-", "_")}}_pattern
        if pattern_arg is not None:
            self._pattern = pattern_arg

    def _handle_config(self, config_parser: configparser.ConfigParser) -> None:
        """Handle the config file.

        Args:
            config_parser: The parsed config file.
        """
        if CONFIG_SECTION not in config_parser:
            return

        self._pattern = config_parser.get(
            CONFIG_SECTION, "pattern", fallback=self._pattern
        )
{% endif %}
