from tkinter import *
from tkinter import ttk
import sqlite3
from sqlite3 import Error
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

    def insert_task(self, text, priority,userid,courseid,assignmentid,examid,projectid):
        self.cur.execute("INSERT INTO tasks VALUES (NULL, ?, ?, ?, ?, ?, ?,?)",
                         (text, priority,userid,courseid,assignmentid,examid,projectid))
        self.conn.commit()

    def delete_task(self, task_id):
        self.cur.execute("DELETE FROM tasks WHERE task_id=?", (task_id,))
        self.conn.commit()

    def update_task(self, task_id,task_name, priority,userid,courseid,assignmentid,examid,projectid):
        self.cur.execute("UPDATE tasks SET task_name = ?, priority = ?, userid = ?, courseid=?,assignmentid = ?, examid = ?, projectid = ? WHERE task_id = ?",
                         (task_name, priority,userid,courseid,assignmentid,examid,projectid,task_id))
        self.conn.commit()

    #add code here for assignment
    def insert_assignment(self, assignment_name, start_date,end_date,length):
        self.cur.execute("INSERT INTO assignments VALUES (NULL, ?, ?, ?, ?)",
                            (assignment_name, start_date,end_date,length))
        self.conn.commit()

    def delete_assignment(self, assignment_id):
        self.cur.execute("DELETE FROM assignments WHERE assignment_id=?", (assignment_id,))
        self.conn.commit()

    def update_assignment(self, assignment_id,assignment_name, start_date,end_date,length):
        self.cur.execute("UPDATE assignments SET assignment_name = ?, start_date = ?, end_date = ?, length=? WHERE assignment_id = ?",
                             (assignment_name, start_date,end_date,length,assignment_id,))
        self.conn.commit()


    def insert_exam(self, exam_id,exam_name, exam_date,courseid):
        self.cur.execute("INSERT INTO exams VALUES (NULL,?, ?, ?,?)",
                            (exam_name, exam_date,courseid,exam_id))
        self.conn.commit()

    def delete_exam(self, assignment_id):
        self.cur.execute("DELETE FROM exams WHERE exam_id=?", (exam_id,))
        self.conn.commit()

    def update_exam(self,exam_id,exam_name, exam_date,courseid):
        self.cur.execute("UPDATE exams SET exam_name = ?, exam_date = ?, course=? WHERE exam_id = ?",
                             (exam_name, exam_date,courseid,exam_id))
        self.conn.commit()


    def __del__(self):
        self.conn.close()


