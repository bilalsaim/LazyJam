'''
Created on 30 Mar 2017

@author: Bilal Saim
'''
# -*- coding: utf-8 -*-
if __name__ == '__main__':
    pass

from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import threading
import time
import os
import subprocess
import inspect
from shutil import copyfile
from pywinauto import Application
import xml.etree.ElementTree as ET

#Library from files
from Questions import Questions
from functions import mkdir, easywrite, delfiles, delfile

root = Tk()
root.wm_title("LazyJam")
root.iconbitmap('fav.ico')
frame = Frame(root)

driver = None
que = []
app = None
#get code jam links from xml file
tree = ET.parse('Contents.xml')
xmlroot = tree.getroot()
queselect = -1

li = [{"year":"","level":[{"name":"","link":""}]}]
selected = [-1,-1]
modevar = StringVar(value="")

########################    
def yearfunc(event):
    "Gets CodeJams links for combobox"
    t = [x for x in range(0,len(li)) if li[x]['year'] == yearvar.get()]
    t = int(t[0])-1
    selected[0] = t
    
    level = Combobox(root, textvariable=levelvar)
    level.grid(row=2,column=0,columnspan=4)
    
    if yearvar.get() == "":
        selected[0] = -1
        selected[1] = -1
        level['values'] = []
        return
    else:
        level['values'] = [li[t]['level'][x]['name'] for x in range(0,len(li[t]['level']))]
        level.bind("<<ComboboxSelected>>", levelfunc)
        
def levelfunc(event):
    "Gets CodeJams sub levels links for combobox"
    if levelvar.get() == "":
        selected[1] = -1
        return
    selected[1] = [x for x in range(0,len(li[selected[0]]['level'])) if li[selected[0]]['level'][x]['name'] == levelvar.get()]
    selected[1] = selected[1][0]
#########################

#read xml file
tix = 0
for child in xmlroot:
    li.append({"year":child.attrib['name'],"level":[{"name":"","link":""}]})
    for subchild in child:
        li[tix]['level'].append({"name": subchild.attrib['name'],"link":subchild.find('link').text})
    tix+=1

levelvar = StringVar(value="")
yearvar = StringVar(value="")
year = Combobox(root, textvariable=yearvar)
year.grid(row=1,column=0,columnspan=4)
year['values'] = [li[x]['year'] for x in range(0,len(li))]
year.bind("<<ComboboxSelected>>", yearfunc)

linktext = Text(root, height=2, width=30)
linktext.grid(row=5,column=0,columnspan=4)

##########################
def select(index):
    global driver
    global que
    global app
    global queselect
    
    driver.get(que[index].link)
    # Disable the button by index
    for i in range(0,len(que)):
        que[i].button.config(state="enable")
    que[index].button.config(state="disabled")

    #proc = subprocess.Popen('pythonw -m idlelib "' + que[index].file + '"', stdin = subprocess.PIPE, stdout = subprocess.PIPE)
    app = Application().start('pythonw -m idlelib "' + que[index].file + '"')
    queselect = index
   
def folderfunc():
    if queselect == -1:
        os.startfile(Questions.gpath)
    else:
        os.startfile(que[queselect].path)

def modefunc(event):
    if queselect == -1:
        messagebox.showinfo("Warning", "You have to select one question!")
        return
    text = str(modevar.get().lower())
    path = que[queselect].infile()
    
    if modevar.get() == "Small":
        path = que[queselect].insmall()
    elif modevar.get() == "Large":
        path = que[queselect].inlarge()
        
    easywrite(que[queselect].opfile(), text+"\n"+que[queselect].path+"\\"+path)

def download():
    if modevar.get() == "Test" or modevar.get() == "" or queselect == -1:
        messagebox.showinfo("Warning", "You have to select one question and change mode with small or large")
        return

    index = queselect
    status = 0 if modevar.get() == "Small" else 1
    infile = que[index].insmall() if status == 0 else que[index].inlarge()
    
    driver.get(que[index].link)
    time.sleep(2)
    elem = driver.find_element_by_id("dsb-input-start-button"+str(index)+"-"+str(status))
    elem.click()
    time.sleep(1)
    elem = driver.find_element_by_id("dsb-input-link-plain-text"+str(index)+"-"+str(status))
    elem.click()
    
    say = 0
    
    inpath = que[index].path + "\\" + infile
    while True:
        if os.path.isfile(Questions.download+"\\"+infile):
            break
        say+=1
        time.sleep(1)
        if say>10:
            return

    #Delete old input file
    delfile(inpath)
    time.sleep(1)
    #Move downloaded file to question folder
    os.rename(Questions.download+"\\"+infile, inpath)
    #Write operation for debug 

def upload():
    if modevar.get() == "Test" or modevar.get() == "" or queselect == -1:
        messagebox.showinfo("Warning", "You have to select one question and change mode with small or large")
        return
    
    index = queselect
    status = 0 if modevar.get() == "Small" else 1
    outfile = que[index].outsmall() if status == 0 else que[index].outlarge()
    

    if not os.path.isfile(outfile):
        return
    selem = driver.find_element_by_id("output-fileio_timer_"+str(index*2+status))
    selem.send_keys(outfile)
    time.sleep(1)
    elem = driver.find_element_by_id("submit-buttonio_timer_"+str(index*2+status))
    elem.click()
    
