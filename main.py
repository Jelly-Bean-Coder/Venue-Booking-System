import sqlite3
db_conn = sqlite3.connect('bookings.db')
db = db_conn.cursor()
def create_table(table_name: str, **kwargs): # Pass colums as [COLUMN_NAME]=[DATA_TYPE]
    db.execute(f"""CREATE TABLE IF NOT EXISTS {table_name}(
            id INTEGER PRIMARY KEY
        )""")
    for name, type in kwargs.items():
        db.execute(f"""ALTER TABLE {table_name}
                    ADD {name} {type};""")