def main():

    # database = r"/Users/gabbypinto/Desktop/student-planner-db/pinto_schema.db"
    database = "pinto_schema.db"
    # create a database connection
    db =  Database(database)
    # db.insert_user('erik','linstead@chapman.edu')
    # db.insert_user('tommy','springer@chapman.edu')
    # db.insert_user('kurz','kurz@chapman.edu')
    #action buttons..
    #populate the entire users table--populate list 2
    def populate_users_list(query='select * from users'):
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
        populate_users_list()
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
        populate_users_list()
    #update a user
    def update_user():
        db.update_user(selected_item[0],username_text.get(),email_text.get())
        populate_users_list()
    #clear text when user is deleted
    def clear_text():
        username_entry.delete(0,END)
        email_entry.delete(0,END)
    #execute the query which calls the first fxn (populate list 2)...execute_query
    def execute_query():
        query = query_search.get()
        populate_users_list(query)


    #populate tasks list
    def populate_tasks_list(query='select * from tasks'):
        for i in tasks_tree_view.get_children():
            tasks_tree_view.delete(i)
        for row in db.search_by_query(query):
            tasks_tree_view.insert('','end',values=row)
    #add a task
    def add_task():
        if task_text.get() == '' or task_priority.get() == '' or task_userid.get() == '' or task_assignmentid.get() == '' or task_examid.get() == '' or task_projectid.get() == '':
            messagebox.showerror('Required Fields','Please include all fields')
            return
        db.insert_task(task_text.get(), task_priority.get(),task_userid.get(),task_courseid.get(),task_assignmentid.get(),task_examid.get(),task_projectid.get())
        clear_text()
        populate_tasks_list()
    #select a task
    def select_task(event):
        try:
            global selected_item
            index = tasks_tree_view.selection()[0]
            selected_item = tasks_tree_view.item(index)['values']
            task_entry.delete(0,END)
            task_entry.insert(END,selected_item[1])
            task_priority_entry.delete(0,END)
            task_priority_entry.insert(END,selected_item[2])
            task_userid_entry.delete(0,END)
            task_userid_entry.insert(END,selected_item[3])
            task_assignmentid_entry.delete(0,END)
            task_assignmentid_entry.insert(END,selected_item[4])
            task_examid_entry.delete(0,END)
            task_examid_entry.insert(END,selected_item[5])
            task_projectid_entry.delete(0,END)
            task_projectid_entry.insert(END,selected_item[6])
        except IndexError:
            pass
    #remove a task
    def remove_task():
        db.delete_task(selected_item[0])
        clear_tasks_text()
        populate_tasks_list()
    #update a task
    def update_task():
        db.update_task(selected_item[0],task_text.get(), task_priority.get(),task_userid.get(),task_courseid.get(),task_assignmentid.get(),task_examid.get(),task_projectid.get())
        populate_tasks_list()
    #clear text when user is deleted
    def clear_tasks_text():
        task_entry.delete(0,END)
        task_priority_entry.delete(0,END)
        task_userid_entry.delete(0,END)
        task_assignmentid_entry.delete(0,END)
        task_examid_entry.delete(0,END)
        task_projectid_entry.delete(0,END)


    #add a task
    def add_assignment():
        if assignment_text.get() == '' or assignment_start_text.get() == '' or assignment_end_text.get() == '' or assignment_length_text.get() == '':
            messagebox.showerror('Required Fields','Please include all fields')
            return
        db.insert_assignment(assignment_text.get(),assignment_start_text.get(),assignment_end_text.get(),assignment_length_text.get())
        clear_text()
        populate_assignments_list()
    #select a assignment
    def select_assignment(event):
        try:
            global selected_assignment
            index = assignments_tree_view.selection()[0]
            selected_assignment = assignments_tree_view.item(index)['values']
            assignment_entry.delete(0,END)
            assignment_entry.insert(END,selected_assignment[1])
            assignment_start_entry.delete(0,END)
            assignment_start_entry.insert(END,selected_assignment[2])
            assignment_end_entry.delete(0,END)
            assignment_end_entry.insert(END,selected_assignment[3])
            assignment_length_entry.delete(0,END)
            assignment_length_entry.insert(END,selected_assignment[4])
        except IndexError:
            pass
    #remove a user
    def remove_assignment():
        db.delete_assignment(selected_assignment[0])
        clear_assignments_text()
        populate_assignments_list()
    #update a user
    def update_assignment():
        print(selected_assignment[0],assignment_text.get(), assignment_start_text.get(),assignment_end_text.get(),assignment_length_text.get())
        db.update_assignment(selected_assignment[0],assignment_text.get(), assignment_start_text.get(),assignment_end_text.get(),assignment_length_text.get())
        populate_assignments_list()
    #clear text when user is deleted
    def clear_assignments_text():
        assignment_entry.delete(0,END)
        assignment_start_entry.delete(0,END)
        assignment_end_entry.delete(0,END)
        assignment_length_entry.delete(0,END)

    def populate_assignments_list(query='select * from assignments'):
        for i in assignments_tree_view.get_children():
            assignments_tree_view.delete(i)
        for row in db.search_by_query(query):
            assignments_tree_view.insert('','end',values=row)


    #add a task
    def add_exam():
        if exam_text.get() == '' or exam_date_text.get() == '' or courseid_text.get() == '':
            messagebox.showerror('Required Fields','Please include all fields')
            return
        db.insert_exam(exam_text.get(),exam_date_text.get(),courseid_text.get())
        clear_exams_text()
        populate_exams_list()
    #select a assignment
    def select_exam(event):
        try:
            global selected_exam
            index = exams_trees_view.selection()[0]
            selected_exam = assignments_tree_view.item(index)['values']
            exam_entry.delete(0,END)
            exam_entry.insert(END,selected_exam[1])
            exam_date_entry.delete(0,END)
            exam_date_entry.insert(END,selected_exam[2])
            courseid_entry.delete(0,END)
            courseid_entry.insert(END,selected_exam[3])
        except IndexError:
            pass
    #remove a user
    def remove_exam():
        db.delete_exam(selected_exam[0])
        clear_exams_text()
        populate_assignments_list()
    #update a user
    def update_exam():
        db.update_exam(selected_exam[0],exam_text.get(), exam_date_text.get(),courseid_text.get())
        populate_exams_list()
    #clear text when user is deleted
    def clear_exams_text():
        exam_entry.delete(0,END)
        exam_date_entry.delete(0,END)
        courseid_entry.delete(0,END)

    def populate_exams_list(query='select * from exams'):
        for i in exams_tree_view.get_children():
            exams_tree_view.delete(i)
        for row in db.search_by_query(query):
            exams_tree_view.insert('','end',values=row)






    app = Tk()
    #main frame
    main_frame  = Frame(app)
    main_frame.pack(fill=BOTH,expand=1)

    #create canvas
    my_canvas= Canvas(main_frame)
    my_canvas.pack(side=LEFT,fill=BOTH,expand=1)

    #add scrollbar
    my_scrollbar=ttk.Scrollbar(main_frame,orient=VERTICAL,command=my_canvas.yview)
    my_scrollbar.pack(side=RIGHT,fill=Y)

    #configure the Canvas
    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>',lambda e:my_canvas.configure(scrollregion=my_canvas.bbox("all")))

    #create another frame in Canvas
    second_frame = Frame(my_canvas)
    my_canvas.create_window((0,0),window=second_frame,anchor="nw")
    my_canvas.create_window(0,0,window=second_frame)


    # for thing in range(100):
        # Button(second_frame,text=f'Button{thing} Yo!').grid(row=thing,column=0)

    lbl_search = Label(second_frame,text='Search by query',font=('bold',12),pady=20)
    lbl_search.pack(side="left")
    query_search = StringVar()
    query_search_entry= Entry(second_frame,textvariable=query_search,width=40)
    query_search_entry.pack(side="left")

    #create another frame in Canvas
    third_frame = Frame(my_canvas)
    my_canvas.create_window(0,40,window=third_frame)
    # #name
    username_text = StringVar()
    username_label = Label(third_frame,text='name',font=('bold',12))
    username_label.pack(side="left")
    username_entry = Entry(third_frame, textvariable=username_text)
    username_entry.pack(side="left")
    #email
    email_text = StringVar()
    email_label = Label(third_frame,text='email',font=('bold',12))
    email_label.pack(side="left")
    email_entry = Entry(third_frame, textvariable=email_text)
    email_entry.pack(side="left")

    #create another frame in Canvas
    fourth_frame = Frame(my_canvas)
    my_canvas.create_window(10,85,window=fourth_frame)

    #add buttons
    add_btn = Button(fourth_frame,text='Add User',width=12,command=add_user)
    add_btn.pack(side="left")
    #remove button
    remove_btn = Button(fourth_frame,text='Remove User',width=12,command=remove_user)
    remove_btn.pack(side="left")
    #update button
    update_btn = Button(fourth_frame,text='Update User',width=12,command=update_user)
    update_btn.pack(side="left")
    #clear button
    clear_btn = Button(fourth_frame,text='Clear Input',width=12,command=clear_text)
    clear_btn.pack(side="left")
    #search button
    search_query_btn = Button(fourth_frame,text='Search Query',width=12,command=execute_query)
    search_query_btn.pack(side="left")

    fifth_frame = Frame(my_canvas)
    my_canvas.create_window(0,200,window=fifth_frame)
    columns = ['id','name','email']
    users_tree_view = Treeview(fifth_frame,columns=columns,show="headings")
    users_tree_view.column("id",width=30)
    for col in columns[1:]:
        users_tree_view.column(col,width=200)
        users_tree_view.heading(col,text=col)
    users_tree_view.bind('<<TreeviewSelect>>',select_user)  #create select user!
    users_tree_view.pack(side="left",fill="y")
    scrollbar = Scrollbar(fifth_frame,orient='vertical')
    scrollbar.configure(command=users_tree_view.yview)
    scrollbar.pack(side="right",fill="y")
    users_tree_view.config(yscrollcommand=scrollbar.set)

