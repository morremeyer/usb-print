FROM python:3.11.4-buster

RUN apt-get update && apt-get install -y \
  libcups2-dev

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src /app/
CMD [ "python", "/app/print.py" ]
