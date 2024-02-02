from urllib.request import urlopen
from bs4 import BeautifulSoup
import codecs
import glob
import time
import requests

with open('hoge/hoge.txt') as f:
 for index, url in enumerate(f):
  url = url.rstrip('\n')
  res = requests.get(url)
  if res.status_code == 404:
   print(url + ';' + '404', file=codecs.open('hoge/'+ f'{index:04}' +'.txt', 'w', encoding='UTF-8'))
   continue
  time.sleep(1)
  html = urlopen(url).read()
  soup = BeautifulSoup(html, features="html.parser")
  title = soup.find('title').text
  des = soup.find('meta', attrs={'name': 'description'}).get('content')     
  key_tag = soup.find('meta', attrs={'name': 'keywords'})
  key = key_tag.get('content') if key_tag else ""  # キーワードがない場合は空文字を設定
  
  # URL;title;description;keywords　という形で出力      
  print(url + ';' + title + ';' + des + ';' + key, file=codecs.open('hoge/'+ f'{index:04}' +'.txt', 'w', 
  encoding='UTF-8'))
  time.sleep(2)

readFiles = glob.glob("hoge/*.txt")
sortReadFiles = sorted(readFiles)
with open("hoge/result.txt", "wb") as resultFile:
 for f in sortReadFiles:
  with open(f, "rb") as infile:
   resultFile.write(infile.read())