#-------------------------------------------------------------------

    #fields/attributes for the tasks table
    six_frame = Frame(my_canvas)
    my_canvas.create_window(0,400,window=six_frame)
    #task
    task_text = StringVar()
    task_label = Label(six_frame,text='task name',font=('bold',12))
    task_label.pack(side="left")
    task_entry = Entry(six_frame, textvariable=task_text)
    task_entry.pack(side="left")
    #priority
    task_priority = IntVar()
    task_priority_label = Label(six_frame,text='priority',font=('bold',12))
    task_priority_label.pack(side="left")
    task_priority_entry = Entry(six_frame, textvariable=task_priority)
    task_priority_entry.pack(side="left")
    #userid
    task_userid = IntVar()
    task_userid_label = Label(six_frame,text='userid',font=('bold',12))
    task_userid_label.pack(side="left")
    task_userid_entry = Entry(six_frame, textvariable=task_userid)
    task_userid_entry.pack(side="left")
    #courseid
    task_courseid = IntVar()
    task_courseid_label = Label(six_frame,text='courseid',font=('bold',12))
    task_courseid_label.pack(side="left")
    task_courseid_entry = Entry(six_frame, textvariable=task_courseid)
    task_courseid_entry.pack(side="left")


    seven_frame = Frame(my_canvas)
    my_canvas.create_window(0,450,window=seven_frame)
    #assignmentid
    task_assignmentid = IntVar()
    task_assignmentid_label = Label(seven_frame,text='assignmentid',font=('bold',12))
    task_assignmentid_label.pack(side="left")
    task_assignmentid_entry = Entry(seven_frame, textvariable=task_assignmentid)
    task_assignmentid_entry.pack(side="left")
    #examid
    task_examid = IntVar()
    task_examid_label = Label(seven_frame,text='examid',font=('bold',12))
    task_examid_label.pack(side="left")
    task_examid_entry = Entry(seven_frame, textvariable=task_examid)
    task_examid_entry.pack(side="left")
    #projectid
    task_projectid = IntVar()
    task_projectid_label = Label(seven_frame,text='projectid',font=('bold',12))
    task_projectid_label.pack(side="left")
    task_projectid_entry = Entry(seven_frame, textvariable=task_projectid)
    task_projectid_entry.pack(side="left")


    #tasks action buttons
    eight_frame = Frame(my_canvas)
    my_canvas.create_window(0,500,window=eight_frame)
    #add buttons
    add_tasks_btn = Button(eight_frame,text='Add Task',width=12,command=add_task)
    add_tasks_btn.pack(side="left")
    #remove button
    remove_tasks_btn = Button(eight_frame,text='Remove Task',width=12,command=remove_task)
    remove_tasks_btn.pack(side="left")
    #update button
    update_tasks_btn = Button(eight_frame,text='Update Task',width=12,command=update_task)
    update_tasks_btn.pack(side="left")
    #clear button
    clear_tasks_btn = Button(eight_frame,text='Clear Input',width=12,command=clear_text)
    clear_tasks_btn.pack(side="left")

    #tasks table frame
    nine_frame = Frame(my_canvas)
    my_canvas.create_window(0,700,window=nine_frame)
    # frame_tasks.grid(row=45,column=0,columnspan=4,rowspan=6,pady=20,padx=20)
    tasks_columns = ['task_id','task_name','priority','userid','courseid','assignmentid','examid','projectid']
    tasks_tree_view = Treeview(nine_frame,columns=tasks_columns,show="headings")
    tasks_tree_view.column("task_id",width=30)
    for col in tasks_columns[1:]:
        tasks_tree_view.column(col,width=130)
        tasks_tree_view.heading(col,text=col)
    tasks_tree_view.bind('<<TreeviewSelect>>',select_task)  #create select user!
    tasks_tree_view.pack(side="left",fill="y")
    scrollbarTasks = Scrollbar(nine_frame,orient='vertical')
    scrollbarTasks.configure(command=tasks_tree_view.yview)
    scrollbarTasks.pack(side="right",fill="y")
    tasks_tree_view.config(yscrollcommand=scrollbarTasks.set)


