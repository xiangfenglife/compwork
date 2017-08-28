# -*- coding:utf-8 -*-

from time import sleep
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from py_project.common import pre_config


class download_report():

    def __init__(self, url, table_path):

        self.table_path = table_path
        self.url = url
        self.driver = pre_config.firefox_browser(proxy=False, download_path=self.table_path)

    def login(self):
        try:
            pre_config.open_page(self)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "id_username")))
            pre_config.login_rdnet(self)
            WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.ID, "rep-report-title")))
            print "login pass!"
            return True
        except exceptions.TimeoutException:
            print "couldn't login, please try again..."
            return False

    def download_excel(self):
        driver = self.driver
        try:
            condition = '//*[contains(@id,"-0-uiGrid-000E-cell")]'
            WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, condition)))
            if pre_config.search_xpath(self, conditon=condition) != "":
                driver.find_element_by_css_selector('.btn.btn-rep.dropdown-toggle').click()
                driver.find_element_by_css_selector('.btn.btn-rep[ng-click="downloadCSV()"]').click()
                print "downloading"
                sleep(30)
            print "download time up"
            return True
        except exceptions.TimeoutException:
            print "couldn't open the data web, Please try again......"
            return False

    def close_page(self):
        self.driver.close()

    def start(self):

        for login_time in range(10):
            if self.login() is True:
                break
            else:
                self.close_page()
            if login_time == 9:
                print "login failure"
                return False

        for load_data_time in range(10):
            if self.download_excel() is True:
                break
            else:
                self.driver.refresh()
                sleep(5)
            if load_data_time == 9:
                print "load data failure"
                return False
        return True

if __name__ == "__main__":
    url1 = 'https://4g-rep-portal.wroclaw.nsn-rdnet.net/reports/test-runs/?result=%22not%20analyzed%22&end_db=2&ca=%22DevSH3%22&limit=200'
    url2 = 'http://asb-rp.wroclaw.nsn-rdnet.net/reports/test-runs/?end_db=2&ca=%22DevSH3%22&limit=200'
    t_path = '/home/xbu/Downloads/log_table/'
    RP = download_report(url2, t_path)
    try:
       RP.start()
    finally:
       RP.close_page()