def start():
    global driver
    global que

    #Our lazyjam.py current path
    mainpath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    #sys.argv[0] can use instead of down part it's shorter and same result
    
    if driver is None:
        fp = webdriver.FirefoxProfile() 
        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference("browser.download.manager.showWhenStarting", False)
        mkdir(Questions.download)
        fp.set_preference("browser.download.dir",mainpath+"\\tmp") 
        fp.set_preference('browser.helperApps.neverAsk.saveToDisk', "text/plain, application/vnd.ms-excel, text/csv, text/comma-separated-values, application/octet-stream") 
        driver = webdriver.Firefox(firefox_profile=fp)
    else:
        que = []
    b2.config(state="normal")
    b3.config(state="normal")
    if selected[0] != -1 and selected[1] != -1:
        redict()

def den():
    app = Application().start('python "D:\OneDrive\Contest\Google Code Jam\LazyJam\Example.py" < "D:\OneDrive\Contest\Google Code Jam\2016\Round 1B\B\Input-test.txt"')
    #proc = subprocess.Popen('python "D:\OneDrive\Contest\Google Code Jam\LazyJam\Example.py" < "D:\OneDrive\Contest\Google Code Jam\2016\Round 1B\B\Input-test.txt"', stdin = subprocess.PIPE, stdout = subprocess.PIPE)
    
def redict(stat):
    global driver
    global que
    global modevari
    
    queselect = -1
    frame.grid(row=7)
    
    mainpath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    que = []

    if not stat:
        if (selected[0] == -1 or selected[1] == -1):
            return
    else:
        if linktext.get(1.0,END) == "":
            return
    
    delfiles(Questions.download) #Be careful with this code! #It's deleting everything under tmp file
    if stat:
        driver.get(linktext.get(1.0, END))
    else:
        driver.get(li[selected[0]]['level'][selected[1]]['link'])
    #assert "Python" in driver.title
    
    a=0
    top = 0
    while True:
        try:
            a+=1
            if a > 5:
                print("HATA")
                return
            time.sleep(2)
            elem = driver.find_element_by_id("dsb-problem-selection-list")
            sub = elem.find_elements_by_xpath("div/*[1]") #div'in i�indeki ilk eleman� se�
            top = len(sub)
            if top > 0 :
                break
        except:
            print("Waiting")

    Questions.gid = driver.execute_script("return GCJ.contest.id;")
    Questions.gname = driver.execute_script("return GCJ.contest.name;")
    Questions.gbase = driver.execute_script("return GCJ.base_url;")
    Questions.gyear = Questions.gname.split()[-1]

    w = Label(frame, text= Questions.gname)
    w.grid(row=0,column=0,columnspan=4,pady=10)
    
    Questions.gpath = os.path.abspath(os.path.join(mainpath, os.pardir)) + "\\" + Questions.gyear
    tmp = Questions.gname.split()
    del tmp[-1]
    
    mkdir(Questions.gpath)
    Questions.gpath += "\\"+ " ".join(tmp)
    mkdir(Questions.gpath)
    
    #driver.current_url
    mylist = list(map(str,[chr(65+b) for b in range(0,top)]))

    contents = driver.find_elements_by_class_name("io-content")

    for i in range(0,len(mylist)):
        button = Button(frame, text=mylist[i], command=lambda x=i: select(x))
        button.grid(row=1+i,column=0)

        #Define Object and add into list
        que.append(Questions(i,button))

        #Create folder of Question
        mkdir(que[i].path)
        
        easywrite(que[i].opfile(),"test\n"+que[i].infile())
        
        #Copy example code template 
        if not os.path.exists(que[i].file):
            copyfile(mainpath+Questions.copyfile,que[i].file )

        #Create input and output files
        easywrite(que[i].infile(),contents[i*2].get_attribute("innerHTML")[:-2])
        easywrite(que[i].outfile(),contents[i*2+1].get_attribute("innerHTML")[:-1])

    buttonf = Button(frame, text="Folder", command=folderfunc)
    buttonf.grid(row=Questions.count,column=1,padx=5)
    
    mlabel = Label(frame, text="Mode")
    mlabel.grid(row=Questions.count+1,column=1,padx=5)
    
    buttond = Button(frame, text="Download", command=download)
    buttond.grid(row=Questions.count,column=2,padx=5)

    buttonu = Button(frame, text="Upload", command=upload)
    buttonu.grid(row=Questions.count+1,column=2,padx=5)

    modevar = StringVar(value="")
    mode = Combobox(frame, textvariable=modevar)
    mode.grid(row=Questions.count+2,column=1,padx=5)
    mode['values'] = ("Test","Small","Large")
    mode.bind("<<ComboboxSelected>>", modefunc)
    
    

b = Button(root, text="Webdriver", command=start,width=15)
b.grid(row=0,column=0,columnspan=4,sticky=NSEW,padx=2)

b2 = Button(root, text="Redict", command= lambda: redict(False),width=15,state=DISABLED)
b2.grid(row=3,column=0,sticky=NSEW,padx=2,columnspan=4)


llabel = Label(root, text="Link!")
llabel.grid(row=4,column=0,columnspan=4)


b3 = Button(root, text="Redict", command= lambda: redict(True), width=15,state=DISABLED)
b3.grid(row=6,column=0,sticky=NSEW,padx=2,columnspan=4)

root.mainloop()
