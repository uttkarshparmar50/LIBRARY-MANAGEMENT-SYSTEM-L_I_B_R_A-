from tkinter import *
from tkinter import messagebox
import sqlite3 as sql
from tkinter.ttk import Combobox
win=Tk()
win.title("My Libra")
win.iconbitmap('tmu.ico')
win.state("zoomed")
win.resizable(width=True,height=False)
win.configure(bg='whitesmoke')
title=Label(win,text="L_I_B_R_A",font=(' ',40,'bold'),bg='ghostwhite',fg='dimgrey')
title.pack()

photo=PhotoImage(file="image.png")
label= Label(win, image=photo)
label.pack()


def login(user_entry,pass_entry,pfrm):
    username=user_entry.get()
    password=pass_entry.get()
    if len(username)==0 or len(password)==0:
        messagebox.showwarning('Login','Username or Password cannot be empty')
    else:
        if username=='uttkarsh' and password=='krishna':
            messagebox.showinfo('Login','Logged in successfully')
            welcome_screen(win,pfrm)
        else:
            messagebox.showerror('Login','Incorrect Username or Password')
            pass_entry.delete(0,END)
            user_entry.focus()

db='library.db'
def db_book(win,frm,title_entry,author_entry,copies_entry):
    title=title_entry.get()
    author=author_entry.get()
    copies=copies_entry.get()
    if len(title)==0 or len(author)==0 or len(copies)==0:
        messagebox.showwarning('Book management','Fields cannot be empty')
    else:
        con=sql.connect(database=db)
        cur=con.cursor()
        cur.execute("select max(title_id) from book")
        tup=cur.fetchone()
        if(tup[0]==None):
            tid=1
        else:
            tid=tup[0]+1
        cur.execute("insert into book(title_id,title,author,copies,left_copies) values(?,?,?,?,?)",(tid,title,author,copies,copies))
        con.commit()
        con.close()
        messagebox.showinfo("Book management","Book entry done...")
        title_entry.delete(0,END)
        author_entry.delete(0,END)
        copies_entry.delete(0,END)
        title_entry.focus()
        
def db_search(title,author_combo,result_left_lbl,result_right_lbl):
    result_left_lbl.configure(text=' ')
    result_right_lbl.configure(text=' ')
    author=author_combo.get()
    con=sql.connect(db)
    cur=con.cursor()
    cur.execute("select * from book where title=? and author=?",(title,author,))
    rows=cur.fetchall()
    result_left_lbl_msg="Copies:\n\nLeft Copies:"
    for row in rows:
        result_right_lbl_msg=str(row[3])+"\n\n"+str(row[4])
    result_left_lbl.configure(text=result_left_lbl_msg)
    result_right_lbl.configure(text=result_right_lbl_msg) 
    con.close()
        
def db_getAuthor(win,frm,title_combo,result_left_lbl,result_right_lbl):
    title=title_combo.get()
    
    con=sql.connect(database=db)
    cur=con.cursor()
    cur.execute("select author from book where title=?",(title,))
    authors=cur.fetchall()
    all_author=[]
    for author in authors:
        all_author.append(author[0])
    author_lbl=Label(frm,text='Authors',font=(' ',25,'bold'),fg='whitesmoke',bg='darkslategrey')
    author_lbl.place(relx=.3,rely=.3)

    author_combo=Combobox(frm,font=(' ',18,'bold'),values=all_author,state="readonly")
    author_combo.current(0)
    author_combo.place(relx=.4,rely=.3)

    search_btn=Button(frm,text='Search for Books',command=lambda:db_search(title,author_combo,result_left_lbl,result_right_lbl),font=(' ',15,'bold'),bd=3,width=17)
    search_btn.place(relx=.62,rely=.3)
    
def reset(user_entry,pass_entry):
    user_entry.delete(0,END)
    pass_entry.delete(0,END)
    user_entry.focus()

