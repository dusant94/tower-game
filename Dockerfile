FROM python:3.7.4

RUN mkdir /app
COPY . /app
WORKDIR /app

ARG CONFIG_FOLDER=./storage/config_templates/docker

COPY $CONFIG_FOLDER /app/storage/config

RUN pip install -r requirements.txt

ENV PORT 8000

# todo: args / env for host, port

EXPOSE ${PORT}
VOLUME ["/app"]


CMD ["uvicorn", "main:app" , "--host", "0.0.0.0", "--port", "8001"]

