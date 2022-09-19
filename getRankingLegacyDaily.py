from asyncio import constants
import requests
import json
import datetime
import os, sys, time

HEADERS = {
  "X-Frontend-Id": "6",
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
}

#過去のやつ 2019-06-26まで
#date 取得する日 2007-04-03~2019-06-26
#type 集計対象 fav=総合ポイント comment/view/mylist
#categoryKey カテゴリ名 all
# g_ent2 ent music sing play dance vocaloid nicoindies asmr mmd virtual
# g_life2 animal cooking nature travel sport lecture drive history train
# g_tech science tech handcraft make
# g_politics
# g_culture2 anime game jikkyo toho imas radio draw trpg
# g_other are diary other
# g_r18
# que chat test owner commons hitokoto fashion g_ent g_life g_try g_culture g_popular
#span 期間 daily/total
# favは2009/10/29kara
#REF: https://site.nicovideo.jp/ranking_archives/
"""
res = requests.get(
  "https://nvapi.nicovideo.jp/v1/ranking/legacy?date=2009-10-30&type={}&categoryKey=all&span=daily".format("fav"),
  headers=HEADERS
)
print(res.json())
"""

#old-ranking api
#date 取得する日 2019-06-11~now (daily,totalでは五時のランキングもあるよ 2019-06-11_05)
#ranking_type 期間 daily weekly monthly total
#file_type file_name_list.json {ジャンル}.json {ジャンル}_{01から始まる連番}.json
#REF: https://dwango.github.io/niconico/genre_ranking/ranking_log/
"""
res = requests.get(
  "https://dcdn.cdn.nimg.jp/nicovideo/old-ranking/{ranking_type}/{date}/{file_type}"
)
"""

categorys = [
  "all",
  "g_ent2", "ent", "music", "sing", "play", "dance", "vocaloid", "nicoindies", "asmr", "mmd", "virtual",
  "g_life2", "animal", "cooking", "nature", "travel", "sport", "lecture", "drive", "history", "train",
  "g_tech", "science", "tech", "handcraft", "make",
  "g_politics",
  "g_culture2", "anime", "game", "jikkyo", "toho", "imas", "radio", "draw", "trpg",
  "g_other", "are", "diary", "other",
  "g_r18",
  "que", "chat", "test", "owner", "commons", "hitokoto", "fashion", "g_ent", "g_life", "g_try", "g_culture", "g_popular"
]
cat={'all': ['2007-04-03', '2019-06-26'], 'g_ent2': ['2011-12-09', '2019-06-26'], 'ent': ['2011-12-09', '2019-06-26'], 'music': ['2011-12-09', '2019-06-26'], 'sing': ['2009-10-29', '2019-06-26'], 'play': ['2009-10-29', '2019-06-26'], 'dance': ['2009-10-29', '2019-06-26'], 'vocaloid': ['2009-10-29', '2019-06-26'], 'nicoindies': ['2011-12-09', '2019-06-26'], 'asmr': ['2018-11-02', '2019-06-26'], 'mmd': ['2018-11-02', '2019-06-26'], 'virtual': ['2018-11-02', '2019-06-26'], 'g_life2': ['2011-12-09', '2019-06-26'], 'animal': ['2009-10-29', '2019-06-26'], 'cooking': ['2009-10-29', '2019-06-26'], 'nature': ['2009-10-29', '2019-06-26'], 'travel': ['2011-12-09', '2019-06-26'], 'sport': ['2009-10-29', '2019-06-26'], 'lecture': ['2009-10-29', '2019-06-26'], 'drive': ['2011-12-09', '2019-06-26'], 'history': ['2009-10-29', '2019-06-26'], 'train': ['2018-11-02', '2019-06-26'], 'g_tech': ['2011-12-09', '2019-06-26'], 'science': ['2018-11-02', '2019-06-26'], 'tech': ['2009-10-29', '2019-06-26'], 'handcraft': ['2011-12-09', '2019-06-26'], 'make': ['2011-12-09', '2019-06-26'], 'g_politics': ['2009-10-29', '2019-06-26'], 'g_culture2': ['2011-12-09', '2019-06-26'], 'anime': ['2009-10-29', '2019-06-26'], 'game': ['2009-10-29', '2019-06-26'], 'jikkyo': ['2016-10-05', '2019-06-26'], 'toho': ['2009-10-29', '2019-06-26'], 'imas': ['2009-10-29', '2019-06-26'], 'radio': ['2009-10-29', '2019-06-26'], 'draw': ['2009-10-29', '2019-06-26'], 'trpg': ['2018-11-02', '2019-06-26'], 'g_other': ['2009-10-29', '2019-06-26'], 'are': ['2009-10-29', '2019-06-26'], 'diary': ['2009-10-29', '2019-06-26'], 'other': ['2009-10-29', '2019-06-26'], 'g_r18': ['2009-10-29', '2019-06-26'], 'que': ['2007-12-15', '2009-10-28'], 'chat': ['2007-12-15', '2009-10-28'], 'test': ['2007-12-15', '2009-10-28'], 'owner': ['2007-12-15', '2009-10-28'], 'commons': ['2008-11-13', '2009-10-28'], 'hitokoto': ['2008-12-18', '2009-10-28'], 'fashion': ['2009-10-29', '2010-01-13'], 'g_ent': ['2009-10-29', '2011-12-13'], 'g_life': ['2009-10-29', '2011-12-13'], 'g_try': ['2009-10-29', '2011-12-13'], 'g_culture': ['2009-10-29', '2011-12-13'], 'g_popular': ['2009-10-29', '2011-12-13']}
# ./legacy/daily/categorys/type/year/date.json
# favは2009-10-29kara

