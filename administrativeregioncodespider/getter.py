# coding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8

import re
import requests
import sqlalchemy
from lxml import etree
from requests.cookies import RequestsCookieJar
import models
from administrativeregioncodespider.utils import get_page_source
from administrativeregioncodespider.useragents import GetRandomUserAgent


class DistrictCodeSpider(object):
    """最新中华人民共和国县以上行政区划代码"""
    def __init__(self):
        """
        初始化
        """
        self.domain = "http://www.mca.gov.cn"
        self.base_url = "http://www.mca.gov.cn/article/sj/xzqh/2020/"
        self.cookies = None

    @staticmethod
    def delete_all_tbl():
        """
        清空数据库中所有表数据
        删除表数据是一行一行删除，效率低，磁盘IO高，影响性能，有待优化。

        可以手动清空数据库表中的所有数据:
        delete from table_name;

        因为mysql数据库使用的数据库引擎为InnoDB， 删除表数据是一行行删除的
        而MyIsAM数据库引擎可以重构表
        :return:
        """
        print("清空数据库所有表数据启动：")
        for _ in models.c_li:
            for item in getattr(models, _)().query.all():
                print(item)
                models.db.session.delete(item)
                models.db.session.commit()
        print("数据库表数据清空完成！")
        print("\n更新数据库数据启动：")

    def get_fake_detail_page_url(self):
        """
        获取最新行政区划分码的伪造详情地址
        :return:
        """
        resp = get_page_source(self.base_url, self.cookies)
        if resp:
            html = etree.HTML(resp.text)
            a_li = html.xpath('//a[@class="artitlelist"]')

            pattern = re.compile('.*以上行政区划代码', re.S)
            for a in a_li:
                title = a.get("title")
                res = pattern.findall(title)
                if res:
                    full_url = self.domain + a.get("href")
                    try:
                        obj = models.Duplicate(url=full_url)
                        models.db.session.add(obj)
                        models.db.session.commit()

                        # 增量式启动前，先清空数据库中所有表数据
                        self.delete_all_tbl()
                        return full_url
                    except sqlalchemy.exc.IntegrityError:
                        print("数据以是最新，无需重爬！")
                        return

    def get_true_detail_page_url(self):
        """
        获取最新行政区划分码的真实的详情地址
        :return:
        """
        fake_detail_url = self.get_fake_detail_page_url()
        resp = get_page_source(fake_detail_url, self.cookies)
        if resp:
            # 提取真实的连接地址
            pattern = re.compile(r'window\.location\.href="(.*?)";', re.S)
            true_detail_url = re.findall(pattern, resp.text)
            if true_detail_url:
                true_detail_url = true_detail_url[0]
                self.parse_detail_page(true_detail_url)

    def parse_detail_page(self, true_detail_url):
        """
        解析详情页所需的数据
        :param true_detail_url: 详情页真实地址
        :return:
        """
        response = get_page_source(true_detail_url, self.cookies)
        if response:
            html = etree.HTML(response.text)
            trs = html.xpath('//table/tr[@height="19"]')
            province_tag = None
            province_code_tag = None
            print({'省份：': '北京市', '划分码': '110000'})
            data = {
                "name": '北京市',
                "code": '110000'
            }
            p = models.Province(**data)
            models.db.session.add(p)
            models.db.session.commit()

            for tr in trs:
                province_code = "".join(tr.xpath('./td[2]//text()')).strip()
                province = "".join(tr.xpath('./td[3]//text()')).strip()

                if province_tag is None:
                    province_tag = province
                    province_code_tag = province_code
                elif not province_code.startswith(province_code_tag[:2]):
                    province_code_tag = province_code
                    province_tag = province
                    print({"省份：": province_tag, "划分码": province_code_tag})
                    data = {
                        "name": province_tag,
                        "code": province_code_tag
                    }
                    p = models.Province(**data)
                    models.db.session.add(p)
                    models.db.session.commit()
                elif all([
                    province_code.startswith(province_code_tag[:2]),
                    province_code.endswith(province_code_tag[-2:])
                ]):
                    print({"省所属市：": province, "划分码": province_code})
                    data = {
                        "name": province,
                        "code": province_code
                    }
                    c = models.City(**data)
                    models.db.session.add(c)
                    models.db.session.commit()

                else:
                    print({"市所属县：": province, "划分码": province_code})
                    data = {
                        "name": province,
                        "code": province_code
                    }
                    dst = models.Destination(**data)
                    models.db.session.add(dst)
                    models.db.session.commit()
            print("\n更新数据库数据完成！")

    def get_cookies(self):
        """获取访问本网站相关的Cookies值"""

        r = requests.get(
            url=self.base_url,
            headers={
                "User-Agent": GetRandomUserAgent().random
            }
        )
        jar = RequestsCookieJar()
        for key, value in r.cookies.items():
            jar.set(key, value)
        self.cookies = jar

    def run(self):
        """程序入口"""
        # 动态获取Cookies值
        self.get_cookies()

        # 获取全国行政划分码数据并保存到数据库中
        self.get_true_detail_page_url()


if __name__ == '__main__':
    # d = DistrictCodeSpider()
    # d.run()
    print(models.c_li)


