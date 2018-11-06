# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 19:36:24 2018

@author: hzp0625
"""
from selenium import webdriver
import pandas as pd
from datetime import datetime
import numpy as np
import time
import os

os.chdir('F:\\python_study\\pachong\\工作细胞')
def gethtml(url):

    browser = webdriver.PhantomJS()    
    browser.get(url)
    browser.implicitly_wait(10)
    return(browser)

def getComment(url):
   
    browser =  gethtml(url)
    i = 1
    AllArticle = pd.DataFrame(columns = ['id','author','comment','stars1','stars2','stars3','stars4','stars5','unlike','like'])
    print('连接成功，开始爬取数据')    
    while True:

        xpath1 = '//*[@id="app"]/div[2]/div[2]/div/div[1]/div/div/div[4]/div/div/ul/li[{}]'.format(i)
        try:
            target = browser.find_element_by_xpath(xpath1)
        except:
            print('全部爬完')
            break
            
        author = target.find_element_by_xpath('div[1]/div[2]').text
        comment = target.find_element_by_xpath('div[2]/div').text
        stars1 = target.find_element_by_xpath('div[1]/div[3]/span/i[1]').get_attribute('class')
        stars2 = target.find_element_by_xpath('div[1]/div[3]/span/i[2]').get_attribute('class')
        stars3 = target.find_element_by_xpath('div[1]/div[3]/span/i[3]').get_attribute('class')
        stars4 = target.find_element_by_xpath('div[1]/div[3]/span/i[4]').get_attribute('class')
        stars5 = target.find_element_by_xpath('div[1]/div[3]/span/i[5]').get_attribute('class')
        date = target.find_element_by_xpath('div[1]/div[4]').text
        like = target.find_element_by_xpath('div[3]/div[1]').text
        unlike = target.find_element_by_xpath('div[3]/div[2]').text
        
        
        comments = pd.DataFrame([i,author,comment,stars1,stars2,stars3,stars4,stars5,like,unlike]).T
        comments.columns = ['id','author','comment','stars1','stars2','stars3','stars4','stars5','unlike','like']
        AllArticle = pd.concat([AllArticle,comments],axis = 0)
        browser.execute_script("arguments[0].scrollIntoView();", target)
        i = i + 1
        if i%100 == 0:
            print('已爬取{}条'.format(i))
    AllArticle = AllArticle.reset_index(drop = True)
    return AllArticle

url = 'https://www.bilibili.com/bangumi/media/md102392/?from=search&seid=8935536260089373525#short'




result = getComment(url)

#result.to_csv('工作细胞爬虫.csv',index = False)