def logout(win,pfrm):
    logout_option=messagebox.askyesno('Logging out','Are you sure You want to logout')
    if logout_option==True:
        pfrm.destroy()
        home_screen(win)
    else:
        pass
def back(win,pfrm):
    welcome_screen(win,pfrm)

def search(win,pfrm):
    pfrm.destroy()
    frm=Frame(win)
    frm.configure(bg='darkslategrey')
    frm.place(x=0,y=125,relwidth=1,relheight=1)

    welcome_lbl=Label(frm,text='Logged in as Admin',font=(' ',20,),fg='powder blue',bg='darkslategrey')
    welcome_lbl.place(relx=0,rely=0)

    logout_btn=Button(frm,text='Logout',command=lambda:logout(win,frm),font=(' ',20,'bold'),bd=3)
    logout_btn.place(relx=.91,rely=0)

    back_btn=Button(frm,text='Back',command=lambda:back(win,frm),font=(' ',20,'bold'),bd=3)
    back_btn.place(relx=0,rely=.1)

    #connection to database library.db to get all titles
    try:
        con=sql.connect(database=db)
        cur=con.cursor()
        cur.execute("select title from book")
        alltitles=cur.fetchall()
        if len(alltitles)==0:
               raise Exception("Sorry")
        unq_titles=set()
        for tup in alltitles:
            unq_titles.add(tup[0])
        con.close()
        
        title_search_lbl=Label(frm,text='Title',bg='darkslategrey',font=(' ',25,'bold'),fg='whitesmoke')
        title_search_lbl.place(relx=.3,rely=.2)

        title_combo=Combobox(frm,font=(' ',18,'bold'),values=list(unq_titles),state="readonly")
        title_combo.current(0)
        title_combo.place(relx=.4,rely=.2)

        result_left_lbl=Label(frm,font=(' ',20,'bold'),bg='darkslategrey',fg='whitesmoke')
        result_left_lbl.place(relx=.3,rely=.4)

        result_right_lbl=Label(frm,font=(' ',17,'bold'),bg='darkslategrey',fg='whitesmoke')
        result_right_lbl.place(relx=.42,rely=.4)
        
        get_author_btn=Button(frm,text='Get Authors List',command=lambda:db_getAuthor(win,frm,title_combo,result_left_lbl,result_right_lbl),font=(' ',15,'bold'),bd=3,width=17)
        get_author_btn.place(relx=.62,rely=.2)

    except:
        messagebox.showerror("Search","No books are added yet in database\nBooks Must be added to database before search")
        back(win,pfrm)

    search_for_books_lbl=Label(frm,text="Books Stock Availability",font=(' ',30,'bold'),bg='darkslategrey',fg='whitesmoke')
    search_for_books_lbl.pack()
    
def book_mgt_screen(win,pfrm):
    pfrm.destroy()
    frm=Frame(win)
    frm.configure(bg='darkslategrey')
    frm.place(x=0,y=125,relwidth=1,relheight=1)

    welcome_lbl=Label(frm,text='Logged in as Admin',font=(' ',20,),fg='powder blue',bg='darkslategrey')
    welcome_lbl.place(relx=0,rely=0)

    logout_btn=Button(frm,text='Logout',command=lambda:logout(win,frm),font=(' ',20,'bold'),bd=3)
    logout_btn.place(relx=.91,rely=0)

    back_btn=Button(frm,text='Back',command=lambda:back(win,frm),font=(' ',20,'bold'),bd=3)
    back_btn.place(relx=0,rely=.1)

    title_lbl=Label(frm,text='Title',bg='darkslategrey',font=(' ',25,'bold'),fg='whitesmoke')
    title_lbl.place(relx=.3,rely=.2)
    
    author_lbl=Label(frm,text='Author',bg='darkslategrey',font=(' ',25,'bold'),fg='whitesmoke')
    author_lbl.place(relx=.3,rely=.28)

    copies_lbl=Label(frm,text='Copies',bg='darkslategrey',font=(' ',25,'bold'),fg='whitesmoke')
    copies_lbl.place(relx=.3,rely=.36)
    
    title_entry=Entry(frm,font=(' ',25,'bold'),bd=3,fg='black')
    title_entry.focus()
    title_entry.place(relx=.40,rely=.2)

    author_entry=Entry(frm,font=(' ',25,'bold'),bd=3,fg='black')
    author_entry.place(relx=.40,rely=.28)

    copies_entry=Entry(frm,font=(' ',25,'bold'),bd=3,fg='black')
    copies_entry.place(relx=.40,rely=.36)

    submit_btn=Button(frm,text='Submit',command=lambda:db_book(win,frm,title_entry,author_entry,copies_entry),font=(' ',20,'bold'),bd=3)
    submit_btn.place(relx=.48,rely=.44)

    search_for_books_lbl=Label(frm,text="Add New Book",font=(' ',30,'bold'),bg='darkslategrey',fg='whitesmoke')
    search_for_books_lbl.pack()

