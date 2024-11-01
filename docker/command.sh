#!/bin/bash

alembic upgrade b09da87d51c2
alembic upgrade aa3416cabbc0
cd app
gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000