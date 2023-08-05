# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['info',
 'info.gianlucacosta.iris',
 'info.gianlucacosta.iris.io',
 'info.gianlucacosta.iris.scripts']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['rmheader = info.gianlucacosta.iris.scripts.rmheader:main',
                     'rmlicense = '
                     'info.gianlucacosta.iris.scripts.rmlicense:main',
                     'rmspaces = '
                     'info.gianlucacosta.iris.scripts.rmspaces:main']}

setup_kwargs = {
    'name': 'info.gianlucacosta.iris',
    'version': '4.0.1',
    'description': 'General-purpose library for Python',
    'long_description': "# Iris\n\n_General-purpose library for Python_\n\n---\n\n## Deprecation & namespace warning\n\n**Please, note**: Iris is now deprecated and should be used only to support ancient projects.\n\nFurthermore, for compatibility with Python's modern packaging system, please **delete from the file system every reference to its 3.x version** and use version 4.x instead.\n\n---\n\n## Introduction\n\nIris is a general-purpose, object-oriented and open source library for Python 3.\n\n## Modules\n\nAll the modules reside within the **info.gianlucacosta.iris** package and subpackages.\n\nIn particular:\n\n- **ioc**, featuring a simple IoC container, that supports transient and singleton objects out of the box and can be extended via OOP by introducing new registration kinds\n\n- **versioning**, introducing a Version class and a VersionDirectory, that, for example, can return the file having the latest version in a directory\n\n- **maven**, dealing with MavenArtifact (which describes the Maven properties of an artifact) and MavenRepository, to query a Maven repository using the concepts introduced in the versioning module\n\n- **rendering** abstracts the templating process by providing a Model class that can be easily reused with different rendering technologies\n\n- **vars** enables developers to create boolean variables (instances of Flag) whose value depends on the existence of underlying files - which can be useful in some situations where multiple technologies are involved\n\n- **io.utils**, contains generic I/O utilities\n\n- **io.tree** defines objects for operating on file trees\n\n## Installation\n\nIris can be installed via **pip**:\n\n> pip install info.gianlucacosta.iris\n",
    'author': 'Gianluca Costa',
    'author_email': 'gianluca@gianlucacosta.info',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/giancosta86/Iris',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
