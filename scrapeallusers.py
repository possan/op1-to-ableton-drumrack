import requests
import re
import json
from contextlib import closing
from bs4 import BeautifulSoup


ALL_USERS = []
HREF_R = re.compile('^\/users\/([^\/]+)\/patches\/(.+)$')
URL_FORMAT = 'https://op1.fun/patches?utf8=%E2%9C%93&q%5Bname_cont%5D=&page={0}&q%5Buser_username_cont%5D=&q%5Bpatch_type_cont%5D=drum&q%5Bs%5D%5B0%5D%5Bname%5D=created_at&q%5Bs%5D%5B0%5D%5Bdir%5D=desc&commit=Search'


keepscraping = True
page = 1
while keepscraping:
    url = URL_FORMAT.format(page)
    print ("Downloading page %d from %s" % (page, url))

    html = None
    try:
        with closing(requests.get(url, stream=True)) as resp:
            if resp.status_code == 200:
                html = resp.content
    except requests.RequestException as e:
        print('Error during requests to {0} : {1}'.format(url, str(e)))

    if html:
        html = BeautifulSoup(html, 'html.parser')
        patches = html.select('li.patch')
        for p in patches:
            link = p.select_one('a.parent-link')
            if link != None:
                href = link['href']
                match = HREF_R.match(href)
                if match:
                    username = match.group(1)
                    patchid = match.group(2)
                    print("Found patch %s by user %s" % (patchid, username))
                    if not username in ALL_USERS:
                        print("Found new user %s" % (username))
                        ALL_USERS.append(username)
        page += 1
        if len(patches) == 0:
            keepscraping = False
    else:
        keepscraping = False

print ("Found users", ALL_USERS)
with open('temp/x-all-users.json', 'wt') as f:
    f.write(json.dumps(ALL_USERS, indent=2))
    f.close()
