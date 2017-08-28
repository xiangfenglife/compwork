# -*- coding:utf-8 -*-

import time

from public import pre_config


class maoyan():

    def __init__(self, url):
        self.url = url
        self.driver = pre_config.chrome(headless=True, proxy=True)

    def open_page(self):
        pre_config.open_page(self)

    def analyze(self):
        value = self.driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[1]/div[1]/div[2]/div/p[2]').text
        return value.strip()

    def quit_web(self):
        self.driver.quit()


if __name__ == "__main__":
    url = "https://piaofang.maoyan.com/dashboard?movieId=344264"
    test = maoyan(url)
    test.open_page()
    old_value = 0.0
    max_delta = 0.0
    counter = 48
    interval = 3600
    for i in range(counter+1):
        value_lst = list(test.analyze())
        value_lst.pop()
        new_value = float("".join(value_lst))
        delta = new_value - old_value
        old_value = new_value
        if max_delta < delta:
            max_delta = delta
        if i == 0:
            start_value = new_value
            max_delta = 0
            delta = 0
            avg = 0
            log = "######\nStart time:%s \nStart value:%.2f \n######\n"%(time.ctime(), start_value)
        else:
            avg = (new_value - start_value)/i
            log = "[%s]: %s--Value:%.2f--delta:%.2f---Avg:%.2f(max Avg is %.2f) \n" % (
            i, time.ctime(), new_value, delta, avg, max_delta)

        with open('tmp.txt','a') as f:
            #print log
            f.write(log)
        if i < counter:
            time.sleep(interval)

    test.quit_web()
