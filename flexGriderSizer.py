# -*- coding: utf-8 -*-



#-------------------------------------------------------------------------------
# Name:        ??1
# Purpose:
#
# Author:      ankier
#
# Created:     09/10/2012
# Copyright:   (c) ankier 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import wx

class Example(wx.Frame):

    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title,
            size=(600, 250))

        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):

        panel = wx.Panel(self)

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        #设置为2行4列
        fgs = wx.FlexGridSizer(2, 4, 9, 25)

        title = wx.StaticText(panel, label="Title")
        author = wx.StaticText(panel, label="Author", style= wx.ALIGN_RIGHT)
        review = wx.StaticText(panel, label="Review", style= wx.ALIGN_RIGHT)

        tc1 = wx.TextCtrl(panel)
        tc2 = wx.TextCtrl(panel)
        tc3 = wx.TextCtrl(panel, style=wx.TE_MULTILINE)

        fgs.AddMany(
                    [(title, 0, wx.ALIGN_RIGHT), (tc1, 0, wx.SHAPED), (author, 0, wx.ALIGN_RIGHT), (tc2, 0, wx.SHAPED),
                     (review, 0, wx.ALIGN_RIGHT), (tc3, 0, wx.EXPAND)])

        #设置索引列1，3为自动增长列
        fgs.AddGrowableCol(1, 1)
        fgs.AddGrowableCol(3, 1)

        hbox.Add(fgs, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)
        panel.SetSizer(hbox)


if __name__ == '__main__':

    app = wx.App()
    Example(None, title='Review')
    app.MainLoop()
