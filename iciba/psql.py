# -*- coding: utf-8 -*-

import sqlite3

conn = sqlite3.connect('wenhaotest.db')
cursor = conn.cursor()
result = cursor.execute("SELECT wordname from english limit 10")
wordlist = result.fetchall()
for row in wordlist:
    print row[0]
print "#############";
conn.close()
