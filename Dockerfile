FROM python:3.8

MAINTAINER C4skg <C4skg@qq.com>

WORKDIR /QickStudy

COPY . .

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple


WORKDIR /QickStudy/libs

RUN unzip flask-uploads-master.zip \
    && python flask-uploads-master/setup.py build \
    && python flask-uploads-master/setup.py install \
    && rm -rf flask-uploads-master


WORKDIR /QickStudy

RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    redis-server

RUN apt-get install -y default-mysql-client

RUN chmod +x start.sh

EXPOSE 8000

# 设置入口命令
ENTRYPOINT ["/bin/bash","start.sh"]