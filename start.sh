#!/bin/bash

service mysql start
service redis-server start
sleep 5

mysql -u root -p'your_mysql_root_password' -e 'CREATE DATABASE IF NOT EXISTS QickStudy;'

# 启动 Python 应用程序
python QickStudy.py deploy
echo '初始化完成....'
echo '注意接收上述管理员的默认账号密码'
python QickStudy.py runserver -h 0.0.0.0 -p 8080 --public --threaded 