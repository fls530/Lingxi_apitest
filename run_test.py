import time
import unittest
from common.handle_logging import log
from common.handle_path import CASE_DIR, REPORT_DIR
from common.qiyeweixin_bot import DingTalkSend, ReportData
from common.handle_config import conf


log.info("---------------开始执行测试用例-----------------------")

# 第一步：加载测试套件
suite = unittest.defaultTestLoader.discover(CASE_DIR)

ticks = time.strftime("%Y%m%d%H%M%S", time.localtime())
filename = str(ticks) + ".html"

# 第二步：创建运行对象，传入测试套件
runner = ReportData(suite, filename, REPORT_DIR, "精准施策1.0自动化项目", "范珑生", "精准施策自动化测试报告", 1)

# 第三步：执行测试
runner.run()
# 第四步: 获取测试数据
data = runner.get_results()
success = data["success"]
allcase = data["all"]
fail = data["fail"]
skip = data["skip"]
error = data["error"]


url = conf.get("env", "base_url") + "Lingxi_apitest/reports/" + filename
DingTalkSend(success, allcase, fail, skip, error, url)

log.info("---------------测试用例执行完毕,正在发送报告前往企业微信,请注意查收-----------------------")
