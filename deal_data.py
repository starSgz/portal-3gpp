import os
import pandas as pd
pd.set_option('display.max_rows', None)
from  concurrent.futures  import ThreadPoolExecutor,as_completed
import multiprocessing
import threading

import logging

lock = threading.Lock()
logging.basicConfig(filename='./testLog.txt', level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',filemode="a+")

##1999-2022





def get_data_pandas(excel_Data,i):
    """
    :param excel_Data:
    :param i:
    :return: df_data:返回的是整个年份的pandas数据 count_meet:这一年的会议次数,i:年份
    """
    data_year = excel_Data[excel_Data['year'] == i]
    count_meet = 0

    # 除掉重复id
    data_year.drop_duplicates(subset='id', inplace=True, keep='last')
    # 创建空值dataframe
    df_data = pd.DataFrame(data=None, columns=['Source', 'TDoc Status'])

    for id, year in zip(data_year['id'], data_year['year']):
        print(id, year)
        try:
            data = pd.read_excel('./excel/{}+{}.xlsx'.format(year, id))[['Source', 'TDoc Status']]
            count_meet=len(data) + count_meet
            # print(data)
            # 出去nan值
            a = data.dropna(axis=0, subset=['Source'])
            if a.empty:
                # logging.info('./excel/{}+{}.xlsx'.format(year, id)+"是NAN！")
                continue
            # 去掉nan值后的数据
        except:
            # logging.error('./excel/{}+{}.xlsx'.format(year,id)+"处理错误！")
            continue

        df_data = pd.concat([df_data, a], axis=0, ignore_index=True)
        # print(df_data)
    return df_data,count_meet,i

def count_excel(year_pandas,year,count_meet):
    #df[df['col_name'].str.contains('sp1') | df['col_name'].str.contains('sp2')]
    huawei_data = year_pandas[year_pandas['Source'].str.contains('Huawei') | year_pandas['Source'].str.contains('huawei')]
    print(huawei_data)
    huawei_data_meetCount =len(huawei_data)

    #Available  agreed approved
    verify = huawei_data['TDoc Status'].str.contains('available') |huawei_data['TDoc Status'].str.contains('agreed')|huawei_data['TDoc Status'].str.contains('approved')
    huawei_data_meetCount_already = huawei_data[verify]

    a ="{}年华为会议出现的次数: {}".format(year,huawei_data_meetCount)
    b ="{}年华为会议出席的次数: {}".format(year,len(huawei_data_meetCount_already))
    c ="{}年会议总次数: {}".format(year,count_meet)

    lock.acquire()
    print("{}年华为会议出现的次数:".format(year),huawei_data_meetCount)
    print("{}年华为会议出席的次数:".format(year),len(huawei_data_meetCount_already))
    print("{}年会议总次数:".format(year),count_meet)

    with open('数据计算.txt',mode="a+",encoding="utf-8-sig") as f:
        f.write('\n')
        f.write("{}年".format(year))
        f.write('\n')
        f.write(a)
        f.write('\n')
        f.write(b)
        f.write('\n')
        f.write(c)
        f.write('\n')
        f.close()
    lock.release()
    return (a,b,c)
    # return huawei_data_meetCount,huawei_data_meetCount_already



if __name__ == '__main__':


    excel_Data = pd.read_csv('1.csv')
    excel_Data.columns = ['id', 'year']

    #进程池
    # mpool = multiprocessing.Pool(processes=1)

    #线程池
    mpool = ThreadPoolExecutor(max_workers=10)
    tpool = ThreadPoolExecutor(max_workers=10)

    # 获取每一年的id year
    task_m = []
    for i in range(1999,2023):
        task = mpool.submit(get_data_pandas,excel_Data,i)
        task_m.append(task)

    task_t = []
    for i in as_completed(task_m):
        year_pandas,count_meet,year =i.result()
        task = tpool.submit(count_excel,year_pandas,year,count_meet)
        task_t.append(task)

    for i in as_completed(task_t):
        data = i.result()




    ##测试
    # dicts = {
    #     'Source':['huawei','Huawei','sss','zzz','huawei',"hau","华为","huawei"],
    #     'TDoc Status':['available','Available','sss','agreed','approved',6,7,8]
    #     # 'TDoc Status':[1,2,3,4,5,6,7,8]
    # }
    # data =pd.DataFrame(dicts)
    #
    # print(count_excel(data, 2020, 100))



