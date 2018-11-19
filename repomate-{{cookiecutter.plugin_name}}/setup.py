from setuptools import setup, find_packages
from repomate_{{cookiecutter.plugin_name}} import __version__

with open('README.md', mode='r', encoding='utf-8') as f:
    readme = f.read()

test_requirements = [
    'pytest',
]
required = ['repomate-plug']

setup(
    name='repomate-{{cookiecutter.plugin_name}}',
    version=__version__,
    description='{{cookiecutter.short_description}}',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='{{cookiecutter.author}}',
    author_email='{{cookiecutter.email}}',
    url=
    'https://github.com/{{cookiecutter.github_username}}/repomate-{{cookiecutter.plugin_name}}',
    download_url=
    'https://github.com/{{cookiecutter.github_username}}/repomate-{{cookiecutter.plugin_name}}/archive/v{}.tar.gz'.format(__version__),
    license='MIT',
    packages=find_packages(exclude=('tests', 'docs')),
    tests_require=test_requirements,
    install_requires=required,
    extras_require=dict(TEST=test_requirements),
    include_package_data=True,
    zip_safe=False)
