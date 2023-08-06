# -*- coding: ascii -*-
"""
package/install slapdsock
"""

import sys
import os
from setuptools import setup, find_packages

PYPI_NAME = 'slapdsock'

BASEDIR = os.path.dirname(os.path.realpath(__file__))

sys.path.insert(0, os.path.join(BASEDIR, PYPI_NAME))
import __about__

setup(
    name=PYPI_NAME,
    license=__about__.__license__,
    version=__about__.__version__,
    description='Module package for back-sock listeners for OpenLDAP',
    author=__about__.__author__,
    author_email=__about__.__mail__,
    maintainer=__about__.__author__,
    maintainer_email=__about__.__mail__,
    url='https://code.stroeder.com/pymod/python-slapdsock',
    download_url='https://pypi.python.org/pypi/%s/' % (PYPI_NAME),
    project_urls={
        'Code': 'https://code.stroeder.com/pymod/python-%s' % (PYPI_NAME),
        'Issue tracker': 'https://code.stroeder.com/pymod/python-%s/issues' % (PYPI_NAME),
    },
    keywords=[
        'LDAP',
        'OpenLDAP',
        'slapd-sock',
        'back-sock',
    ],
    packages=find_packages(exclude=['tests']),
    package_dir={'': '.'},
    test_suite='tests',
    python_requires='>=3.6',
    include_package_data=True,
    data_files=[],
    install_requires=[
        'setuptools',
        'ldap0>=1.2.1',
    ],
    zip_safe=True,
)
