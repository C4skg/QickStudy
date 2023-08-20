FROM python:3.8

WORKDIR /QickStudy

COPY . .

RUN pip install -r requirements.txt


WORKDIR /QickStudy/libs

RUN unzip flask-uploads-master.zip
RUN python flask-uploads-master/setup.py build
RUN python flask-uploads-master/setup.py install
RUN rm -rf flask-uploads-master


WORKDIR /QickStudy

RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    redis-server

RUN apt-get install -y mysql-client


# 设置入口命令
ENTRYPOINT ["start.sh"]