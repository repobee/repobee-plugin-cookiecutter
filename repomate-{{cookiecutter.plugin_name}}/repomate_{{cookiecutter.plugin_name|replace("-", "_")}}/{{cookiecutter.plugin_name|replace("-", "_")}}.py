"""Write your plugin in here!

This module comes with two example implementations of a hook, one wrapped in
a class and one as a standalone hook function.

.. module:: {{cookiecutter.plugin_name}}
    :synopsis: {{cookiecutter.short_description}}

.. moduleauthor:: {{cookiecutter.author}}
"""

# these two imports are just for the sample plugin, remove if not used!
import pathlib
import os
from typing import Union

# this import you'll need
import repomate_plug as plug

PLUGIN_NAME = '{{cookiecutter.plugin_name}}'


class ExamplePlugin(plug.Plugin):
    """Example plugin that implements the act_on_cloned_repo hook."""

    def act_on_cloned_repo(self,
                           path: Union[str, pathlib.Path], api) -> plug.HookResult:
        """List all files in a cloned repo.
        
        Args:
            path: Path to the student repo.
            api: An instance of :py:class:`repomate.github_api.GitHubAPI`.
        Returns:
            a plug.HookResult specifying the outcome.
        """
        path = pathlib.Path(path)
        filepaths = [
            str(p) for p in path.resolve().rglob('.')
            if '.git' not in str(p).split(os.sep)
        ]
        output = os.linesep.join(filepaths)
        return plug.HookResult(
            hook=PLUGIN_NAME, status=plug.Status.SUCCESS, msg=output)


@plug.repomate_hook
def act_on_cloned_repo(path: Union[str, pathlib.Path], api) -> plug.HookResult:
    """Return an error hookresult with a garbage message.
    
    Args:
        path: Path to the student repo.
            api: An instance of :py:class:`repomate.github_api.GitHubAPI`.
    Returns:
        a plug.HookResult specifying the outcome.
    """
    return plug.HookResult(
        hook=PLUGIN_NAME,
        status=plug.Status.ERROR,
        msg="This plugin is not implemented.")
