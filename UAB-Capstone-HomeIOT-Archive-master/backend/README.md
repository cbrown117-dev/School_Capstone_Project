# HomeIOT REST API

This REST API is designed with Python, Flask, and Flask-RESTplus to aid in API documentation via Swagger.

## Python3 Dependencies
A quick list of dependencies are specified in the Pipfile for use with `pipenv`. We use pipenv to ensure we all have
the same dependencies througout our development environments.

First, ensure your installation of python3.6/3.7 has pipenv:
```bash
python3/python -m pip install pipenv
```

Then, install the dependencies:
```bash
python3/python -m pipenv install
```

## Running the app

Before running the API, we must first generate some dummy data to work with.

Currently, I have configured it to create a dummy SQLite db which will aid in local testing and
development, and later on we can migrate to the UAB PostgreSQL database easily.

Generate data using the command:
```bash
# THIS WILL TAKE A WHILE!!! BE PATIENT.
python3/python -m pipenv run generate
```

Once data has been generated, run the API with:
```bash
python3/python -m pipenv run api
```

which will run the local app at http://localhost:5000/

When you visit http://localhost:5000/ , you will see the Swagger API documentation, which is
dynamically generated based on the annotations you provide in the view spec under the `views` subfolder

