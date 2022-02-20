#FROM --platform=${TARGETPLATFORM:-linux/amd64} python:3-alpine
FROM python:3.6.9-slim
WORKDIR /usr/src/app
RUN apt update -y && apt-get install -y python3-pip
#RUN set -xe && apt update -y && apt-get install -y python3 && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata && apt-get install -y --no-install-recommends apt-utils && apt-get install -y python3-pip
COPY influx_foreign_exchange.py /usr/src/app/influx_foreign_exchange.py
RUN apt-get update -y && apt-get install -y curl && curl -sL https://repos.influxdata.com/influxdb.key | apt-key add -
RUN echo "deb https://repos.influxdata.com/ubuntu bionic stable" | tee /etc/apt/sources.list.d/influxdb.list
RUN apt install -y influxdb
docker network create --driver bridge influxdb-telegraf-net
#RUN apt-get update -y && apt-get install -y systemctl && systemctl status influxdb
RUN pip install bs4
RUN pip install schedule
#RUN kijart/python-influxdb:latest
RUN apt install -y python3-influxdb
RUN pip install influxdb
RUN pip install influxdb-client
RUN pip3 install python-dotenv
CMD ["python3","./influx_foreign_exchange.py"]

