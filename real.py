#!/usr/bin/python
# -*- coding: UTF-8 -*-
import wx
import sys,random
import string
import sqlite3
import data
import platform
#import time
import threading
from autocomplete import AutocompleteTextCtrl

template = "%s<b><u>%s</b></u>%s"

class WordFrame(wx.Frame):
    def __init__(self):

        self.pageSize = 18
        self.page_num = 1

        system_os = platform.system()
        if system_os == 'Windows':
            self.fileType = '.wav'
        else:
            self.fileType = '.mp3'

        #wx.Frame.__init__(self, None, -1, "Real World dict",size=(800,780))
        wx.Frame.__init__(self, None, -1, "Real World dict")
        self.panel = wx.Panel(self,-1)
        #self.panel.SetBackgroundColour('Green')
        #self.panel.Refresh()

        self.panel.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)  
        self.panel.Bind(wx.EVT_CHAR, self.OnKeyDown)  
        #self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
       
        #top 
        topSizer = wx.BoxSizer(wx.HORIZONTAL)

        topTitle = wx.StaticText(self.panel, -1, "DICT")
        topTitle.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        #搜索展示部分
        #self.searchCtrl = wx.TextCtrl(self.panel, -1, "",size=(205, -1),style=wx.TE_PROCESS_ENTER)
        self.searchCtrl = AutocompleteTextCtrl(self.panel,completer = self.result_generator,frequency=1000)

        searchBtn = wx.Button(self.panel, -1, "search")
        #给按钮绑定搜索事件
        searchBtn.Bind(wx.EVT_BUTTON, self.BtnSearch)
       
        topSizer.Add(topTitle)
        topSizer.Add((20,20), 1)
        topSizer.Add(self.searchCtrl)
        topSizer.Add(searchBtn)

        #self.searchCtrl.Bind(wx.EVT_TEXT,self.OnEnterTyped)
        self.searchCtrl.Bind(wx.EVT_TEXT_ENTER,self.OnEnterTyped)


        #居中显示的单词
        self.wordLabel = wx.StaticText(self.panel, -1, "",(600, 60),(160,-1),wx.ALIGN_CENTER|wx.ST_NO_AUTORESIZE)
        #self.wordLabel = wx.StaticText(self.panel,-1,style = wx.ALIGN_CENTER)
        self.wordLabel.SetFont(wx.Font(28, wx.SWISS, wx.NORMAL, wx.NORMAL))

        #self.descLabel = wx.StaticText(self.panel, -1, "desc",(600, 60),(160,-1),wx.ALIGN_CENTER))
        self.descLabel = wx.StaticText(self.panel,-1,style = wx.ALIGN_CENTER|wx.ST_NO_AUTORESIZE)
        self.descLabel.SetFont(wx.Font(16, wx.SWISS, wx.NORMAL, wx.NORMAL))
        #self.descLabel.SetLabel('test label')

        prevBtn = wx.Button(self.panel, -1, "Prev Page")
        nextBtn = wx.Button(self.panel, -1, "Next Page")

        clearBtn = wx.Button(self.panel, -1, "Clear")
        speakBtn = wx.Button(self.panel, -1, "Speak")

        self.Bind(wx.EVT_BUTTON, self.GoPrev,prevBtn)
        self.Bind(wx.EVT_BUTTON, self.GoNext,nextBtn)

        self.Bind(wx.EVT_BUTTON, self.Clear,clearBtn)
        self.Bind(wx.EVT_BUTTON, self.PreSpeak,speakBtn)

        # Now do the layout.

        # mainSizer is the top-level one that manages everything
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        mainSizer.Add(topSizer, 0, wx.EXPAND, 10)
        #mainSizer.Add(topLbl, 0, wx.ALL, 5)

        #加一条分割线
        mainSizer.Add(wx.StaticLine(self.panel), 0,
                wx.EXPAND|wx.TOP|wx.BOTTOM, 5)

        self.InitList()
        self.GetWordList()
        listSizer = wx.BoxSizer(wx.HORIZONTAL)
        listSizer.Add(self.list)

        mainSizer.Add(listSizer, 0, wx.EXPAND|wx.BOTTOM, 10)
        #mainSizer.Add(self.list, 0, wx.EXPAND|wx.BOTTOM, 10)

        mainSizer.Add(self.wordLabel, 0,wx.EXPAND|wx.BOTTOM, 10)
        mainSizer.Add(self.descLabel, 0,wx.EXPAND|wx.BOTTOM, 10)

        # The buttons sizer will put them in a row with resizeable
        # gaps between and on either side of the buttons
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add(prevBtn)
        btnSizer.Add(nextBtn)
        #添加一个空格...
        btnSizer.Add((20,20), 1)
        btnSizer.Add(speakBtn)
        btnSizer.Add(clearBtn)

        mainSizer.Add(btnSizer, 0, wx.EXPAND|wx.BOTTOM, 10)

        self.panel.SetSizer(mainSizer)

        # Fit the frame to the needs of the sizer.  The frame will
        # automatically resize the panel as needed.  Also prevent the
        # frame from getting smaller than this size.
        mainSizer.Fit(self)
        #mainSizer.SetSizeHints(self)
    def OnSimple(self, event):
        wx.MessageBox("You selected the simple menu item")

    def OnExit(self, event):
        #self.Close()
        wx.Exit()

    def Clear(self, event):       
        self.list.DeleteAllItems()     
    #按钮搜索
    def BtnSearch(self,event):
        searchStr = self.searchCtrl.GetValue()
        if(searchStr and len(searchStr.strip()) > 0):
            #调用搜索
            listResult = self.Search(searchStr) 
            if len(listResult) > 0:
                wordRecord = listResult[0]
                self.SetInfoLabel(wordRecord)

    def Search(self,searchStr):
        #if (searchStr and searchStr.strip()):
        searchStr = searchStr.lower()
        conn = sqlite3.connect('wenhaotest.db')
        cursor = conn.cursor()
        result = cursor.execute("SELECT id,wordname,desc from english where wordname = '"+ searchStr.strip() + "'")
        resultList = result.fetchall()
        conn.close()
        return resultList
    def PreSpeak(self,event):
            if hasattr(self,'WordId'):
                self.Speak(self.WordId,self.WordReal)
            else:
                wx.MessageBox("No Selected Word", "Stupid")


    def Speak(self,wordId,wordReal):
            folder_size = 500
            folder_name = 'within_' + str( ( int( (wordId - 1) / folder_size) + 1) * folder_size )
            save_path = 'iciba/audio_wav/' + folder_name
            mp3_path = save_path + '/' + wordReal  + self.fileType
            print mp3_path

            self.sound = wx.Sound(mp3_path)
            # error handling ...
            if self.sound.IsOk():
                self.sound.Play(wx.SOUND_ASYNC)
            else:
                wx.MessageBox("Missing or invalid sound file", "Error")


    def OnEnterTyped(self,event):
        searchStr = event.GetString()
        #self.Search(searchStr)
        #调用搜索
        print 'sstr',searchStr
        listResult = self.Search(searchStr) 
        if len(listResult) > 0:
            wordRecord = listResult[0]
            self.SetInfoLabel(wordRecord)
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
        self.list = wx.ListCtrl(self.panel, -1, style=wx.LC_REPORT,size=(680,440))
           # Add some columns
        for col, text in enumerate(['id','wordname','desc','sound']):
            self.list.InsertColumn(col, text)
        self.list.SetTextColour('gray')

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
            self.list.SetStringItem(index,3,'speak')

        # set the width of the columns in various ways
        self.list.SetColumnWidth(0, 120)
        self.list.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        self.list.SetColumnWidth(2, wx.LIST_AUTOSIZE)
        self.list.SetColumnWidth(3, wx.LIST_AUTOSIZE_USEHEADER)

        # bind some interesting events
        #self.Bind(wx.EVT_LIST_ITEM_SelectED, self.OnItemSelected, self.list)
        #self.Bind(wx.EVT_LIST_ITEM_DESelectED, self.OnItemDeselected, self.list)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated, self.list)

    def OnKeyDown(self, event):
        print 'OnKeyDown'
        #按键时相应代码  
        kc = event.GetKeyCode()
        print kc
    def OnItemSelected(self, evt):
        item = evt.GetItem()
        #print "Item selected:", item.GetText()
        
    def OnItemDeselected(self, evt):
        item = evt.GetItem()
        #print "Item deselected:", item.GetText()
    def SpellWord(self):
        if not self.WordReal:
            return

        if self.LetterNo >= len(self.WordReal):
            self.timer.cancel()
            return

        self.LetterTemp += self.WordReal[self.LetterNo]
        self.wordLabel.SetLabel(self.LetterTemp)

        self.timer = threading.Timer(0.2,self.SpellWord)
        self.timer.start()
        self.LetterNo += 1
        

    def SetInfoLabel(self,wordRecord):
        if wordRecord[0] and wordRecord[1]:
            #把单词id和单词保存到全局
            self.WordId = wordRecord[0]
            self.WordReal = wordRecord[1]
            #设置单词和描述标签
            '''
            wordTemp = ''
            for i in range(len(wordRecord[1])):  
                #time.sleep(0.1)  
                wordTemp += wordRecord[1][i]
                self.wordLabel.SetLabel(wordTemp)
            '''
            self.LetterNo = 0
            self.LetterTemp = ''
            self.timer = threading.Timer(1,self.SpellWord)
            
            self.timer.start()

            self.wordLabel.SetLabel(wordRecord[1])
            self.descLabel.SetLabel(wordRecord[2])
    def OnItemActivated(self, evt): 
        item = evt.GetItem()
        #print "Item activated:", item.GetText()
        #print 'item ', item
        print 'evt Index', evt.GetIndex()
        #根据id大小来识别相应的文件夹
        word_id = int(item.GetText())
        li_index = evt.GetIndex()
        word_real = self.list.GetItem(li_index,1).Text
        word_real = word_real.strip()

        desc = self.list.GetItem(li_index,2).Text

        self.WordId = word_id
        self.WordReal = word_real

        #self.SetInfoLabel(word_real,desc)
        self.SetInfoLabel([word_id,word_real,desc])
        self.Speak(word_id,word_real)

    def result_generator(self,query):
        formatted, unformatted = list(), list()
        #wx.Sleep(0.8)
        if query:
            print query
            query = query.strip().lower()
            conn = sqlite3.connect('wenhaotest.db')
            cursor = conn.cursor()
            result = cursor.execute("SELECT wordname from english where wordname like '%"+ query.strip() + "%' limit 20")
            resultList = result.fetchall()
            conn.close()
            '''
            for i in xrange(random.randint(0, 30)):
                prefix = "".join(random.sample(string.letters, random.randint(0, 10)))
                postfix = "".join(random.sample(string.letters, random.randint(0, 10)))
                value = (prefix, query, postfix)
                '''
            for row in resultList:
                word = row[0]
                #wordSp = word.split(query)
                #wordSp = [item for item in filter(lambda x:x != '', wordSp)]
                #print wordSp
                #formatted.append(template % wordSp)
                #unformatted.append("".join(row[0]))
                unformatted.append(word)

            return unformatted,unformatted
  
app = wx.App()
WordFrame().Show()
app.MainLoop()
