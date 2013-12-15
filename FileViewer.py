from wx.lib import sheet
import wx
import os
import Utility

__name__ = "FileViewer"

SAVEFILE = "save.sae"

class FilePanel(wx.Panel):
    def __init__(self, parent, tree):
        wx.Panel.__init__(self, parent, size=(150,20))
        self.tree = tree
        self.parent = parent
        box = wx.GridBagSizer()
        self.SetSizer(box)
        
        filterPanel = wx.Panel(self)
        filterBox = wx.GridBagSizer()
        filterPanel.SetSizer(filterBox)
        searchBar = wx.TextCtrl(filterPanel, size=(110,20))
        filterButton = wx.Button(filterPanel, -1, 'F',size=(20,20))
        #clearButton = wx.Button(filterPanel, -1, 'C',size=(20,20))
        clearButton = wx.BitmapButton(self, -1, bitmap=wx.Image('clear.ico', wx.BITMAP_TYPE_ANY).ConvertToBitmap(), size=(20,20))
        filterBox.Add(searchBar,(0,0), (1,1), wx.EXPAND)
        filterBox.Add(filterButton,(0,1))
        filterBox.Add(clearButton,(0,2))
        box.Add(filterPanel,(0,0),(1,1),wx.EXPAND)

        baseDirPanel = wx.Panel(self)
        baseDirBox = wx.GridBagSizer()
        baseDirPanel.SetSizer(baseDirBox)
        openButton = wx.Button(baseDirPanel,-1,label="Open", size=(37,20))
        saveButton = wx.Button(baseDirPanel,-1,label="Save", size=(37,20))
        clearButton = wx.Button(baseDirPanel,-1,label="Clear", size=(37,20))
        loadButton = wx.Button(baseDirPanel,-1,label="Load", size=(37,20))
        openButton.Bind(wx.EVT_BUTTON, self.onOpen)
        saveButton.Bind(wx.EVT_BUTTON, self.onSave)
        clearButton.Bind(wx.EVT_BUTTON, self.onClear)
        loadButton.Bind(wx.EVT_BUTTON, self.onLoad)
        baseDirBox.Add(openButton, (0,0))
        baseDirBox.Add(loadButton, (0,1))
        baseDirBox.Add(saveButton, (0,2))
        baseDirBox.Add(clearButton, (0,3))
        box.Add(baseDirPanel, (1,0),(1,1),wx.EXPAND)
        
        self.baseDirs = []
        self.fileSelector = FileViewer(self)
        self.fileSelector.SetMinSize((150,400))
        box.Add(self.fileSelector, (2,0),(1,1),wx.EXPAND)
        
    def onOpen(self, event): 
        dirText = wx.DirDialog(self, "Choose a directory:",
                           style=wx.DD_DEFAULT_STYLE
                           )
        if dirText.ShowModal() == wx.ID_OK:
            self.baseDirs.append(dirText.GetPath())
            self.fileSelector.populate(os.walk(dirText.GetPath()))
        dirText.Destroy()
        
    def onLoad(self, file):
        savefile = Utility.MyFile(SAVEFILE)
        savefile.Open()
        self.baseDirs = savefile.data[:] #make a copy instead of reference
        for file in self.baseDirs:
            self.fileSelector.populate(os.walk(file))

    def onSave(self, event):
        savefile = Utility.MyFile(SAVEFILE)
        savefile.data = self.baseDirs[:]
        savefile.Save()

    def onClear(self, event):
        self.fileSelector.cleanUp()
        self.baseDirs = []
        
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
        self.SetColSize(0, 150)
        self.DisableDragColSize()
        self.DisableDragRowSize()
        self.DisableCellEditControl()
        self.EnableEditing(False)
        InstallGridHint(self, self.GetFileName)

    def GetFileName(self, row):
        return self.GetCellValue(row, 0)

    def populate(self, results):
        index = self.GetNumberRows()
        excludedFiletypes = ['.png','.lua','.wav', '.psd', '.log']
        for root, dirs, files in results: 
            for file in files:
                 if not file.endswith(tuple(excludedFiletypes)):
                    self.InsertRows(index)
                    self.SetCellValue(index, 0, file)               
                    self.files.append(Utility.MyFile(os.path.join(root, file)))
                    index += 1
        #self.AutoSize()
                
    def OnFileSelect(self, event):
        self.OpenFile(event.GetRow())

    def OpenFile(self, row): 
        self.SetGridCursor(row, 0)
        self.files[row].Open()
        self.files[row].Tuple()
        self.parent.tree.populate(self.files[row].data)
        self.lastSelected = row
        self.parent.parent.SetStatusText(self.files[row].loc)
        
    def SpawnContextMenu(self, event):
        self.SelectRow(event.GetRow())
        self.DisableCellEditControl()
        menu = FVPopupMenu(self, event)
        self.PopupMenu(menu, event.GetPosition())
        menu.Destroy()
        self.ClearSelection()
        event.Veto()
        
    def cleanUp(self):
        self.SetNumberRows(0)
        self.files = []

class FVPopupMenu(wx.Menu):
    def __init__(self, fileViewer, event):
        wx.Menu.__init__(self)
        self.fileViewer = fileViewer
        self.rclickevent = event

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
        self.fileViewer.OpenFile(self.rclickevent.GetRow())

    def Save(self, event):
        self.fileViewer.files[self.rclickevent.GetRow()].Save()

    def SaveAs(self, event):
        print "Func Exec"

    def DiscardChanges(self, event):
        print "Func Exec"

    def New(self, event):
        print "Func Exec"

    def Delete(self, event):
        print "Func Exec"

def InstallGridHint(grid, rowcolhintcallback):
    prev_rowcol = [None,None]
    def OnMouseMotion(evt):
        # evt.GetRow() and evt.GetCol() would be nice to have here,
        # but as this is a mouse event, not a grid event, they are not
        # available and we need to compute them by hand.
        x, y = grid.CalcUnscrolledPosition(evt.GetPosition())
        row = grid.YToRow(y)
        col = grid.XToCol(x)

        if (row,col) != prev_rowcol and row >= 0 and col >= 0:
            prev_rowcol[:] = [row,col]
            hinttext = rowcolhintcallback(row)
            if hinttext is None:
                hinttext = ''
            grid.GetGridWindow().SetToolTipString(hinttext)
        evt.Skip()

    wx.EVT_MOTION(grid.GetGridWindow(), OnMouseMotion)
