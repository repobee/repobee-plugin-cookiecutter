# repobee-plugin-cookiecutter
This is a simple `cookiecutter` template for
[RepoBee](https://github.com/repobee/repobee) plugins. It should provide you
with everything you need to quickly write a plugin.

## Requirements
The only requirement for using this template is to have
[cookiecutter](https://github.com/audreyr/cookiecutter) installed. It's on PyPi,
so you can install it with `pip install cookiecutter` (or whichever variation
works for you).

## Quick-use
1. Execute `python3 -m cookiecutter gh:repobee/repobee-plugin-cookiecutter`
2. Complete the setup.
3. You should now have a directory called `repobee-<plugin_name>` in the
   current working directory.

Optionally, you may also install the local plugin with RepoBee's distribution.
Run `repobee plugin install --local /path/to/repobee-<plugin_name>` to install
the plugin locally. This creates an editable install of the package, such that
you can keep developing it and the changes will immediately be reflected in
your RepoBee dist install. Note that major changes such as update requirements
and version increments requires a reinstall of the plugin.

## Tutorial
For an in-depth tutorial on creating plugins, see the
[Creating plugins docs](https://repobee.readthedocs.io/en/latest/repobee_plug/creating_plugins.html).
