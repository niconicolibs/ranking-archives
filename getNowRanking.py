import datetime
import requests
import os, sys, json, time

HEADERS = {
    "User-Agent": "GetRankingData"
}

req_url = "https://dcdn.cdn.nimg.jp/nicovideo/old-ranking/{}/{}/{}"

TZ_JST = datetime.timezone(datetime.timedelta(hours=9))
NOW = datetime.datetime.now(TZ_JST)

GITHUB_USERNAME = "RankingCollectBot"
GITHUB_REPO_OWNERNANE = "niconicolibs"
GITHUB_REPO_NANE = "ranking-archives"
PERSONAL_ACCESS_TOKEN = os.environ.get("PERSONAL_ACCESS_TOKEN")
session = requests.Session()
session.auth = (GITHUB_USERNAME, PERSONAL_ACCESS_TOKEN)
issue_url = 'https://api.github.com/repos/%s/%s/issues' % (GITHUB_REPO_OWNERNANE, GITHUB_REPO_NANE)

def sendIssue(titleDay, errorMes, statusCode):
    session.post(issue_url, data=json.dumps({
        "title": "[Failed] API request failed ({})".format(titleDay),
        "body": "Date: {}\nStatusCode: {}\nError Log: \n```\n{}```".format(titleDay, statusCode, errorMes)
    }).encode("utf-8"), headers={"Content-Type" : "application/json"})

def downloadFiles(type):
    additionTimes = [""]
    if type == "daily" or type == "total":
        additionTimes.append("_05")
    for additionTime in additionTimes:
        name_list_res = requests.get(
            req_url.format(type, NOW.strftime("%Y-%m-%d")+additionTime, "file_name_list.json"),
            headers=HEADERS
        )
        if name_list_res.status_code != 200:
            sendIssue(NOW.strftime("%Y-%m-%d")+additionTime, name_list_res.status_code, name_list_res.text)
            continue
        try:
            name_list_res.json()
        except:
            print("NotFound {} ({}/{})".format(additionTime,type,NOW.strftime("%Y-%m-%d")))
            sendIssue(NOW.strftime("%Y-%m-%d")+additionTime, name_list_res.status_code, name_list_res.text)
            continue
        currentFolder = ""
        if type == "monthly" or type == "weekly":
            currentFolder = "./ranking/{}/{}/{}/".format(type, NOW.strftime("%Y"), NOW.strftime("%Y-%m-%d")+additionTime)
        else:
            currentFolder = "./ranking/{}/{}/{}/{}/".format(type, NOW.strftime("%Y"), NOW.strftime("%m"), NOW.strftime("%Y-%m-%d")+additionTime)
        if not os.path.exists(currentFolder):
            os.makedirs(currentFolder)
        with open(currentFolder + "file_name_list.json", mode="w", encoding="utf-8") as f:
            f.write(name_list_res.text)
        for cat in name_list_res.json():
            res = requests.get(
                req_url.format(type, NOW.strftime("%Y-%m-%d")+additionTime, cat["file"]),
                headers=HEADERS
            )
            with open(currentFolder + cat["file"], mode="w", encoding="utf-8") as f:
                f.write(res.text)

downloadFiles("daily")
downloadFiles("total")

if NOW.day == 1:
    downloadFiles("monthly")

if NOW.weekday() == 0:
    downloadFiles("weekly")