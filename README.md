american-gut-web
================

The website for the American Gut Project participant portal

### Quick-start

- [OS X] install [Postgres.app](http://postgresapp.com/)
- [OS X] `brew install redis`
- `mkvirtualenv amgut`
- `workon amgut`
- `pip install -e .[test]` (this installs the all dependencies, including those
  in `extras_require`)
- `cp ag_config.txt.example amgut/ag_config.txt`
- set options in `amgut/ag_config.txt`
- to enable uuid v4 function in postgres:
  - `echo 'CREATE EXTENSION "uuid-ossp";' | psql`
- `./scripts/ag make test`
- `python amgut/webserver.py`
