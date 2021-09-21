#!/usr/bin/python3
# -*- coding: utf-8 -*-
from http import cookies
import requests, json, sys

#####
# Парсинг текста из телефонного справочника - http://elib.shpl.ru/ru/nodes/25631-na-1936-god-1936
#####

cookies_title={
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Host': 'elib.shpl.ru',
    #'If-None-Match': 'W/"ce67811fc53365e7291ddaaac70f2664"',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/7.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.69 Safari/537.3'
}
headers={}
headers['Referer']='http://elib.shpl.ru/ru/nodes/25631-na-1936-god-1936'
headers['Host']='elib.shpl.ru'
headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.69 Safari/537.36'
headers['DNT']='1'
headers['Accept']  = 'application/json, text/javascript, */*; q=0.01'
headers['Connection'] = 'keep-alive'
headers['Accept-Encoding'] = 'gzip, deflate'

def get_title():
    myList = ['ahoy_visitor','ahoy_visit','_platform_session','elibshplcounter']
    cookies={}
    url = 'http://elib.shpl.ru/ru/nodes/25631-na-1936-god-1936'
    res = requests.get(url, cookies=cookies_title)
    for item in res.headers['Set-Cookie'].split(' '):
        if any(x in item for x in myList):
            cookies[item[0:item.index('=')]] = item[item.index('=')+1:len(item)-1]
    return cookies


#http://sssr-rutracker.org/forum/viewtopic.php?t=4351488


def get_page(page,cookies):
    global headers
    url1 = 'http://elib.shpl.ru/pages/{}/read'.format(page+2358428)
    #print(cookies)
    res = requests.get(url1,cookies=cookies,headers=headers)
    print('*****************************  {}  ***************************'.format(page))
    print(json.loads(res.text)['text'])

    
#2358435 = 7 2358428
#2359185 = 757
original_stdout = sys.stdout # Save a reference to the original standard output

cookies_page = get_title()
with open('filename.txt', 'w') as f:
    sys.stdout = f # Change the standard output to the file we created.
    for page in range(7,757):
        get_page(page,cookies_page)
    sys.stdout = original_stdout # Reset the standard output to its original value

