import tkinter as tk
from tkinter import simpledialog
import Feeder

class setGUI:
    
    def __init__(self,defaults = []):
        self.foodToSearch = ['food']
        self.doCalendar = 'YES'        
        self.URLlist = ['http://calendar.utexas.edu/calendar.xml']
        self.FIXEDdefaults = defaults
        self.defaults = defaults.copy()
        
        self.launch = tk.Tk()
        self.launch.title("Initial Settings")
        
        #Ask if calendar should be made
        tk.Label(self.launch,
                 text = "CURRENT CALENDAR OUTPUT:",
                 fg = "white",
                 bg = "red",
                 font = ('Georgia','24','bold')).grid(row = 0, column = 0)        
        self.calendar = tk.Label(self.launch,
                 text = '\nYES Calendar ==> .ics file will be saved\n',
                 fg = "red",
                 font = ('Georgia','14','italic'))
        self.calendar.grid(row = 1, column = 0)
        
        tk.Button(self.launch,text = "CHANGE CALENDAR OPTION", command = self.tkYesNo).grid(row = 2, column = 0)
        
        #Ask to add food options, and display list of options
        tk.Label(self.launch,
                 text = "CURRENT FOOD OPTIONS:",
                 fg = "white",
                 bg = "red",
                 font = ('Georgia','24','bold')).grid(row = 4, column = 0)
        
        scrollfood = tk.Scrollbar(self.launch)
        scrollfood.grid(row = 5, column = 50, sticky='ns')
        self.foodlist = tk.Listbox(self.launch, 
                                   width =  40, height = 5,
                                   yscrollcommand = scrollfood.set)
        
        #initial foodlist
        for fd in self.foodToSearch:
            self.foodlist.insert(tk.END,fd)
        
        self.foodlist.config(fg = "red", font = ('Georgia','14','italic'))
        self.foodlist.grid(row = 5, column = 0)
        
        scrollfood.config(command=self.foodlist.yview)

        tk.Label(self.launch,
                 text = "\nAdd more food options to search from:\n",
                 fg = "black",
                 font = ('Georgia','12')).grid(row = 11, column = 0)
               
        tk.Button(self.launch,text = "ADD FOOD",command = self.dialfood).grid(row = 12, column = 0)
        
        #Ask to add the url links and include a check to make sure that the link contains a valid rss feed (.xml or /rss)
        tk.Label(self.launch,
                 text = "CURRENT URL OPTIONS:",
                 fg = "white",
                 bg = "red",
                 font = ('Georgia','24','bold')).grid(row = 13, column = 0) 
        
        scrollurl = tk.Scrollbar(self.launch)
        scrollurl.grid(row = 14, column = 65, sticky='ns')
        self.url = tk.Listbox(self.launch, 
                              width =  60, height = 5,
                              yscrollcommand = scrollurl.set)
        
        #initial urllist
        for ul in self.URLlist:
            self.url.insert(tk.END,ul)
        
        self.url.config(fg = "red", font = ('Georgia','14','italic'))
        self.url.grid(row = 14, column = 0)
        
        scrollfood.config(command=self.url.yview)
        
        tk.Label(self.launch,
                 text = "\nAdd more url options to search from:\n",
                 fg = "black",
                 font = ('Georgia','12')).grid(row = 20, column = 0)
        
        tk.Button(self.launch,text = "ADD URL",command = self.dialurl).grid(row = 21, column = 0)
        tk.Label(self.launch,
                 text = "\nOr select from loaded defaults:\n",
                 fg = "black",
                 font = ('Georgia','12')).grid(row=22,column = 0)
        tk.Button(self.launch,text = "LOAD DEFAULT URLS",command = self.defaulturls).grid(row = 23, column = 0)
        
        #Exit when done
        tk.Button(self.launch,text = "DONE",command = self.done).grid(row = 24, column = 0)
        
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
        self.URLlist = []
        for url in self.defaults:
            addtolist(url,self.URLlist)
            self.url.insert(tk.END, url) 
        self.deflt.destroy()
        
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
        
def listTostr(foodIn,sep,item=0):
    #item sets if the list string should be itemized
    foods = foodIn.copy()
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

'''
#For debugging settingGUI
defaultALL = ['http://calendar.utexas.edu/calendar.xml', 'http://calendar.mit.edu/calendar.xml', 'http://events.umich.edu/day/rss', 'http://events.umich.edu/week/rss']        
a = setGUI(defaultALL)    
print('INITIAL SETTINGS FROM GUI:')
print(a.doCalendar + ' Calendar', a.foodToSearch, a.URLlist, sep = '\n')
'''