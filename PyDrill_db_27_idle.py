import wx
import Filer
import datetime
import sqlite3
import sys
import time
import FilerUpdate

conn = sqlite3.connect('updateTime.db')
c = conn.cursor()

class windowClass(wx.Frame):
    
    def __init__(self, *args, **kwargs):
        super(windowClass, self).__init__(*args, **kwargs)

        self.basicGUI()
    
    def Quit(self, e):
            sys.exit()

    def loadDirectory(self, e):
        global loadDir
        dialog1 = wx.DirDialog(None, "Choose a Load directory:"
                               ,style = wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dialog1.ShowModal() == wx.ID_OK:
            print dialog1.GetPath()
            loadDir = dialog1.GetPath()

    def destinationDirectory(self, e):
        global destinationDir
        dialog2 = wx.DirDialog(None, "Choose a Destination directory:"
                               ,style = wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dialog2.ShowModal() == wx.ID_OK:
            print dialog2.GetPath()
            destinationDir = dialog2.GetPath()

    def moveFiles(self, e):
        Filer.moveFilesIfModified(loadDir, destinationDir)
        moveFilesTime = datetime.datetime.now()
        self.moveFilesTimeFormat = moveFilesTime.strftime("%a %b %d %H:%M:%S %Y")
        print self.moveFilesTimeFormat
        c.execute("INSERT INTO lastFileMove (datestamp) VALUES (?)"
                  ,(self.moveFilesTimeFormat,))
        conn.commit()

    def checkLastUpdate(self, e):
        for row in c.execute("SELECT * FROM lastFileMove"):
            string = str(row)
            self.datestamp = string[3:27]
            print self.datestamp
            width = 250
            txt = wx.StaticText(self.panel, -1
                                , 'The last update was performed on: ' + self.datestamp, (10,10))
            txt.Wrap(width)

    def moveFilesFromLastUpdate(self, e):
        FilerUpdate.moveFilesIfModified(loadDir, destinationDir)
        moveFilesTime = datetime.datetime.now()
        self.moveFilesTimeFormat = moveFilesTime.strftime("%a %b %d %H:%M:%S %Y")
        print self.moveFilesTimeFormat
        c.execute("INSERT INTO lastFileMove (datestamp) VALUES (?)"
                  ,(self.moveFilesTimeFormat,))
        conn.commit()
        
    def basicGUI(self):
        self.panel = wx.Panel(self)
        
        menuBar = wx.MenuBar()
        
        fileButton = wx.Menu()
        actionsButton = wx.Menu()
        
        exitItem = fileButton.Append(wx.ID_EXIT, 'Exit')
        loadItem = actionsButton.Append(wx.ID_ANY, 'Choose a Load Directory')
        destinationItem = actionsButton.Append(wx.ID_ANY, 'Choose a Destination directory')
        checkLastUpdateItem = actionsButton.Append(wx.ID_ANY, 'Check last update time')
        moveFilesFromLastUpdateItem = actionsButton.Append(wx.ID_ANY
                                                     ,'Copy and move modified files from last update time')
        moveFilesItem = actionsButton.Append(wx.ID_ANY
                                             ,'Copy and move modified files from past 24hrs')
        menuBar.Append(fileButton, 'File')
        menuBar.Append(actionsButton, 'Actions')
        
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.loadDirectory, loadItem)
        self.Bind(wx.EVT_MENU, self.Quit, exitItem)
        self.Bind(wx.EVT_MENU, self.destinationDirectory, destinationItem)
        self.Bind(wx.EVT_MENU, self.moveFilesFromLastUpdate, moveFilesFromLastUpdateItem)
        self.Bind(wx.EVT_MENU, self.moveFiles, moveFilesItem)
        self.Bind(wx.EVT_MENU, self.checkLastUpdate, checkLastUpdateItem)

        nameBox = wx.TextEntryDialog(None, 'What is your name?', 'Welcome', 'name')
        if nameBox.ShowModal() == wx.ID_OK:
            userName = nameBox.GetValue()
        else:
            userName = 'Default'

        self.SetTitle('Welcome ' +userName)
        self.Show(True)
            
def main():
    app = wx.App()
    windowClass(None)
    app.MainLoop()

main()
