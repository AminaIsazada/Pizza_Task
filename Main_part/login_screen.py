from tkinter import *
from Main_part import user_screen
from Main_part import register_screen
from Main_part import admin_screen
from Main_part import decorator_pattern
import sqlite3

class LoginScreen(Tk):
    def __init__(self):
        super().__init__()
        self.title("Pizza order")
        self.userFrame = Frame(self)
        self.userLabel = Label(self.userFrame,width = 12,text = "Username:",anchor = 'w',bg="#ff82e1")
        self.userLabel.config(font=("Fixedsys", 15))
        self.userLabel.pack(side = TOP,fill=X)
        self.userEntry = Entry(self.userFrame,font=("Fixedsys", 15))
        self.userEntry.pack(side = TOP,fill = X,expand = YES)
        self.userFrame.pack(side = TOP,fill = X,padx = 5,pady = 5)
        self.passwordFrame = Frame(self)
        self.passwordLabel = Label(self.passwordFrame,width = 12,text = "Password:",anchor = 'w',bg="#ff82e1")
        self.passwordLabel.config(font=("Fixedsys", 15))
        self.passwordLabel.pack(side = TOP,fill=X)
        self.passwordEntry = Entry(self.passwordFrame,show = "*",font=("Fixedsys", 15))
        self.passwordEntry.pack(side = TOP,fill = X,expand = YES)
        self.passwordFrame.pack(side = TOP,fill = X,padx = 5,pady = 5)
        self.loginButton = Button(self,text = "Log in",command = self.loginClick,bg="#ff0000",width = 15,height = 2,font=("Fixedsys", 15)).pack(side = TOP,pady = 5,fill=X)
        self.registerButton = Button(self,text = "Register",command = self.registerClick,bg="#ff0000",width = 15,height = 2,font=("Fixedsys", 15)).pack(side = TOP,fill = X,pady = 5)
        self.successLabel = None

    def loginClick(self):
        username = self.userEntry.get()
        password = self.passwordEntry.get()
        state = False
        if(username == "admin" and password == "admin"):
            adminscreen = admin_screen.AdminScreen()
            self.destroy()
            adminscreen.title("Admin Screen")
            adminscreen.geometry("+300+100")
            adminscreen.configure(bg="#ff82e1")
            adminscreen.mainloop()
        
        file = sqlite3.connect("accounts.db")
        c = file.cursor()
        c.execute("SELECT username, password FROM accounts WHERE username=? AND password=?",(username,password))
        if c.fetchone() != None:
            state = True

        if(state):
            screen =user_screen.UserScreen(decorator_pattern.Customer(self.userEntry.get(),self.passwordEntry.get()))
            self.destroy()
            screen.title("User Screen")
            screen.geometry("+300+42")
            screen.configure(bg="#ff82e1")
            screen.mainloop()
        else:
            if self.successLabel != None:
                self.successLabel.destroy()
            self.successLabel = Label(self,text = "Sorry,try again",fg = "red")
            self.successLabel.pack()
    
    def registerClick(self):
        register_screen.registerScreen(self).geometry("+300+150")