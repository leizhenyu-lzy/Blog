FROM ubuntu:22.04

RUN apt update

RUN apt install -y nodejs npm

WORKDIR /home/lzy

COPY index.js WORKDIR/index.js

# 暴露应用程序运行的端口
EXPOSE 3000

CMD ["node", "WORKDIR/index.js"]

# docker build -t hello-docker .