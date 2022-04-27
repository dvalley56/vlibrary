from asyncio.windows_events import NULL
from tkinter import messagebox
from tkinter import *
import mysql.connector as ms
from datetime import date, timedelta

from services.SMTP import send_email

def insert(title,author,year,isbn):
    conn=ms.connect(host='127.0.0.1',database='user',user='root', password="asdf1234@#")
    cur = conn.cursor()
    cur.execute('INSERT INTO books(isbn,bname,author,publishing_year) VALUES(%s,%s,%s,%s)',(isbn,title,author,int(year)))
    conn.commit()
    conn.close()

def get_name():
    conn=ms.connect(host='127.0.0.1',database='user',user='root', password="asdf1234@#")
    a=[]
    cur = conn.cursor()
    cur.execute("SELECT Time FROM login")
    for i in cur.fetchall():
        a.append(i)
    b=max(a)
    dur = conn.cursor()
    dur.execute("SELECT name FROM login Where Time=%s",(b))
    name=dur.fetchone()
    return name

#create a function to get user email
def get_email():
    name = get_name()
    conn=ms.connect(host='127.0.0.1',database='user',user='root', password="asdf1234@#")
    a=[]
    cur = conn.cursor()
    cur.execute("SELECT Email FROM login where name=%s", (name[0],))
    email = cur.fetchone()
    return email

def request_insert(title,author,isbn):
    conn=ms.connect(host='127.0.0.1',database='user',user='root', password="asdf1234@#")
    name=get_name()
    cur = conn.cursor()
    if (title=="" or author==""):
        messagebox.showinfo("Something Unfilled","Please enter right Title & Author name")
    else :
        #get user email
        email= get_email()[0]
        cur.execute('INSERT INTO request(Name, Book_name,isbn,Author_Name, Requested_date) VALUES(%s,%s,%s,%s,%s)',(name[0],title,isbn,author,date.today()))
        #send email 
        resp = send_email(email,"145H1HBKSQ4R8QJQYMST3KYVJJC4", {
            "name" : name[0],
            "bookname" : title,
            "isbn" : isbn,
            "author" : author
        })
    conn.commit()
    conn.close()

def request_view(title,author,year,isbn):
    conn=ms.connect(host='127.0.0.1',database='user',user='root', password="asdf1234@#")
    cur = conn.cursor()
    if title=='' or author=='' or year=='' or isbn=='':
        cur.execute("SELECT * FROM request")
    else:
        cur.execute("SELECT * FROM request WHERE Book_name=%s or isbn=%s",(title.upper(),isbn))
    rows=cur.fetchall()
    conn.close()
    return rows

def request_delete(title,isbn):
    conn=ms.connect(host='127.0.0.1',database='user',user='root', password="asdf1234@#")
    cur = conn.cursor()
    dur = conn.cursor()
    sur = conn.cursor()
    dur.execute("SELECT Name FROM request WHERE Book_name=%s AND isbn=%s",(title.upper(),isbn))
    a=dur.fetchone()
    cur.execute("SELECT Email FROM login WHERE name=%s",(a[0],))
    b=cur.fetchone()
    sur.execute("DELETE FROM request WHERE Book_name=%s AND isbn=%s",(title.upper(),isbn))
    messagebox.showinfo("Successfull","Request Completed..")
    conn.commit()
    conn.close()
    return b
    
                                                                                       
def issue_delete():
    conn=ms.connect(host='127.0.0.1',database='user',user='root', password="asdf1234@#")
    cur = conn.cursor()
    a=get_name()
    cur.execute("DELETE FROM issue WHERE Name=%s",(a[0],) )
    conn.commit()
    conn.close()

