#!/bin/bash


# Database migrations
flask db init
flask db migrate
flask db upgrade

# Run Application
flask run
