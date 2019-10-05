import json
import os
import requests
from contextlib import closing


APIKEY = "<PUT YOUR API KEY HERE>"
APIEMAIL = "<PUT YOUR EMAIL HERE>"


ALL_USERS = []
with open('temp/x-all-users.json', 'rt') as f:
    ALL_USERS = json.loads(f.read())
    f.close()

ALL_PATCHES = []

print("All users", ALL_USERS)
for username in ALL_USERS:
    print("Fetching user patches", username)

    patches = None
    fn = 'temp/' + username + '.json'
    if os.path.exists(fn):
        with open(fn, 'rt') as f:
            patches = json.loads(f.read())
            f.close()
    else:
        url = 'https://api.op1.fun/v1/users/' + username + '/patches'
        headers = {'X-User-Token': APIKEY, 'X-User-Email': APIEMAIL}
        try:
            with closing(requests.get(url, headers=headers, stream=True)) as resp:
                if resp.status_code == 200:
                    patches = resp.content
                    print("patches", patches)
                else:
                    print('Non-200 response ({0}) {1}'.format(resp.status_code, resp.content))
        except requests.RequestException as e:
            print('Error during requests to {0} : {1}'.format(url, str(e)))
        print("Got patches: ", patches)
        if patches:
            patches = json.loads(patches)
            with open(fn, 'wt') as f:
                f.write(json.dumps(patches, indent=2))
                f.close()
    if patches:
        for k in patches['data']:
            ALL_PATCHES.append(k)

# print("All patches", ALL_PATCHES)
with open('temp/x-all-patches.json', 'wt') as f:
    f.write(json.dumps(ALL_PATCHES, indent=2))
    f.close()

for p in ALL_PATCHES:
    if p['attributes']['patch-type'] == 'drum':
        url = p['links']['file']
        filename = os.path.basename(url)
        downloadpath = 'temp/' + filename
        print("Processing drum patch %s (%s)" % (p['id'], url))
        if not os.path.exists(downloadpath):
            print("Downloading %s to %s" % (url, downloadpath))
            r = requests.get(url, allow_redirects=True)
            open(downloadpath, 'wb').write(r.content)
