# coding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8

import functools


# 定义一个用来获取指定类名的装饰器
def external(class_name):
    def get_class_name(cls):
        class_name.append(cls.__name__)

        @functools.wraps(cls)
        def wrapper(*args, **kwargs):
            return cls(*args, **kwargs)
        return wrapper
    return get_class_name

