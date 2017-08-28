#coding:utf-8

import time
import os
#from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def chrome(headless=False, proxy=False): 
    #driver_path = "/usr/local/chromedriver"
    driver_path = "E:\Computer\virtualenv\pyspider\src\chromedriver.exe"
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    if headless is True:
        chrome_options.add_argument('--headless')
    if proxy is True:
        chrome_options.add_argument('--proxy-server=135.245.48.34:8000')
 
    return chrome_options, driver_path
 
 
def open_page(self):
    self.driver.get(self.url)
    self.driver.implicitly_wait(10)
    
def webdriver_env_setup():
    #chrome path error solution (II)
    os.environ["webdriver.chrome.driver"] = "E:\Computer\virtualenv\pyspider\src\chromedriver.exe"
    #OR
    driver = webdriver.Chrome(r"E:\Computer\virtualenv\pyspider\src\chromedriver.exe")

def login(browser,loginurl):
    browser.get(loginurl)  
    time.sleep(1)

    username = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='id_username']")))
    username.clear()
    username.send_keys("bhe001")   
    #print "name sent"    
    time.sleep(1)
    
    browser.execute_script("document.getElementById('id_password').setAttribute('class', 'form-control')") #purpose?
    password = WebDriverWait(browser, 50).until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='id_password']")))
    password.clear()
    password.send_keys("Navice20@")    
    browser.execute_script("document.getElementById('id_password').disabled=false") #purpose?
    #print "password sent"    
    sign = WebDriverWait(browser, 50).until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='submit-id-sign_in']")))
    #sign.send_keys(u"Log in")
    sign.click()
    #print "sign sent"    
    time.sleep(1)
    
def wait_until_web_loaded(browser, timeout=50):
    cell_id = WebDriverWait(browser, timeout).until(
        EC.presence_of_element_located((By.CLASS_NAME, "ui-grid-cell-id"))) 
    if cell_id:
        return True
    return False
    
def go_to_next_page(browser, len):
    next = WebDriverWait(browser, 50).until(
        EC.presence_of_element_located((By.XPATH, "//button[@class='ui-grid-pager-next']")))
        #EC.presence_of_element_located((By.XPATH, "//button[@class=''ui-grid-pager-last']")))
    next.click()    
    #time.sleep(10) # click next page, index will be updated immediately, content will be loaded later, ? HOW TO CHECK whether new content is loaded?
    #wait_until_web_loaded(browser)
    wait_count = 0
    while(wait_count < 500):
        print "waiting ajax loading...... [%d]" % wait_count
        new_first_line = get_first_line(browser, len)
        print last_list_first_line
        print new_first_line
        if new_first_line != last_list_first_line :
            break;
        wait_count = wait_count + 1
    

def get_first_line(browser, column_length):
    list_export = []
    list_elems_in_one_page = browser.find_elements_by_class_name('ui-grid-cell')
    lines = len(browser.find_elements_by_class_name('ui-grid-icon-ok'))
    list_elems_in_one_page = list_elems_in_one_page[lines-1:] # remove icon OK
    list_elems_in_one_page = list_elems_in_one_page[1:] # remove No

    for loop_elem,count in zip(list_elems_in_one_page,range(0,column_length-1)):
        list_export.append(loop_elem.text)
        
    return list_export

    
