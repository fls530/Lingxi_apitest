import re
from hashlib import md5
from common.handle_config import conf
from requests import request
import warnings

warnings.filterwarnings("ignore")


class EnvData:
    """定义一个类，用来保存用例执行过程中，提取出来的数据（当成环境变量的容器）"""
    pass


def replace_data(data):
    """替换数据"""

    while re.search("#(.*?)#", data):
        res = re.search("#(.*?)#", data)
        # 返回的式一个匹配对象
        # 获取匹配到的数据
        key = res.group()
        # 获取匹配规则中括号里面的内容
        item = res.group(1)
        try:
            # 获取配置文件中对应的值
            value = conf.get("test_data", item)
        except BaseException:
            # 去EnvData这个类里面获取对应的属性（环境变量）
            value = getattr(EnvData, item)
        data = data.replace(key, value)
    return data


def get_token():
    method = 'post'
    url = 'https://mylink-x.lingxitest.com/api/lingxi-auth/oauth/token'
    data = {"tenantId": "000000",
            "username": conf.get("test_data", "username"),
            "password": md5(conf.get("test_data", "password").encode('utf8')).hexdigest(),
            "grant_type": "password",
            "scope": "all",
            "type": "account"}

    token = \
        ((request(url=url, method=method, data=data, headers=eval(conf.get("env", "headers")), verify=False)).json())[
            'access_token']

    return token
