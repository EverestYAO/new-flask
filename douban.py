#-*- coding: UTF-8 -*-
from urllib.request import Request, urlopen
from urllib.error import URLError,HTTPError
import re
import sys
import sqlite3
import time

import sys
import json

conn = sqlite3.connect('data-dev.sqlite')

#sql = """CREATE TABLE douban( id int primary key not null auto_increment,title text,actor text ,rating char(20))"""
#conn.execute('DROP TABLE IF EXISTS douban')
#conn.execute(''' CREATE TABLE douban
				#(id INT PRIMARY KEY ,
				#title TEXT, actor TEXT,body TEXT,rating STRING(50),pic TEXT,url TEXT)''')
#连接数据库，查看有没有douban这个表，如果有，删掉然后新建一个


url ='https://movie.douban.com/j/chart/top_list?type=10&interval_id=100:90&action=&start=20&limit=20'
req = Request(url)
user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit'
req.add_header('User-Agent' ,user_agent)
try:
	response = urlopen(req)
except HTTPError as e:
	print ('The server couldn\'t fulfill the request.')
	print ('Error code:',e.code)
except URLError as e:
	print('We failed to reach a server.')
	print('Reason:',e.reason)
html = response.read().decode('utf-8')

lp= re.compile(r'movie.douban.com.*?subject.*?\d+')
link=lp.findall(html)
#连接豆瓣网，找出分类页面中所有电影的超链接地址




for i in link:
	i=(i.replace('\\',''))
#由于找出来的链接都存在着'\'这个转义符，所以要替换掉
	url ='https://'+ i
	req = Request(url)
	user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit'
	req.add_header('User-Agent' ,user_agent)
	try:
		response = urlopen(req)
	except HTTPError as e:
		print ('The server couldn\'t fulfill the request.')
		print ('Error code:',e.code)
	except URLError as e:
		print('We failed to reach a server.')
		print('Reason:',e.reason)
	html = response.read().decode('utf-8')

#从找出来的所有链接中，利用for循环一条一条接入


	p1 = re.compile(r'<span property="v:itemreviewed">(.*?)</span>')
	p2=re.compile(r'"v:starring">(.*?)</a>')
	p3=re.compile(r'<strong class="ll rating_num" property="v:average">(.*?)</strong>')
	p4=re.compile(r'<span property="v:summary".*\s(.*)')
	p5=re.compile(r'<img src="(.*?)" title="点击')
	t =p1.findall(html)
	a=p2.findall(html)
	r=p3.findall(html)
	b=p4.findall(html)
	p=p5.findall(html)

	sql2='INSERT INTO douban(TITLE,ACTOR,RATING) \
	 VALUES("%s","%s","%s")'
	print (b)
	try:
		conn.execute('INSERT INTO douban(id,title,actor,body,rating,pic,url) \
	 	VALUES(null,"{title}","{actor}","{body}","{rating}","{pic}","{url}")'.format(title=t[0],actor=a[0],body=b[0].strip(),rating=r,pic=p[0],url=url))
	except:
		print('faild')
	conn.commit()
	for j in t:
		print("正在写入"+j)
	time.sleep(0.5)
#然后利用正则把每部电影的标题，演员，评分找出来写进数据库
#休息个0.5秒，下一步电影
