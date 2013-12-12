#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from wx.lib import sheet
import wx

__name__ = "DispTree"

class DispTree(wx.TreeCtrl):
    def __init__(self, parent):
        wx.TreeCtrl.__init__(self, parent, size=(400,600), style=wx.TR_EDIT_LABELS | wx.TR_DEFAULT_STYLE | wx.TR_TWIST_BUTTONS)
        #root = self.AddRoot("Root")
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.Try1)
        
    def Try1(self, event):
        self.EditLabel(self.GetSelection())
        
    def populate(self, data):
        #clear
        root = self.AddRoot("Root")
        self.AddToTree(root, data)
        
    def AddToTree(self, itemID, data):
        if type(data) is dict:
            self.AppendText(itemID, "{")
            for key, val in  data.iteritems():
                newnode = self.AppendItem(itemID, str(key) + " : ")
                self.AddToTree(newnode, val)
        elif type(data) is list:
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