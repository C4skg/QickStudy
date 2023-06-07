# QickStudy(快学平台)
<div align="center"><img src='img/logo.png' width="50px"></div>

### 0x01 前言

基于 `Flask` 框架实现的多用户学习论坛。
采用可移植性数据库，可实现不同服务器上的快速部署

### 0x02 基本功能

1. 不同用户权限分割
2. 支持 `markdown` 文档且自动渲染
3. 支持在线编辑 `markdown` 文档并储存草稿
4. 支持用户文章数统计、打卡统计，用户文章发表和点赞采取积分制竞争
5. 自动生成周报，统计每周好文章
6. 支持多用户同时在线

### 0x03 部署

1. 安装依赖
   ```bash
    conda create -n QickEnv python=3.7
    conda activate QickEnv
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```

2. 启动命令
   
   启动前需开启 `mysql` 数据库，并编辑 `config.py` 中的 `SQLALCHEMY_DATABASE_URI` 值
   ```python
    SQLALCHEMY_DATABASE_URI = 'mysql+pymsql://用户名:密码@ip:port/数据库名'
   ```
   初始化数据库
   ```bash
    python QickStudy.py db upgrade
   ```
   启动服务
   ```bash
    python QickStudy.py runserver -h ip -p port --threaded
   ```

### 0x04 所参考的开源项目

+ `flasky`
  
   [https://github.com/miguelgrinberg/flasky](https://github.com/miguelgrinberg/flasky)

+ `vditor`

   [https://github.com/Vanessa219/vditor](https://github.com/Vanessa219/vditor)