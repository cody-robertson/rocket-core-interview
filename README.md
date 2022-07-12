# Rocket Core Interview Take-Home Assignment

## Author: Cody Robertson

## Tech

This project is built with Python3 and Django Rest Framework.

A Postman collection is provided for testing the endpoints.

## Project Structure

Urls are defined in rocket_interview/rocket_interview/urls.py

Serializers are defined in rocket_interview/products/serializers.py

Models are defined in rocket_interview/products/models.py

Views are defined in rocket_interview/products/views.py

Code to initialize the database is defined in rocket_interview/products/management/init_db.py

## How to Run

This project requires Docker to be installed in order to run.

All other commands are included in the Makefile.

1. Run `make start` to start the project
2. Run `make migrate` to run database migrations
3. Run `make init_db` to initialize the database with the provided products.json file

The API can now be accessed at http://localhost:8000.