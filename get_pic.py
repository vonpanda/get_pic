#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import socket
import threading
import re
import os
import requests
import time
from bs4 import BeautifulSoup
from tkinter import *
from urllib import request 
from PIL import Image,ImageTk
#----------------------------------------
#作者：panda
#软件用途：爬取特定网站图片，并显示
#版本：v0.1
'getpicture'

__auther__='panda'


class get_picture(Frame):  #继承Frame，自tkinter
    def __init__(self):
        self.url='https://bing.ioliu.cn/?p='#期望爬取的网页
        self.path="bgpic"
        self.mini_path="bgpic/minipic"
        self.pagenum=1 #当前页码
        self.pic_name=[]
        self.pic_url=[]
        self.pic_dict=dict()

    def show_page(self):
        print(self.page)#test
    
    def get_page_num(self):
        self.response=request.urlopen(self.url+str(self.pagenum))#get html
        self.page=self.response.read()
        self.page=self.page.decode('utf-8')
        self.html=BeautifulSoup(self.page,'html.parser')#use bs4 
        for self.span in self.html.find_all(re.compile('span')):#get span
            self.span
        self.pagenum=re.match(r'^.*(\d+) / (\d+).*$',str(self.span),0).group(2)
        self.pagenum=int(self.pagenum)
        print(self.pagenum)


    def get_pic_name(self):
        for tag in self.html.find_all(re.compile('h3')):
           self.pic_name.append(re.match(r'^<h3>(.*)</h3>$',str(tag)).group(1))



    def get_picture_url(self):
        for loop_page in range(1,self.pagenum+1):
            self.response=request.urlopen(self.url+(str(loop_page)))#get html
            self.page=self.response.read().decode('utf-8')
            self.html=BeautifulSoup(self.page,'html.parser')
            for tag in self.html.find_all(re.compile('img')):
                self.pic_url.append(str(tag['data-progressive']))
            self.get_pic_name()
        self.pic_dict=dict(zip(self.pic_name,self.pic_url))
    
    def show_pic_name_and_url(self):
        for i in range(len(self.pic_name)):
            print(self.pic_url[i],self.pic_name[i])
    

    

    def gui_main(self):
        self.t_gui=Tk()
        

        list_name=StringVar(value=self.pic_name)


        self.yscrollbar=Scrollbar(self.t_gui,command=YView)
        self.yscrollbar.pack(side=RIGHT,fill=Y)
        self.blist=Listbox(self.t_gui,width=80,listvariable=list_name,yscrollcommand=self.yscrollbar.set)
        self.label=Label(self.t_gui)
        self.yscrollbar.config(command=self.blist.yview)

    def show_pic(self):
        s=-1
        while(1):
            if(self.blist.curselection()):#有选中
                if(s==self.blist.curselection()[0]):
                    continue
                i=self.pic_url[self.blist.curselection()[0]]
                s=self.blist.curselection()[0]
                
                photopath='./bgpic/minipic/'+i.replace("http://h1.ioliu.cn/bing/","").replace('jpg','png')
                photo=Image.open(photopath)
                self.render=ImageTk.PhotoImage(photo)
                #self.label.image=render
                print(photopath)
                #
                self.label.config(imag=self.render)
                self.label.pack()
            else:#无选中,展示第一张图片
                i=self.pic_url[0]
                if(s==i):
                    continue
                s=i
                photopath='./bgpic/minipic/'+i.replace("http://h1.ioliu.cn/bing/","").replace('jpg','png')
                photo=Image.open(photopath)
                self.render=ImageTk.PhotoImage(photo)
                #self.label.image=render
                print(photopath)
                #
                self.label.config(imag=self.render)
                self.label.pack()
    
    def showselect(self):
            while(1):
                if(self.blist.curselection()):
                    #print(self.blist.curselection()[0])
                    print(self.pic_name[self.blist.curselection()[0]],self.pic_url[self.blist.curselection()[0]])

    def gui_start(self):
        self.t=threading.Thread(target=self.show_pic,name='thread_loop')
        self.t.setDaemon(True)
        self.t.start()
        
        self.label.pack()
        self.blist.pack()
        
    def download_pic_mini(self):#使用requests 提示403，被反爬虫，只好模拟浏览器
        #伪装成火狐后成功
        headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
        for i in self.pic_url:
            print(i)
            #urlopen("Get "+i.replace("http://h1.ioliu.cn/bing/","")+send_text
            req=request.Request(url=i,headers=headers) 
            #r=requests.get(i,headers={'Connection':'close'})
            with open('./bgpic/minipic/'+i.replace("http://h1.ioliu.cn/bing/","").replace('jpg','png'),'wb') as f:
                f.write(request.urlopen(req).read())

    
    def make_picdir(self):
        os.makedirs(self.path+"/minipic",777)



fp=get_picture()
fp.get_page_num()
fp.get_picture_url()
fp.show_pic_name_and_url()
fp.gui_main()
#fp.make_picdir()
fp.download_pic_mini()
fp.gui_start()
fp.t_gui.mainloop()
