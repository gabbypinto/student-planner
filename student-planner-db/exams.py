"""CREATE TABLE IF NOT EXISTS exams (
                                exam_id integer PRIMARY KEY,
                                exam_name text NOT NULL,
                                exam_date text,
                                courseid integer,
                                FOREIGN KEY (courseid) REFERENCES courses (course_id)
                            );"""
