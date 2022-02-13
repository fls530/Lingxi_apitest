import base64
import hashlib
import json
import re
import jsonpath
from common.handle_config import conf
from requests import request
import datetime
import warnings
from hashlib import md5
from requests.packages.urllib3.exceptions import InsecureRequestWarning


def login():
    method = 'post'
    url = 'https://mylink-x.lingxitest.com/api/lingxi-auth/oauth/token'
    data = {"tenantId": "000000",
            "username": conf.get("test_data", "username"),
            "password": conf.get("test_data", "password"),
            "grant_type": "password",
            "scope": "all",
            "type": "account"}

    token = \
        ((request(url=url, method=method, data=data, headers=eval(conf.get("env", "headers")), verify=False)).json())[
            'access_token']

    print(token)


login()
