# AdministrativeRegionCodeSpider

##  本项目主要用增量式方案抓取《中华人民共和国县以上行政区划代码》
本网站url地址：[http://www.mca.gov.cn]

## 涉及到的技术点：
1. 反爬虫方面详情url地址伪装，以js重定向方式实现
2. 网络请求库使用三方requests库
3. 网页解析库使用三方lxml库、Python标准re库, xpath提取器工具
4. 数据存储方面使用flask_sqlalchemy以面向对象方式对接mysql数据库
5. 使用装饰器动态获取指定类名，便于更新数据前清空数据表
6. 通过sqlalchemy的ORM框架定义的模型类给存储url字段添加`unique=True`唯一约束实现url去重，从而实现增量式抓取
7. 反反爬虫方面：构建UA池  动态获取Cookie

--------
## 安装

### 安装Python3.7.2以上版本

### 安装MySQL数据库
安装好之后开启MySQL数据库

###安装三方依赖库

```
pip3 install -r requirements.txt
```

## 配置 AdministrativeRegionCodeSpider
### 打开 models.py 配置mysql数据库连接
```
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://数据库用户名:数据库连接密码@数据库所在宿主机ip:3306/数据库名称'
e.g.
 SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:qcl123@127.0.0.1:3306/district_code'
 
```
### 手动创建数据库
```
mysql -u数据库用户名 -p数据库连接密码

mysql> create database district_code default charset="utf8";

```
### 创建迁移仓库
#### 这个命令会创建migrations文件夹，所有迁移文件都放在里面。
```
python database.py db init
```
### 创建迁移脚本
#### 创建自动迁移脚本
```
python database.py db migrate -m 'initial migration'
```

### 更新数据库
```
python database.py db upgrade
```

## 启动程序
```
cd administrativeregioncodespider
python main.py
```





