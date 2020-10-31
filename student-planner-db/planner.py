import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    # finally:
    #     if conn:
    #         conn.close()

    return conn

def exit():
    return conn.close()

#-----------------------------------------------------------------

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

#-----------------------------------------------------------------

def create_user(conn, user):
    """
    create a new user into users table
    :param conn:
    :param user:
    :return: user id
    """
    sql = ''' INSERT INTO users(name,email)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()
    return cur.lastrowid


#create a task..i.e. studying,do HW, project, etc..in tasks table
def create_task(conn, task):
    """
    Create a new task into tasks table
    :param conn:
    :param task:
    :return:
    """
    sql = ''' INSERT INTO tasks(task_name,priority,userid,courseid,assignmentid,examid,projectid)
              VALUES(?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()
    return cur.lastrowid

def create_assignment(conn, assignment):
    """
    Create a new task into assignments table
    :param conn:
    :param assignment:
    :return:
    """
    sql = ''' INSERT INTO assignments(assignment_name,start_date,end_date,length)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, assignment)
    conn.commit()
    return cur.lastrowid


def create_exam(conn, exam):
    """
    Create a new exam into exams table
    :param conn:
    :param exam:
    :return:
    """
    sql = ''' INSERT INTO exams(exam_name,exam_date,courseid)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, exam)
    conn.commit()
    return cur.lastrowid

def create_projects(conn, project):
    """
    Create a new project into projects table
    :param conn:
    :param project:
    :return:
    """
    sql = ''' INSERT INTO projects(project_name,start_date,end_date, length,courseid)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    return cur.lastrowid

def create_course(conn, course):
    """
    Create a new course into courses table
    :param conn:
    :param course:
    :return:
    """
    #include professor?????
    sql = ''' INSERT INTO courses(course_name,major,start_time,end_time,length,dayOne,dayTwo)
              VALUES(?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, course)
    conn.commit()
    return cur.lastrowid

def delete_user(conn, user_id):
    """
    Delete a task by user id
    :param conn:  Connection to the SQLite database
    :param id: id of the task
    :return:
    """
    sql = 'DELETE FROM users WHERE user_id=?'
    cur = conn.cursor()
    cur.execute(sql, (user_id,))
    conn.commit()

def delete_task(conn, task_id):
    """
    Delete a task by task id
    :param conn:  Connection to the SQLite database
    :param id: id of the task
    :return:
    """
    sql = 'DELETE FROM tasks WHERE task_id=?'
    cur = conn.cursor()
    cur.execute(sql, (task_id,))
    conn.commit()

def delete_assignment(conn, assignment_id):
    """
    Delete a task by task id
    :param conn:  Connection to the SQLite database
    :param id: id of the task
    :return:
    """
    sql = 'DELETE FROM assignments WHERE assignment_id=?'
    cur = conn.cursor()
    cur.execute(sql, (assignment_id,))
    conn.commit()

def delete_exam(conn, exam_id):
    """
    Delete a task by task id
    :param conn:  Connection to the SQLite database
    :param id: id of the task
    :return:
    """
    sql = 'DELETE FROM exams WHERE exam_id=?'
    cur = conn.cursor()
    cur.execute(sql, (exam_id,))
    conn.commit()

def delete_project(conn, project_id):
    """
    Delete a task by task id
    :param conn:  Connection to the SQLite database
    :param id: id of the task
    :return:
    """
    sql = 'DELETE FROM projects WHERE project_id=?'
    cur = conn.cursor()
    cur.execute(sql, (project_id,))
    conn.commit()

def delete_course(conn, course_id):
    """
    Delete a task by task id
    :param conn:  Connection to the SQLite database
    :param id: id of the task
    :return:
    """
    sql = 'DELETE FROM courses WHERE course_id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()


def delete_all_tasks(conn):
    """
    Delete all rows in the tasks table
    :param conn: Connection to the SQLite database
    :return:
    """
    sql = 'DELETE FROM tasks'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()


def main():
    database = r"/Users/gabbypinto/Desktop/student-planner-db/pinto_schema.db"

#creating tables....
# '''
    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                        user_id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        email text NOT NULL,
                                        unique(name,email)
                                    ); """

    sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
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
                                );"""


    sql_create_assignments_table = """CREATE TABLE IF NOT EXISTS assignments (
                                    assignment_id integer PRIMARY KEY,
                                    assignment_name text NOT NULL,
                                    start_date text,
                                    end_date text,
                                    length integer
                                );"""

    sql_create_exams_table = """CREATE TABLE IF NOT EXISTS exams (
                                    exam_id integer PRIMARY KEY,
                                    exam_name text NOT NULL,
                                    exam_date text,
                                    courseid integer,
                                    FOREIGN KEY (courseid) REFERENCES courses (course_id)
                                );"""

    sql_create_projects_table = """CREATE TABLE IF NOT EXISTS projects (
                                    project_id integer PRIMARY KEY,
                                    project_name text NOT NULL,
                                    start_date text,
                                    end_date text,
                                    length integer,
                                    courseid integer,
                                    FOREIGN KEY (courseid) REFERENCES courses (course_id)
                                );"""

    sql_create_courses_table = """CREATE TABLE IF NOT EXISTS courses (
                                    course_id integer PRIMARY KEY,
                                    course_name text NOT NULL,
                                    major text,
                                    start_time text,
                                    end_time text,
                                    length integer,
                                    dayOne text NOT NULL,
                                    dayTwo text,
                                    unique(course_name,major)
                                );"""
#
    # create a database connection
    conn = create_connection(database)
#
# '''

    if conn is not None:
        #create users table
        # create_table(conn, sql_create_users_table)
        #
        # # create tasks table
        #
        # create_table(conn, sql_create_tasks_table)
        #
        # # create assignments table
        # create_table(conn, sql_create_assignments_table)
        #
        # #create exams table
        # create_table(conn, sql_create_exams_table)
        #
        # #create projects table
        # create_table(conn,sql_create_projects_table)
        #
        # #create courses table
        # create_table(conn,sql_create_courses_table)


        #add a prof attribute for courses table
        #only include courseid once (in the task table)??

        # create users
        # user1 = ('Gabby Pinto', 'pinto@chapman.edu')
        # user_id = create_user(conn,user1)
        #
        # #create an assignment
        # assignment_1 = ("Online Problem Set","10-1","10-7",7)
        # create_assignment(conn,assignment_1)
        #
        # #create course
        # course_1 = ("Database Management","CPSC","11:30","12:45",1.25,"Tuesday","Thursday")
        # create_course(conn,course_1)
        # course_2 = ("Operating Systems","CPSC","4:00","5:15",1.25,"Monday","Wednesday")
        # create_course(conn,course_2)
        #
        # create a task
        # task_1 = ('study',None,None,None,None,None,None )
        # create_task(conn,task_1)
        #
        # #create a project
        # project_1 = ("SQLite Project","10-23","11-03",14,1)
        # create_projects(conn,project_1)
        # #create exam
        # exam_1 = ("OS Exam","10-24",2)
        # create_exam(conn,exam_1)


        #delete_task(conn,1);
        delete_assignment(conn,1)
        # delete_all_tasks(conn);
    else:
         print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()
