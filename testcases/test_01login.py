import os
import unittest
from common.handle_config import conf
from common.handle_excel import HandleExcel
from library.myddt import ddt, data
from requests import request
from common.handle_logging import log
from common.handle_path import DATA_DIR
from common.handle_data import replace_data, get_token

filename = os.path.join(DATA_DIR, "login.xlsx")


@ddt
class LoginTestCase(unittest.TestCase):
    excel = HandleExcel(filename, "login")
    cases = excel.read_data()

    @data(*cases)
    def test_login(self, case):
        # 请求方法
        method = case["method"]
        # 请求地址
        url = conf.get("env", "url") + case["url"]
        # 请求参数
        data = eval(replace_data(case["data"]))
        # 请求头
        headers = eval(conf.get("env", "headers"))
        # 预期结果
        expected = eval(case["expected"])
        # 用例所在行
        row = case["case_id"] + 1
        # 第二步：发送请求获取实际结果
        response = request(method=method, url=url, data=data, headers=headers, verify=False)
        # 获取实际结果
        res = response.json()
        if "account" in res:
            try:
                self.assertEqual(expected["account"], res["account"])
                self.assertEqual(expected["user_name"], res["user_name"])
            except AssertionError as e:
                # 结果回写excel中
                log.error("用例--{}--执行未通过".format(case["title"]))
                log.debug("预期结果：{}".format(expected))
                log.debug("实际结果：{}".format(res))
                log.exception(e)
                self.excel.write_data(row=row, column=8, value="未通过")
                raise e
            else:
                # 结果回写excel中
                log.info("用例--{}--执行通过".format(case["title"]))
                self.excel.write_data(row=row, column=8, value="通过")
        else:
            try:
                self.assertEqual(expected["error"], res["error"])
                self.assertEqual(expected["error_description"], res["error_description"])
            except AssertionError as e:
                log.error("用例--{}--执行未通过".format(case["title"]))
                log.debug("预期结果：{}".format(expected))
                log.debug("实际结果：{}".format(res))
                log.exception(e)
                self.excel.write_data(row=row, column=8, value="未通过")
                raise e
            else:
                # 结果回写excel中
                log.info("用例--{}--执行通过".format(case["title"]))
                self.excel.write_data(row=row, column=8, value="通过")


@ddt
class LogoutTestCase(unittest.TestCase):
    excel = HandleExcel(filename, "logout")
    cases = excel.read_data()

    @data(*cases)
    def test_logout(self, case):
        token = get_token()
        url = conf.get("env", "url") + case["url"]
        method = case["method"]
        headers = eval(conf.get("env", "headers"))
        headers["lingxi-auth"] = token
        expected = eval(case["expected"])
        row = case["case_id"] + 1
        res = (request(method=method, url=url, data=data, headers=headers, verify=False)).json()
        try:
            self.assertEqual(expected["success"], res["success"])
            self.assertEqual(expected["msg"], res["msg"])
        except AssertionError as e:
            log.error("用例--{}--执行未通过".format(case["title"]))
            log.debug("预期结果：{}".format(expected))
            log.debug("实际结果：{}".format(res))
            log.exception(e)
            self.excel.write_data(row=row, column=8, value="未通过")
            raise e
        else:
            # 结果回写excel中
            log.info("用例--{}--执行通过".format(case["title"]))
            self.excel.write_data(row=row, column=8, value="通过")
