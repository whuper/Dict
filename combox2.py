# -*- coding: utf-8 -*-
import wx

class PromptingComboBox(wx.ComboBox) :
    def __init__(self, parent, value, choices=[], style=0, **par):
        wx.ComboBox.__init__(self, parent, wx.ID_ANY, value, style=style|wx.CB_DROPDOWN, choices=choices, **par)
        self.choices = choices
        #分别绑定多个事件，文本内容变化，字符输入
        self.Bind(wx.EVT_TEXT, self.EvtText)
        self.Bind(wx.EVT_CHAR, self.EvtChar)
        self.Bind(wx.EVT_COMBOBOX, self.EvtCombobox) 
        self.ignoreEvtText = False

    def EvtCombobox(self, event):
        self.ignoreEvtText = True
        event.Skip()

    def EvtChar(self, event):
        #这里需要注意一点事，回车键如果不过滤掉的话，EvtText会类似于进入死循环，这里还不太清楚到底是为什么
        if event.GetKeyCode() == 8:
            self.ignoreEvtText = True
        event.Skip()

    def EvtText(self, event):

        currentText = event.GetString()
        #这里先判断内容是否为空，如果为空的话，需要让下拉菜单隐藏起来
        if currentText=='':
            self.SetItems(self.choices)
            self.Dismiss()
        if self.ignoreEvtText:
            self.ignoreEvtText = False
            return

        currentText = event.GetString()
        found = False
        choiceTemp = []
        for choice in self.choices :
            if choice.startswith(currentText):
                self.ignoreEvtText = True
                found = True
                choiceTemp.append(choice)
        #进行文本匹配后，如果存在的话，就将combobox的内容置为匹配到的列表,再弹出下拉菜单
        if found:
            print choiceTemp[0]
            self.SetItems(choiceTemp)
            self.Popup()
            self.SetValue(currentText)
            self.SetInsertionPoint(len(currentText))
            self.ignoreEvtText = False
        if not found:
            self.Dismiss()
            self.SetInsertionPoint(len(currentText))
            event.Skip()

class TrialPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, wx.ID_ANY)

        choices = [u'中国', u'中文', u'中美', 'aunt', 'uncle', 'grandson', 'granddaughter']

        cb = PromptingComboBox(self, "", choices, style=wx.CB_DROPDOWN) 

    def derivedRelatives(self, relative):
        return [relative, 'step' + relative, relative + '-in-law']


if __name__ == '__main__':
    app = wx.App()
    frame = wx.Frame (None, -1, 'Demo PromptingComboBox Control', size=(400, 200))
    TrialPanel(frame)
    frame.Show()
    app.MainLoop()
