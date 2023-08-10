FROM --platform=${BUILDPLATFORM} python:3.11.4-buster

# hadolint ignore=DL3008
RUN apt-get update && apt-get install -y --no-install-recommends \
  libcups2-dev \
  && rm -rf /var/lib/apt/lists/*
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src /app/
CMD [ "python", "/app/print.py" ]
