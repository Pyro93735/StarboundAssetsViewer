from wx.lib import sheet
import wx
import os
import Utility

__name__ = "DispTree"

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
        
    def populate(self, data):
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
                if type(item[0]) is dict or type(item[0]) is list:
                    newnode = self.AppendItem(itemID, str(index) + " ")
                    self.AddToTree(newnode, item)
                else:
                    newnode = self.AppendItem(itemID, str(item[0]))
                index = index + 1
        else:
            self.AppendText(itemID, str(data[0]))
            
    def AppendText(self, itemID, text):
        self.SetItemText(itemID, self.GetItemText(itemID) + text)
        
    def Children(self,itemID):
        (node,cookie) = self.GetFirstChild(itemID)
        while node.IsOk():
            yield node
            (node, cookie) = self.GetNextChild(itemID, cookie)