session = requests.Session()
session.cookies.set("user_session", "user_session_90733226_15f2f37fd76ca48b3b8cf1d928c3d065fd5bb8ed798ba1f8dd245ab879709b0b")

for c in cat.keys():
  for t in ["fav", "comment", "view", "mylist"]:
    start_date = cat[c][0]
    if start_date == "":
      continue
    if c == "all" or c == "g_ent2" or c == "ent":
      continue
    start_dt = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    if t == "fav":
      if start_dt <= datetime.datetime.strptime("2009-10-29", "%Y-%m-%d"):
        start_dt = datetime.datetime.strptime("2009-10-29", "%Y-%m-%d")
    if not os.path.exists("./legacy/daily/{}".format(c)):
        os.mkdir("./legacy/daily/{}".format(c))
    if not os.path.exists("./legacy/daily/{}/{}".format(c,t)):
      os.mkdir("./legacy/daily/{}/{}".format(c,t))
    batCount = 0
    while True:
      res = session.get(
        "https://nvapi.nicovideo.jp/v1/ranking/legacy?date={}&type={}&categoryKey={}&span=daily".format(start_dt.strftime("%Y-%m-%d"), t, c),
        headers=HEADERS
      );
      r = res.json()
      if not os.path.exists("./legacy/daily/{}/{}/{}".format(c,t,start_dt.strftime("%Y"))):
        os.mkdir("./legacy/daily/{}/{}/{}".format(c,t,start_dt.strftime("%Y")))
      if not os.path.exists("./legacy/daily/{}/{}/{}/{}".format(c,t,start_dt.strftime("%Y"),start_dt.strftime("%m"))):
        os.mkdir("./legacy/daily/{}/{}/{}/{}".format(c,t,start_dt.strftime("%Y"),start_dt.strftime("%m")))
      with open("./legacy/daily/{}/{}/{}/{}/{}.json".format(c,t,start_dt.strftime("%Y"),start_dt.strftime("%m"),start_dt.strftime("%Y-%m-%d")), mode="w", encoding="utf-8") as f:
        f.write(res.text)
        print("Save:{}/{} {}".format(c,t,start_dt.strftime("%Y-%m-%d")))
      start_dt += datetime.timedelta(days=1)
      if start_dt > datetime.datetime.strptime(cat[c][1], "%Y-%m-%d"):
        break
