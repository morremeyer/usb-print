FROM olbat/cupsd:latest

RUN apt-get update && apt-get install -y \
  python3-pip \
  libcups2-dev

COPY entrypoint.sh /

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY src /app/
CMD [ "/entrypoint.sh" ]
