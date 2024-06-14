# QickStudy(快学平台)
> OpenSourceID: HM807VSRFM

<div align="center"><img src='img/logo.png' width="50px"></div>
<br>
<div align="center">
<a href='https://www.murphysec.com/console/report/1674402525447217152/1674402525975699456'><img src='https://www.murphysec.com/platform3/v31/badge/1674402525975699456.svg'></a>
</div>

### 0x01 前言

基于 `Flask` 框架实现的多用户学习论坛。
采用可移植性数据库，可实现不同服务器上的快速部署

### 0x02 功能亮点

1. 不同用户权限分割
2. 支持 `markdown` 文档
3. 支持在线编辑 `markdown` 文档并实时渲染、存储
4. 支持用户文章数统计、打卡统计，用户文章发表和点赞
5. 自动生成周报，统计每周好文章
6. 自动生成好文海报，快速分享知识
7. 多主题一键切换


### 0x03 样式展示
+ 主页面 `night`
   <div align="center"><img src='img/1.png'></div>

+ 文章详情 `night`
   <div align="center"><img src='img/2.png'></div>

+ 在线编辑 `night`
   <div align="center"><img src='img/3.png'></div>

+ 登录
   <div align="center"><img src='img/4.png'></div>


### 0x04 部署
#### 使用 `Docker` 部署
在项目根目录下使用以下命令
```bash
docker-compose up
```
第一次启动成功后，变可停止服务并于后台重新运行
```bash
docker-compose up -d
```

#### 本地部署
1. 安装依赖

   ```bash
   conda create -n QickEnv python=3.7
   conda activate QickEnv
   cd requirements
   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```

   由于 `Flask-Uploads` 插件在 `pip` 上的版本更新并不及时，所以需要收到另外安装
   项目包中已经将合适的版本放在 `libs` 目录下
   通过以下命令安装

   ```bash
   unzip flask-uploads-master.zip
   python flask-uploads-master/setup.py build
   python flask-uploads-master/setup.py install
   ```

   使用命令 `pip list | grep flask-Uploads` 查看是否成功安装

2. 准备

   + 启动前需开启 `mysql` 数据库,并编辑 `config.py` 中的值

      ```python
      SQL_USER = "root"          #目标数据库用户名
      SQL_PASSWORD = "123456"    #目标数据库密码
      SQL_PORT = "3306"          #目标数据库端口
      SQL_SCHEMA = "QickStudy"   #目标数据库
      ```
   + 项目依赖了 `redis` 作为中间件,编辑 `config.py` 中的值对项目的 `redis` 进行配置

      ```python
      REDIS_URI = "127.0.0.1"       #redis 地址
      REDIS_PORT = 6379             #redis 端口
      ```

3. 部署
   
   部署前请确保 `MySQL` 和 `Redis` 处于正常运行
   使用以下命令部署

   ```bash
   python QickStudy.py deploy
   ```

4. 启动服务
   
   + 对外

      ```bash
      python QickStudy.py runserver -h 0.0.0.0 -p port --threaded
      ```
   
   + 对内

      ```bash
      python QickStudy.py runserver -h 127.0.0.1 -p port --threaded
      ```

### 0x05 致谢

本项目或使用、或参考了以下，但不限于以下的开源项目，下面列出了主要的参考和使用开源项目

+ `vditor`
  
  [https://github.com/Vanessa219/vditor](https://github.com/Vanessa219/vditor)

+ `Flask`
  
  [https://github.com/pallets/flask](https://github.com/pallets/flask)
