import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import json
import webbrowser
    
class getUserInfo(simpledialog.Dialog):
    '''
    Class for the mapbox access token GUI. This gets initialized only if there 
    isn't a config.json file in the current directory
    '''
    def __init__(self):
        self.iscancelled = 1
        self.tableOnly = False
        self.window = tk.Tk()
        self.window.title('Optional Map Functionality')
        tk.Label(self.window, text="Please enter Mapbox Access Token",font=("Helvetica", 16)).grid(row=0,columnspan=2,padx=5,pady=5)

        self.e1 = tk.Entry(self.window,font=("Helvetica", 14))
        self.e1.grid(row=1,columnspan=2,padx=5,pady=5)
        
        tk.Button(self.window, text="Submit", command=self.submit,font=("Helvetica", 14)).grid(row=2,columnspan=2,padx=5,pady=5)    
        tk.Button(self.window, text="Don't have a Mapbox account?", command=self.newAccount,font=("Helvetica", 14)).grid(row=3,column=0,padx=5,pady=5)
        tk.Button(self.window, text="Show Table Instead", command=self.showtableOnly,font=("Helvetica", 14)).grid(row=3,column=1,padx=5,pady=5)  
        self.window.mainloop()
        
    def submit(self):
        simpledialog.Dialog.apply(self.e1)
        self.e1 = self.e1.get()
        self.iscancelled = 0
        self.window.destroy() 
        
    def showtableOnly(self):
        self.iscancelled = 0
        self.tableOnly = True
        self.window.destroy()   
        
    def newAccount(self):
        webbrowser.open('https://account.mapbox.com/auth/signup/')
    


        
def return_token():
    '''
    Return the mapbox access token. If the user has selected to show the table
    only, then return 0 instead
    '''
    try:
        fh = open('config.json','r')
        with fh as json_file:  
            data = json.load(json_file)
            token = data['AccessToken'][0]
        fh.close()
        return token
        
    except FileNotFoundError:
        while True:
            info = getUserInfo()
            if info.iscancelled == 1:
                print('Cancelled by user')
                break
            elif info.tableOnly:
                return 0
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