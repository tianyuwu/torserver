FROM torserver_base

EXPOSE 8888

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . .
ENTRYPOINT ["python3", "-u", "server.py"]