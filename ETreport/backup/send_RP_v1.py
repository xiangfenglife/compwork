# -*- coding:utf-8 -*-

import subprocess

from download_report import download_report as dr
from table_html import table_html as th
from common.function_plus import rename_file

t_path = '/home/xbu/Downloads/log_table/'
h_path = '/home/xbu/Downloads/log_html/'
url = 'http://asb-rp.wroclaw.nsn-rdnet.net/reports/test-runs/?end_db=2&ca=%22DevSH3%22&limit=200'
filter1 = 'tester'
perl_script = "/home/xbu/python/report/ToSendMail"
mail_recevier = "xiangfeng.bu@nokia-sbell.com"
mail_cc = "xiangfeng.bu@nokia-sbell.com"
mail_title = "ET Test report"

def send_RP():
    #login web and get the data
    table = dr(url, t_path)
    #get table from web
    try:
        download_stat = table.start()
        if download_stat is True:
            file_name = rename_file(t_path)[0]
            #generate html
            html = th(h_path)
            gen_html = html.gen_html(file_name, filter1)
            subprocess.call(["perl", perl_script, mail_recevier, mail_title, gen_html, mail_cc])

    finally:
        table.close_page()


if __name__ == "__main__":
    send_RP()










