# -*- coding: ascii -*-
"""
package/install python-aedir
"""

import sys
import os
from setuptools import setup, find_packages

PYPI_NAME = 'aedir'

BASEDIR = os.path.dirname(os.path.realpath(__file__))

sys.path.insert(0, os.path.join(BASEDIR, PYPI_NAME))
import __about__

setup(
    name=PYPI_NAME,
    license=__about__.__license__,
    version=__about__.__version__,
    description='AE-DIR library',
    author=__about__.__author__,
    author_email=__about__.__mail__,
    maintainer=__about__.__author__,
    maintainer_email=__about__.__mail__,
    url='https://ae-dir.com/python.html',
    download_url='https://pypi.org/project/%s/#files' % (PYPI_NAME),
    project_urls={
        'Code': 'https://code.stroeder.com/AE-DIR/python-%s' % (PYPI_NAME),
        'Issue tracker': 'https://code.stroeder.com/AE-DIR/python-%s/issues' % (PYPI_NAME),
    },
    keywords=['LDAP', 'LDAPv3', 'OpenLDAP', 'AE-DIR', '\xC6-DIR'],
    packages=find_packages(exclude=['tests']),
    package_dir={'': '.'},
    package_data = {
        PYPI_NAME: ['py.typed'],
    },
    test_suite='tests',
    python_requires='>=3.6',
    include_package_data=True,
    data_files=[],
    install_requires=[
        'setuptools',
        'ldap0>=1.2.7',
    ],
    extras_require={
        'mail':  ['mailutil>=0.4.0'],
        'test': ['Jinja2'],
    },
    zip_safe=False,
)
