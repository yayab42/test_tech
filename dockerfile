FROM python:3.10

WORKDIR /app

COPY test_tech/requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt
