import base64
import json
import re
import jsonpath
from common.handle_config import conf
from requests import request
import datetime
import warnings


def login():
    method = 'post'
    headers = {"authorization": "Basic bHhfb3BlcmF0aW9uOmx4X29wZXJhdGlvbl9zZWNyZXQ="}
    url = 'https://xha.lingxitest.com/api/lx-operation/lingxi-auth/oauth/token'
    data = {"tenantId": "000000",
            "username": conf.get("test_data", "username"),
            "password": conf.get("test_data", "password"),
            "grant_type": "password",
            "scope": "all",
            "type": "account"}
    token = ((request(url=url, method=method, data=data, headers=headers)).json())['access_token']
    print(token)
    return


login()
