#!/usr/bin/python
# -*- encoding:utf-8 -*-

for i in range(1,10):
    s=''
    for j in range(1,i+1):
        s+="%d*%d=%d\t"%(i,j,i*j) #这是比较关键一步，如果不这样，就会成为全部竖着的，而不是一个三角形
    print s

