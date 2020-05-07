from tkinter import *
from Main_part import decorator_pattern
import sqlite3
import json

class UserScreen(Tk):
    def __init__(self,customer):
        super().__init__()
        self.config(bg="#ff82e1")
        self.currentCustomer = customer
        self.currentPizza = None
        self.result = None
        self.customerUsername = Label(self,text = "Username: " + self.currentCustomer.get_username(),bg="#ff82e1",font=("Fixedsys", 15)).pack(side=TOP,fill=X)
        self.pizzaFrame = Frame(self)
        self.pizzaFrame.pack(side=TOP,fill=X)
        self.exFrame = Frame(self)
        self.exFrame.pack(side=TOP,fill=X)
        self.pizzaLabel = Label(self.pizzaFrame,text="Pizzas:",bg="#ff82e1",font=("Fixedsys", 15)).pack(fill=X)
        self.pizzalistFrame = Frame(self.pizzaFrame)
        self.pizzalistFrame.pack(fill=X)
        self.pizzaList = Listbox(self.pizzalistFrame)
        self.pizzaList.config(bg="#ff82e1",font=("Fixedsys", 15))
        pizzascrollbar = Scrollbar(self.pizzalistFrame, orient="vertical")
        pizzascrollbar.config(command=self.pizzaList.yview)
        pizzascrollbar.pack(side="right", fill="y")
        file = sqlite3.connect('pizzas.db')
        c = file.cursor()
        for i in (c.execute("SELECT name FROM pizzas ")):
            self.pizzaList.insert(END,i[0])
        file.commit()
        self.pizzaList.pack(side=LEFT,fill=X)
        self.selectPizzaButton = Button(self.pizzaFrame,text = "Select",command = self.selectPizza,bg="#ff0000",font=("Fixedsys", 15)).pack(fill=X)
        self.exLabel = Label(self.exFrame,text="Extentions:",bg="#ff82e1",font=("Fixedsys", 15)).pack(fill=X)
        self.extentionlistFrame = Frame(self.exFrame)
        self.extentionlistFrame.pack(fill=X)
        self.extensionsList = Listbox(self.extentionlistFrame,selectmode=MULTIPLE)
        self.extensionsList.config(bg="#ff82e1",font=("Fixedsys", 15))
        exscrollbar = Scrollbar(self.extentionlistFrame, orient="vertical")
        exscrollbar.config(command=self.extensionsList.yview)
        exscrollbar.pack(side="right", fill="y")
        file = sqlite3.connect('extentions.db')
        c = file.cursor()
        for i in (c.execute("SELECT name FROM extentions ")):
            self.extensionsList.insert(END,i[0])
        file.commit()
        self.extensionsList.pack(side=LEFT,fill=X)
        self.buttonFrame = Frame(self.exFrame)
        self.buttonFrame.config(bg="#ff82e1")
        self.buttonFrame.pack(fill=X)
        self.addExtensionButton = Button(self.buttonFrame,text = "Add",command = self.addExtension,width=8,bg="#ff0000",font=("Fixedsys", 15)).pack(side=LEFT)
        self.removeExtensionButton = Button(self.buttonFrame,text = "Remove",command = self.removeExtension,width=8,bg="#ff0000",font=("Fixedsys", 15)).pack(side=LEFT)
        self.orderButton = Button(self,text = "Order",command = self.order,bg="#ff0000",font=("Fixedsys", 15)).pack(fill=X)

    def removeExtension(self):
        file = sqlite3.connect('extentions.db')
        c = file.cursor()
        file.commit()
        reslist = list()
        selections = self.extensionsList.curselection()
        for i in selections:
            current = self.extensionsList.get(i)
            reslist.append(current)
        for val in reslist:
            self.currentPizza.remove_extention(val)
        file.close()
        if (self.result != None):
            self.result.destroy()
        self.result = Text(self,bg="#ff82e1",height=7,width=27)
        self.result.insert(END,self.currentPizza.get_status()+"\n" + "Price: " + str(self.currentPizza.get_price()))
        self.result.config()
        self.result.pack()
    
    def addExtension(self):
        file = sqlite3.connect('extentions.db')
        c = file.cursor()
        file.commit()
        reslist = list()
        selections = self.extensionsList.curselection()
        for i in selections:
            current = self.extensionsList.get(i)
            reslist.append(current)
        for val in reslist:
            c.execute("SELECT price FROM extentions WHERE name=?",(val,))
            try:
                self.currentPizza.add_extention(val,c.fetchone()[0])
            except:
                pass
        file.close()
        if (self.result != None):
            self.result.destroy()
        try:
            self.result = Text(self,bg="#ff82e1",height=7,width=27)
            self.result.insert(END,self.currentPizza.get_status()+"\n" + "Price: " + str(self.currentPizza.get_price()))
            self.result.config()
            self.result.pack()
        except: pass
        
    def selectPizza(self):
        file = sqlite3.connect('pizzas.db')
        c = file.cursor()
        pizzaType = self.pizzaList.get(ANCHOR)
        c.execute("SELECT price FROM pizzas WHERE name=?",(pizzaType,))
        self.currentPizza = decorator_pattern.PizzaBuilder(pizzaType,c.fetchone()[0])
        file.commit()
        file.close()
        if (self.result != None):
            self.result.destroy()
        self.result = Text(self,bg="#ff82e1",height=7,width=27)
        self.result.insert(END,self.currentPizza.get_status()+"\n" + "Price: " + str(self.currentPizza.get_price()))
        self.result.config()
        self.result.pack()
        
    
    def order(self):
        if self.result != None:
            self.result.destroy()
        self.result = Text(self,bg="#ff82e1",height=7,width=27)
        self.result.insert(END,"Pizza: " + self.currentPizza.get_status() + "\n" + "Price: " + str(self.currentPizza.get_price()) + "\nOrdered!")
        self.result.config(bg="#ff82e1",fg="green")
        file = sqlite3.connect("accounts.db")
        c = file.cursor()
        c.execute("SELECT orderlist FROM accounts WHERE username =?",(self.currentCustomer.get_username(),))
        data = json.loads(c.fetchone()[0])
        data.append("Pizza: " + self.currentPizza.get_status() + "\n" + "Price: " + str(self.currentPizza.get_price()))
        new = json.dumps(data)
        c.execute("UPDATE accounts SET orderlist=? WHERE username=?",(new,self.currentCustomer.get_username()))
        file.commit()
        file.close()
        self.result.pack()
    
