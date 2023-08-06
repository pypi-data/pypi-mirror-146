# Sotero JDBC Dialect for SQLAlchemy

Sotero JDBC Driver integrates with Sotero Protect Platform to selectively encrypt/decrypt sensitive data stored in
relational databases.

## Installation

Installing the dialect is straightforward::

```
python3 -m pip install sqlalchemy-sotero
```

## Supported drivers

- PostgreSQL

## Pre-Requisite

In order to authenticate the JDBC driver client application with Sotero Platform,
you should have access to a Sotero Client Credentials file. If you don't have this file already,
please follow the instructions below.

- Login to Sotero Main API URL using Sotero admin username and password to get an access token
- POST a request to `<SOTERO_API_URL>/appclients/generate` endpoint with the access token
  in the authorization header and the body containing the name of your application.

```
Authorization: Bearer <the-access-token>
```

- Request body should contain the `name` of the application:

```
{
    "name":"Enter Your JDBC Application Name"
}
```

- The response will contain `client_id` and `private_key`:

```
{
    "client_id": "6f5010fc-9e13-41f8-b483-88527658bc81",
    "private_key": "MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCyKiGZq1mzXyqMYTPDNXfxiDJSk/yvNJX58Cd9A5QSEh6MOOu5LEcBig1e9jROGFpn+TqrycjNp4jEckTvcC1UjCfZ+o8Lxh6lMMW9leV4cr1r6ONiRs5Vrisv1tOBVkz+m4AqARjqcgejcM/iV5dIhZkm2OH1s00gmsLmqf7LfAmJl6tTkw2P7CW0nCWg4RGjcUYKmr43vViX1oqnO5uwxyXoZiM1cam2c7KrjYWs52cSrInkWfgWwwcMNf6vnGykNIgZPz3jf64h+rsiMZRz3Havs8NKSy8kSVFAmA1sIvzhDgOD/jRyfP2zdXjuy5qXMPQsfEA0w1nTmSL9xvGRAgMBAAECggEATMNkWL6AVo2BWpyi3c/SzwlcjUHf1Gl22QqFKRL6oFKYQNhhkBYovdwKaMjxvlg106iJv7c="
}
```

- Save the above response json in a file. This credentials file is required while using the Sotero JDBC driver

## Usage

Set a CLASSPATH environment variable for the Sotero driver and the driver for your database

`export CLASSPATH=<path>/sotero-jdbc-driver-1.2.0.jar:<path>/postgresql-42.3.1.jar`

or in Python application

`os.environ['CLASSPATH'] = "<path>/sotero-jdbc-driver-1.2.0.jar:<path>/postgresql-42.3.1.jar"`

### PostgreSQL:

```python
from sqlalchemy import create_engine

os.environ['CLASSPATH'] = "<path>/sotero-jdbc-driver-1.2.0.jar:<path>/postgresql-42.3.1.jar"

url = f'sotero+postgres://{username}:{password}@{sotero-api-url}?creds_file={creds-file-path}&dataset={sotero-dataset-id}'

conn = create_engine(url)
```

Note: In S4 platform <sotero-api-url> should point to your tenant API URL instead of the main API URL.

## Driver Options

Sotero driver options are specified as key=value pairs separated by &.

### Basic options

- `creds_file=<creds-file-path>` => JSON file containing the client_id and private_key
- `dataset=<sotero-dataset-id>` => Id of a dataset configured in the Sotero platform. The target driver class and JDBC url will be derived based on the dataset configuration
- `client_user=<dataset-userid>` => check the decrypt permissions using this value instead of the target database user id

### Controlling the driver behavior

By default, Sotero driver will encrypt the data inserting in to the database and optionally
decrypt data retrieving from the database if the user has decrypt permissions. This behavior
can be changed by specifying the optional mode parameter

- `mode=encrypt`&nbsp;&nbsp;=> perform encryption while querying non-encrypted database, no decryption is performed
- `mode=none`&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;=> perform no encryption or decryption
- `mode=protect`&nbsp;=> default behavior

## Testing

Read more information on deploying the package [here](https://devarea.com/deploying-a-new-python-package-to-pypi/)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -U pip setuptools twine wheel JayDeBeApi

python setup.py sdist
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
pip install -i https://testpypi.python.org/pypi  sqlalchemy-sotero --no-build-isolation --extra-index-url=https://test.pypi.org/simple/
```

## Deploy the package

```bash
twine upload dist/sqlalchemy_sotero-0.0.2.tar.gz
```
