#!/usr/bin/python
# -*- coding: UTF-8 -*-
import wx
import sys,random
import sqlite3
import data
class WordFrame(wx.Frame):
    def __init__(self):

        self.pageSize = 20
        self.page_num = 1

        wx.Frame.__init__(self, None, -1, "Real World dict",size=(1000,480))
        self.panel = wx.Panel(self)

          #创建菜单

        menu = wx.Menu()
        simple = menu.Append(-1, "Simple menu item")
        menu.AppendSeparator()
        exit = menu.Append(-1, "Exit")

        self.Bind(wx.EVT_MENU, self.OnSimple, simple)
        self.Bind(wx.EVT_MENU, self.OnExit, exit)

        menuBar = wx.MenuBar()
        menuBar.Append(menu, "Simple Menu")
        self.SetMenuBar(menuBar)

        # First create the controls
        topLbl = wx.StaticText(self.panel, -1, "Words of KAOYAN")
        topLbl.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))

        '''
        nameLbl = wx.StaticText(panel, -1, "Name:")
        name = wx.TextCtrl(panel, -1, "");
        '''

        prevBtn = wx.Button(self.panel, -1, "Prev")
        nextBtn = wx.Button(self.panel, -1, "Next")
        clearBtn = wx.Button(self.panel, -1, "Clear")

        self.Bind(wx.EVT_BUTTON, self.GoPrev,prevBtn)
        self.Bind(wx.EVT_BUTTON, self.GoNext,nextBtn)

        self.Bind(wx.EVT_BUTTON, self.Clear,clearBtn)

        # Now do the layout.

        # mainSizer is the top-level one that manages everything
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topLbl, 0, wx.ALL, 5)
        #加一条分割线
        mainSizer.Add(wx.StaticLine(self.panel), 0,
                wx.EXPAND|wx.TOP|wx.BOTTOM, 5)

        '''
        # addrSizer is a grid that holds all of the address info
        addrSizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)

        addrSizer.AddGrowableCol(1)

        addrSizer.Add(nameLbl, 0,
                wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(name, 0, wx.EXPAND)

      

        # now add the addrSizer to the mainSizer
        mainSizer.Add(addrSizer, 0, wx.EXPAND|wx.ALL, 10)
        
        '''


        self.InitList()
        self.GetWordList()
        listSizer = wx.BoxSizer(wx.HORIZONTAL)
        listSizer.Add(self.list)

        mainSizer.Add(listSizer, 0, wx.EXPAND|wx.BOTTOM, 10)
        #mainSizer.Add(self.list, 0, wx.EXPAND|wx.BOTTOM, 10)


        # The buttons sizer will put them in a row with resizeable
        # gaps between and on either side of the buttons
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add(prevBtn)
        #btnSizer.Add((20,20), 1)
        btnSizer.Add(nextBtn)
        btnSizer.Add(clearBtn)

        mainSizer.Add(btnSizer, 0, wx.EXPAND|wx.BOTTOM, 10)

        self.panel.SetSizer(mainSizer)

        # Fit the frame to the needs of the sizer.  The frame will
        # automatically resize the panel as needed.  Also prevent the
        # frame from getting smaller than this size.
        mainSizer.Fit(self)
        mainSizer.SetSizeHints(self)

    def OnSimple(self, event):
        wx.MessageBox("You selected the simple menu item")

    def OnExit(self, event):
        self.Close()

    def Clear(self, event):       
        self.list.DeleteAllItems()     

    def GoNext(self, event):
        self.page_num += 1
        self.list.DeleteAllItems()
        self.GetWordList()
    def GoPrev(self, event):
        if self.page_num > 1:
            self.list.DeleteAllItems()
            self.page_num -= 1
            self.GetWordList()
        else:
            pass


    def InitList(self):
        self.list = wx.ListCtrl(self.panel, -1, style=wx.LC_REPORT,size=(800,480))
           # Add some columns
        for col, text in enumerate(['id','wordname','desc']):
            self.list.InsertColumn(col, text)

    def GetList(self):
    

        # add the rows
        for item in data.rows:
            index = self.list.InsertStringItem(sys.maxint, item[0])
            for col, text in enumerate(item[1:]):
                self.list.SetStringItem(index, col+1, text)
    def GetWordList(self):



        if self.page_num == 1:
            off_set = 0
        else:
           off_set = self.pageSize * (self.page_num - 1)

        conn = sqlite3.connect('wenhaotest.db')
        cursor = conn.cursor()
        result = cursor.execute("SELECT id,wordname,desc from english limit "+ str(self.pageSize) + " offset " + str(off_set))
        wordlist = result.fetchall()
        conn.close()
        # add the rows
        for item in wordlist:
            index = self.list.InsertStringItem(sys.maxint, str(item[0]))
            for col, text in enumerate(item[1:]):
                self.list.SetStringItem(index, col+1, text)


app = wx.PySimpleApp()
WordFrame().Show()
app.MainLoop()

