"""CREATE TABLE IF NOT EXISTS projects (
                                project_id integer PRIMARY KEY,
                                project_name text NOT NULL,
                                start_date text,
                                end_date text,
                                length integer,
                                courseid integer,
                                FOREIGN KEY (courseid) REFERENCES courses (course_id)
                            );""")
