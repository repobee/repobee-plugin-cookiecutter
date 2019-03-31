from repomate import plugin

from repomate_{{cookiecutter.plugin_name|replace("-", "_")}} import {{cookiecutter.plugin_name|replace("-", "_")}}


def test_register():
    """Just test that there is no crash"""
    plugin.register_plugins([{{cookiecutter.plugin_name|replace("-", "_")}}])
