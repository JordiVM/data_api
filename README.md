# Coding Challenge - Data API

This repository contains the implementation of a REST API (Data API) compliant with data regulation laws.

## Installation

### Local Installation
Download the source code from this repository and access the `data_api` folder:

```sh
$ cd data_api
```

Create a new Python virtual environment and activate it:

```sh
$ python3 -m venv venv && source venv/bin/activate
```

Install the Python packages specified in `requirements.txt`:

```sh
(venv) $ pip install -r requirements.txt
```

### Database Initialization
This Flask application needs a SQLite database to store data. Initialize an instance by running `db.py`:

```sh
(venv) $ python db.py
```

### Running the Flask App
Define the Flask application file path and environment (development or production) as environment variables:

```sh
(venv) $ export FLASK_APP=app.py
(venv) $ export FLASK_ENV=development
```

Run server with Flask application:

```sh
(venv) $ flask run
```

You can now send HTTP requests to the API at `http://localhost:5000`.

## Flask via Docker
Build the Dockerfile:

```sh
$ docker build . -t data_api
```

Once the image has been built, start the container with port `5000` exposed:

```sh
$ docker run -p 5000:5000 data_api
```

The application is running containerized and can be accessed at `http://localhost:5000`.

# Implementation decisions

Flask provided all the features needed for the implementation of the API, including an easy way to handle the DB.
Some key decisions:
1. Individual conversations are stored in-memory by the Data API because:
- I want to avoid writing every individual message to the database. This would increase the complexity of the schema
(would need to add a field that indicates which records have been given consent by the user, so that Data Scientists
don't retrieve non-authorized records).
- Additionally, if the customer decides not to consent to dialog storage, each individual message would need to be
retrieved and deleted, causing unnecessary stress to the database.

Assumptions:
- The chatbot application has a timeout so dialogues cannot be open indefinitely.
- The Data API can scale in/out to handle traffic variability.
- The Data API has sticky sessions so that all messages for a given dialog are stored in-memory in the same server.

2. Complete dialogues with customer consent are stored in a SQLite database because:
- It has a simple setup for API development and quick prototyping.
- A relational database is a good option given that the data schema is known beforehand.
- Separating the database from the application allows both to scale independently.


## Improvements at scale deployment
- Add a Load Balancer to route requests to a distributed Data API backend.
- Add logging, monitoring and alerting both at the infrastructure (metrics) and the application layer (logs).
- If deploying to the cloud, consider distributing servers in different availability zones for resiliency.
- If deploying on-prem, consider deploying applications instances in isolated hardware for resiliency.
- Implement authentication and authorization, ideally relying on external services (i.e. not handled by the application).
- In a production scenario, SQLite will be substituted by a more robust database (e.g. PostgreSQL, SQLServer, etc.).
