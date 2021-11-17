#!/bin/bash
flask db migrate
flask db upgrade
flask seed run
flask run --host=0.0.0.0 --port=80
