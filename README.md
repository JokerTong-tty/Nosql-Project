# 基于Nosql的在线医疗健康系统

## 简介

  本项目是一套基于nosql的在线医疗系统,为了更好地方便用户了解各种疾病的症状以及应对措施，使人们可以完成居家看病。

  项目制作者:童天宇

## 使用

本项目部署在 10.132.221.201（仅校园网可访问）机器下, 使用django框架进行开发

**启动浏览器,输入网址 开始使用**

   > http://10.132.221.201:8000/user/login/
   >
   > 用户名: tty
   >
   > 密码: tty

## 文件说明

> code: 内含django框架使用到的代码与数据库文件
>
> code/data: 数据库文件
>
> code/基于Nosql的在线医疗健康系统代码: django框架使用到的代码与数据库文件

## 可能遇到的问题

### 数据库未配置

需要完成redis, mongodb,neo4j,mysql的数据初始化方可运行

### 项目未启动

操作步骤:

1. 使用Xshell或计算机自带ssh工具连接服务器

   > 用户名: hadoop
   >
   > 密码: hadoop

2. 进入项目目录下,并以特定环境启动

   ```
   workon djangoenv
   cd /home/hadoop/tty/nosqlPro
   python manage.py runserver 0.0.0.0:8000
   ```

### 数据库未启动

> 启动redis

```bash
cd /usr/local/bin
redis-server ttyconfig/redis.conf # 启动服务
# 连接并设置
redis-cli
select 5
```

> 启动mongodb

```bash
/usr/local/mongodb/bin/mongod -f /mongodb/single/mongod.conf
```

> 启动neo4j

```bash
/usr/local/neo4j/bin/neo4j start
```

