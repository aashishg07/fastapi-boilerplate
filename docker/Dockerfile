FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends iputils-ping netcat-openbsd && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/

EXPOSE 8000

ENTRYPOINT [ "/code/docker/docker-entrypoint.sh" ]