import datetime
import requests
import os, sys, json, time
from dateutil.relativedelta import relativedelta

HEADERS = {
    "User-Agent": "GetRankingData"
}

req_url = "https://dcdn.cdn.nimg.jp/nicovideo/old-ranking/{}/{}/{}"

dt = datetime.datetime.strptime("2019-12-24", "%Y-%m-%d")

while True:
    print("Start:{}".format(dt.strftime("%Y-%m-%d")))
    for type in ["total", "daily"]:
        for additionTime in ["", "_05"]:
            currentFolder = "./ranking/{}/{}/{}/{}/".format(type, dt.strftime("%Y"), dt.strftime("%m"), dt.strftime("%Y-%m-%d")+additionTime)
            print("Download:{}{}".format(currentFolder, "file_name_list"))
            name_list_res = requests.get(
                req_url.format(type, dt.strftime("%Y-%m-%d")+additionTime, "file_name_list.json"),
                headers=HEADERS
            )
            try:
                name_list_res.json()
            except:
                print("NotFound _05 ({}/{})".format(type,dt.strftime("%Y-%m-%d")))
                break
            if not os.path.exists(currentFolder):
                os.makedirs(currentFolder)
            with open(currentFolder + "file_name_list.json", mode="w", encoding="utf-8") as f:
                f.write(name_list_res.text)
            for cat in name_list_res.json():
                print("Download:{}{}".format(currentFolder, cat["file"]))
                res = requests.get(
                    req_url.format(type, dt.strftime("%Y-%m-%d")+additionTime, cat["file"]),
                    headers=HEADERS
                )
                with open(currentFolder + cat["file"], mode="w", encoding="utf-8") as f:
                    f.write(res.text)
            os.system("git add {}".format(currentFolder))
            print("add: ranking data (current/{}/{})".format(type, dt.strftime("%Y-%m-%d")+additionTime))
    os.system("git commit -m \"{}\"".format("add: ranking data (current/total,daily/{})".format(dt.strftime("%Y-%m-%d"))))
    os.system("git push")
    dt = dt + relativedelta(days=1)
    if dt > datetime.datetime.strptime("2022-09-19", "%Y-%m-%d"):
        break

