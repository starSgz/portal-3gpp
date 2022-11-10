import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import  pandas as  pd
def downloac_excel(year,id):
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
    try:
        r = requests.get(url='https://portal.3gpp.org/ngppapp/GenerateDocumentList.Aspx?meetingId={}'.format(id),headers=headers,timeout=10)
        with open("./excel/{}+{}.xlsx".format(year,id), "wb") as f:
            f.write(r.content)
            f.close()
        return "{}执行成功".format(id)
    except:
        return "{}执行失败".format(id)

if __name__ == '__main__':
    # downloac_excel(2020,28629)
    pool = ThreadPoolExecutor(max_workers=2)

    excel_Data = pd.read_csv('1.csv')

    excel_Data.columns = ['id', 'year']

    task_list=[]
    for id,year in zip(excel_Data['id'],excel_Data['year']):
        th = pool.submit(downloac_excel,year,id)
        task_list.append(th)
    for i in as_completed(task_list):
        print(i.result())