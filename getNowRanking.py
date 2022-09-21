import datetime
import requests
import os, sys, json, time

HEADERS = {
    "User-Agent": "GetRankingData"
}

req_url = "https://dcdn.cdn.nimg.jp/nicovideo/old-ranking/{}/{}/{}"

TZ_JST = datetime.timezone(datetime.timedelta(hours=9))
NOW = datetime.datetime.now(TZ_JST)

def downloadFiles(type):
    additionTimes = [""]
    if type == "daily" or type == "total":
        additionTimes.append("_05")
    for additionTime in additionTimes:
        name_list_res = requests.get(
            req_url.format(type, NOW.strftime("%Y-%m-%d")+additionTime, "file_name_list.json"),
            headers=HEADERS
        )
        try:
            name_list_res.json()
        except:
            print("NotFound _05 ({}/{})".format(type,dt.strftime("%Y-%m-%d")))
            break
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