#globAL variable used in function getAuthor
unq_author=set()
def getAuthor(event):
    title=event.widget.get()
    
    #DAtabase connection
    con=sql.connect(database=db)
    cur=con.cursor()
    cur.execute("select author from book where title=?",(title,))
    allauthor=cur.fetchall()
    for tup in allauthor:
        unq_author.add(tup[0])
    con.close()

    author_combo.configure(values=list(unq_author))
    author_combo.current(0)

    return list(unq_author)

def db_allot(win,frm,title_combo,author_combo,student_name_entry,student_roll_entry):
    title=title_combo.get()
    author=author_combo.get()
    stuname=student_name_entry.get()
    sturoll=student_roll_entry.get()
    stuname=stuname.lower()
    
    con=sql.connect(database=db)
    cur=con.cursor()
    cur.execute("select studentname from allotment where studentroll=? and author=? and title=?",(sturoll,author,title))
    name_db=cur.fetchall()
    if len(name_db)==1:
        messagebox.showwarning('Same Book already alloted','same book can not be alloted to a student only once')
        student_name_entry.delete(0,END)
        student_roll_entry.delete(0,END)
        student_name_entry.focus()
        return 0
    con.close()
    
    if len(title)==0 or len(author)==0 or len(stuname)==0 or len(sturoll)==0:
        messagebox.showwarning('Book Allotment','Fields cannot be empty')
    else:
        con=sql.connect(database=db)
        cur=con.cursor()
        cur.execute("select studentname from allotment where studentroll=?",(sturoll,))
        tup=cur.fetchall()
        if len(tup)>=3:
            messagebox.showinfo('Allotment',"Book allotment is exceeded to this Student")
            student_name_entry
            student_roll_entry.delete(0,END)
        else:
            #connection to database library.db to update left copies in table book
            #and insert allotment table entry
            con=sql.connect(database=db)
            cur=con.cursor()
            cur.execute("select left_copies from book where title=? and author=?",(title,author))
            tup=cur.fetchone()
            left_copies=tup[0]
            if(left_copies>0):
                cur.execute("insert into allotment values(?,?,?,?)",(title,author,stuname,sturoll))
                cur.execute("update book set left_copies=left_copies-1 where title=? and author=?",(title,author))
                con.commit()
                messagebox.showinfo('Allotment',"Book is Alloted")
            else:
                messagebox.showarning('Allotment',"Book is not availabe")
            con.close()
  
