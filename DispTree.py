from wx.lib import sheet
import wx
import os
import Utility

__name__ = "DispTree"

class DispTree(wx.TreeCtrl):
    def __init__(self, parent):
        wx.TreeCtrl.__init__(self, parent, size=(400,600), style=wx.TR_EDIT_LABELS | wx.TR_DEFAULT_STYLE | wx.TR_TWIST_BUTTONS)
        self.parent = parent
        #root = self.AddRoot("Root")
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.ItemActivated)
        
    def ItemActivated(self, event):
        data = self.GetItemData(event.GetItem()).GetData()
        if type(data) is dict or list:
            self.parent.sheet1.populate(event.GetItem(), self)
        else:
            print "trying stuff"
            self.parent.sheet1.populate(self.GetItemParent(event.GetItem()), self)
            #select cell
        
    def populate(self, data):
        self.DeleteAllItems()
        root = self.AddRoot("Root ")
        self.AddToTree(root, data)
        self.Expand(root)
        self.parent.sheet1.populate(root, self)
        
    def AddToTree(self, itemID, data):
        if type(data) is dict:
            self.SetItemData(itemID, wx.TreeItemData(data))
            self.AppendText(itemID, "{")
            for key, val in  data.iteritems():
                newnode = self.AppendItem(itemID, str(key) + " : ")
                self.AddToTree(newnode, val)
        elif type(data) is list:
            self.SetItemData(itemID, wx.TreeItemData(data))
            self.AppendText(itemID, "[")
            index = 0
            for item in data:
                if type(item) is dict or type(item) is list:
                    newnode = self.AppendItem(itemID, str(index) + " ")
                    self.AddToTree(newnode, item)
                else:
                    newnode = self.AppendItem(itemID, str(item))
                index = index + 1
        else:
            self.AppendText(itemID, str(data))
            
    def AppendText(self, itemID, text):
        self.SetItemText(itemID, self.GetItemText(itemID) + text)
        
    def Children(self,itemID):
        (node,cookie) = self.GetFirstChild(itemID)
        while node.IsOk():
            yield node
            (node, cookie) = self.GetNextChild(itemID, cookie)