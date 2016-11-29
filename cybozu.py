#!/usr/bin/python
# -*- coding: utf-8 -*-
import ConfigParser
import datetime
import urllib
import re
import requests

inifile = ConfigParser.SafeConfigParser()
inifile.read('./config.ini')

DURATION_AFTER = int(inifile.get("settings","DURATION_AFTER"))
DURATION_BEFORE = int(inifile.get("settings","DURATION_BEFORE"))
BASE_URL = inifile.get("settings","BASE_URL")
ID = inifile.get("settings","ID")
PASSWORD = inifile.get("settings","PASSWORD")
SAVE_FILE_NAME= inifile.get("settings","SAVE_FILE_NAME")
SAVE_FILE_ENCODING = inifile.get("settings","SAVE_FILE_ENCODING")

today = datetime.date.today()
start_day = today - datetime.timedelta(days=DURATION_BEFORE)
end_day = today + datetime.timedelta(days=DURATION_AFTER)

START_YEAR = start_day.year
START_MONTH = start_day.month
START_DAY = start_day.day
END_YEAR = end_day.year
END_MONTH = end_day.month
END_DAY = end_day.day

login_dic = {
    "csrf_ticket": "",
    "_System": "login",
    "_Login": "1",
    "LoginMethod": "",
    "_ID": ID,
    "Password": PASSWORD,
    "Submit": "ログイン"
}

csv_dic = {
    "Page": "PersonalScheduleExport",
    "CT": "1",
    "SetDate.Year": START_YEAR,
    "SetDate.Month": START_MONTH,
    "SetDate.Day": START_DAY,
    "EndDate.Year": END_YEAR,
    "EndDate.Month": END_MONTH,
    "EndDate.Day": END_DAY,
    "ItemName": "1",
    "oencoding": "UTF-8",
    "EncodeNCR": ";NCR",
    "Export": "書き出し",
    "ext": ".csv"
}


session = requests.Session()
try:
    response = session.post(BASE_URL + urllib.urlencode(login_dic))
except:
    pass

toppage = session.get(BASE_URL)

csv_dic["csrf_ticket"] = re.findall(
    r"csrf_ticket\" value=\"(.+)\"", toppage.text)[0]

csv_data = session.post(BASE_URL + urllib.urlencode(csv_dic))

with open(SAVE_FILE_NAME, "wb") as f:
    f.write(csv_data.text.encode(SAVE_FILE_ENCODING))
