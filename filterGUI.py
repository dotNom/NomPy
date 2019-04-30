import tkinter as tk
from tkinter import messagebox
import datetime
import EventMap

class filterResults:

    def __init__(self,foods):

        self.options = []
        self.iscancelled = 0
        self.tableOnly = False
        self.window = tk.Tk()
        self.window.title('Filter Search Results')
        tk.Label(self.window, text="Filter by Food",font=("Helvetica", 14)).grid(row=0,columnspan=6,padx=5,pady=5,sticky='we')
        tk.Label(self.window, text="Filter by Date",font=("Helvetica", 14)).grid(row=2,columnspan=6,padx=5,pady=5,sticky='we')
        tk.Label(self.window, text="Start Date",font=("Helvetica", 12)).grid(row=3,column=0,padx=5,pady=5,sticky='we')
        tk.Label(self.window, text="Month",font=("Helvetica", 12),width=10).grid(row=4,column=0,padx=5,pady=5,sticky='we')
        tk.Label(self.window, text="Day",font=("Helvetica", 12),width=10).grid(row=4,column=2,padx=5,pady=5,sticky='we')
        tk.Label(self.window, text="Year",font=("Helvetica", 12),width=10).grid(row=4,column=4,padx=5,pady=5,sticky='we')
        tk.Label(self.window, text="End Date",font=("Helvetica", 12)).grid(row=6,column=0,padx=5,pady=5,sticky='we')
        tk.Label(self.window, text="Month",font=("Helvetica", 12)).grid(row=7,column=0,padx=5,pady=5,sticky='we')
        tk.Label(self.window, text="Day",font=("Helvetica", 12)).grid(row=7,column=2,padx=5,pady=5,sticky='we')
        tk.Label(self.window, text="Year",font=("Helvetica", 12)).grid(row=7,column=4,padx=5,pady=5,sticky='we')

        self.Fooddefault = tk.StringVar(self.window)
        self.Fooddefault.set('None')
        tk.OptionMenu(self.window, self.Fooddefault, *foods).grid(row=1,column=0,columnspan=6,padx=5,pady=5)   
        
        now = datetime.datetime.now()
        months = ['January','February','March','April','May','June','July','August','September','October','November','December']
        
        self.Monthdefault1 = tk.StringVar(self.window)
        self.Daydefault1 = tk.StringVar(self.window)
        self.Yeardefault1 = tk.StringVar(self.window)
        self.Monthdefault1.set(str(now.month))
        self.Daydefault1.set(str(now.day))
        self.Yeardefault1.set(str(now.year))
        self.Monthdefault2 = tk.StringVar(self.window)
        self.Daydefault2 = tk.StringVar(self.window)
        self.Yeardefault2 = tk.StringVar(self.window)
        self.Monthdefault2.set('None')
        self.Daydefault2.set('None')
        self.Yeardefault2.set('None')
        days = []
        
        years = [str(now.year-1)]
        for i in range(4):
            years.append(str(now.year+i))
        for i in range(31):
            days.append(str(i+1))
        tk.OptionMenu(self.window, self.Monthdefault1, *months).grid(row=5,column=0,columnspan=2,padx=5,pady=5,sticky='we')   
        tk.OptionMenu(self.window, self.Daydefault1, *days).grid(row=5,column=2,columnspan=2,padx=5,pady=5,sticky='we')
        tk.OptionMenu(self.window, self.Yeardefault1, *years).grid(row=5,column=4,columnspan=2,padx=5,pady=5,sticky='we')     
        tk.OptionMenu(self.window, self.Monthdefault2, *months).grid(row=8,column=0,columnspan=2,padx=5,pady=5,sticky='we')   
        tk.OptionMenu(self.window, self.Daydefault2, *days).grid(row=8,column=2,columnspan=2,padx=5,pady=5,sticky='we')
        tk.OptionMenu(self.window, self.Yeardefault2, *years).grid(row=8,column=4,columnspan=2,padx=5,pady=5,sticky='we')                  
        
        tk.Button(self.window, text="Submit", command=self.submit,font=("Helvetica", 14),width=7).grid(row=9,column=0,columnspan=2,padx=5,pady=5,sticky='w')    
        tk.Button(self.window, text="Cancel", command=self.cancel,font=("Helvetica", 14),width=7).grid(row=9,column=4,columnspan=2,padx=5,pady=5,sticky='e')    
  
        self.window.lift()
        self.window.attributes('-topmost', 1)
        self.window.attributes('-topmost', 0)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()
        
    def submit(self):
       
        food = self.Fooddefault.get()
        m1 =  self.Monthdefault1.get()
        d1 = self.Daydefault1.get()
        y1 = self.Yeardefault1.get()
        m2 =  self.Monthdefault2.get()
        d2 = self.Daydefault2.get()
        y2 = self.Yeardefault2.get()
        
        if food != 'None':
            self.options.append(food)
        else:
            self.options.append('')
        
        if m1 != 'None' and  d1 != 'None' and  y1 != 'None' and  m2 != 'None' and  d2 != 'None' and  y2 != 'None':
            months = ['January','February','March','April','May','June','July','August','September','October','November','December']
            m1= months.index(m1)+1
            m2 = months.index(m2)+1
            
            date1 = y1+str(m1).zfill(2)+d1.zfill(2)
            date2 = y2+str(m2).zfill(2)+d2.zfill(2)
               
            self.options.append(date1)
            self.options.append(date2)
        else:
            self.options.append('')
            self.options.append('')

        self.window.destroy() 
        
    def cancel(self):
        self.iscancelled = 1
        self.window.destroy() 
    
    def on_closing(self):
        self.iscancelled = 1
        self.window.destroy()
    
def return_filter(foodEvents,mapbox_access_token,csvFlag):
    filteredEvents = []
    
    foods = []
    options = []
    for event in foodEvents:
        for item in event.food:
            if item not in foods:
                foods.append(item)              
    while True:
        response = filterResults(foods)
        if response.iscancelled == 1:
                print('Cancelled by User')
                break            
        options = response.options 
        dateFlag = 0
        flag = 0
        if options:
            if options[0]:            
                flag += 1
                Food = options[0]
            if options[1]:            
                flag += 10
                startDate = options[1]
                endDate = options[2]
                if startDate>endDate:
                    dateFlag == 1
                    root = tk.Tk()
                    root.withdraw()
                    messagebox.showinfo('Invalid Entry', 'Starting date occurs after the ending date')   
                    root.destroy()
            
            if flag == 0:
#                print('Nothing Selected')
                root = tk.Tk()
                root.withdraw()
                messagebox.showinfo('Invalid Entry', 'Nothing selected')   
                root.destroy()
            for event in foodEvents:
                testFood = event.food
                testDate = event.timestart.split(':')[-1][:8]
                if flag == 1:
                    if Food in testFood:
                        filteredEvents.append(event)
                elif flag == 10:
                    if startDate<=endDate and testDate>=startDate and testDate<=endDate:
                        filteredEvents.append(event)
                elif flag == 11:
                    if Food in testFood and startDate<=endDate and testDate>=startDate and testDate<=endDate:
                        filteredEvents.append(event)
            if filteredEvents:
                EventMap.plotMap(filteredEvents,mapbox_access_token,csvFlag)
                filteredEvents = []
            elif flag !=0 and dateFlag==0:
                root = tk.Tk()
                root.withdraw()
                messagebox.showinfo('Invalid Entry', 'No events found for the given user input')   
                root.destroy()
    return filteredEvents