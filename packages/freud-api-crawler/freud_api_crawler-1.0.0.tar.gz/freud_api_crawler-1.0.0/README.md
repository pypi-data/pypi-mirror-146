[![codecov](https://codecov.io/gh/acdh-oeaw/freud_api_crawler/branch/master/graph/badge.svg?token=7OBAOGEFTY)](https://codecov.io/gh/acdh-oeaw/freud_api_crawler)

# Freud API Crawler

A client to interact with freud-net API


## install

* create a virtual environment and install the package with `pip install freud_api_crawler` 
* provide FRD_USER (freud-net username) and FRD_PW (freud-net password) as environment varibles, e.g. by
  * create a file called `env.secret` to store you freud-net api credentials
  * run `./set_env_variables.sh` 

### example `env.secret`

```
FRD_USER=username
FRD_PW=password
```

## usage

### Download a Work

* `download_work -s . -w 2da622da-de12-46e4-bb1d-c9c4a7ae877e` 
* `-s` path to save the created files into; `.` will write the files into `./werke/...`
* `-w` the Drupal-API-ID of the Werk to process (see below on how to get those IDs)

## dev

* clone the repo
* create virtual env
* install dev-depenencies `pip install -r requirements_dev.txt`
* install the package (so you have the actual dependencies as well) `pip install -e .`

* run test with `coverage run -m pytest -v`
* create test-report `coverage report` or `coverage html`

## api-utils

### get work by title

https://www.freud-edition.net/jsonapi/node/werk?filter[field_titel.value]=%C3%9Cber%20den%20Traum
https://www.freud-edition.net/jsonapi/node/werk?filter[field_titel.value]=Über den Traum

### get manifestaion by node id

this ID can be taken from edit-url, e.g. https://www.freud-edition.net/node/51190/edit

https://www.freud-edition.net/jsonapi/node/manifestation?filter[drupal_internal__nid]=51190
