# -*- coding: UTF-8 -*-
import sqlite3
import xlrd
import os,sys

wlx_obj = xlrd.open_workbook('en500.xls')
# 获取sheet
sheet_name = wlx_obj.sheet_names()[0]
sheet = wlx_obj.sheet_by_name(sheet_name)

print sheet
