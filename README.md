# student-planner


#### queries:
- select assignment_name from assignments join tasks on tasks.assignmentid = assignments.assignment_id where tasks.courseid = 1;
- select tasks.task_id, exams.exam_name, courses.course_name from exams join tasks join courses where tasks.examid = exams.exam_id and exams.courseid = courses.course_id
 and tasks.task_name = "study";
- select users.name, projects.project_name, tasks.task_name from users join tasks join projects where users.user_id = tasks.userid and tasks.projectid = projects.project
_id and projects.project_name = "random website";
- select users.name, projects.project_name, tasks.task_name from users join tasks join projects where users.user_id = tasks.userid and tasks.projectid = projects.project
_id and projects.project_name = "random website" group by users.name;
- select user_id, name, email from users where email like '%@gmail.com';

#### instructions/notes
- went entering a query in the query search bar, you have to take out the semicolon
- after you enter a query (in the query search bar) it's going to print in the terminal. every else (updating,deleting,insert) will populate in the table
- when you're updating (after clicking/selecting a row) for integer values please put a 0 (which is a equivalent to a NULL) and for string value enter an empty string (" ")


#### references:
- https://www.python4networkengineers.com/posts/python-intermediate/create_a_tkinter_gui_with_sqlite_backend/
- https://www.tutorialspoint.com/python3/python_gui_programming.htm
