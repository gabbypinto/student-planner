""" CREATE TABLE IF NOT EXISTS users (
                                user_id integer PRIMARY KEY,
                                name text NOT NULL,
                                email text NOT NULL,
                                unique(name,email)
                            );""")