#-----------------------------------------------------------------------------------
    #fields/attributes for the assignments table
    ten_frame = Frame(my_canvas)
    my_canvas.create_window(0,850,window=ten_frame)
    #assignment name
    assignment_text = StringVar()
    assignment_label = Label(ten_frame,text='assignment name',font=('bold',12))
    assignment_label.pack(side="left")
    assignment_entry = Entry(ten_frame, textvariable=assignment_text)
    assignment_entry.pack(side="left")
    #start date
    assignment_start_text = StringVar()
    assignment_start_label = Label(ten_frame,text='start date',font=('bold',12))
    assignment_start_label.pack(side="left")
    assignment_start_entry = Entry(ten_frame, textvariable=assignment_start_text)
    assignment_start_entry.pack(side="left")
    #end date
    assignment_end_text = StringVar()
    assignment_end_label = Label(ten_frame,text='end date',font=('bold',12))
    assignment_end_label.pack(side="left")
    assignment_end_entry = Entry(ten_frame, textvariable=assignment_end_text)
    assignment_end_entry.pack(side="left")
#length
    assignment_length_text = IntVar()
    assignment_length_label = Label(ten_frame,text='length',font=('bold',12))
    assignment_length_label.pack(side="left")
    assignment_length_entry = Entry(ten_frame, textvariable=assignment_length_text)
    assignment_length_entry.pack(side="left")

    #assignment action buttons
    assignment_btn_frame = Frame(my_canvas)
    my_canvas.create_window(0,900,window=assignment_btn_frame)
    #add buttons
    add_assignment_btn = Button(assignment_btn_frame,text='Add Assignment',width=12,command=add_assignment)
    add_assignment_btn.pack(side="left")
    #remove button
    remove_assignment_btn = Button(assignment_btn_frame,text='Remove Assignment',width=16,command=remove_assignment)
    remove_assignment_btn.pack(side="left")
    #update button
    update_assignment_btn = Button(assignment_btn_frame,text='Update Assignment',width=16,command=update_assignment)
    update_assignment_btn.pack(side="left")
    #clear button
    clear_assignment_btn = Button(assignment_btn_frame,text='Clear Input',width=12,command=clear_text)
    clear_assignment_btn.pack(side="left")

    #assignments table frame
    eleven_frame = Frame(my_canvas)
    my_canvas.create_window(0,1050,window=eleven_frame)
    assignments_columns = ['assignment_id','assignment_name','start_date','end_date','length']
    assignments_tree_view = Treeview(eleven_frame,columns=assignments_columns,show="headings")
    assignments_tree_view.column("assignment_id",width=30)
    for col in assignments_columns[1:]:
        assignments_tree_view.column(col,width=130)
        assignments_tree_view.heading(col,text=col)
    assignments_tree_view.bind('<<TreeviewSelect>>',select_assignment)  #create select user!
    assignments_tree_view.pack(side="left",fill="y")
    scrollbarAssignments = Scrollbar(eleven_frame,orient='vertical')
    scrollbarAssignments.configure(command=assignments_tree_view.yview)
    scrollbarAssignments.pack(side="right",fill="y")
    assignments_tree_view.config(yscrollcommand=scrollbarAssignments.set)

