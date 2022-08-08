import unittest
from BeautifulReport import BeautifulReport
from Common.handle_path import testcase_dir,reports_dir

# base_dir = os.path.dirname(os.path.abspath(__file__))

ss = unittest.TestLoader().discover(testcase_dir)
br = BeautifulReport(ss)
br.report("测试报告","report.html",reports_dir)