'''
    OPEN Chrome
'''
#webdriver_env_setup()
#chrome_option, driver_path = chrome(headless=True, proxy=True)
#browser = webdriver.Chrome(chrome_options=chrome_option, executable_path=driver_path)
#browser = webdriver.Chrome(chrome_options=chrome_option)
browser = webdriver.Chrome(executable_path="/usr/local/chromedriver")
#loginurl = 'http://asb-rp.wroclaw.nsn-rdnet.net/login/?next=/reports/test-runs/%3Fca%3D%2522DevSH3%2522%26result%3D%2522not%2520analyzed%2522%26fs%3D4g/'  
loginurl = 'http://asb-rp.wroclaw.nsn-rdnet.net/login/?next=/reports/test-runs/%3Fca%3D%2522DevSH3%2522%26result%3D%2522not%2520analyzed%2522%26fs%3D4g/'  
#targeturl = 'http://asb-rp.wroclaw.nsn-rdnet.net/reports/test-runs/%3Fca%3D%2522DevSH3%2522%26result%3D%2522not%2520analyzed%2522%26fs%3D4g/'  
#targeturl = 'http://asb-rp.wroclaw.nsn-rdnet.net/reports/test-runs/?result=%2522not%2520analyzed%2522&end_db=25&ca=%2522DevSH3%2522&limit=25&res_tester=huihz'  
#targeturl = 'http://asb-rp.wroclaw.nsn-rdnet.net/reports/test-runs/?result=%22not%20analyzed%22&end_db=5&ca=%22DevSH3%22&limit=25&res_tester=huihz'  
targeturl = 'http://asb-rp.wroclaw.nsn-rdnet.net/reports/test-runs/?result=%22not%20analyzed%22&end_db=2&ca=%22DevSH3%22&limit=200'
#targeturl = 'http://asb-rp.wroclaw.nsn-rdnet.net/reports/test-runs/?result=%22not%20analyzed%22&end_db=10&ca=%22DevSH3%22&limit=25&end_date=2017-07-26'  

login(browser,loginurl)
browser.get(targeturl) 
"""
    Wait until loaded
"""
if False == wait_until_web_loaded(browser):
    #browser.refresh()
    browser.get(targeturl) 
    #time.sleep(60)    

"""
    Get Header
"""

file = open('output\output_%s.csv' % (time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))), 'w')

# find_element_by_class_name WebElement
headers = browser.find_elements_by_class_name('ui-grid-header-cell-label')
list_elems_of_header = []
for elem_of_header,count in zip(headers,range(0,len(headers))):
    list_elems_of_header.append(elem_of_header.get_attribute('innerHTML'))    

print "list_elems_of_header>>>>>>>>>>>"
print list_elems_of_header
#os._exit(0)

"""
    Get Body cells
"""    

    
#list_list_elems_per_row = [[]]*(len(list_elems_in_first_page)/len(headers))
list_list_elems_per_row = [[]]
last_list_first_line = []
'''
[ [elem1, elem2] [] [] [] ]
'''

inner_index = 0  #index in one page
last_index = 0   #index in total


while 1:
#while browser.find_element_by_class_name('ui-grid-pager-last').is_enabled():    
    list_elems_in_next_page = []
    last_list_first_line = get_first_line(browser,len(headers))
    
    list_elems_in_next_page = browser.find_elements_by_class_name('ui-grid-cell')
    lines = len(browser.find_elements_by_class_name('ui-grid-icon-ok'))
    print lines
    
    list_elems_in_next_page = list_elems_in_next_page[lines-1:] #remove the header icon-ok
    
    for loop_elem,count in zip(list_elems_in_next_page,range(0,len(list_elems_in_next_page))):
        inner_index = count/len(headers)
        try:
            if 'ui-grid-icon-ok' in loop_elem.get_attribute('innerHTML'):
                continue
                
            list_list_elems_per_row[last_index + inner_index].append(loop_elem.text)

        except:
            print "raised exception during zip elems to test result row" # for the last page
            print "last_index : " + str(last_index) + ". inner_index : " + str(inner_index) + ". elem count : " + str(count)
            print "len(list_list_elems_per_row) : " + str(len(list_list_elems_per_row)) + ". len(list_elems_in_next_page) : " + str(len(list_elems_in_next_page))
            break
            
        if count % len(headers) == (len(headers)-1):
            print list_list_elems_per_row[last_index + inner_index]

        if last_index + inner_index >= len(list_list_elems_per_row)-1:
            list_list_elems_per_row.append([])

    last_index = last_index +  inner_index + 1
    
    if browser.find_element_by_class_name('ui-grid-pager-last').is_enabled():
        list_list_elems_per_row.append([])
        go_to_next_page(browser, len(headers))
    else: # last page
        break


