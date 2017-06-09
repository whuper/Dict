# -*- coding: utf-8 -*-

import os
import urllib2
import sqlite3
class Crawler:
  def main(self):

    folder_size = 500

    conn = sqlite3.connect('wenhaotest.db')
    cursor = conn.cursor()
    result = cursor.execute("SELECT id,wordname from english LIMIT 1500 OFFSET 4000")
    wordlist = result.fetchall()
    cursor.close()
    conn.close()
    for row in wordlist:
        word_id = row[0]
        word = row[1].strip()
        print(word + '###' + str(word_id))
        req = urllib2.Request('http://dict.youdao.com/dictvoice?audio=' + word + '&type=1')
        req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:5.0)')

        urllib2.socket.setdefaulttimeout(10) # 超时10秒
        response = urllib2.urlopen(req)
        #获取文件流
        data = response.read()
        #根据id大小来放进相应的文件夹
        folder_name = 'within_' + str( ( int( (word_id - 1) / folder_size) + 1) * folder_size )
        save_path = 'audio/' + folder_name

        # 如果不存在,创建目录
        if not os.path.exists(save_path):
           os.mkdir(save_path)

        #写入文件
        with open(save_path + '/' + word + '.mp3','wb') as bitfile:
            bitfile.write(data)  
            bitfile.close()

if __name__ == '__main__':
  me=Crawler()
  me.main()
