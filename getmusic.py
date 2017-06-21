#!/usr/bin/python
#coding:utf-8

import re
import requests
import json
import urllib2
import os
import sys

minimumsize = 1

print "ID: " + sys.argv[1] + "\n";
url = "http://music.163.com/playlist?id=" + sys.argv[1]
r = requests.get(url)
contents = r.text
res = r'<ul class="f-hide">(.*?)</ul>'
mm = re.findall(res, contents, re.S | re.M)
res = r'<li><a .*?>(.*?)</a></li>'
mm = re.findall(res, contents, re.S | re.M)

for value in mm:

    url = 'http://sug.music.baidu.com/info/suggestion'
    payload = {'word': value, 'version': '2', 'from': '0'}
    print "Song Name: " + value

    r = requests.get(url, params=payload)
    contents = r.text
    d = json.loads(contents, encoding="utf-8")
    if('data' not in d):
    	print "do not have flac\n"
        continue
    if('song' not in d["data"]):
    	print "do not have flac\n"
    	continue
    songid = d["data"]["song"][0]["songid"]
    print "Song ID: " + songid 

    url = "http://music.baidu.com/data/music/fmlink"
    payload = {'songIds': songid, 'type': 'mp3'}
    r = requests.get(url, params=payload)
    contents = r.text
    d = json.loads(contents, encoding="utf-8")
    if d is not None and 'data' not in d or d['data'] == '':
        continue
    songlink = d["data"]["songList"][0]["songLink"]
    if(len(songlink) < 10):
        print "do not have flac\n"
        continue
	print "Song Source: " + songlink + "\n";

    songdir = "songs"
    if not os.path.exists(songdir):
        os.makedirs(songdir)

    songname = d["data"]["songList"][0]["songName"]
    artistName = d["data"]["songList"][0]["artistName"]
    filename = "./" + songdir + "/" + songname + "-" + artistName + ".flac"

    f = urllib2.urlopen(songlink)
    headers = requests.head(songlink).headers
    size = int(headers['Content-Length']) / (1024 ** 2)

    if not os.path.isfile(filename) or os.path.getsize(filename) < minimumsize:
        print "%s is downloading now ......\n" % songname
        with open(filename, "wb") as code:
                code.write(f.read())
    else:
        print "%s is already downloaded. Finding next song...\n\n" % songname
print "\n================================================================\n"
print "Download finish!"
