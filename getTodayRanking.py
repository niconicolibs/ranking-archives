import datetime
import requests
import os

TZ_JST = datetime.timezone(datetime.timedelta(hours=9))
NOW = datetime.datetime.now(TZ_JST)

HEADERS = {
    "User-Agent": "GetRankingData"
}

req_url = "https://dcdn.cdn.nimg.jp/nicovideo/old-ranking/{}/{}/{}"

def downloadFiles(type):
    name_list_res = requests.get(
        req_url.format(type, NOW.strftime("%y-%m-%d"), "file_name_list.json"),
        headers=HEADERS
    )
    currentFolder = ""
    if type == "monthly":
        currentFolder = "./ranking/{}/{}/{}/".format(type, NOW.year, NOW.strftime("%y-%m-%d"))
    else:
        currentFolder = "./ranking/{}/{}/{}/{}/".format(type, NOW.year, NOW.month, NOW.strftime("%y-%m-%d"))
    with open(currentFolder + "file_name_list.json", mode="w", encoding="utf-8") as f:
        f.write(name_list_res.text)
    for cat in name_list_res.json():
        res = requests.get(
            req_url.format(type, NOW.strftime("%y-%m-%d"), cat["file"]),
            headers=HEADERS
        )
        with open(currentFolder + cat["file"], mode="w", encoding="utf-8") as f:
            f.write(res.text)