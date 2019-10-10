import requests
import datetime
import json

from dateutil.relativedelta import *
from dateutil.parser import *
from datetime import *

DAYS = 7
SEPERATOR = "|"
DATES = False

users = ['omnipresent07']#['omnipresent07','barakstout','PatrickHSI']
pushEventVars = ["size","distinct_size"]
pullRequestEventActions = ["open","edited","closed","reopened","merged"]
issuesEventActions = ["opened","edited","closed","reopened"]

pushEventsDict = {}
pullRequestEventDict = {}
issuesEventDict = {}
otherEvents = {}
dict = {}
pullUrl = {}
pullUrlTitle = {}
pullDate = {}
issueUrlTitle = {}
issueUrl = {}
issueDate = {}
urlMeta = {}

def zeroDict(d,arr):
    print(d)
    for i in arr:
        d[i] = 0

def printDict(d):
    for key in d.keys():
        print(key,d[key])
    print("\n")

def printDoubleDict(d1,d2):
    for key in d1.keys():
        print(d2[key],SEPERATOR,key,SEPERATOR,d1[key])
    print("\n")

def printTripleDict(d1,d2,d3):
    for key in d1.keys():
        print(d3[key],SEPERATOR,d2[key],SEPERATOR,key,SEPERATOR,d1[key])
    print("\n")

def counter(arr,url):
    try:
        arr[url] += 1
    except:
        arr[url] = 1

zeroDict(pushEventsDict,users)
zeroDict(pullRequestEventDict,pullRequestEventActions)
zeroDict(issuesEventDict,issuesEventActions)
count = 0

print("GitHub Activity Fetch v0.1")

for user in users:
    page = 1
    done = False
    while(not done):

        r = requests.get('https://api.github.com/users/'+user+'/events?per_page=100&page='+str(page))
        results = r.json()
        page += 1
        for item in r.json():
            #print(item["actor"]["display_login"],item["repo"]["name"],item["type"])

            count += 1
            dt = parse(item["created_at"]).replace(tzinfo=None)
            now = dt.now().replace(tzinfo=None)
            rdelta = -1*relativedelta(dt, now).days
            if(rdelta > DAYS):
                done = True
                break
            try:
                dict[item["type"]] += 1
            except:
                dict[item["type"]] = 1

            if(item["type"] == "PushEvent"):
                for i in pushEventVars:
                    pushEventsDict[user] += item["payload"][i]
            elif(item["type"] == "PullRequestEvent"):
                if(item["payload"]["action"] in pullRequestEventActions):
                    pullRequestEventDict[item["payload"]["action"]] += 1
                    url = item["payload"]["pull_request"]["html_url"]
                    counter(pullUrl,url)
                    pullDate[url] = dt
                    pullUrlTitle[url] = item["payload"]["pull_request"]['title']
            elif(item["type"] == "IssuesEvent"):
                if(item["payload"]["action"] in issuesEventActions):
                    issuesEventDict[item["payload"]["action"]] += 1
                    url = item["payload"]["issue"]["html_url"]
                    counter(issueUrl,url)
                    issueDate[url] = dt
                    issueUrlTitle[url] =  item["payload"]["issue"]['title']

            else:
                counter(otherEvents,item["type"])

print("Total records: ",count)

print("Event Totals:\n==============")
printDict(dict)

print("PushEvent Totals\n==============")
printDict(pushEventsDict)

print("PullRequestEvent Totals\n==============")
printDict(pullRequestEventDict)

print("IssueEvent Totals\n==============")
printDict(issuesEventDict)

print("Pulls URLs\n==============")
if(DATES): printTripleDict(pullUrl,pullUrlTitle,pullDate)
else: printDoubleDict(pullUrl,pullUrlTitle)

print("Issues URLs\n==============")
if(DATES): printTripleDict(issueUrl,issueUrlTitle,issueDate)
else: printDoubleDict(issueUrl,issueUrlTitle)

print("URL-METAs\n==============")
printDict(urlMeta)

print("OtherEvent Totals\n==============")
printDict(otherEvents)

print("All Done!")
