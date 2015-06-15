import sys
import csv
import requests

owner = sys.argv[1];
repo = sys.argv[2];
token = sys.argv[3]
issue_url = 'https://api.github.com/repos/%s/%s/issues?state=all&access_token=%s' % (owner, repo, token)
pr_url = 'https://api.github.com/repos/%s/%s/pulls?state=all&access_token=%s' % (owner, repo, token)
headers = {'user-agent': 'request'}
users = set()


def getUserName(url):
    r = requests.get(url, headers=headers)
    data = r.json()
    for i in data:
        users.add(i['user']['login'])
        c = requests.get('%s?access_token=%s'%(i['comments_url'],token), headers=headers)
        for j in c.json():
            users.add(i['user']['login'])
    try:
        getUserName(r.links["next"]['url'])
    except:
        return


def getUserInfo(name):
    url = 'https://api.github.com/users/%s?access_token=%s' % (name, token)
    r = requests.get(url, headers=headers)
    data = r.json()
    return data


getUserName(issue_url)
getUserName(pr_url)

user_info = [ {
                "user_name": b["login"],
                "profile_url":b["html_url"],
                "account_created_at":b["created_at"]
              }
              for b in [getUserInfo(u) for u in users]]

with open('users.csv', 'w') as outfile:
    fp = csv.DictWriter(outfile, user_info[0].keys())
    fp.writeheader()
    fp.writerows(user_info)
