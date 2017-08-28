from collections import Counter
from time import strftime, localtime
from html import html
import xlrd
import os
import csv


class table_html:

    def __init__(self, h_path):
        self.Start_name = u'Start'
        self.End_name = u'End'
        self.table = None
        self.html_path = h_path

    def gen_html(self, filepath, param='tester'):
        file_lst = []
        date_lst = []
        param_lst = []
        if '/*' in filepath:
            table_path = filepath.split('*')[0]
            name_lst = os.listdir(table_path)
            file_lst = [table_path + m for m in name_lst if ("xls"in m) or ("csv" in m) ]
            html_name = self.html_path + 'Total_' + strftime("%Y-%m-%d-%H-%M",localtime())
        else:
            file_lst.append(filepath)
            html_name = self.html_path+filepath.split('/')[-1].split('.')[0]

        for f in file_lst:
            ftype = f.split('.')[-1]
            self.open_file(f, ftype)
            date_lst.extend(self.time_lst(self.End_name))
            param_lst.extend(self.params(param))

        data_dic = {}
        for t in tuple(date_lst):
            tmp_lst = []
            for l in range(len(date_lst)):
                if t == date_lst[l]:
                    tmp_lst.append(param_lst[l])
            data_dic[str(t)] = tmp_lst
        gen_html = self.write_html(data_dic)
        full_html_name = '%s.html' % html_name
        with open(full_html_name, 'w') as f:
            f.write(gen_html)
        return full_html_name

    def open_file(self, fname, ftype = "csv"):
        if ftype == "csv":
            with open(fname,'r') as f:
                row = f.readlines()
                if len(row[0]) < 10:
                    row.pop(0)
                    with open(fname,'w') as f:
                        f.write(''.join(row))

            with open(fname,'r') as f:
                Reader = csv.DictReader(f)
                self.table = [row for row in Reader]

        elif ftype == "xls":
            book = xlrd.open_workbook(fname)
            self.table = book.sheets()[0]
        else:
            print "ERROR: The type of the file is not supported !!"

    def get_index_cols(self, param):
        headers_row = self.table.row_values(0)
        for i in range(len(headers_row)):
            if headers_row[i] == param:
                cols_num = i
                break
        return cols_num

    def time_lst(self, time_name):
        time_lst = []
        if isinstance(self.table, xlrd.sheet.Sheet):
            cols_num = self.get_index_cols(time_name)
            for t in self.table.col_values(cols_num):
                time_lst.append(t.split("T")[0])
            time_lst.pop(0)
        else:
            #print "csv1"
            str(time_name).lower()
            for row in self.table:

                time_lst.append(row[str(time_name).lower()].split("T")[0])

        return time_lst

    def params(self, param):
        param_lst = []

        if isinstance(self.table, xlrd.sheet.Sheet):
            if param == "tester":
                flt = u"Responsible Tester"
            param_cols_num = self.get_index_cols(flt)
            # print "time,cols num:", param_cols_num
            for p in self.table.col_values(param_cols_num):
                param_lst.append(p)
            param_lst.pop(0)

        else:
            #print "csv2"
            if param == "tester":
                flt = 'test_case.test_instance.res_tester'
            for row in self.table:
                param_lst.append(row[str(flt).lower()])

        return param_lst

    @staticmethod
    def write_html(data_dic):

        head = ""
        body = ""
        fill_content = "<td>" + str(0) + "</td>"
        fill_time = 0
        tester_info = {}
        count_dic = {}
        sum_value = "<tr>" + "<td>" + "SUM" + "</td>"
        for time_key in sorted(data_dic):
            head = head + "<th><b>" + str(time_key) + "</b></th>"
            sum_value += "<td><b>" + str(len(data_dic[time_key])) + "</b></td>"
            count_dic[time_key] = Counter(data_dic[time_key])


        for count_key in count_dic:
            print count_key
            for tester_key, value in count_dic[count_key].items():
                if tester_key not in tester_info.keys():
                    output_bodies = "<tr>"+ "<td>" + tester_key + "</td>"
                    tester_info[tester_key] = output_bodies + fill_content*fill_time
                tester_info[tester_key] = tester_info[tester_key] + "<td class='highlight'>" + str(value) + "</td>"

            for tester in tester_info.keys():
                if count_dic[count_key].has_key(tester) is False:
                    tester_info[tester] = tester_info[tester]+fill_content

            fill_time += 1

        for key, value in tester_info.items():
            body = body + value
        output_bodies = body + sum_value +"</tr>"
        now_time = strftime('%Y-%m-%d %H:%M:%S', localtime())
        return html(now_time,head, output_bodies)


if __name__ == "__main__":
    h_path = "/root/Downloads/log_html/"
    data = table_html(h_path)
    testers = 'tester'
    file_name = '/root/Downloads/log_table/report_2017-08-25-21-17-01.csv'
    data.gen_html(file_name, testers)
