import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import json
import webbrowser


class getUserInfo(simpledialog.Dialog):
    def __init__(self):
        self.iscancelled = 1
        self.window = tk.Tk()
        tk.Label(self.window, text="Please enter Mapbox Access Token",font=("Helvetica", 16)).grid(row=0)
#        tk.Label(self.window, text="Please enter Mapbox info",font=("Helvetica", 16)).grid(row=0,columnspan=2)
#        tk.Label(self.window, text="Mapbox Access Token",font=("Helvetica", 14)).grid(row=1,sticky='W')
#        tk.Label(self.window, text="Mapbox Access Token",font=("Helvetica", 14)).grid(row=2,sticky='W')

        self.e1 = tk.Entry(self.window,font=("Helvetica", 14))
        self.e1.grid(row=1)
#        self.e2 = tk.Entry(self.window,font=("Helvetica", 14))
#        self.e1.grid(row=1, column=1)
#        self.e2.grid(row=2, column=1)
#        tk.Button(self.window, text="Submit", command=self.submit,font=("Helvetica", 14)).grid(row=3,columnspan=2)    
#        tk.Button(self.window, text="Don't have a Mapbox account?", command=self.newAccount,font=("Helvetica", 14)).grid(row=4,columnspan=2)    
        tk.Button(self.window, text="Submit", command=self.submit,font=("Helvetica", 14)).grid(row=2)    
        tk.Button(self.window, text="Don't have a Mapbox account?", command=self.newAccount,font=("Helvetica", 14)).grid(row=3)    
        self.window.mainloop()
    def submit(self):
        simpledialog.Dialog.apply(self.e1)
#        simpledialog.Dialog.apply(self.e2)
        self.e1 = self.e1.get()
#        self.e2 = self.e2.get()
        self.iscancelled = 0
        self.window.destroy() 
    def newAccount(self):
        webbrowser.open('https://account.mapbox.com/auth/signup/')

def return_token():
    try:
        fh = open('config.json','r')
        with fh as json_file:  
            data = json.load(json_file)
            token = data['AccessToken'][0]
    #        Username = data['Username'][0]
    #        Password = data['Password'][0]
        fh.close()
        return token
        
    except FileNotFoundError:
        while True:
            info = getUserInfo()
            if info.iscancelled == 1:
                print('Cancelled by user')
                break
            else:
                if info.e1:
                    data = {}
                    data['AccessToken'] = [info.e1]
                    token = info.e1
                    with open('config.json', 'w') as outfile:  
                        json.dump(data, outfile)
                    return token
                    break
                else:
                    root = tk.Tk()
                    root.withdraw()
                    messagebox.showinfo('Invalid Entry', 'Please enter an access token or create a Mapbox account to continue')   
                    root.destroy()
    

#            if info.e1 and info.e2:
#                data = {}
#                data['Username'] = [info.e1]
#                data['Password'] = [info.e2]
#                Username = info.e1
#                Password = info.e2
#                with open('config.json', 'w') as outfile:  
#                    json.dump(data, outfile)
#                break
#            else:
#                if not info.e1 and not info.e2:
#                    root = tk.Tk()
#                    root.withdraw()
#                    messagebox.showinfo('Invalid Entry', 'Please enter a username and password')   
#                    root.destroy()
#                else:
#                    if not info.e1:
#                        root = tk.Tk()
#                        root.withdraw()
#                        messagebox.showinfo('Invalid Entry', 'Please enter a username')
#                        root.destroy() 
#                    if not info.e2:
#                        root = tk.Tk()
#                        root.withdraw()
#                        messagebox.showinfo('Invalid Entry', 'Please enter a password')
#                        root.destroy()

#    with open('config.json', 'w') as outfile:  
#        json.dump(data, outfile)
    
    


#class MyDialog(simpledialog.Dialog):
#
#    def body(self, master):
#
#        tk.Label(master, text="First:").grid(row=0)
#        tk.Label(master, text="Second:").grid(row=1)
#
#        self.e1 = tk.Entry(master)
#        self.e2 = tk.Entry(master)
#
#        self.e1.grid(row=0, column=1)
#        self.e2.grid(row=1, column=1)
#        return self.e1 # initial focus
#
#    def apply(self):
#        first = self.e1.get()
#        second = self.e2.get()
#        print (first, second )
#    
#def processOK():
#    credentials = MyDialog(window)
#    
#    print(credentials.e1.get())
##
#def processCancel():
#    print("I 2 am Groot!")
##    
#window = tk.Tk()
#window.geometry("500x500") #You want the size of the app to be 500x500
#window.resizable(0, 0) #Don't allow resizing in the x or y direction
#
#Username = tk.StringVar()
#Password = tk.StringVar()
#
#label = tk.Label(window,textvariable=Username)
#label2 = tk.Label(window,textvariable=Password)
#
#btOK = tk.Button(window, text="OK", command=processOK).grid(row=0)
#btCancel = tk.Button(window, text="Cancel", command=processCancel).grid(row=1)
#tk.Label(window, text="Username").grid(row=2)
#tk.Label(window, text="Password").grid(row=3)
#e1 = tk.Entry(window)
#e2 = tk.Entry(window)
#e1.grid(row=2, column=1)
#e2.grid(row=3, column=1)
#
#tk.Label(window, text="Username").grid(row=5)
#tk.Label(window, text="Password").grid(row=6)
#e3 = tk.Entry(window)
#e4 = tk.Entry(window)
#e3.grid(row=5, column=1)
#e4.grid(row=6, column=1)
#
#
#window.mainloop() #create an event loop for this window
