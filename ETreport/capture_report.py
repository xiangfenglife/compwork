# -*- coding:utf-8 -*-

import time

from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from xlwt import Workbook

from common import pre_config
from table_html import table_html


class  nsbreport():

    def __init__(self, url):
        self.url = url
        self.driver = pre_config.chrome(headless=True, proxy=False)

    def login(self):
        try:
            pre_config.open_page(self)
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID, "id_username")))
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
            tmp_items = self.driver.find_element_by_class_name('ui-grid-pager-count-container').text
            num = int(tmpNum.split('/')[-1])
            iterms = int(tmp_items.split(" ")[-2])
            print "Total pages: %d" % num, "Total Items: %d" % iterms
            return num
        except exceptions.NoSuchElementException:
            print "couldn't find the total number"
            return None

    @staticmethod
    def write_data_excel(name,data):
        new_f = Workbook()
        create_time = time.strftime('%Y-%m-%d-%H-%M',time.localtime(time.time()))
        sheet1 = new_f.add_sheet(create_time)
        for i in range(len(data)):
            for j in range(len(data[i])):
                sheet1.write(i, j, data[i][j])
        file_name = '%s_%s.xls' % (name, create_time)
        new_f.save(file_name)
        return file_name

    def get_headers(self, driver):
        headers_lst = []
        headers = driver.find_elements_by_class_name('ui-grid-header-cell-label')
        for element in headers:
            headers_lst.append(element.get_attribute('innerHTML'))
        return headers_lst

    def get_data(self, driver):
        data_lst = []
        data = driver.find_elements_by_css_selector('.ui-grid-row.ng-scope')
        index = len(data)/2
        for d in range(index,len(data)):
            data_lst.append(data[d].text.split('\n'))
        #print len(data_lst)
        #print data_lst[0][0],'\n',data_lst[-1][0]
        return data_lst

    def start(self):
        self.login()
        num = self.get_pageNum()
        condition = '//*[contains(@id,"-0-uiGrid-000D-cell")]'
        if num == 0 or num is None:
            print "No page found!!"
        else:
            driver = self.driver
            headers = self.get_headers(driver)
            data = [headers]
            for n in range(num):
                m = n+1
                print "Saving page %d data ...." % m
                # pageCode = driver.page_source.encode('utf-8', 'ignore')
                # filename = "page_%d.html" % (n+1)
                # with open(filename, 'w') as f:
                #     f.write(pageCode)
                data.extend(self.get_data(driver))
                if m == num:
                    break
                old_time = pre_config.search_xpath(self, conditon=condition)
                #print old_time
                driver.find_element_by_css_selector('.ui-grid-pager-next').click()
                timer = 0
                while old_time == pre_config.search_xpath(self, conditon=condition):
                    if timer >60:
                        print "WARNING: load page %d time out"%m
                        break
                    timer +=1
                    time.sleep(1)

            name_path = 'log_table/ET_Test_Report'
            excel_file_name = self.write_data_excel(name_path, data)
            # html_file = table_html()
            # html_file.gen_html(excel_file_name)

    def exit_browser(self):
        #time.sleep(10)
        self.driver.quit()

if __name__ == "__main__":
    url = '''http://asb-rp.wroclaw.nsn-rdnet.net/reports/test-runs/?columns=no,test_case.test_instance.m_path,
    test_case.test_set,test_case.name,test_col.name,test_case.test_instance.res_tester,start,end,result,test_line,build,
    test_case.test_instance.platform,test_col.ute_version,test_case.test_instance.organization,
    test_col.tool,iphy_name,test_case.test_instance.feature&limit=200&ca=%22DevSH3%22&end_db=2'''

    #url ="http://asb-cm.wroclaw.nsn-rdnet.net/user/login"
    RP = nsbreport(url)
    while True:
        try:
            RP.start()
        finally:
            RP.exit_browser()
        time.sleep(1200)

