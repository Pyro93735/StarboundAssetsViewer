#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

try:
    from wx.lib import sheet
    import wx
except ImportError:
    raise ImportError,"The wxPython module is required to run this program"

class MySheet(sheet.CSheet):
    def __init__(self, parent):
        sheet.CSheet.__init__(self, parent)
        self.row = self.col = 0
        self.SetNumberRows(10)
        self.SetNumberCols(2)
        self.SetRowLabelSize(0)
        self.SetColLabelSize(0)

        for i in range(10):
            self.SetRowSize(i, 20)

    # def OnGridSelectCell(self, event):
        # self.row, self.col = event.GetRow(), event.GetCol()
        # value =  self.GetColLabelValue(self.col) + self.GetRowLabelValue(self.row)
        # self.SetCellValue(self.row, self.col, value)
        # super(MySheet, self).OnGridSelectCell(event)


class MainApp(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, -1, title, size = ( 550, 500))

        box = wx.GridBagSizer()
        menuBar = wx.MenuBar()

        self.SetSizer(box)

        sheet1 = MySheet(self)
        sheet1.SetFocus()
        searchbox = wx.TextCtrl(self,-1,value=u"try1",size=(100,20))
        panel1 = wx.Panel(self)
        panel2 = wx.Panel(self)
        panel1.SetBackgroundColour('Blue')
        panel2.SetBackgroundColour('Red')

        box.Add(searchbox, (0,0), (1,1), wx.EXPAND)
        box.Add(panel2, (1,0), (1,1), wx.EXPAND)
        box.Add(sheet1, (0,1), (2,1) ,wx.EXPAND)

        self.CreateStatusBar()
        self.Centre()
        self.Show(True)

app = wx.App(0)
newt = MainApp(None, -1, 'SpreadSheet')
app.MainLoop()