def allotment_screen(win,pfrm):
    pfrm.destroy()
    frm=Frame(win)
    frm.configure(bg='darkslategrey')
    frm.place(x=0,y=125,relwidth=1,relheight=1)

    welcome_lbl=Label(frm,text='Logged in as Admin',font=(' ',20,),fg='powder blue',bg='darkslategrey')
    welcome_lbl.place(relx=0,rely=0)

    logout_btn=Button(frm,text='Logout',command=lambda:logout(win,frm),font=(' ',20,'bold'),bd=3)
    logout_btn.place(relx=.91,rely=0)

    back_btn=Button(frm,text='Back',command=lambda:back(win,frm),font=(' ',20,'bold'),bd=3)
    back_btn.place(relx=0,rely=.1)

    title_lbl=Label(frm,text='Title',bg='darkslategrey',font=(' ',25,'bold'),fg='whitesmoke')
    title_lbl.place(relx=.25,rely=.2)

    #connection to database library.db to get all tiles
    con=sql.connect(database=db)
    cur=con.cursor()
    cur.execute("select title from book")
    alltitles=cur.fetchall()
    if len(alltitles)==0:
        con.close()
        messagebox.showerror("Search","No books are added yet in database\nBooks Must be added to database before Allotment")
        back(win,pfrm)
        
    else:
        unq_titles=set()
        for tup in alltitles:
            unq_titles.add(tup[0])
        con.close()
        title_combo=Combobox(frm,font=(' ',18,'bold'),values=list(unq_titles),state="readonly")
        title_combo.place(relx=.45,rely=.2)
        title_combo.current(0)

        title_combo.bind("<<ComboboxSelected>>",getAuthor)

        
        author_lbl=Label(frm,text='Author',bg='darkslategrey',font=(' ',25,'bold'),fg='whitesmoke')
        author_lbl.place(relx=.25,rely=.28)

        global author_combo
        author_combo=Combobox(frm,font=(' ',18,'bold'),value=list(unq_author),state="readonly")
        author_combo.place(relx=.45,rely=.28)

        student_name_lbl=Label(frm,text='Student name',bg='darkslategrey',font=(' ',25,'bold'),fg='whitesmoke')
        student_name_lbl.place(relx=.25,rely=.36)

        global student_name_entry 
        student_name_entry=Entry(frm,font=(' ',25,'bold'),bd=3,fg='black')
        student_name_entry.place(relx=.45,rely=.36)

        student_roll_lbl=Label(frm,text='Roll no.',bg='darkslategrey',font=(' ',25,'bold'),fg='whitesmoke')
        student_roll_lbl.place(relx=.25,rely=.44)

        global student_roll_entry
        student_roll_entry=Entry(frm,font=(' ',25,'bold'),bd=3,fg='black')
        student_roll_entry.place(relx=.45,rely=.44)

        allot_btn=Button(frm,text='Allot',command=lambda:db_allot(win,frm,title_combo,author_combo,student_name_entry,student_roll_entry),font=(' ',22,'bold'),bd=3,width=8)
        allot_btn.place(relx=.5,rely=.52)
    
##        messagebox.showerror("Search","No books are added yet in database\nBooks Must be added to database before Allotment")
##        back(win,pfrm)
##        

    search_for_books_lbl=Label(frm,text="Books Allotment",font=(' ',30,'bold'),bg='darkslategrey',fg='whitesmoke')
    search_for_books_lbl.pack()

title=list()
author=list()
def getBookTitle(event):
    sturoll=event.widget.get()
    con=sql.connect(database=db)
    cur=con.cursor()
    cur.execute("select title from allotment where studentroll=?",(sturoll,))
    tup=cur.fetchall()
    con.close()
    title_set=set()
    for t in tup:
        title_set.add(t[0])
    title=list(title_set)

    con=sql.connect(database=db)
    cur=con.cursor()
    cur.execute("select author from allotment where studentroll=?",(sturoll,))
    tupple=cur.fetchall()
    author_set=set()
    for a in tupple:
        author_set.add(a[0])
    con.close()
    author=list(author_set)
    
    book_title_combobox.configure(values=title)
    book_title_combobox.current(0)

    book_author_combobox.configure(values=author)
    book_author_combobox.current(0)
