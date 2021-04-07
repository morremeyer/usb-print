FROM olbat/cupsd:latest

RUN apt-get update && apt-get install -y \
  python3-pip \
  libcups2-dev

COPY requirements.txt /app/
COPY src /app/
WORKDIR /app

RUN pip3 install -r requirements.txt

CMD [ "/entrypoint.sh" ]
