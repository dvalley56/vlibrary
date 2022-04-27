import mysql.connector as ms
from tkinter import messagebox
from tkinter import *
from datetime import datetime

from services.SMTP import send_email
def connect():
    conn=ms.connect(host="127.0.0.1", user="root", password="Manish@2432",database="user")
    conn.commit()
    conn.close()

def insert(name,password,rollno,email):
    conn=ms.connect(host="127.0.0.1", user="root", password="Manish@2432",database="user")
    cur = conn.cursor()
    cur.execute('INSERT INTO login(name,pass,roll,Email, Time)' 'VALUES(%s,%s,%s,%s,%s)', (name,password,rollno,email, datetime.now()))
    send_email(email, "PAHA3EY34T4JDJGMN1BQ3A4PMWAD", {"name": name})
    messagebox.showinfo("Successfull", "You are successfully registered")
    conn.commit()
    conn.close()

def check(name,password):
    from admin import admin
    conn=ms.connect(host="127.0.0.1", user="root", password="Manish@2432",database="user")
    cur = conn.cursor()
    if(cur.execute('SELECT * FROM admin WHERE Aname =%s AND Apass = %s',(name,password))):
        if cur.fetchone():
            messagebox.showinfo("Successfull", "You are successfully logged in")
            window = Tk()
            window.title('Admin_User')
            window.geometry('700x450')
            obj=admin(window)
            window.mainloop()
            conn.close()
        else:
            messagebox.showinfo('error','INVALID CREDENTIALS for ADMIN LOGIN')

def checks(name,password):                       # for student login
    conn=ms.connect(host="127.0.0.1", user="root", password="Manish@2432",database="user")
    cur = conn.cursor()
    t= datetime.now()
    cur.execute('SELECT * FROM login WHERE name = %s AND pass = %s', (name, password))
    if cur.fetchone():
        tc = conn.cursor()
        tc.execute("UPDATE login SET Time=%s WHERE name=%s AND pass= %s",(t,name,password))
        conn.commit()
        messagebox.showinfo("Successfull", "You are successfully logged in")
        from student import student
        window = Tk()
        window.title('Student_User')
        window.geometry('700x400')
        obj=student(window)
        window.mainloop()
        conn.close()
    else:
        messagebox.showinfo('error','INVALID CREDENTIALS for STUDENT LOGIN')


connect()