#-*- coding: UTF-8 -*-  
import requests

req = requests.get('http://music.baidu.com/data/music/file?link=&song_id=1128053'.decode('utf-8'))  
with open('C:/冰雨.mp3'.decode('utf-8'), 'wb') as code:  
    code.write(req.content) 
