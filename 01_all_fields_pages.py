#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests, re
import asyncio,urllib.parse
import csv,sys
import sqlite3
import argparse
from bs4 import BeautifulSoup

conn = sqlite3.connect('./db/all_fields.db') # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()
 
def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('name', nargs='?')
    return parser
 
 
if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args()
    # если что-то передали в аргументах, удаляем таблицы и все заново
    if namespace.name:
        cursor.execute("DROP TABLE if exists search_ids")
        cursor.execute("DROP TABLE if exists pages")
        #print ("Привет, {}!".format (namespace.name) )

# Создание таблицы
cursor.execute("DROP TABLE if exists cookies")
cursor.execute("DROP TABLE if exists headers")


cursor.execute("CREATE TABLE if not exists pages (num integer)")
cursor.execute("CREATE TABLE if not exists search_ids (id integer,doc text, f1 text,f2 text,f3 text,f4 text,f5 text,f6 text,f7 text,f8 text,f9 text,f10 text, flag integer)")
cursor.execute("CREATE TABLE if not exists cookies (key text, value text )")
cursor.execute("CREATE TABLE if not exists headers (key text, value text )")
cursor.execute("SELECT num FROM pages")
data = cursor.fetchone()
if data is None:
    cursor.execute('insert into pages(num) values (0)')
    conn.commit()
    insertedPages=int(0)
else:
    insertedPages = data[0]


sys.tracebacklimit = None
cookies = {}
headers={}
secret_cookie = "3fbe47cd30daea60fc16041479413da2"
secret_cookie_value = ''
JSESSIONID_value = ''
countPages = ''

loop = asyncio.get_event_loop()

url1= 'https://obd-memorial.ru/html'
url2 = '/search.htm?'

# место призыва - d
# место рождения - pb
# место службы - lp
url3='d=P~липецкая%20обл&entity=000000011111110&entities=24,28,27,23,34,22,20,21&ps=200'


def excepthook(type, value, traceback):
    print(value)
    print('excepthook')

sys.excepthook = excepthook

def main():
    global JSESSIONID_value, secret_cookie,secret_cookie_value, countPages, headers, cookies, url2,url3
    URL = 'https://obd-memorial.ru/html'
    URL_search = URL + '/search.htm?'+url3
    s = requests.get('https://obd-memorial.ru/html/advanced-search.htm')
    print(s.status_code)
    if(s.status_code==307 or s.status_code==200):
        secret_cookie_value = s.cookies[secret_cookie]
        cookies = { secret_cookie:secret_cookie_value}
        cookies['request']=urllib.parse.quote(url3)
        headers['cookie']=secret_cookie+"="+secret_cookie_value
        headers['path'] = '/html/search.htm?'+urllib.parse.quote(url3)
        headers['referer']='https://obd-memorial.ru/html/advanced-search.htm'
        headers['cookie']=secret_cookie+"="+secret_cookie_value+'; request='+urllib.parse.quote(url3)
        headers['referer']='https://obd-memorial.ru/html/advanced-search.htm'
        headers['authority'] = 'obd-memorial.ru'
        headers['User-Agent']='Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0'
        headers['Accept']='text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        headers['Accept-Language'] = 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'
        headers['Accept-Encoding'] = 'gzip, deflate, br'
        headers['Connection'] = 'keep-alive'
        headers['Upgrade-Insecure-Requests']='1'
        headers['path'] = '/html/search.htm?'+urllib.parse.quote(url3)
        r1 = requests.get(URL_search,cookies=cookies,headers=headers)
        if('JSESSIONID' in r1.cookies.keys()):
            #print(r1.cookies)
            JSESSIONID_value =  r1.cookies["JSESSIONID"]
            cookies = {'JSESSIONID': JSESSIONID_value, secret_cookie:secret_cookie_value}
            cookies['request']=urllib.parse.quote(url3)
            cookies['showExtendedParams']='false'
            headers['JSESSIONID'] = JSESSIONID_value
            headers['referer']='https://obd-memorial.ru/html/advanced-search.htm'
            headers['authority'] = 'obd-memorial.ru'
            headers['User-Agent']='Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0'
            headers['Accept']='text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
            headers['Accept-Language'] = 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'
            headers['Accept-Encoding'] = 'gzip, deflate, br'
            headers['Connection'] = 'keep-alive'
            headers['cookie']=secret_cookie+"="+secret_cookie_value+'; request='+urllib.parse.quote(url3)+'; JSESSIONID='+JSESSIONID_value
            headers['Upgrade-Insecure-Requests']='1'
            headers['path'] = '/html/search.htm?'+urllib.parse.quote(url3)

            r2 = requests.get(URL_search,cookies=cookies,headers=headers)
            print(r2)
            match = re.search(r'countPages = \d+',r2.text)
            if match:
                m1=re.search(r'\d+',match[0])
                countPages = (m1[0])
            if(countPages==''):
                raise ValueError('Не определилось число страниц!')

            for key, value in cookies.items():
                sql= 'insert into cookies (key, value) VALUES("'+key+'","'+value+'")'
                cursor.execute(sql)
            for key, value in headers.items():
                sql= 'insert into headers (key, value) VALUES("'+key+'","'+value+'")'
                cursor.execute(sql)
            conn.commit
        else:
            print('else')


