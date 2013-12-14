from wx.lib import sheet
import wx
import os
import Utility

__name__ = "FileViewer"

class FileViewer(sheet.CSheet):

    def __init__(self, parent):
        self.files = []
        self.parent = parent
        sheet.CSheet.__init__(self, parent)
        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.OnFileSelect)
        self.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.SpawnContextMenu)
        self.SetNumberRows(0)
        self.SetNumberCols(1)
        self.SetRowLabelSize(0)
        self.SetColLabelSize(0)
        self.EnableCellEditControl(False)

    def populate(self, results):
        index = 0
        excludedFiletypes = ['.png','.lua','.wav'] 
        for root, dirs, files in results: 
            for file in files:
                 if not file.endswith(tuple(excludedFiletypes)):
                    self.InsertRows(index)
                    self.SetCellValue(index, 0, file)               
                    self.files.append(Utility.MyFile(os.path.join(root, file)))
                    index = index + 1
        self.AutoSize()
                
    def OnFileSelect(self, event):
        self.files[event.GetRow()].Open()
        self.parent.tree.populate(self.files[event.GetRow()].data)
        self.lastSelected = event.GetRow()

    def SpawnContextMenu(self, event):
        print "right clicked"
        menu = FVPopupMenu()
        self.PopupMenu(menu, event.GetPosition())
        menu.Destroy()

class FVPopupMenu(wx.Menu):
    def __init__(self):
        wx.Menu.__init__(self)

        item = wx.MenuItem(self, wx.NewId(), "Open")
        self.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.Open, item)

        item = wx.MenuItem(self, wx.NewId(), "Save")
        self.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.Save, item)

        item = wx.MenuItem(self, wx.NewId(), "Save As")
        self.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.SaveAs, item)

        item = wx.MenuItem(self, wx.NewId(), "Discard Changes")
        self.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.DiscardChanges, item)

        item = wx.MenuItem(self, wx.NewId(), "New")
        self.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.New, item)

        item = wx.MenuItem(self, wx.NewId(), "Delete")
        self.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.Delete, item)

    def Open(self, event):
        print "Func Exec"

    def Save(self, event):
        print "Func Exec"

    def SaveAs(self, event):
        print "Func Exec"

    def DiscardChanges(self, event):
        print "Func Exec"

    def New(self, event):
        print "Func Exec"

    def Delete(self, event):
        print "Func Exec"