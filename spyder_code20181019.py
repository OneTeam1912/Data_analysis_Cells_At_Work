# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 18:50:03 2018

@author: yoshiki
"""

import requests
from fake_useragent import UserAgent
import json
import pandas as pd
import time
import datetime
headers = { "User-Agent": UserAgent(verify_ssl=False).random}
comment_api = 'https://bangumi.bilibili.com/review/web_api/short/list?media_id=102392&folded=0&page_size=20&sort=0'

# 发送get请求
response_comment = requests.get(comment_api,headers = headers)
json_comment = response_comment.text
json_comment = json.loads(json_comment)

total = json_comment['result']['total']

cols = ['author','score','disliked','likes','liked','ctime','score','content','last_ep_index','cursor']
dataall = pd.DataFrame(index = range(total),columns = cols)


j = 0
while j <total:
    n = len(json_comment['result']['list'])
    for i in range(n):
        dataall.loc[j,'author'] = json_comment['result']['list'][i]['author']['uname']
        dataall.loc[j,'score'] = json_comment['result']['list'][i]['user_rating']['score']
        dataall.loc[j,'disliked'] = json_comment['result']['list'][i]['disliked']
        dataall.loc[j,'likes'] = json_comment['result']['list'][i]['likes']
        dataall.loc[j,'liked'] = json_comment['result']['list'][i]['liked']
        dataall.loc[j,'ctime'] = json_comment['result']['list'][i]['ctime']
        dataall.loc[j,'content'] = json_comment['result']['list'][i]['content']
        dataall.loc[j,'cursor'] = json_comment['result']['list'][n-1]['cursor'] 
        j+= 1
    try:        
        dataall.loc[j,'last_ep_index'] = json_comment['result']['list'][i]['user_season']['last_ep_index']
    except:
        pass

    comment_api1 = comment_api + '&cursor=' + dataall.loc[j-1,'cursor'] 
    response_comment = requests.get(comment_api1,headers = headers)
    json_comment = response_comment.text
    json_comment = json.loads(json_comment)
    
    if j % 50 ==0:
        print('已完成 {}% !'.format(round(j/total*100,2)))
    time.sleep(0.5)
    
        

dataall = dataall.fillna(0)

def getDate(x):
    x = time.gmtime(x)
    return(pd.Timestamp(datetime.datetime(x[0],x[1],x[2],x[3],x[4],x[5])))

dataall['date'] = dataall.ctime.apply(lambda x:getDate(x))
now = datetime.datetime.now()
now = now.strftime('%y-%m-%H-%M')
dataall.to_csv('bilibilib_gongzuoxibao_%s.xlsx'%now,index = False)

