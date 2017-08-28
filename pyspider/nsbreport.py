# -*- coding:utf-8 -*-

import time

from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# from info.userinfo import ad4info
from public import pre_config


class  nsbreport():

    def __init__(self, url):
        self.url = url
        self.driver = pre_config.chrome(headless=False, proxy=False)

    def login(self):
        try:
            pre_config.open_page(self)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "id_username")))
            pre_config.login_rdnet(self)
        except exceptions.TimeoutException:
            print "couldn't get login page"

    def get_pageNum(self):
        try:
            for i in range(60):
                flter = self.driver.find_element_by_css_selector(
                   '.ui-grid-pager-count > span:nth-child(1)').text.split(" ")
                #print i, flter
                if len(flter) == 6 and int(flter[4]) > 0:
                    break
                time.sleep(1)
            else:
                print "No item found!!"
                return None

            tmpNum = self.driver.find_element_by_css_selector('.ui-grid-pager-max-pages-number').text
            num = int(tmpNum.split('/')[-1])
            print "Total pages: %d" % num
            return num
        except exceptions.NoSuchElementException:
            print "couldn't find the total number"
            return None

    def download_savepages(self):
        driver = self.driver
        num = self.get_pageNum()
        conditon = '//*[contains(@id,"0-uiGrid-000E-cell")]'
        if num == 0 or num is None:
            print "No page found!!"
        else:
            for n in range(num):
                m = n+1
                print "Saving page %d ...." % m
                pageCode = driver.page_source.encode('utf-8', 'ignore')
                filename = "page_%d.html" % (n+1)
                with open(filename, 'w') as f:
                    f.write(pageCode)
                if m == num:
                    break
                old_time = pre_config.search_xpath(self, conditon=conditon)
                print old_time
                driver.find_element_by_css_selector('.ui-grid-pager-next').click()
                while old_time == pre_config.search_xpath(self, conditon=conditon):
                    time.sleep(1)

    def exit_browser(self):
        time.sleep(10)
        self.driver.quit()

if __name__ == "__main__":
    url = "http://asb-rp.wroclaw.nsn-rdnet.net/login/?next=/reports/test-runs/%3Fresult%3D%2522not%2520analyzed%2522%26end_ft%3D2017-06-16%252000%3A00%3A00%2C2017-08-04%252013%3A27%3A36%26ca%3D%2522DevSH3%2522%26limit%3D100%26fs%3D4g"
    #url ="http://asb-cm.wroclaw.nsn-rdnet.net/user/login"
    RP = nsbreport(url)
    RP.login()
    try:
        RP.download_savepages()
    finally:
        RP.exit_browser()
