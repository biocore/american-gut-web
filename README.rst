american-gut-web
================
|Build Status| |Coverage Status|

The website for the American Gut Project participant portal

Installation Guide for OSX
--------------------------

First install and run `Postgres.app <http://postgresapp.com/>`_. Make sure that the path is configured properly so add the following to your `.bash_profile`::

   export PATH=$PATH:/Applications/Postgres.app/Contents/Versions/9.4/bin

   
Now setup a new conda environment via `miniconda <http://conda.pydata.org/miniconda.html>`_::

   conda create -n amgut python=2.7 tornado psycopg2
   source activate amgut
   
Next install and start Redis via conda. ::

   conda install redis
   redis-server

Now by forking, clone and install the repository.  This will also install
dependencies included in `extras_require`::

   git clone https://github.com/YOUR-GITHUB-USERNAME/american-gut-web.git
   pip install -e .[test]

And copy over the configuration file::

   cp ag_config.txt.example amgut/ag_config.txt

To configure the webserver.  Feel free to fill in entries for `POSTGRES` and `REDIS`.  The default user for `POSTGRES` is `postgres`.

To enable uuid v4 function in postgres::

   echo 'CREATE EXTENSION "uuid-ossp";' | psql

Make sure that all of your permissions are set correctly.  The following can be run with a user named `postgres`

```
CREATE USER postgres;
ALTER ROLE postgres SUPERUSER;
```

See `CREATE USER <https://www.postgresql.org/docs/9.5/static/sql-createuser.html>`_ and `ALTER USER <http://www.postgresql.org/docs/9.4/static/sql-alterrole.html>`_ for more details.

Finally create the database and populate it with test data, then launch the website::

   ./scripts/ag make test
   python amgut/webserver.py
   
Navigating to localhost:8888 will now show the american gut site. Try using `tst_ACJUJ` as the username to log in. All test kits have `test` as their password.

.. |Build Status| image:: https://travis-ci.org/biocore/american-gut-web.svg?branch=master
   :target: https://travis-ci.org/biocore/american-gut-web
.. |Coverage Status| image:: https://coveralls.io/repos/biocore/american-gut-web/badge.png
   :target: https://coveralls.io/r/biocore/american-gut-web
