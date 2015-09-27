american-gut-web
================
|Build Status| |Coverage Status|

The website for the American Gut Project participant portal

Installation Guide for OSX
--------------------------

First install [Postgres.app](http://postgresapp.com/)
Make sure that the path is configured properly so add the following to your `.profile` file
```export PATH=$PATH:/Applications/Postgres.app/Contents/Versions/9.4/bin```

Next install Redis.  To install via [Homebrew](http://brew.sh/) do

   brew install redis
   
Now setup an virtual environment via [virtualenv](https://virtualenvwrapper.readthedocs.org/en/latest/)


   mkvirtualenv amgut
   workon amgut

Now install all of the dependencies.  This will also install dependencies included in `extras_require`

   pip install -e .[test]

And copy over the configuration file

   cp ag_config.txt.example amgut/ag_config.txt

To configure some of the configurations.  Namely, make sure to fill in entries for `DATABASE`.

To enable uuid v4 function in postgres:

   echo 'CREATE EXTENSION "uuid-ossp";' | psql

Make sure that all of your permissions are set correctly.  See [ALTER USER](http://www.postgresql.org/docs/9.4/static/sql-alterrole.html)

Finally run the tests to populate the databases and launch the website

   ./scripts/ag make test
   python amgut/webserver.py

.. |Build Status| image:: https://travis-ci.org/biocore/american-gut-web.svg?branch=master
   :target: https://travis-ci.org/biocore/american-gut-web
.. |Coverage Status| image:: https://coveralls.io/repos/biocore/american-gut-web/badge.png
   :target: https://coveralls.io/r/biocore/american-gut-web
