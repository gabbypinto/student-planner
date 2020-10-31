"""CREATE TABLE IF NOT EXISTS courses (
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
