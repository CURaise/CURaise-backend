FROM ubuntu:latest

WORKDIR src

COPY . .

RUN set -xe && \
    apt-get update -y &&  \
    apt-get install python3-pip -y &&  \
    pip install -r requirements.txt

CMD bash ./start_server.sh
