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
                 font = ('Georgia','24','bold')).pack()        
        self.calendar = tk.Label(self.launch,
                 text = '\nYES Calendar ==> .ics file will be saved\n',
                 fg = "red",
                 font = ('Georgia','14','italic'))
        self.calendar.pack()
        
        tk.Button(self.launch,text = "CHANGE CALENDAR OPTION", command = self.tkYesNo).pack()
        
        tk.Label(self.launch,text="\n").pack() #empty line
        
        #Ask to add food options, and display list of options
        tk.Label(self.launch,
                 text = "CURRENT FOOD OPTIONS:",
                 fg = "white",
                 bg = "red",
                 font = ('Georgia','24','bold')).pack()
        tk.Label(self.launch,text="").pack() #empty line
        self.foodList = tk.Label(self.launch,
                 text = listTostr(self.foodToSearch,', '),
                 fg = "red",
                 font = ('Georgia','14','italic'))
        self.foodList.pack()
        tk.Label(self.launch,
                 text = "\nAdd more food options to search from:\n",
                 fg = "black",
                 font = ('Georgia','12')).pack()
               
        tk.Button(self.launch,text = "ADD FOOD",command = self.dialfood).pack()
        
        tk.Label(self.launch,text="\n").pack() #empty line
        
        #Ask to add the url links and include a check to make sure that the link contains a valid rss feed (.xml or /rss)
        tk.Label(self.launch,
                 text = "CURRENT URL OPTIONS:",
                 fg = "white",
                 bg = "red",
                 font = ('Georgia','24','bold')).pack() 
        tk.Label(self.launch,text="").pack() #empty line
        self.url = tk.Label(self.launch,
                 text = listTostr(self.URLlist,'\n'),
                 fg = "red",
                 font = ('Georgia','14','italic'))
        self.url.pack()
        tk.Label(self.launch,
                 text = "\nAdd more url options to search from:\n",
                 fg = "black",
                 font = ('Georgia','12')).pack()
        
        tk.Button(self.launch,text = "ADD URL",command = self.dialurl).pack()
        tk.Label(self.launch,
                 text = "\nOr select from loaded defaults:\n",
                 fg = "black",
                 font = ('Georgia','12')).pack()
        tk.Button(self.launch,text = "LOAD DEFAULT URLS",command = self.defaulturls).pack()
        
        tk.Label(self.launch,text="\n").pack() #empty line
        
        #Exit when done
        tk.Button(self.launch,text = "DONE",command = self.done).pack()
        
        self.launch.mainloop()
        
    def dialfood(self):
        newfood = simpledialog.askstring("More food","Please Enter food.",parent=self.launch)
        addtolist(newfood,self.foodToSearch)
        self.foodList['text'] = listTostr(self.foodToSearch,', ')
    
    
    def dialurl(self):
        newurl = simpledialog.askstring("More links","Please Enter URL.",parent=self.launch)
        
        urlOK = False
        
        if newurl:
            if '/rss' in newurl or '.xml' in newurl:    
                urlOK = Feeder.validlink(newurl)
            
            if urlOK:
                addtolist(newurl,self.URLlist)
                self.url['text'] = listTostr(self.URLlist,'\n')  
            else:
                self.tkInvalid()
    
    def dialdel(self):
        torem = simpledialog.askinteger("delete url","Please Enter index of URL to remove.\nIndices are given in the LOADED DEFAULTS list by the URL.",parent=self.launch,minvalue=0,maxvalue=len(self.defaults)-1) 
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
        self.url['text'] = listTostr(self.URLlist,'\n')  
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