#-----------------------------------------------------------------------------------
    #fields/attributes for the assignments table
    exam_frame = Frame(my_canvas)
    my_canvas.create_window(0,1200,window=exam_frame)
    #exam name
    exam_text = StringVar()
    exam_label = Label(exam_frame,text='exam',font=('bold',12))
    exam_label.pack(side="left")
    exam_entry = Entry(exam_frame, textvariable=exam_text)
    exam_entry.pack(side="left")
    #exam date
    exam_date_text = StringVar()
    exam_date_label = Label(exam_frame,text='exam date',font=('bold',12))
    exam_date_label.pack(side="left")
    exam_date_entry = Entry(exam_frame, textvariable=exam_date_text)
    exam_date_entry.pack(side="left")
    #course id
    courseid_text = IntVar()
    courseid_label = Label(exam_frame,text='course id',font=('bold',12))
    courseid_label.pack(side="left")
    courseid_entry = Entry(exam_frame, textvariable=courseid_text)
    courseid_entry.pack(side="left")


    #assignment action buttons
    exam_btn_frame = Frame(my_canvas)
    my_canvas.create_window(0,1250,window=exam_btn_frame)
    #add buttons
    add_exam_btn = Button(exam_btn_frame,text='Add Exam',width=12,command=add_exam)
    add_exam_btn.pack(side="left")
    #remove button
    remove_exam_btn = Button(exam_btn_frame,text='Remove Exam',width=16,command=remove_exam)
    remove_exam_btn.pack(side="left")
    #update button
    update_exam_btn = Button(exam_btn_frame,text='Update Exam',width=16,command=update_exam)
    update_exam_btn.pack(side="left")
    #clear button
    clear_exam_btn = Button(exam_btn_frame,text='Clear Input',width=12,command=clear_exams_text)
    clear_exam_btn.pack(side="left")

    #assignments table frame
    exam_table_frame = Frame(my_canvas)
    my_canvas.create_window(0,1400,window=exam_table_frame)
    exam_columns = ['exam id','exam','exam date','course id']
    exams_tree_view = Treeview(exam_table_frame,columns=exam_columns,show="headings")
    exams_tree_view.column("exam id",width=30)
    for col in exam_columns[1:]:
        exams_tree_view.column(col,width=130)
        exams_tree_view.heading(col,text=col)
    exams_tree_view.bind('<<TreeviewSelect>>',select_exam)
    exams_tree_view.pack(side="left",fill="y")
    scrollbarExams = Scrollbar(exam_table_frame,orient='vertical')
    scrollbarExams.configure(command=exams_tree_view.yview)
    scrollbarExams.pack(side="right",fill="y")
    exams_tree_view.config(yscrollcommand=scrollbarExams.set)


    app.title('Student Planner')
    app.geometry('1000x800')

    populate_users_list()
    populate_tasks_list()
    populate_assignments_list()
    populate_exams_list()

    app.mainloop()
if __name__== '__main__':
    main()
