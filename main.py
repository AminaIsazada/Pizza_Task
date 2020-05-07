from tkinter import *
import sqlite3
from Main_part import login_screen

def main():
    conn = sqlite3.connect('accounts.db')
    c = conn.cursor()
    try:
        c.execute("""CREATE TABLE accounts (
                username text,
                password text,
                orderlist text
        )""")
    except:
        pass
    conn.commit()
    root = login_screen.LoginScreen()
    root.geometry("+300+150")
    root.configure(bg="#ff82e1")
    root.mainloop()

if __name__ == "__main__":
    main()





