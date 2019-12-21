from _repobee import plugin

from repobee_{{cookiecutter.plugin_name}} import {{cookiecutter.plugin_name}}


def test_register():
    """Just test that there is no crash"""
    plugin.register_plugins([{{cookiecutter.plugin_name|replace("-", "_")}}])
