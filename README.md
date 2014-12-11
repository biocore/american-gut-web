american-gut-web
================

The website for the American Gut Project participant portal

### Quick-start

- [OS X] install [Postgres.app](http://postgresapp.com/)
- [OS X] `brew install redis`
- `mkvirtualenv amgut`
- `workon amgut`
- `python setup.py develop` (this gets you the dependencies from `setup.py`)
- `pip install -e .[test]` (this installs the test dependencies in
  `extras_require`)
- `cp ag_config.txt.example amgut/ag_config.txt`
- set options in `amgut/ag_config.txt`
- to enable uuid v4 function in postgres:
  - `echo 'CREATE EXTENSION "uuid-ossp";' | psql`
- `./scripts/ag make test`
- `python amgut/webserver.py`
