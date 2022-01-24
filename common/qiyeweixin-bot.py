import json
import requests
from unittestreport import TestRunner
from common.handle_config import conf


class ReportData(TestRunner):
    def get_results(self):
        test_result = {
            "success": 0,
            "all": 0,
            "fail": 0,
            "skip": 0,
            "error": 0,
            "results": [],
            "testClass": [],
        }
        # 整合测试结果
        for res in self.result:
            for item in test_result:
                test_result[item] += res.fields[item]

        return test_result


def DingTalkSend(testPass, testAll, testFail, testSkip, testError, url):
    # 钉钉推送
    webhook = conf.get("env", "webhook")
    headers = {"Content-Type": "application/json", "Charset": "UTF-8"}
    data = {"msgtype": "text",
            "text": {"content": "自动化测试项目" + ":掌上医馆接口自动化脚本执行完成。"
                                            "\n通过用例数量:" + "  " + str(testPass) +
                                "\n运行用例总数:" + "  " + str(testAll) +
                                "\n失败用例数量:" + "  " + str(testFail) +
                                "\n跳过用例数量:" + "  " + str(testSkip) +
                                "\n错误用例数量:" + "  " + str(testError) +
                                "\n报告地址:" + "  " + url},
            "at": {"atMobiles": [], "isAtAll": False}
            }

    res = requests.post(webhook, data=json.dumps(data), headers=headers)
    print(res.text)


if __name__ == '__main__':
    DingTalkSend(url="http://localhost:63342/Romens_apitest/reports/20220124181414.html?_ijt=vs0r9hl3sajjjpkfmm9cknurh&_ij_reload=RELOAD_ON_SAVE")
