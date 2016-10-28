import os
import time
import datetime
import shutil
from datetime import datetime as dt
import sqlite3

# connect to database
conn = sqlite3.connect('updateTime.db')
c = conn.cursor()

# grab the most recent datestamp from the database and turn it in to a date object
stringg = c.execute("SELECT datestamp FROM lastFileMove WHERE datestamp = (SELECT MAX(datestamp) FROM lastFileMove)")
string = str(c.fetchone())
most_recent = string[3:27]
most_recent_object = datetime.datetime.strptime(most_recent, "%a %b %d %H:%M:%S %Y")

def movefile(file_, des):
        shutil.copy(file_, des)
        print (file_)
        print ('{} copied to {}'.format(file_.replace('\\','/'), des.replace('\\','/')))

def checkFileModTime(file_): 
        modified = time.ctime(os.path.getmtime(file_))
        
        # turn the modified date/time string into a date object
        modified_object = datetime.datetime.strptime(modified, "%a %b %d %H:%M:%S %Y")

        # grab the current date/time
        now = datetime.datetime.now()

        # format current date/time to that of modified date/time
        now_format = now.strftime("%a %b %d %H:%M:%S %Y")

        # turn current formatted date/time string back into a date object
        now_format_object = datetime.datetime.strptime(now_format, "%a %b %d %H:%M:%S %Y")

        # check if file has been modified since last check, if so, copy it to destination folder
        if most_recent_object < modified_object < now_format_object:
                print ('This file will be moved:')
                return True
        else:
                return False

def moveFilesIfModified(src, des):
        for filename in os.listdir(src):
                absoluteFilePath = os.path.join(src, filename)
                if checkFileModTime(absoluteFilePath):
                        movefile(absoluteFilePath, des)

def main():
        source_folder = "C:/Users/Stephen/Desktop/A"
        destination_folder = "C:/Users/Stephen/Desktop/B"
        moveFilesIfModified(source_folder, destination_folder)

if __name__=='__main__': main()                
