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

        #for i in range(10):
        #    self.SetRowSize(i, 20)

    # def OnGridSelectCell(self, event):
        # self.row, self.col = event.GetRow(), event.GetCol()
        # value =  self.GetColLabelValue(self.col) + self.GetRowLabelValue(self.row)
        # self.SetCellValue(self.row, self.col, value)
        # super(MySheet, self).OnGridSelectCell(event)


class Newt(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, -1, title, size = ( 550, 500))

        fonts = ['Times New Roman', 'Times', 'Courier', 'Courier New', 'Helvetica', 'Sans', 'verdana', 'utkal', 'aakar', 'Arial']
        box = wx.BoxSizer(wx.VERTICAL)
        menuBar = wx.MenuBar()
        
        

        menu1 = wx.Menu()
        menuBar.Append(menu1, '&File')
        menu2 = wx.Menu()
        menuBar.Append(menu2, '&Edit')
        menu3 = wx.Menu()
        menuBar.Append(menu3, '&Edit')
        menu4 = wx.Menu()
        menuBar.Append(menu4, '&Insert')
        menu5 = wx.Menu()
        menuBar.Append(menu5, '&Format')
        menu6 = wx.Menu()
        menuBar.Append(menu6, '&Tools')
        menu7 = wx.Menu()
        menuBar.Append(menu7, '&Data')

        menu7 = wx.Menu()
        menuBar.Append(menu7, '&Help')

        self.SetSizer(box)

        sheet1 = MySheet(self)
        sheet1.SetFocus()

        box.Add(sheet1, 1, wx.EXPAND)

        self.CreateStatusBar()
        self.Centre()
        self.Show(True)

app = wx.App(0)
newt = Newt(None, -1, 'SpreadSheet')
app.MainLoop()