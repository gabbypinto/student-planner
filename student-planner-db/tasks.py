"""CREATE TABLE IF NOT EXISTS tasks (
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
