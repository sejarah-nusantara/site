# Testing

Tests depend on a large number of services running


You must start:


* The server on port 8000, with `bin/django runserver`
* The repository must run on port `5000`.  See https://github.com/sejarah-nusantara/repository for instructions.


Now you can run all tests by running:

```sh
bin/django test  -v 2 -x --failed --settings=project.settings_test dasa
bin/django test --settings=project.settings_test apps/dasa/tests/test_auth # run a specific test
```
