import sqlite3
import string
db_conn = sqlite3.connect('bookings.db')
db = db_conn.cursor()
def create_table(table_name: str, **kwargs): # Pass colums as [COLUMN_NAME]=[DATA_TYPE]
    db.execute(f"""CREATE TABLE IF NOT EXISTS {table_name}(
            id INTEGER PRIMARY KEY
        )""")
    try:
        for name, type in kwargs.items():
            db.execute(f"""ALTER TABLE {table_name}
                        ADD {name} {type};""")
    except:
        raise Exception("Error")
        
create_table("venue",  name="VARCHAR(50)", guests="INTEGER", time="TIME", date="DATE")

guests = input("Enter number of guests: ")
if not guests.isdigit():
    raise TypeError("Guests must be a number")
guests = int(guests)
name = input("Enter name: ")

NUMBERS = set(string.digits)
SPECIAL_CHARS = set(string.punctuation) # Includes !@#$%^&*()-=_+[]{}|;:'",.<>/?`~
WHITESPACE = set(string.whitespace)
for char in name:
    if char in NUMBERS or char in SPECIAL_CHARS or char in WHITESPACE:
        raise ValueError("Name must not contain numbers, special characters, or whitespace")
    
time = input("Enter time in 24-hr format(HH:MM): ")
for char in time:
    if char not in string.digits and char != ':':
        raise ValueError("Time must be in HH:MM format with digits and colon only")
time = time.strip() if ":00" in time else time.strip() + ":00" # Append seconds to match TIME format in SQLite
