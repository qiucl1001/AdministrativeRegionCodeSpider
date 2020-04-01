# coding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8

import requests


# 请求头基本配置
BASE_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en,en-US;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Cookie": "_gscu_190942352=85299020z8fyva97; _gscbrs_190942352=1; _gscs_190942352=85386207oz17kh42|pv:1",

    "Host": "www.mca.gov.cn",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/80.0.3987.132 Safari/537.36",
}


def get_page_source(dst_url, cookies, options={}):
    """
    获取网页源代码
    :param dst_url:网页源代码对应的url地址
    :param cookies: 访问该网站的cookies值
    :param options: 关键字参数
    :return: 返回网页源代码response
    """
    headers = dict(BASE_HEADERS, **options)
    try:
        response = requests.get(
            url=dst_url,
            cookies=cookies,
            headers=headers
        )
        if response.status_code == 200:
            return response
    except Exception as e:
        print(e.args)
        return None

