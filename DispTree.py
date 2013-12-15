from wx.lib import sheet
import wx
import os
import Utility

__name__ = "DispTree"
MODCOLOR = '#B20000'

class DispTree(wx.TreeCtrl):
    def __init__(self, parent, sheet):
        wx.TreeCtrl.__init__(self, parent, style=wx.TR_EDIT_LABELS | wx.TR_DEFAULT_STYLE | wx.TR_TWIST_BUTTONS)
        self.sheet = sheet
        self.SetMinSize((200,400))
        self.parent = parent
        #root = self.AddRoot("Root")
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.ItemActivated)
        
    def ItemActivated(self, event):
        #data = self.GetItemData(event.GetItem()).GetData()
        if self.ItemHasChildren(event.GetItem()):  #type(data) is dict or list:
            self.sheet.populate(event.GetItem(), self)
        else:
            print "trying stuff"
            self.sheet.populate(self.GetItemParent(event.GetItem()), self)
            #select cell
        
    def populate(self, data, file):
        self.file = file
        self.DeleteAllItems()
        root = self.AddRoot("Root ")
        self.AddToTree(root, data)
        self.Expand(root)
        self.sheet.populate(root, self)
        
    def AddToTree(self, itemID, data):
        #Utility.COUT(data)
        self.SetItemData(itemID, wx.TreeItemData(data))
        if type(data[0]) is dict:
            self.AppendText(itemID, "{")
            for key, val in  data[0].iteritems():
                newnode = self.AppendItem(itemID, str(key) + " : ")
                self.AddToTree(newnode, val)
        elif type(data[0]) is list:
            self.AppendText(itemID, "[")
            index = 0
            for item in data[0]:
                newnode = self.AppendItem(itemID, str(index) + " ")
                self.AddToTree(newnode, item)
                index += 1
        else:
            self.AppendText(itemID, str(data[0]))
            
    def AppendText(self, itemID, text):
        self.SetItemText(itemID, self.GetItemText(itemID) + text)
        
    def Children(self,itemID):
        (node,cookie) = self.GetFirstChild(itemID)
        while node.IsOk():
            yield node
            (node, cookie) = self.GetNextChild(itemID, cookie)

    def Modified(self, itemID, modkey, mod):
        newdata = self.GetItemData(itemID).GetData()
        if modkey == None:
            modkey = newdata[1]
        if mod == None:
            mod = newdata[2]
        self.SetItemData(itemID, wx.TreeItemData((newdata[0],modkey,mod)))
        self.SetItemTextColour(itemID, '#B20000')
        parent = self.GetItemParent(itemID)
        if not self.GetItemData(parent).GetData()[2]:
            self.Modified(parent, None, True)
        