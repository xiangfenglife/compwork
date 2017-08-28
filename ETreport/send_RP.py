# -*- coding:utf-8 -*-

import subprocess
from time import gmtime, sleep, strftime
from download_report import download_report as dr
from table_html import table_html as th
from common.function_plus import rename_file

t_path = '/root/Downloads/log_table/'
h_path = '/root/Downloads/log_html/'
url = 'http://asb-rp.wroclaw.nsn-rdnet.net/reports/test-runs/?end_db=6&ca=%22DevSH3%22&limit=25'
filter1 = 'tester'
perl_script = "/usr/nsb/py_project/common/ToSendMail"
mail_recevier = "bin.c.he@nokia-sbell.com"
mail_cc = "xiangfeng.bu@nokia-sbell.com"
mail_title = "ET Test report"

def send_RP():
    #login web and get the data
    table = dr(url, t_path)
    #get table from web

    try:
        download_stat = table.start()
        print "download table down"
        if download_stat is True:
            file_name = rename_file(t_path)[0]
            #generate html
            html = th(h_path)
            gen_html = html.gen_html(file_name, filter1)
            print "gen html done!"
            subprocess.call(["perl", perl_script, mail_recevier, mail_title, gen_html, mail_cc])
            print "send mail done!"
    finally:
        table.close_page()


if __name__ == "__main__":

    start_time = '16'  # starts at 8 o'clock
    send_flag = True
    while True:
        tmp_time = strftime("%H", gmtime())
        print tmp_time

        if start_time == tmp_time and send_flag is True:
            send_flag = False
            send_RP()
        elif start_time != tmp_time:
            send_flag = True

        sleep(1200)













