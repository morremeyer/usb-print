FROM olbat/cupsd:latest

RUN apt-get update && apt-get install -y \
  python3 \
  libcups2-dev

COPY src /app
WORKDIR /app

RUN pip3 install -r requirements.txt

CMD [ "/entrypoint.sh" ]
