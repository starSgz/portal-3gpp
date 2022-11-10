# https://portal.3gpp.org/#/55930-meetings

import requests
import json
import csv

from concurrent.futures import ThreadPoolExecutor, as_completed

#从99年开始

def get_number(year):
    headers = {
        "authority": "portal.3gpp.org",
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "content-type": "application/json;charset=UTF-8",
        "origin": "https://portal.3gpp.org",
        "pragma": "no-cache",
        "referer": "https://portal.3gpp.org/",
        "sec-ch-ua": "\"Google Chrome\";v=\"107\", \"Chromium\";v=\"107\", \"Not=A?Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }
    url = "https://portal.3gpp.org/webservices/Rest/Meetings.svc/GetMeetings"

    data = {
        "getMeetingsInput": {
            "StartRow": 0,
            "ResultsPerPage": 100,
            "SortBy": "Date",
            "SortAscending": True,
            "StartDate": "{}-01-01 00:00:00".format(year),
            "EndDate": "{}-12-31 00:00:00".format(year),
            "Tbs": [
                369
            ],
            "IncludeChildTbs": True,
            "IncludeNonTBMeetings": False,
            "Reference": "",
            "Registered": False
        }
    }
    data = json.dumps(data)
    response = requests.post(url, headers=headers, data=data)
    print(response)
    res = json.loads(response.text)

    return res,year

if __name__ == '__main__':
    pool = ThreadPoolExecutor(max_workers=10)
    task_list=[]
    for i in range(1999,2023):
        th = pool.submit(get_number,i)
        task_list.append(th)

    for i in as_completed(task_list):
        data,year = i.result()
        for i in data:
            u = [i['Id'],year]
            with open('1.csv', mode="a+", encoding="utf-8-sig", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(u)
