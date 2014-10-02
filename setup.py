#!/usr/bin/env python

# -----------------------------------------------------------------------------
# Copyright (c) 2013, The Qiita Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------

__version__ = "0.1.0-dev"

from setuptools import setup
from glob import glob


classes = """
    Development Status :: 4 - Beta
    License :: OSI Approved :: BSD License
    Topic :: Scientific/Engineering :: Bio-Informatics
    Topic :: Software Development :: Libraries :: Application Frameworks
    Topic :: Software Development :: Libraries :: Python Modules
    Programming Language :: Python
    Programming Language :: Python :: 2.7
    Programming Language :: Python :: Implementation :: CPython
    Operating System :: OS Independent
    Operating System :: POSIX :: Linux
    Operating System :: MacOS :: MacOS X
"""

long_description = """American Gut participant UI"""

classifiers = [s.strip() for s in classes.split('\n') if s]

setup(name='American Gut participant UI',
      version=__version__,
      long_description=long_description,
      license="BSD",
      description='American Gut Project',
      author="American Gut Project",
      author_email="mcdonadt@colorado.edu",
      url='http://www.microbio.me/AmericanGut',
      test_suite='nose.collector',
      packages=['amgut'],
      package_data={'amgut': [],
                    'amgut.lib': [],
                    'amgut.lib.data_access': [],
                    'amgut.handlers': []},
      extras_require={'test': ["nose >= 0.10.1", "pep8"]},
      install_requires=['psycopg2', 'tornado==3.1.1', 'WTForms==2.0.1',
                        'redis'],
      classifiers=classifiers
      )
