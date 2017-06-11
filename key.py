#-*- coding:utf-8 -*-

import wx

class KeyEvent(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title)
        panel = wx.Panel(self, -1)
        panel.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        
        self.Centre()
        self.Show(True)
 
    def OnKeyDown(self, event):
        #按键时相应代码
        kc=event.GetKeyCode()
        if 32<=kc<=126:
            self.SetTitle(chr(kc))

app = wx.App()
KeyEvent(None, -1, 'Test KeyDown Event of wxPython')
app.MainLoop()
