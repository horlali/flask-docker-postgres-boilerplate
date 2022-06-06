#!/bin/bash


# Database migrations
flask db init
flask db migrate

# Run Application
flask run
