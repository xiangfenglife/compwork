#coding:utf-8

from selenium.webdriver.chrome.options import Options
from selenium import webdriver

proxy_http = '135.245.48.34'
proxy_port = '8000'


def chrome_brower(headless=False, proxy=False, download_path=""):
    driver_path = "/usr/local/chromedriver"
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')

    if headless is True:
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--headless')

    if proxy is True:
        chrome_options.add_argument('--proxy-server=%s:%s'%(proxy_http, proxy_port))

    if download_path != "":
        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': '%s' % download_path}
        chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=driver_path)

    return driver


def firefox_browser(proxy=False, download_path=""):
    profile_dir = "/home/xbu/git/py_project/common/firefox.default"
    profile = webdriver.FirefoxProfile(profile_dir)
    profile.set_preference("extensions.firebug.allPagesActivation", "on")

    if proxy is True:
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.http", proxy_http)
        profile.set_preference("network.proxy.http_port", proxy_port)
    if download_path !="":
        profile.set_preference("browser.download.folderList", 2)
        profile.set_preference("browser.download.dir", download_path)
        profile.set_preference('browser.download.manager.showWhenStarting', False)

        application = '''application/zip,text/plain,application/vnd.ms-excel,text/csv,text/comma-separated-values,
        application/octet-stream,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,
        application/vnd.openxmlformats-officedocument.wordprocessingml.document'''

        profile.set_preference('browser.helperApps.neverAsk.saveToDisk', application)
    driver = webdriver.Firefox(profile)

    return driver


def firefox():
    pass


def open_page(self):
    self.driver.get(self.url)
    self.driver.implicitly_wait(10)


def login_rdnet(self):
    #username = raw_input("please input your user name:")
    #password = raw_input("please input your user name:")
    username, password = ad4info()
    self.driver.find_element_by_id('id_username').send_keys(username)
    self.driver.find_element_by_id('id_password').send_keys(password)
    self.driver.find_element_by_css_selector('input.btn').click()
    self.driver.implicitly_wait(20)


def search_xpath(self,conditon):
    flter = self.driver.find_element_by_xpath(conditon).text
    return flter


def ad4info():
    username = "xbu"
    userpasword = "Feng#1234"
    return username, userpasword


