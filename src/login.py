# -*- coding: UTF-8 -*-
# !/usr/bin/python

'''
用户登录模块自动化测试
'''


import unittest, traceback
from selenium import webdriver
from utils.utils import get_mysqldb, loads_json
from utils.log import Log
import dao, config
import time
import re


class LoginTest(unittest.TestCase):

    def setUp(self):
        self.db = get_mysqldb()
        self.log = Log("../logs", name="auto-test", dividelevel=0, loglevel="info")
        self.testdriver = webdriver.Firefox()
        self.testdriver.get("https://qa-online.haizol.com/user/loginform")

    def tearDown(self):
        self.db.close()
        time.sleep(2)
        print('自动测试完毕！')
        self.testdriver.close()

    def test_user_login(self):
        cases = dao.get_base_test_cases(self.db, "login")
        for case in cases:
            self.testdriver.delete_all_cookies()
            self.testdriver.get("https://qa-online.haizol.com/user/loginform")
            inputs = loads_json(case.case_input)
            message = self.input_username_passwd(inputs.get('username'), inputs.get('password'))
            if message is not None:
                dao.set_base_test_case(self.db, case.case_id, config.STATUS_FAILED, message)
            else:
                status = self.is_login_status()
                if status is True:
                    dao.set_base_test_case(self.db, case.case_id, config.STATUS_SUCCESS, config.MESSAGE_SUCCESS)
                else:
                    message = self.get_failed_page_message()
                    dao.set_base_test_case(self.db, case.case_id, config.STATUS_FAILED, message)


    def input_username_passwd(self, user_name, passwd):
        try:
            userName = self.testdriver.find_element_by_id("userName")
            userName.send_keys(user_name)
            password = self.testdriver.find_element_by_id("password")
            password.send_keys(passwd)
            click_button = self.testdriver.find_element_by_xpath('//*[@id="userForLogin"]/div[4]/button')
            click_button.click()
            time.sleep(config.TEST_TIME_SCALE)
            return None
        except Exception as e :
            self.log.error(traceback.format_exc())
            return traceback.format_exc()
    def get_failed_page_message(self):
        try:
            err_msg = self.testdriver.find_element_by_xpath('//*[@id="userForLogin"]/div[1]')
            return err_msg.text
        except Exception as e:
            self.log.error(traceback.format_exc())
            return None

    def is_login_status(self):
        try:
            current_url = self.testdriver.current_url
            if re.match(r'.*(/work-panel/).*', current_url):
                return True
            else:
                return False
        except Exception as e:
            self.log.error(traceback.format_exc())
            return None

if __name__ == "__main__":
    unittest.main()