rolls=list()    
def getStudentRoll(event):
    stuname=student_name_entry.get()
    con=sql.connect(database=db)
    cur=con.cursor()
    cur.execute("select studentroll from allotment where studentname=?",(stuname,))
    tup=cur.fetchall()
    con.close()
    if tup==[]:
        messagebox.showerror("Book allotment","Empty Field or No record found\nCheck Student name...")
        student_name_entry.focus()
        return 0
    else:
        rolls=set(tup)
        student_roll_combobox.configure(values=list(rolls))
        student_roll_combobox.current(0)
        
def book_refund(win,frm,student_name_entry,student_roll_combobox,book_title_combobox,book_author_combobox):
    stuname=student_name_entry.get()
    sturoll=student_roll_combobox.get()
    book_title=book_title_combobox.get()
    book_author=book_author_combobox.get()

    con=sql.connect(database=db)
    cur=con.cursor()
    cur.execute("select studentroll from allotment where studentname=? and title=? and author=?",(stuname,book_title,book_author))
    all_roll=cur.fetchall()
    con.close()
    all_roll_list=[]
    for t in all_roll:
        all_roll_list.append(t[0])
    if len(stuname)==0:
        return 0    
    elif len(sturoll)==0:
        messagebox.showwarning("Refund","Roll no. details cannot be empty")
    elif len(book_title)==0:
        messagebox.showwarning("Refund","Book title field cannot be empty")
    elif len(book_author)==0:
        messagebox.showwarning("Refund","Author of book cannot be empty")
    else:
        con=sql.connect(database=db)
        cur=con.cursor()
        cur.execute("delete from allotment where studentname=? and studentroll=? and title=? and author=?",(stuname,sturoll,book_title,book_author))
        con.commit()
        con.close()
        
        con=sql.connect(database=db)
        cur=con.cursor()
        cur.execute("update book set left_copies=left_copies+1 where title=? and author=?",(book_title,book_author))
        con.commit()
        con.close()
        
        messagebox.showinfo("Refund","Refund of book is successfully completed")

        student_name_entry.delete(0,END)
        student_name_entry.focus()
        refund_screen(win,frm)
    
def refund_screen(win,pfrm):
    pfrm.destroy()
    frm=Frame(win)
    frm.configure(bg='darkslategrey')
    frm.place(x=0,y=125,relwidth=1,relheight=1)

    welcome_lbl=Label(frm,text='Logged in as Admin',font=(' ',20,),fg='powder blue',bg='darkslategrey')
    welcome_lbl.place(relx=0,rely=0)

    logout_btn=Button(frm,text='Logout',command=lambda:logout(win,frm),font=(' ',20,'bold'),bd=3)
    logout_btn.place(relx=.91,rely=0)

    back_btn=Button(frm,text='Back',command=lambda:back(win,frm),font=(' ',20,'bold'),bd=3)
    back_btn.place(relx=0,rely=.1)

    #student name
    student_name_lbl=Label(frm,text='Student Name',bg='darkslategrey',font=(' ',25,'bold'),fg='whitesmoke')
    student_name_lbl.place(relx=.2,rely=.2)
    global student_name_entry
    student_name_entry=Entry(frm,font=('calibri',25,'italic'),bd=3,fg='grey')
    student_name_entry.insert(0,"Enter Student's name here ")
    student_name_entry.place(relx=.45,rely=.2)
    def getclear(event):
        student_name_entry.delete(0,END)
        student_name_entry.configure(font=(' ',25,'bold'),bd=3,fg='black')
    student_name_entry.bind("<FocusIn>",getclear)
    
    student_name_entry.bind("<FocusOut>",getStudentRoll)

    #student roll number
    student_roll_lbl=Label(frm,text='Student Roll No',bg='darkslategrey',font=(' ',25,'bold'),fg='whitesmoke')
    student_roll_lbl.place(relx=.2,rely=.3)

    
    global student_roll_combobox
    student_roll_combobox=Combobox(frm,font=(' ',25,'bold'),value=list(rolls),state="readonly")
    student_roll_combobox.place(relx=.45,rely=.3)

    title_lbl=Label(frm,text='Title of book',bg='darkslategrey',font=(' ',25,'bold'),fg='whitesmoke')
    title_lbl.place(relx=.2,rely=.4)

    student_roll_combobox.bind("<<ComboboxSelected>>",getBookTitle)

    global book_title_combobox
    book_title_combobox=Combobox(frm,font=(' ',25,'bold'),value=title,state="readonly")
    book_title_combobox.place(relx=.45,rely=.4)

    author_lbl=Label(frm,text='Author of book',bg='darkslategrey',font=(' ',25,'bold'),fg='whitesmoke')
    author_lbl.place(relx=.2,rely=.5)

    global book_author_combobox
    book_author_combobox=Combobox(frm,font=(' ',25,'bold'),value=author,state="readonly")
    book_author_combobox.place(relx=.45,rely=.5)

    book_refund_btn=Button(frm,text='Refund',command=lambda:book_refund(win,frm,student_name_entry,student_roll_combobox,book_title_combobox,book_author_combobox),font=(' ',20,'bold'),bd=3)
    book_refund_btn.place(relx=.48,rely=.6)

    search_for_books_lbl=Label(frm,text="Refund for Books",font=(' ',30,'bold'),bg='darkslategrey',fg='whitesmoke')
    search_for_books_lbl.pack()

