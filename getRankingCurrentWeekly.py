import datetime
import requests
import os, sys, json, time
from dateutil.relativedelta import relativedelta

HEADERS = {
    "User-Agent": "GetRankingData"
}

req_url = "https://dcdn.cdn.nimg.jp/nicovideo/old-ranking/{}/{}/{}"

currentFolder = "./ranking/{}/{}/{}/"

dt = datetime.datetime.strptime("2022-09-26", "%Y-%m-%d")

while True:
    print("Start:{}".format(currentFolder.format("weekly", dt.year, dt.strftime("%Y-%m-%d"))))
    name_list_res = requests.get(
        req_url.format("weekly", dt.strftime("%Y-%m-%d"), "file_name_list.json"),
        headers=HEADERS
    )
    if not os.path.exists(currentFolder.format("weekly", dt.year, dt.strftime("%Y-%m-%d"))):
        os.makedirs(currentFolder.format("weekly", dt.year, dt.strftime("%Y-%m-%d")))
    with open(currentFolder.format("weekly", dt.year, dt.strftime("%Y-%m-%d")) + "file_name_list.json", mode="w", encoding="utf-8") as f:
        f.write(name_list_res.text)
    for cat in name_list_res.json():
        res = requests.get(
            req_url.format("weekly", dt.strftime("%Y-%m-%d"), cat["file"]),
            headers=HEADERS
        )
        with open(currentFolder.format("weekly", dt.year, dt.strftime("%Y-%m-%d")) + cat["file"], mode="w", encoding="utf-8") as f:
            f.write(res.text)
        time.sleep(0.5)
    os.system("git add {}".format(currentFolder.format("weekly", dt.year, dt.strftime("%Y-%m-%d"))))
    print("add: ranking data (current/weekly/{})".format(dt.strftime("%Y-%m-%d")))
    os.system("git commit -m \"{}\"".format("add: ranking data (current/weekly/{})".format(dt.strftime("%Y-%m-%d"))))
    dt = dt + relativedelta(weeks=1)
    time.sleep(5)
    if dt > datetime.datetime.strptime("2022-09-26", "%Y-%m-%d"):
        os.system("git push")
        break