idx_Responsible_Tester  = list_elems_of_header.index('Responsible Tester')  
idx_exe_time = list_elems_of_header.index('End')
list_header_extended = list(list_elems_of_header)
list_header_extended.insert(idx_exe_time+1,"Exe Time") 

'''
{ date : { tester : number}
'''
dict_not_analysis_per_date = {}
'''
{ tester : { date : number}
'''
dict_not_analysis_per_tester = {}

for elem_head in list_header_extended:
    file.write( elem_head + "$")
file.write('\n')

#print "list_list_elems_per_row>>>>"
#print list_list_elems_per_row

for loop_list_elems_per_row in list_list_elems_per_row:    
    try:
        tester_name = loop_list_elems_per_row[idx_Responsible_Tester]
        exe_time = loop_list_elems_per_row[idx_exe_time][0:10] 
        
        dict_not_analysis_per_tester.update({tester_name:{exe_time:0}})     
               
        if dict_not_analysis_per_date.has_key(exe_time):
            dic_not_analy_per_day = dict_not_analysis_per_date.get(exe_time)
            if dic_not_analy_per_day.has_key(tester_name):
                dic_not_analy_per_day[tester_name] = dic_not_analy_per_day[tester_name] + 1
            else:
                dic_not_analy_per_day.update({tester_name:1})
        else:
            dict_not_analysis_per_date.update({exe_time:{tester_name:1}})
            
        loop_list_elems_per_row.insert(idx_exe_time+1, exe_time )
    except:
        print "len(loop_list_elems_per_row) : " + str(len(loop_list_elems_per_row))
        if 0 == len(loop_list_elems_per_row):
            continue
            
    for elem_loop_in_row in loop_list_elems_per_row:
        file.write("".join(elem_loop_in_row.split()) + "$")
    file.write('\n')


for key_date,value in dict_not_analysis_per_date.items():
    for key_tester,value0 in value.items():
        if dict_not_analysis_per_tester.has_key(key_tester):
            dict_not_analysis_per_tester[key_tester].update({key_date : value0})
        else:
            dict_not_analysis_per_tester.update({key_tester : {key_date : 0} })

print dict_not_analysis_per_tester
print dict_not_analysis_per_date

html_file = open('export\export_%s.html' % (time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))), 'w')
head = ""
output_bodies = ""
date_keys = list(dict_not_analysis_per_date.keys())
date_keys.sort()

for key in date_keys:
    head = head + "<th>" + str(key) + "</th>"
for key_tester, value in dict_not_analysis_per_tester.items():
    output_bodies = output_bodies+ "<tr>"
    output_bodies = output_bodies + "<td>" + key_tester + "</td>"
    for key in date_keys:
        if value.has_key(key):
            output_bodies = output_bodies + "<td class='highlight'>" +  str(value.get(key,0)) + "</td>"
        else:
            output_bodies = output_bodies + "<td>" +  str(0) + "</td>"
    output_bodies = output_bodies+ "</tr>"

html = """\
<style type="text/css">
<!--
table.t1 {
border-width: 1px 0 0 1px;
border-style: solid;
border-color: #666;
}
table.t1 td{
border-width: 0 1px 1px 0;
border-style: solid;
border-color: #666;
font:Arial;
text-align:center;
}
table.t1 td.highlight{
font-color:red;
background-color:yellow;
}
-->
</style>

<html>
  <head></head>
  <body>
    <p>Hi All!<br>
      Not Analysis Test Cases to be completed, please take actions!!
        <table border="1" class="t1">
          <tr>
            <th>Name</th> """ + head + """
          </tr>""" + output_bodies + """
        </table>
    </p>
  </body>
</html>
"""

html_file.write(html)
html_file.close()
            
file.close()
#browser.close()
#browser.quit()
    
'''
driver=webdriver.PhantomJS()
driver.get(targeturl)
result = BeautifulSoup(driver.page_source,'lxml').find_all('div',class_='ui-grid-contents-wrapper')
print len(result)
'''
 