def home_screen(win):
    frm=Frame(win)
    frm.configure(bg='darkslategrey')
    frm.place(x=0,y=125,relwidth=1,relheight=1)
    
    user_lbl=Label(frm,text='Username',bg='darkslategrey',font=(' ',25,'bold'),fg='whitesmoke')
    user_lbl.place(relx=.3,rely=.2)
    
    pass_lbl=Label(frm,text='Password',bg='darkslategrey',font=(' ',25,'bold'),fg='whitesmoke')
    pass_lbl.place(relx=.3,rely=.28)

    user_entry=Entry(frm,font=(' ',25,'bold'),bd=3,fg='black')
    user_entry.focus()
    user_entry.place(relx=.43,rely=.2)

    pass_entry=Entry(frm,font=(' ',25,'bold'),bd=3,fg='black',show='*')
    pass_entry.place(relx=.43,rely=.28)

    login_btn=Button(frm,text='Login',command=lambda:login(user_entry,pass_entry,frm),font=(' ',20,'bold'),bd=3)
    login_btn.place(relx=.45,rely=.38)
    
    reset_btn=Button(frm,text='Reset',command=lambda:reset(user_entry,pass_entry),font=(' ',20,'bold'),bd=3)
    reset_btn.place(relx=.55,rely=.38)
    
def welcome_screen(win,pfrm):
    pfrm.destroy()
    frm=Frame(win)
    frm.configure(bg='darkslategrey')
    frm.place(x=0,y=125,relwidth=1,relheight=1)

    welcome_lbl=Label(frm,text='Logged in as Admin',font=(' ',20,),fg='powder blue',bg='darkslategrey')
    welcome_lbl.place(relx=0,rely=0)

    logout_btn=Button(frm,text='Logout',command=lambda:logout(win,frm),font=(' ',20,'bold'),bd=3)
    logout_btn.place(relx=.91,rely=0)

    book_management_btn=Button(frm,text='Book Management',command=lambda:book_mgt_screen(win,frm),font=(' ',25,'bold'),bd=3,width=18)
    book_management_btn.place(relx=.4,rely=.2)

    allot_btn=Button(frm,text='Book Allotment',command=lambda:allotment_screen(win,frm),font=(' ',25,'bold'),bd=3,width=18)
    allot_btn.place(relx=.4,rely=.3)

    search_btn=Button(frm,text='Search',command=lambda:search(win,frm),font=(' ',25,'bold'),bd=3,width=18)
    search_btn.place(relx=.4,rely=.5)

    refund_btn=Button(frm,text='Refund book',command=lambda:refund_screen(win,frm),font=(' ',25,'bold'),bd=3,width=18)
    refund_btn.place(relx=.4,rely=.4)

home_screen(win)
win.mainloop()
