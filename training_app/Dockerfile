FROM ubuntu:20.04

RUN apt update && apt-get autoremove -y && \
    apt-get install -y python3.8 python3-pip && \
    apt-get clean

ADD . /training_app
WORKDIR /training_app
COPY ./training_app/requirements.txt .

RUN python3.8 -m pip install --upgrade pip && \
    python3.8 -m pip install -r requirements.txt

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers=2", "--threads=2", "--timeout=60","app"]