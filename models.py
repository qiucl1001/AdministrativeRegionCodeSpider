# coding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from administrativeregioncodespider.decorator import external

app = Flask(__name__)

# 定义一个用来存储指定的类名列表
c_li = []


class Config(object):
    """app配置相关信息类"""

    # SQLAlchemy相关配置选项
    # 设置连接数据库的URL
    # 注意：district_code数据库要事先手动创建
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:qcl123@127.0.0.1:3306/district_code'

    # 动态跟踪配置
    SQLALCHEMY_TRACK_MODIFICATIONS = True


app.config.from_object(Config)


# 创建一个SQLAlchemy数据库连接对象
db = SQLAlchemy(app)

# 创建flask脚本管理工具对象
manager = Manager(app)

# 创建数据库迁移工具对象
Migrate(app, db)

# 向manager对象中添加数据库操作命令
manager.add_command("db", MigrateCommand)


class Duplicate(db.Model):
    """定义一个用来对url去重实现增量式爬取的url表格模型类"""
    # 定义表名
    __tblname__ = "duplicates"

    # 定义列对象
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(256), unique=True)  # url地址

    def __str__(self):
        return 'Duplicate:%s' % self.url


@external(c_li)
class Province(db.Model):
    """定义一个省份表格模型类"""
    __tblname__ = "provinces"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)  # 省份或直辖市名称
    code = db.Column(db.String(64))  # 对应的划分码
    # city = db.relationship("City", backref="province")

    def __str__(self):
        return 'Province:%s' % self.name


@external(c_li)
class City(db.Model):
    """定义一个地区市表格模型类"""
    __tblname__ = "citys"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)  # 市或区名称
    code = db.Column(db.String(64))  # 对应的划分码
    # p_city = db.Column(db.Integer, db.ForeignKey('provinces.id'))  # 关联字段，市或区名称所属的省份或直辖市id
    # destination = db.relationship("Destination", backref="city")

    def __str__(self):
        return 'City:%s' % self.name


@external(c_li)
class Destination(db.Model):
    """定义一个县级表格模型类"""
    __tblname__ = "destinations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))  # 县级名称
    code = db.Column(db.String(64))  # 对应的划分码
    # city_id = db.Column(db.Integer, db.ForeignKey("citys.id"))  # 关联字段， 县所属的市id

    def __str__(self):
        return 'Destination:%s' % self.name


# #定义模型类-作者
# class Author(db.Model):
#     __tablename__ = 'author'
#     id = db.Column(db.Integer,primary_key=True)
#     name = db.Column(db.String(32),unique=True)
#     email = db.Column(db.String(64))
#     au_book = db.relationship('Book',backref='author')
#     def __str__(self):
#         return 'Author:%s' %self.name
#
# #定义模型类-书名
# class Book(db.Model):
#     __tablename__ = 'books'
#     id = db.Column(db.Integer,primary_key=True)
#     info = db.Column(db.String(32),unique=True)
#     leader = db.Column(db.String(32))
#     au_book = db.Column(db.Integer,db.ForeignKey('author.id'))
#     def __str__(self):
#         return 'Book:%s,%s'%(self.info,self.lead)


if __name__ == '__main__':
    # # 清空district_code数据库中的所有表
    # db.drop_all()
    # # 创建所有模型类对应的表格
    # db.create_all()

    manager.run()

    print(c_li)  # ['Province', 'City', 'Destination']