main()

async def get_page(page):
    global cookies,headers
    ids={}
    if(page==0):
        URL_search =url1+url2+url3
        cookies[secret_cookie]=secret_cookie_value
        cookies['request']=urllib.parse.quote(url3)
        headers['cookie']=secret_cookie+"="+secret_cookie_value
        res1 = requests.get(URL_search,cookies=cookies,headers=headers)
        if('JSESSIONID' in res1.cookies.keys()):
            cookies[secret_cookie]=secret_cookie_value
            cookies['request']=urllib.parse.quote(url3)
            cookies['JSESSIONID'] = JSESSIONID_value
            print('URL = '+URL_search)
            res2 = requests.get(URL_search,cookies=cookies,headers=headers,timeout=10)
            soup = BeautifulSoup(res2.text, 'html.parser')
            list_result = soup.find_all("div", {"class": "search-result"})
            while (len(list_result)==0):
                res2 = requests.get(URL_search,cookies=cookies,headers=headers,timeout=10)
                soup = BeautifulSoup(res2.text, 'html.parser')
                list_result = soup.find_all("div", {"class": "search-result"})
            #print('status - {}, length - {}'.format(res2.status_code,len(list_result)))
            for res in list_result:
                ids[res['id']]=res.find('div', {"class":"search-result__col-pos-and-icon"}).find('img')['title']
            return ids
    else:
        URL_search =url1+url2+url3+'&p='+str(page+1)
        cookies[secret_cookie]=secret_cookie_value
        cookies['request']=urllib.parse.quote(url3)
        cookies['JSESSIONID'] = JSESSIONID_value
        res1 = requests.get(URL_search,cookies=cookies,headers=headers)
        if(secret_cookie in res1.cookies.keys()):
            res2 = requests.get(URL_search,cookies=cookies,headers=headers,timeout=10)
            soup = BeautifulSoup(res2.text, 'html.parser')
            list_result = soup.find_all("div", {"class": "search-result"})
            while (len(list_result)==0):
                res2 = requests.get(URL_search,cookies=cookies,headers=headers,timeout=10)
                soup = BeautifulSoup(res2.text, 'html.parser')
                list_result = soup.find_all("div", {"class": "search-result"})

            #print('status - {}, length - {}'.format(res2.status_code,len(list_result)))
            for res in list_result:
                ids[res['id']]=res.find('div', {"class":"search-result__col-pos-and-icon"}).find('img')['title']
            return ids


async def fxMain():
    global countPages, insertedPages
    print('countPages = {}'.format(countPages))
    print('insertedPages = {}'.format(insertedPages))

    futures = [get_page(i) for i in range(insertedPages, int(countPages))]

    print('futures.count = {}'.format(len(futures)))
    for i, future in enumerate(futures):
        result = await future
        for key, value in result.items():
            #print('insert into search_ids(id,doc,flag) values ('+key+','+value+',0)')
            cursor.execute('insert into search_ids(id,doc,flag) values ('+key+',"'+value+'",0)')
        cursor.execute('update pages set num='+str(i+insertedPages+1))
        conn.commit()
        print('{} {} {}'.format((i+insertedPages), countPages,len(result)))


loop.run_until_complete(fxMain())
loop.close()
