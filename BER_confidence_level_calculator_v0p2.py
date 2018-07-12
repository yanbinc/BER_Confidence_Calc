#!python3
# -*- coding: utf-8 -*-
"""
@author: yanbin
Any suggestion? Please contract yanbin_c@hotmail.com
"""
import  os
import  wx
import sys
import time,datetime
import numpy as np
import math
from time import clock
from threading import Thread
from wx.lib.embeddedimage import PyEmbeddedImage

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,'BER Confidence Level Calculator V0.2',size=(600,400))
        nb_main=wx.Notebook(self,-1,pos=(0,0),size=(600,400),style=wx.BK_DEFAULT)
        self.panel_c=panel_Calculator(nb_main,-1)
        self.panel_v=panel_version(nb_main,-1)
        nb_main.AddPage(self.panel_c,"BER Cal")
        nb_main.AddPage(self.panel_v,"Version")
        self.panel_c.btn_run.Bind(wx.EVT_BUTTON,self.On_Run)
        
    def On_Run(self, event): 
        thread = Thread(target = self.On_Run_cal, args = (), name = self.On_Run_cal.__name__)
        thread.start()  
        
    def On_Run_cal(self): 
        basic_setting=self.panel_c.get_setting()
        bers=float(basic_setting["BER"]) 
        bps=float(basic_setting["BPS"]) 
        t=float(basic_setting["T"]) 
        error=int(basic_setting["E"]) 
        unit_list=(1,60,3600)
        unit=unit_list[int(basic_setting["U"]) ]
        p=0
        N=bps*unit*t
        for i in range (error+1):
            p+=math.pow(N*bers,i)/math.factorial(i)
        Pnk=math.exp(-N*bers)*p
        CL=1-Pnk
        self.panel_c.txt_N.SetValue (str(N))
        self.panel_c.txt_CL.SetValue (str(CL*100))
        print ('\n\n\t***Simulation Done.***')
        return()        

class panel_Calculator(wx.Panel):
    def __init__(self,*args,**kwargs):
        wx.Panel.__init__(self,*args,**kwargs)
        self.sizer=wx.GridBagSizer(hgap=10,vgap=5)    
        self.sizer.Add(wx.StaticText(self,-1,r'BER Confidence Level Calculator'),pos=(0,0),flag=wx.ALIGN_CENTER_VERTICAL)
        
        self.sizer.Add(wx.StaticText(self,-1,r'Specified BER (BERs)'),pos=(1,0),flag=wx.ALIGN_CENTER_VERTICAL)
        self.txt_ber=wx.TextCtrl(self,-1,"1e-16",size=(50,-1)) 
        self.sizer.Add(self.txt_ber,pos=(1,1),span=(1,1),flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)

        self.sizer.Add(wx.StaticText(self,-1,r'Datarate in bits per second(BPS)'),pos=(2,0),flag=wx.ALIGN_CENTER_VERTICAL)
        self.txt_bps=wx.TextCtrl(self,-1,"4.8e9",size=(50,-1)) 
        self.sizer.Add(self.txt_bps,pos=(2,1),span=(1,1),flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)
        
        self.sizer.Add(wx.StaticText(self,-1,r'Numbers of measured bit errors(E)'),pos=(3,0),flag=wx.ALIGN_CENTER_VERTICAL)
        self.txt_error=wx.TextCtrl(self,-1,"0",size=(50,-1)) 
        self.sizer.Add(self.txt_error,pos=(3,1),span=(1,1),flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)

        self.sizer.Add(wx.StaticText(self,-1,r'Measurement time(T)'),pos=(4,0),flag=wx.ALIGN_CENTER_VERTICAL)
        self.txt_time=wx.TextCtrl(self,-1,"2000",size=(50,-1)) 
        self.sizer.Add(self.txt_time,pos=(4,1),span=(1,1),flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)
        self.sizer.Add(wx.StaticText(self,-1,r'in units of:'),pos=(4,2),flag=wx.ALIGN_CENTER_VERTICAL)
        sampleList = ['Seconds', 'Minutes', 'Hours']  
        self.u_choice = wx.ComboBox(self,-1,'Hours',(740,18),(80,20),sampleList, wx.CB_DROPDOWN)
        self.sizer.Add(self.u_choice,pos=(4,3),flag=wx.ALIGN_CENTER_VERTICAL)
        self.btn_run = wx.Button(self, 20, "Calculate", (20, 100)) 
        self.btn_run.SetToolTip("Run Analysis...")
        self.sizer.Add(self.btn_run,pos=(5,0),span=(1,1),flag=wx.ALIGN_CENTER_VERTICAL) 
        self.sizer.Add(wx.StaticText(self,-1,r'Numbers of transmitted bits(N=BPS*T)'),pos=(6,0),flag=wx.ALIGN_CENTER_VERTICAL)
        self.txt_N=wx.TextCtrl(self,-1,"",size=(100,-1)) 
        self.sizer.Add(self.txt_N,pos=(6,1),span=(1,2),flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)
        self.sizer.Add(wx.StaticText(self,-1,r'BER confidence level(CL*100%)'),pos=(7,0),flag=wx.ALIGN_CENTER_VERTICAL)
        self.txt_CL=wx.TextCtrl(self,-1,"",size=(100,-1)) 
        self.sizer.Add(self.txt_CL,pos=(7,1),span=(1,2),flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)
        jpg_file = wx.Image('eqn_ber_cl.jpg', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.sizer.Add(wx.StaticBitmap(self, -1, jpg_file, (10 + jpg_file.GetWidth(), 5), (jpg_file.GetWidth(), jpg_file.GetHeight())),pos=(8,0),span=(1,1),flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)
        self.SetSizer(self.sizer)    
        self.sizer.Add(wx.StaticText(self,-1,r'Reference: JitterLabs website of "BER Confidence-level Calculator".'),pos=(9,0),span=(1,4))
        self.sizer.Add(wx.StaticText(self,-1,r'Link:         https://www.jitterlabs.com/support/calculators/ber-confidence-level-calculator'),pos=(10,0),span=(1,4))

    def get_setting(self):
        res={}
        res["BER"]=self.txt_ber.GetValue()
        res["BPS"]=self.txt_bps.GetValue()
        res["T"]=self.txt_time.GetValue()
        res["U"]=self.u_choice.GetSelection ()
        res["E"]=self.txt_error.GetValue()
        return res

class panel_version(wx.Panel):
    def __init__(self,*args,**kwargs):
        wx.Panel.__init__(self,*args,**kwargs)        
        self.sizer=wx.GridBagSizer(hgap=10,vgap=5)  
        self.sizer.Add(wx.StaticText(self,-1,'version 0.1:Initial Release'),pos=(0,0))
        self.sizer.Add(wx.StaticText(self,-1,'yanbin_c@hotmail.com'),pos=(1,0))
        self.SetSizer(self.sizer)    
        self.sizer.Fit(self)    
        self.Fit 

if __name__ == "__main__":
    app = wx.App()
    frame=MyFrame()
    frame.Show()
    app.MainLoop()


