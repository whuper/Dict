# -*- coding: UTF-8 -*-

#-------------------------------------------------------------------------------
# Name:        模块1
# Purpose:
#
# Author:      ankier
#
# Created:     10/10/2012
# Copyright:   (c) ankier 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import wx

class ComboBoxFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Combo Box Example', size=(350, 300))
        panel = wx.Panel(self, -1)
        sampleList = ['zero', 'one', 'two', 'three', 'four', 'five','six', 'seven', 'eight']

        flexSizer = wx.FlexGridSizer(4,4,6,6)
        flexSizer.AddGrowableCol(1)
        flexSizer.AddGrowableCol(3)

        #定义普通样式的comboBox, 接受键盘输入，但不会改变Item
        commonLable = wx.StaticText(panel, -1, "normal")
        commonComboBox = wx.ComboBox(panel, -1, value = "zero", choices = sampleList, style = wx.CB_DROPDOWN)

        #定义简单样式的ComboBox，
        simpleLable = wx.StaticText(panel, -1, "simple:")
        simpleComboBox = wx.ComboBox(panel, -1, value =  "zero", choices = sampleList, style = wx.CB_SIMPLE)

        #定义只读样式的ComboBox，
        readonlyLable = wx.StaticText(panel, -1, "readOnly:")
        readonlyComboBox = wx.ComboBox(panel, -1, value =  "zero", choices = sampleList, style = wx.CB_READONLY)

        #定义二级联动下拉列表
        cityDict = {'anhui':["hefei", "huinan"], "jiangsu":["suzhou","nanjing"]}

        #定义第一级菜单
        proviceLable = wx.StaticText(panel, -1, "province:")
        proviceComboBox = wx.ComboBox(panel, -1, value =  cityDict.keys()[0], choices = cityDict.keys(), style = wx.CB_READONLY)
        #定义第二级菜单
        cityLable = wx.StaticText(panel, -1, "city:")
        cityComboBox = wx.ComboBox(panel, -1, value =  cityDict[cityDict.keys()[0]][0], choices = cityDict[cityDict.keys()[0]], style = wx.CB_READONLY)

        flexSizer.AddMany([
                            (commonLable, 0, wx.SHAPED|wx.ALIGN_RIGHT), (commonComboBox, 1, wx.EXPAND), (simpleLable, 0, wx.SHAPED|wx.ALIGN_RIGHT),(simpleComboBox, 1, wx.EXPAND)
                            ,(readonlyLable, 0, wx.SHAPED|wx.ALIGN_RIGHT), (readonlyComboBox, 1, wx.EXPAND),(wx.Size(6,6), 0, wx.SHAPED|wx.ALIGN_RIGHT), (wx.Size(6,6), 1, wx.EXPAND)
                            ,(proviceLable, 0, wx.SHAPED|wx.ALIGN_RIGHT), (proviceComboBox, 1, wx.EXPAND),(wx.Size(6,6), 0, wx.SHAPED|wx.ALIGN_RIGHT), (wx.Size(6,6), 1, wx.EXPAND)
                            ,(cityLable, 0, wx.SHAPED|wx.ALIGN_RIGHT), (cityComboBox, 1, wx.EXPAND),(wx.Size(6,6), 0, wx.SHAPED|wx.ALIGN_RIGHT), (wx.Size(6,6), 1, wx.EXPAND)
                            ])

        panel.SetSizerAndFit(flexSizer)


        #定义 一级下拉列表切换时，刷新二级菜单项的响应事件
        self.__ProvinceComboBox = proviceComboBox
        self.__SecityDict = cityDict
        self.__CityComboBox= cityComboBox
        panel.Bind(wx.EVT_COMBOBOX,  self.__OnComboBoxSelected, proviceComboBox,)

    def __OnComboBoxSelected(self, event):
        currentProvinceIndex = self.__ProvinceComboBox.GetSelection()
        if wx.NOT_FOUND == currentProvinceIndex: return
        value = self.__ProvinceComboBox.GetItems()[currentProvinceIndex]
        
        #注意中文在List dict 等存储时候, utf-8 格式不一致问题
        value = value.encode('utf-8')
        
        cityList = self.__SecityDict[value]
        self.__CityComboBox.SetItems(cityList)
        self.__CityComboBox.SetValue(cityList[0])




def main():
    app = wx.App()
    ComboBoxFrame().Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
