import tkinter as tk
from tkinter import simpledialog
import Feeder
from PIL import ImageTk, Image

class setGUI:
    
    def __init__(self,defaults = [],fooddefaults = []):
        self.foodToSearch = ['food']
        self.doCalendar = 'YES'        
        self.URLlist = ['http://calendar.utexas.edu/calendar.xml']
        self.FIXEDdefaults = defaults
        self.defaults = defaults.copy()
        self.FIXEDFOODdefaults = fooddefaults
        self.fooddefaults = fooddefaults.copy()
        
        boldbg = 'red' #'#BF5700' #"red"
        txtfg = 'red' #'#BF5700' #"red"
        UTcol = '#BF5700'
        
        self.launch = tk.Tk()
        self.launch.title("Initial Settings")
        
        #Set dotnom image in GUI
        img = ImageTk.PhotoImage(Image.open("dotnom.png"))
        imgset = tk.Label(self.launch,image = img)
        imgset.grid(row = 0, column = 0, rowspan = 14)
        #Put .nom in 
        tk.Label(self.launch,
                 text = ".nom",
                 fg = "white",
                 bg = UTcol,
                 font = ('Algerian','24','bold')).grid(row = 0, column = 0)         
        
        #Ask if calendar should be made
        tk.Label(self.launch,
                 text = "CURRENT CALENDAR OUTPUT:",
                 fg = "white",
                 bg = boldbg,
                 font = ('Georgia','24','bold')).grid(row = 0, column = 1)        
        self.calendar = tk.Label(self.launch,
                 text = '\nYES Calendar ==> .ics file will be saved\n',
                 fg = txtfg,
                 font = ('Georgia','14','italic'))
        self.calendar.grid(row = 1, column = 1)
        
        tk.Button(self.launch,text = "CHANGE CALENDAR OPTION", command = self.tkYesNo).grid(row = 2, column = 1)
        
        #Ask to add food options, and display list of options
        tk.Label(self.launch,
                 text = "CURRENT FOOD OPTIONS:",
                 fg = "white",
                 bg = boldbg,
                 font = ('Georgia','24','bold')).grid(row = 4, column = 1)
        
        scrollfood = tk.Scrollbar(self.launch)
        scrollfood.grid(row = 5, column = 50, sticky='ns')
        self.foodlist = tk.Listbox(self.launch, 
                                   width =  40, height = 5,
                                   yscrollcommand = scrollfood.set)
        
        #initial foodlist
        for fd in self.foodToSearch:
            self.foodlist.insert(tk.END,fd)
        
        self.foodlist.config(fg = txtfg, font = ('Georgia','14','italic'))
        self.foodlist.grid(row = 5, column = 1)
        
        scrollfood.config(command=self.foodlist.yview)

        tk.Label(self.launch,
                 text = "\nAdd more food options to search from:\n",
                 fg = "black",
                 font = ('Georgia','12')).grid(row = 11, column = 0)
               
        tk.Button(self.launch,text = "ADD FOOD",command = self.dialfood).grid(row = 12, column = 0)

        tk.Label(self.launch,
                 text = "\nClear all food options:\n",
                 fg = "black",
                 font = ('Georgia','12')).grid(row = 11, column = 2)
               
        tk.Button(self.launch,text = "CLEAR FOOD LIST",command = self.clearfood).grid(row = 12, column = 2)

        tk.Label(self.launch,
                 text = "\nOr select from loaded defaults:\n",
                 fg = "black",
                 font = ('Georgia','12')).grid(row=11,column = 1)
        tk.Button(self.launch,text = "LOAD DEFAULT FOODS",command = self.defaultfoods).grid(row = 12, column = 1)
        
        #Ask to add the url links and include a check to make sure that the link contains a valid rss feed (.xml or /rss)
        tk.Label(self.launch,
                 text = "CURRENT URL OPTIONS:",
                 fg = "white",
                 bg = boldbg,
                 font = ('Georgia','24','bold')).grid(row = 13, column = 1) 
        
        scrollurl = tk.Scrollbar(self.launch)
        scrollurl.grid(row = 14, column = 65, sticky='ns')
        self.url = tk.Listbox(self.launch, 
                              width =  60, height = 5,
                              yscrollcommand = scrollurl.set)
        
        #initial urllist
        for ul in self.URLlist:
            self.url.insert(tk.END,ul)
        
        self.url.config(fg = txtfg, font = ('Georgia','14','italic'))
        self.url.grid(row = 14, column = 1)
        
        scrollfood.config(command=self.url.yview)
        
        tk.Label(self.launch,
                 text = "\nAdd more url options to search from:\n",
                 fg = "black",
                 font = ('Georgia','12')).grid(row = 20, column = 0)
        
        tk.Button(self.launch,text = "ADD URL",command = self.dialurl).grid(row = 21, column = 0)
 
        tk.Label(self.launch,
                 text = "\nClear all url options:\n",
                 fg = "black",
                 font = ('Georgia','12')).grid(row = 20, column = 2)
        
        tk.Button(self.launch,text = "CLEAR URL LIST",command = self.clearurl).grid(row = 21, column = 2)
        
        tk.Label(self.launch,
                 text = "\nOr select from loaded defaults:\n",
                 fg = "black",
                 font = ('Georgia','12')).grid(row=20,column = 1)
        tk.Button(self.launch,text = "LOAD DEFAULT URLS",command = self.defaulturls).grid(row = 21, column = 1)
        
        tk.Label(self.launch,text = "\n").grid(row=22,column = 0) #blank space       
        
        #Exit when done
        tk.Button(self.launch,text = "DONE",bg = "blue",fg = "white",font = ('Georgia','12','bold'),command = self.done).grid(row = 23, column = 1)
        
        self.launch.mainloop()
        
    def dialfood(self):
        newfood = simpledialog.askstring("More food","Please Enter food.",parent=self.launch)
        addtolist(newfood,self.foodToSearch)
        self.foodlist.insert(tk.END,newfood)    
    
    def dialurl(self):
        newurl = simpledialog.askstring("More links","Please Enter URL.",parent=self.launch)
        
        urlOK = False
        
        if newurl:
            if '/rss' in newurl or '.xml' in newurl:    
                urlOK = Feeder.validlink(newurl)
            
            if urlOK:
                addtolist(newurl,self.URLlist)
                self.url.insert(tk.END,newurl) 
            else:
                self.tkInvalid()
    
    def dialdel(self):
        torem = simpledialog.askinteger("delete url","Please Enter index of URL to remove.\nIndices are given in the LOADED DEFAULTS list by the URL.",parent=self.deflt,minvalue=0,maxvalue=len(self.defaults)-1) 
        if torem in range(len(self.defaults)): del(self.defaults[torem])
        self.defList['text'] = listTostr(self.defaults,'\n',item=1)

    def dialfdel(self):
        torem = simpledialog.askstring("delete food","Please Enter name of FOOD to remove.",parent=self.fdeflt) 
        torem = torem.strip()
        if torem in self.fooddefaults:
            LIST = self.fdeflist.get(0,tk.END)
            idx = LIST.index(torem)
            self.fdeflist.delete(idx)
            
            del(self.fooddefaults[idx])
    
    def clearfood(self):
        self.foodToSearch = []
        LIST = self.foodlist.get(0,tk.END)
        Rerun = True
        while Rerun:
            for food in LIST:
                self.foodlist.delete(LIST.index(food))
            if self.foodlist.get(0,tk.END): 
                Rerun = True
                LIST = self.foodlist.get(0,tk.END)
            else: Rerun = False
            
    def clearurl(self):
        self.URLlist = []
        LIST = self.url.get(0,tk.END)
        Rerun = True
        while Rerun:
            for url in LIST:
                self.url.delete(LIST.index(url))
            if self.url.get(0,tk.END): 
                Rerun = True
                LIST = self.url.get(0,tk.END)
            else: Rerun = False
            
    def YESDOCalendar(self):
        self.calendar['text'] = '\nYES Calendar ==> .ics file will be saved\n'
        self.doCalendar = 'YES'
        self.yn.destroy()
    
    def NODONTCalendar(self):
        self.calendar['text'] = '\nNO Calendar ==> .ics file will not be saved\n'
        self.doCalendar = 'NO' 
        self.yn.destroy()
    
    def kill(self):
        self.msg.destroy()
    
    def done(self):
        self.launch.destroy()
        
    def loaddef(self):
        for url in self.defaults:
            addtolist(url,self.URLlist)
            self.url.insert(tk.END, url)
        self.deflt.destroy()
        
    def loadfdef(self):
        for url in self.fooddefaults:
            addtolist(url,self.foodToSearch)
            self.foodlist.insert(tk.END, url)
        self.fdeflt.destroy()   
        
    def tkYesNo(self):
        #simple yes no dialogue box for calendar
        self.yn = tk.Tk()
        self.yn.title("calendar")
        tk.Label(self.yn,text = "Ouput Calendar?").pack()
        tk.Button(self.yn,text = "YES", command = self.YESDOCalendar).pack(side = 'left')
        tk.Button(self.yn,text = "NO", command = self.NODONTCalendar).pack(side = 'right')
        self.yn.mainloop()
        
    def tkInvalid(self):
        #simple message box for invalid URL
        self.msg = tk.Tk()
        self.msg.title("invalid")
        tk.Label(self.msg,
                 text = "\n!!!\nINVALID LINK ENTERED\n!!!\n",
                 fg = "white",
                 bg = "red",
                 font = ('Georgia','18','bold')).pack() 
        tk.Button(self.msg,text = "\nOK\n", command = self.kill).pack()
        self.msg.mainloop()
     
    def defaulturls(self):
        #show all loaded defaults and let users choose which to delete/load
        self.defaults = self.FIXEDdefaults.copy()
        self.deflt = tk.Tk()
        self.deflt.title("default URLS")
        tk.Label(self.deflt,
                 text = "LOADED DEFAULTS:",
                 fg = "white",
                 bg = "black",
                 font = ('Georgia','18','bold')).pack() 
        self.defList = tk.Label(self.deflt,
                 text = listTostr(self.defaults,'\n',item=1),
                 fg = "black",
                 bg = "white",
                 font = ('Georgia','14','italic'))
        self.defList.pack()
        tk.Button(self.deflt,text = "LOAD DEFAULTS", command = self.loaddef).pack()
        tk.Button(self.deflt,text = "DELETE URL FROM DEFAULTS", command = self.dialdel).pack()
        self.deflt.mainloop()

    def defaultfoods(self):
        #show all loaded defaults and let users choose which to delete/load
        self.fooddefaults = self.FIXEDFOODdefaults.copy()
        self.fdeflt = tk.Tk()
        self.fdeflt.title("default FOODS")
        tk.Label(self.fdeflt,
                 text = "LOADED DEFAULTS:",
                 fg = "white",
                 bg = "black",
                 font = ('Georgia','18','bold')).grid(row = 0, column = 0)
        
        scrollfood = tk.Scrollbar(self.fdeflt)
        scrollfood.grid(row = 1, column = 30, sticky='ns')
       
        self.fdeflist = tk.Listbox(self.fdeflt,
                                   width =  30, height = 22,
                                   yscrollcommand = scrollfood.set)

        #initial foodlist
        for fd in self.fooddefaults:
            self.fdeflist.insert(tk.END,fd)
        
        self.fdeflist.config(fg = "black", font = ('Georgia','14','italic'))
        self.fdeflist.grid(row = 1, column = 0, sticky='ns')

        scrollfood.config(command=self.fdeflist.yview)
        
        tk.Button(self.fdeflt,text = "LOAD DEFAULTS", command = self.loadfdef).grid(row = 23, column = 0)
        tk.Button(self.fdeflt,text = "DELETE FOOD FROM DEFAULTS", command = self.dialfdel).grid(row = 24, column = 0)
        self.fdeflt.mainloop()
        
def listTostr(foodIn,sep,item=0):
    #item sets if the list string should be itemized
    foods = foodIn.copy()
    outstr = ''
    if foods:
        outstr = str(foods[0])
        ctr = 0
        if item:
            outstr += ' ['+str(ctr)+']'
            ctr += 1
            
        foods.pop(0)
        
        for food in foods:
            outstr += sep + str(food)
            if item: outstr += ' ['+str(ctr)+']' 
            ctr += 1
        
    return outstr

def addtolist(guibut,listIn):
    if guibut and (guibut not in listIn):
        listIn.append(guibut)
