#!/usr/bin/env python

# -----------------------------------------------------------------------------
# Copyright (c) 2013, The Qiita Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------

from setuptools import setup
from glob import glob

__version__ = "0.1.0-dev"

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
      package_data={'amgut': [
          'static/css/*.css', 'static/img/*.*', 'static/js/*.js',
          'static/vendor/css/*.css', 'static/vendor/css/*.png',
          'amgut/static/vendor/css/ui-lightness/*.css',
          'amgut/static/vendor/css/ui-lightness/images/*.png',
          'static/vendor/data/*', 'static/vendor/js/*.js',
          'static/vendor/licences/*', 'db/*.*', 'db/patches/*.sql',
          'handlers/*', 'lib/*.*', 'lib/data_access/*.*',
          'lib/data_access/test/*', 'lib/locale_data/*',
          'templates/*.html', 'test/*.py'
      ]},
      scripts=glob('scripts/*'),
      extras_require={
          'test': [
              'mock',
              'nose >= 0.10.1',
              'pep8',
              'flake8'
          ]
      },
      install_requires=[
          'click==3.3',
          'future==0.13.1',
          'open-humans-tornado-oauth2==2.1.0',
          'psycopg2',
          'pycrypto==2.6.1',
          'bcrypt',
          'redis',
          'requests',
          'tornado==4.4.2',
          'WTForms==2.0.1',
          'natsort',
          'pillow'
      ],
      classifiers=classifiers)
