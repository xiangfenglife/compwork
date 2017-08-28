# -*- coding:utf-8 -*-

import subprocess
from time import sleep, strftime, localtime
from download_report import download_report as dr
from table_html import table_html as th
from py_project.common.function_plus import rename_file
from py_project.common.smtp_client_plain_html import  send_mail_plain_html

t_path = '/home/xbu/Downloads/log_table/'
h_path = '/home/xbu/Downloads/log_html/'
url = 'http://asb-rp.wroclaw.nsn-rdnet.net/reports/test-runs/?result=%22not%20analyzed%22&end_db=6&ca=%22DevSH3%22&limit=25'
filter1 = 'tester'
#perl_script = "/home/xbu/git/py_project/common/ToSendMail"
mail_from = 'ET.Report@sh-dev03.com'
mail_to = ["xiangfeng.bu@nokia-sbell.com"]
mail_cc = ["xiangfeng.bu@nokia-sbell.com"]
mail_title = "ET Test report"

def send_RP():
    #login web and get the data
    table = dr(url, t_path)
    #get table from web

    try:
        print "download table down"
        download_stat = table.start()
        if download_stat is True:
            file_name = rename_file(t_path)[0]
            #generate html
            html = th(h_path)
            gen_html = html.gen_html(file_name, filter1)
            print "gen html done!"
            #subprocess.call(["perl", perl_script, ','.join(mail_to), mail_title, gen_html, ','.join(mail_cc)])
            send_mail_plain_html(mailfrom=mail_from,mailto=mail_to,subject=mail_title,body=gen_html)
            print "send mail done!"
    except Exception as e:
        print e
    finally:
        table.close_page()


if __name__ == "__main__":

    start_time = '05'  # starts at 0 o'clock
    send_flag = True
    while True:
        tmp_time = strftime("%H", localtime())
        if start_time == tmp_time and send_flag is True:
            print "start time: %s" % strftime("%Y-%m-%d %H:%M:%S",localtime())
            send_flag = False
            send_RP()
        elif int(start_time) - int(tmp_time) == 1:
            send_flag = True
            sleep(600)
            continue
        else:
            sleep(3600)













