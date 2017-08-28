# -*- coding:utf-8 -*-

import dns.resolver


def dns_xm(domain):
    MX = dns.resolver.query(domain, 'MX')
    min_num = 100
    if len(MX) != 0:
        for info in MX:
            #print info
            if info.preference < min_num:
                min_num = info.preference
                addr = str(info.exchange)[:-1]
        #print addr
        return addr

    else:
        print "couldn't get MX for %s"%domain


if __name__ == "__main__":

    print dns_xm('nokia-sbell.com')
