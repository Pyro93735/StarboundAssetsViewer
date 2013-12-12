#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from wx.lib import sheet
import wx

__name__ = "DispSheet"

class DispSheet(sheet.CSheet):
    def __init__(self, parent):
        sheet.CSheet.__init__(self, parent)
        self.Bind(wx.grid.EVT_GRID_CELL_CHANGE, self.OnGridCellChange)
        self.row = self.col = 0
        self.SetNumberRows(100)
        self.SetNumberCols(2)
        self.SetRowLabelSize(0)
        self.SetColLabelSize(0)
        self.EnableCellEditControl(True)
        self.EnableGridLines(False)
    
    def populate(self, file):
        self.file = file
        self.Unbind(wx.grid.EVT_GRID_CELL_CHANGE)
        index = 0
        for key in file.data.iterkeys():
            self.SetCellValue(index, 0, str(key))
            self.SetCellValue(index, 1, str(file.data[key]))
            index = index + 1
        self.SetNumberRows(index-1)
        self.AutoSize()
        self.Bind(wx.grid.EVT_GRID_CELL_CHANGE, self.OnGridCellChange)

    def OnGridCellChange(self, event):
        if hasattr(self, "file"):
            key = self.GetCellValue(event.GetRow(), 0)
            if event.GetCol() > 0: # changing a value
                self.file.data[key] = self.GetCellValue(event.GetRow(), event.GetCol())
            else:                  # changing an attribute
                newkey = self.GetCellValue(event.GetRow(), event.GetCol())
                self.file.data[newkey] = self.file.data.pop(key)
            self.file.Save()
        else:
            print "error editing something with no file"