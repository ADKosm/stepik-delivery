import sqlite3

connection = sqlite3.connect("test.db")

c = connection.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS tests (
    id integer PRIMARY KEY,
    test_int integer,
    test_text text
)
""")

c.execute("""
INSERT INTO tests VALUES (1, 2, "test1")
""")

c.execute("""
INSERT INTO tests VALUES (2, 150, "test2")
""")

c.connection.commit()

for item in c.execute("SELECT * FROM tests"):
    print(item)
