#database
import sqlite3
from sqlite3 import Error

from tkinter import *
from tkinter.ttk import Treeview



class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        #create users tablle
        self.cur.execute(""" CREATE TABLE IF NOT EXISTS users (
                                        user_id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        email text NOT NULL,
                                        unique(name,email)
                                    );""")
        #create tasks table
        self.cur.execute("""CREATE TABLE IF NOT EXISTS tasks (
                                        task_id integer PRIMARY KEY,
                                        task_name text NOT NULL,
                                        priority integer,
                                        userid integer,
                                        courseid integer,
                                        assignmentid integer,
                                        examid integer,
                                        projectid integer,
                                        FOREIGN KEY (userid) REFERENCES users (user_id),
                                        FOREIGN KEY (courseid) REFERENCES courses (course_id),
                                        FOREIGN KEY (assignmentid) REFERENCES assignments (assignment_id),
                                        FOREIGN KEY (examid) REFERENCES exams(exam_id),
                                        FOREIGN KEY (projectid) REFERENCES projects(project_id)
                                    );""")

        #create assignments table
        self.cur.execute("""CREATE TABLE IF NOT EXISTS assignments (
                                        assignment_id integer PRIMARY KEY,
                                        assignment_name text NOT NULL,
                                        start_date text,
                                        end_date text,
                                        length integer
                                    );""")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS exams (
                                        exam_id integer PRIMARY KEY,
                                        exam_name text NOT NULL,
                                        exam_date text,
                                        courseid integer,
                                        FOREIGN KEY (courseid) REFERENCES courses (course_id)
                                    );""")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS projects (
                                        project_id integer PRIMARY KEY,
                                        project_name text NOT NULL,
                                        start_date text,
                                        end_date text,
                                        length integer,
                                        courseid integer,
                                        FOREIGN KEY (courseid) REFERENCES courses (course_id)
                                    );""")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS courses (
                                        course_id integer PRIMARY KEY,
                                        course_name text NOT NULL,
                                        major text,
                                        start_time text,
                                        end_time text,
                                        length integer,
                                        dayOne text NOT NULL,
                                        dayTwo text,
                                        unique(course_name,major)
                                    );""")
        self.conn.commit()


    def search_by_query(self, query):
        self.cur.execute(query)
        rows = self.cur.fetchall()
        print(rows)
        return rows

    def insert_user(self, name,email):
        self.cur.execute("INSERT INTO users VALUES (NULL, ?, ?)",
                         (name,email))
        self.conn.commit()

    def delete_user(self, user_id):
        self.cur.execute("DELETE FROM users WHERE user_id=?", (user_id,))
        self.conn.commit()

    def update_user(self, user_id, name, email):
        self.cur.execute("UPDATE users SET name = ?, email = ? WHERE user_id = ?",
                         (name,email,user_id))
        self.conn.commit()

    def __del__(self):
        self.conn.close()



def main():
    database = r"/Users/gabbypinto/Desktop/student-planner-db/pinto_schema.db"
    # create a database connection
    db =  Database(database)

    #action buttons..
    #populate the entire users table--populate list 2
    def populate_list(query='select * from users'):
        for i in users_tree_view.get_children():
            users_tree_view.delete(i)
        for row in db.search_by_query(query):
            users_tree_view.insert('','end',values=row)
    #add a user  -- add router
    def add_user():
        if username_text.get() == '' or email_text.get() == '':
            messagebox.showerror('Required Fields','Please include all fields')
            return
        db.insert_user(username_text.get(),email_text.get())
        clear_text()
        populate_list()
    #select a user --select_router
    def select_user(event):
        try:
            global selected_item
            index = users_tree_view.selection()[0]
            selected_item = users_tree_view.item(index)['values']
            username_entry.delete(0,END)
            username_entry.insert(END,selected_item[1])
            email_entry.delete(0,END)
            email_entry.insert(END,selected_item[2])
        except IndexError:
            pass
    #remove a user
    def remove_user():
        db.delete_user(selected_item[0])
        clear_text()
        populate_list()
    #update a user
    def update_user():
        db.update(selected_item[0],username_text.get(),email_text.get())
        populate_list()
    #clear text when user is deleted
    def clear_text():
        username_entry.delete(0,END)
        email_entry.delete(0,END)
    #execute the query which calls the first fxn (populate list 2)...execute_query
    def execute_query():
        query = query_search.get()
        populate_list(query)


    app = Tk()

    frame_search = Frame(app)
    #search by query grid
    frame_search.grid(row=0,column=0)
    lbl_search = Label(frame_search,text='Search by query',font=('bold',12),pady=20)
    lbl_search.grid(row=0,column=0,sticky=W)
    query_search = StringVar()
    query_search_entry= Entry(frame_search,textvariable=query_search,width=40)
    query_search_entry.grid(row=0,column=1)

    #fields/attributes for the users table
    frame_fields = Frame(app)
    frame_fields.grid(row=1,column=0)
    #name
    username_text = StringVar()
    username_label = Label(frame_fields,text='name',font=('bold',12))
    username_label.grid(row=0,column=0,sticky=E)
    username_entry = Entry(frame_fields, textvariable=username_text)
    username_entry.grid(row=0,column=1,sticky=W)
    #email
    email_text = StringVar()
    email_label = Label(frame_fields,text='email',font=('bold',12))
    email_label.grid(row=0,column=2,sticky=E)
    email_entry = Entry(frame_fields, textvariable=email_text)
    email_entry.grid(row=0,column=3,sticky=W)


    #users table frame
    frame_users = Frame(app)
    frame_users.grid(row=4,column=0,columnspan=4,rowspan=6,pady=20,padx=20)
    columns = ['id','name','email']
    users_tree_view = Treeview(frame_users,columns=columns,show="headings")
    users_tree_view.column("id",width=30)
    for col in columns[1:]:
        users_tree_view.column(col,width=200)
        users_tree_view.heading(col,text=col)
    users_tree_view.bind('<<TreeviewSelect>>',select_user)  #create select user!
    users_tree_view.pack(side="left",fill="y")
    scrollbar = Scrollbar(frame_users,orient='vertical')
    scrollbar.configure(command=users_tree_view.yview)
    scrollbar.pack(side="right",fill="y")
    users_tree_view.config(yscrollcommand=scrollbar.set)


    #action buttons
    frame_btns = Frame(app)
    frame_btns.grid(row=3,column=0)

    #add buttons
    add_btn = Button(frame_btns,text='Add User',width=12,command=add_user)
    add_btn.grid(row=0,column=0,pady=20)

    #remove button
    remove_btn = Button(frame_btns,text='Remove User',width=12,command=remove_user)
    remove_btn.grid(row=0,column=1)

    #update button
    update_btn = Button(frame_btns,text='Update User',width=12,command=update_user)
    update_btn.grid(row=0,column=2)

    #clear button
    clear_btn = Button(frame_btns,text='Clear Input',width=12,command=clear_text)
    clear_btn.grid(row=0,column=3)

    #search button
    search_query_btn = Button(frame_search,text='Search Query',width=12,command=execute_query)
    search_query_btn.grid(row=0,column=2)

    app.title('Student Planner')
    app.geometry('900x750')

    #Populate user data
    populate_list()
    # Start program
    app.mainloop()

    # db.insert_user('gabby','gabrielapintogp@gmail.com')
    # db.update_user(1,'gabby','pinto@chapman.edu')
    # db.insert_user('erik','linstead@chapman.edu')
    # db.insert_user('tommy','springer@chapman.edu')
    # db.insert_user('kurz','kurz@chapman.edu')
    # db.delete_user(1)

    # db.search_by_query("select * from users where email like '% @chapman.edu'; ")
    db.search_by_query("select * from users where email like '%.edu'; ")

if __name__ == '__main__':
    main()
