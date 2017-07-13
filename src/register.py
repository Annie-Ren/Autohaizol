#  -*- coding: UTF-8 -*-
#  !/usr/bin/python

'''
用户注册模块自动化测试
'''


import unittest, traceback
from selenium import webdriver
from utils.utils import get_mysqldb, loads_json
from utils.log import Log
import dao, config
import time
from selenium.webdriver.support.ui import Select


class RegisterTest(unittest.TestCase):

    def setUp(self):
        self.db = get_mysqldb()
        self.log = Log("../logs", name="auto-test", dividelevel=0, loglevel="info")
        self.testdriver = webdriver.Firefox()
        self.testdriver.get("https://qa-online.haizol.com/user/to-register-supplier")

    def tearDown(self):
        self.db.close()
        time.sleep(2)
        print('自动测试完毕！')
        self.testdriver.close()

    def test_user_register(self):
        cases = dao.get_base_test_cases(self.db, "register")
        for case in cases:
            self.testdriver.delete_all_cookies()
            self.testdriver.get("https://qa-online.haizol.com/user/to-register-supplier")
            inputs = loads_json(case.case_input)
            message = self.input_content(inputs.get('cn_name'), inputs.get('en_name'), inputs.get('user_name'),
                                         inputs.get('in_email'), inputs.get('password'), inputs.get('in_rePassword'),
                                         inputs.get('in_tel'), inputs.get('in_mobile'), )
            if inputs.get('cn_name') == '':
                message = self.get_faild_cnname_message()
                dao.set_base_test_case(self.db, case.case_id, config.STATUS_FAILED, message)
            elif inputs.get('en_name') == '':
                message = self.get_faild_enname_message()
                dao.set_base_test_case(self.db, case.case_id, config.STATUS_FAILED, message)
            elif inputs.get('user_name') == '':
                message = self.get_faild_name_message()
                dao.set_base_test_case(self.db, case.case_id, config.STATUS_FAILED, message)
            elif inputs.get('in_email') == '':
                message = self.get_faild_cnname_message()
                dao.set_base_test_case(self.db, case.case_id, config.STATUS_FAILED, message)
            elif inputs.get('password') == '':
                message = self.get_faild_password_message()
                dao.set_base_test_case(self.db, case.case_id, config.STATUS_FAILED, message)
            elif inputs.get('in_rePassword') == '':
                message = self.get_faild_repassword_message()
                dao.set_base_test_case(self.db, case.case_id, config.STATUS_FAILED, message)
            elif inputs.get('in_tel') == '':
                message = self.get_faild_tel_message()
                dao.set_base_test_case(self.db, case.case_id, config.STATUS_FAILED, message)
            if message is not None:
                dao.set_base_test_case(self.db, case.case_id, config.STATUS_FAILED, message)
            else:
                status = self.is_register_status()
                if status is True:
                    print '=======================', status
                    dao.set_base_test_case(self.db, case.case_id, config.STATUS_SUCCESS, config.MESSAGE_SUCCESS)
                else:
                    if inputs.get('cn_name') == '':
                        message = self.get_faild_cnname_message()
                        dao.set_base_test_case(self.db, case.case_id, config.STATUS_FAILED, message)
                    elif inputs.get('en_name') == '':
                        message = self.get_faild_enname_message()
                        dao.set_base_test_case(self.db, case.case_id, config.STATUS_FAILED, message)
                    elif inputs.get('user_name') == '':
                        message = self.get_faild_name_message()
                        dao.set_base_test_case(self.db, case.case_id, config.STATUS_FAILED, message)
                    elif inputs.get('in_email') == '':
                        message = self.get_faild_cnname_message()
                        dao.set_base_test_case(self.db, case.case_id, config.STATUS_FAILED, message)
                    elif inputs.get('password') == '':
                        message = self.get_faild_password_message()
                        dao.set_base_test_case(self.db, case.case_id, config.STATUS_FAILED, message)
                    elif inputs.get('in_rePassword') == '':
                        message = self.get_faild_repassword_message()
                        dao.set_base_test_case(self.db, case.case_id, config.STATUS_FAILED, message)
                    elif inputs.get('in_tel') == '':
                        message = self.get_faild_tel_message()
                        dao.set_base_test_case(self.db, case.case_id, config.STATUS_FAILED, message)

    def input_content(self, cn_name, en_name,user_name,in_email,in_password,in_rePassword,in_tel,in_mobile):
        try:
            cnname = self.testdriver.find_element_by_id("comp.cnName")
            cnname.send_keys(cn_name)
            enname = self.testdriver.find_element_by_id("comp.enName")
            enname.send_keys(en_name)
            username = self.testdriver.find_element_by_id("user.name")
            username.send_keys(user_name)
            email = self.testdriver.find_element_by_id("user.email")
            email.send_keys(in_email)
            password = self.testdriver.find_element_by_id("user.password")
            password.send_keys(in_password)
            repassword = self.testdriver.find_element_by_id("rePassword")
            repassword.send_keys(in_rePassword)
            s1 = Select(self.testdriver.find_element_by_id('stateId'))
            s1.select_by_index(3)
            s1.select_by_value("209")
            for select in s1.all_selected_options:
                s1 = Select(self.testdriver.find_element_by_id('provinceId'))
                s1.select_by_index(3)
            tel = self.testdriver.find_element_by_id("user.tel")
            tel.send_keys(in_tel)
            mobile = self.testdriver.find_element_by_id("user.mobile")
            mobile.send_keys(in_mobile)
            s1 = Select(self.testdriver.find_element_by_id('leftList'))
            s1.select_by_index(13)
            self.testdriver.find_element_by_xpath(
                """.//*[@id='compUserVo']/div/div/div[10]/div/div[2]/div[1]/div[2]/button[1]""").click()
            submit_btn = self.testdriver.find_element_by_xpath(""".//*[@id='compUserVo']/div/div/div[12]/div/div/button""")
            submit_btn.click()
            time.sleep(config.TEST_TIME_SCALE)
            return None
        except Exception as e :
            self.log.error(traceback.format_exc())
            return traceback.format_exc()

    def get_faild_cnname_message(self):
        err_cnname_msg = self.testdriver.find_element_by_id('comp.cnName.errors')
        return err_cnname_msg.text
    def get_faild_enname_message(self):
        err_enname_msg = self.testdriver.find_element_by_id('comp.enName.errors')
        return err_enname_msg.text
    def get_faild_name_message(self):
        err_name_msg = self.testdriver.find_element_by_id('comp.name.errors')
        return err_name_msg.text
    def get_faild_email_message(self):
        err_email_msg = self.testdriver.find_element_by_id('comp.email.errors')
        return err_email_msg.text
    def get_faild_password_message(self):
        err_password_msg = self.testdriver.find_element_by_id('comp.password.errors')
        return err_password_msg.text
    def get_faild_repassword_message(self):
        err_repassword_msg = self.testdriver.find_element_by_id('rePassword.errors')
        return err_repassword_msg.text
    def get_faild_stateId_message(self):
        err_stateId_msg = self.testdriver.find_element_by_id('comp.stateId.errors')
        return err_stateId_msg.text
    def get_faild_tel_message(self):
        err_tel_msg = self.testdriver.find_element_by_id('comp.tel.errors')
        return err_tel_msg.text
    def get_faild_validateCode_message(self):
        err_validateCode_msg = self.testdriver.find_element_by_id('validateCode.errors')
        return err_validateCode_msg.text
    def is_register_status(self):
        try:
            cc = self.testdriver.find_element_by_xpath("""html/body/div[1]/div/div/div/div[1]/h3""")
            if cc.text == ' 恭喜你注册成为HAIZOL海智在线供应商，你可以——' :
                return True
            else:
                return False
        except Exception as e:
            self.log.error(traceback.format_exc())
            return None


if __name__ == "__main__":
    unittest.main()