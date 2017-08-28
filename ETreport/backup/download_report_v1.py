# -*- coding:utf-8 -*-

from time import gmtime, strftime, sleep
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from common import pre_config


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
        except exceptions.TimeoutException:
            print "couldn't login"

    def download_excel(self, driver):
        try:
            for t in range(60):
                condition = '//*[contains(@id,"-0-uiGrid-000E-cell")]'
                WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, condition)))
                if pre_config.search_xpath(self, conditon=condition) != "":
                    driver.find_element_by_css_selector('.btn.btn-rep.dropdown-toggle').click()
                    driver.find_element_by_css_selector('.btn.btn-rep[ng-click="downloadCSV()"]').click()
                    print "downloading"
                    sleep(30)
                    break
                else:
                    sleep(2)
            print "download time up"
        except exceptions.TimeoutException:
            print "couldn't open the data web, will try again......"
            driver.refresh()
            self.login()

    def start(self):
        self.login()
        file_name = 'ET_Test_Report_%s' % strftime("%Y-%m-%d-%H-%M", gmtime())
        self.download_excel(self.driver)
        sleep(60)

    def close_page(self):
        self.driver.close()

    def exit_browser(self):
        #time.sleep(10)
        self.driver.close()
        self.driver.quit()

if __name__ == "__main__":
    url1 = 'https://4g-rep-portal.wroclaw.nsn-rdnet.net/reports/test-runs/?result=%22not%20analyzed%22&end_db=2&ca=%22DevSH3%22&limit=200'
    url2 = 'http://asb-rp.wroclaw.nsn-rdnet.net/reports/test-runs/?end_db=2&ca=%22DevSH3%22&limit=200'
    t_path = '/root/log_table/'
    RP = download_report(url2, t_path)
    try:
        RP.login()
        num = 2
        while num:
            RP.download_excel(RP.driver)
            #sleep(60)
            RP.driver.refresh()
            sleep(5)
            num -= 1
    finally:
            RP.close_page()