def issue_insert(bname,aname):
    isdate=date.today()
    redate_expected=isdate + timedelta(days=3)
    conn=ms.connect(host='127.0.0.1',database='user',user='root', password="asdf1234@#")
    cur = conn.cursor()
    tc= conn.cursor()
    name=get_name()
    tc.execute('SELECT bcount FROM books WHERE bname=%s AND author=%s',(bname.upper(),aname.upper()))
    cnt=tc.fetchone()
    if cnt!=0:
        cur.execute('INSERT INTO issue(Name,Bname,Issued_Date,Author) Values(%s,%s,%s,%s)',(name[0],bname,isdate,aname))
        tc.execute('UPDATE books SET bcount=%s WHERE bname=%s AND author=%s',(cnt[0]-1,bname.upper(),aname.upper()))   
        conn.commit()
        resp = send_email(get_email()[0], "GNWSK3ECT2M62ZHKGMVCJ7SNQP35", {
            "name" : name[0],
            "bookname" : bname,
            "author" : aname,
            "returnDate" : '{} 12:00PM'.format(str(redate_expected))
        })
        messagebox.showinfo("Successfully Issued", "Please return it on time...")
    elif cnt[0]==0 :
        messagebox.showinfo("sorry","This book is not available for a now, please make a request..!")
    else :
        messagebox.showinfo("Sorry","This book is not available, please make a request..!")
    conn.close()

def issue_view(title):
    conn=ms.connect(host='127.0.0.1',database='user',user='root', password="asdf1234@#")
    cur = conn.cursor()
    if title=="":
        cur.execute("SELECT * FROM issue")
    else :
        cur.execute("SELECT * FROM issue WHERE Bname=%s",(title.upper(),))
    rows=cur.fetchall()
    conn.close()
    return rows


def view():
    conn=ms.connect(host='127.0.0.1',database='user',user='root', password="asdf1234@#")
    cur = conn.cursor()
    cur.execute("SELECT * FROM books")
    rows=cur.fetchall()
    conn.close()
    return rows

def get_id(isbn):
    conn=ms.connect(host='127.0.0.1',database='user',user='root', password="asdf1234@#")
    cur=conn.cursor()
    cur.execute('SELECT B_id FROM books WHERE isbn=%s',(isbn,))
    r1=cur.fetchone()
    return r1

def search(title,author,year,isbn):
    try :
        conn=ms.connect(host='127.0.0.1',database='user',user='root', password="asdf1234@#")
        cur = conn.cursor()
        cur.execute("SELECT * FROM books WHERE bname=%s OR author=%s OR publishing_year=%s OR isbn=%s",(title.upper(),author.upper(),year,isbn))
        rows=cur.fetchall()
        conn.close()
        return rows
    except :
        print("Error")

def delete(isbn):
    conn = ms.connect(host='127.0.0.1',database='user',user='root', password="asdf1234@#")
    cur = conn.cursor()
    a= get_id(isbn)
    if(a!=NULL):
        cur.execute('DELETE FROM books WHERE B_id=%s',(a))
        messagebox.showinfo("successfull","Entry Deleted")
        conn.commit()
    else :
        messagebox.showinfo("Error","Can't Find this entry...")
    conn.close()

def update(id,title,author,year,isbn):
    conn=ms.connect(host='127.0.0.1',database='user',user='root', password="asdf1234@#")
    cur = conn.cursor()
    cur.execute("UPDATE books SET bname=%s,author=%s,publishing_year=%s,isbn=%s WHERE B_id=%s",(title,author,year,isbn,id[0]))
    conn.commit()
    conn.close()

def check_return(bname,author):
    conn=ms.connect(host='127.0.0.1',database='user',user='root', password="asdf1234@#")
    dur = conn.cursor()
    sname=get_name()
    dur.execute("SELECT Issued_Date FROM issue WHERE Bname=%s AND Author=%s OR Name=%s",(bname,author,sname[0]))
    a=dur.fetchone()
    if (date.today()-a[0] > timedelta(days=3)):
        messagebox.showinfo('Penalty','You have made it late please Pay your fine')
        cur = conn.cursor()
        cur.execute('UPDATE issue SET Returned_Date=%s WHERE Bname=%s AND Name=%s',(date.today(),bname.upper(),sname[0]))
        conn.commit()
    elif (date.today()-a[0] <= timedelta(days=3)):
        cur = conn.cursor()
        cur.execute('UPDATE issue SET Returned_Date=%s WHERE Bname=%s AND Name=%s',(date.today(),bname.upper(),sname[0]))
        messagebox.showinfo('Successfull','Thank you for returning it on time...')
        conn.commit()
    else :
        messagebox.showinfo("Error","Wrong Book, select proper one...")
    conn.close()