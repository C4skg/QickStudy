#!/bin/bash

cd /QickStudy/libs
unzip flask-uploads-master.zip
cd flask-uploads-master/
python setup.py build
python setup.py install
cd .. && rm -rf flask-uploads-master
cd /QickStudy

python QickStudy.py deploy
echo '初始化完成....'
echo '注意接收上述管理员的默认账号密码'
echo 'Starting QickStudy....'
python QickStudy.py runserver -h 0.0.0.0 -p 8080 --threaded