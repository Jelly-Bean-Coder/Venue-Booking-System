import sqlite3
import string
import time
import datetime

db_conn = sqlite3.connect('bookings.db')
db = db_conn.cursor()
def create_table(table_name: str, **kwargs): # Pass colums as [COLUMN_NAME]=[DATA_TYPE]
    db.execute(f"""CREATE TABLE IF NOT EXISTS {table_name}(
            id INTEGER PRIMARY KEY
        )""")
    try:
        for name, type in kwargs.items():
            db.execute("""PRAGMA table_info({})""".format(table_name))
            db.execute(f"""ALTER TABLE {table_name}
                        ADD {name} {type} IF NOT EXISTS;""")
    except:
        pass
        
create_table("venue",  name="VARCHAR(50)", guests="INTEGER", time="TIME", date="DATE")

while True:
    guests = input("Enter number of guests: ")
    if not guests.isdigit():
        print("Guests must be a number")
        continue
    guests = int(guests)
    break


while True:
    name = input("Enter name: ")
    NUMBERS = set(string.digits)
    SPECIAL_CHARS = set(string.punctuation) # Includes !@#$%^&*()-=_+[]{}|;:'",.<>/?`~
    WHITESPACE = set(string.whitespace)
    for char in name:
        if char in NUMBERS or char in SPECIAL_CHARS or char in WHITESPACE:
            print("Name must not contain numbers, special characters, or whitespace")
            continue
    break
        

while True:
    date = input("Enter date in YYYY-MM-DD format: ")
    try:
        time.strptime(date, "%Y-%m-%d")
    except:
        print("Wrong format.")
        continue
        
    time = input("Enter time in 24-hr format(HH:MM): ")
    for char in time:
        if char not in NUMBERS and char != ':':
           print("Time must be in HH:MM format with digits and colon only")
           continue
    time = time.strip() if ":00" in time and time.index(":00") == 5 else time.strip() + ":00" # Append seconds to match TIME format in SQLite
    # Check for overlapping bookings within 1 hour of the requested time
    db.execute("""
        SELECT * FROM venue 
        WHERE date = ? 
        AND ABS(strftime('%s', time) - strftime('%s', ?)) < 3600
    """, (date, time))
    booked = len(db.fetchall()) > 0
    if booked:
        print("This time is already booked. Please choose another time.")
        continue
    elif not booked:
        db.execute(f"""INSERT INTO venue(name, guests, time, date) VALUES(?, ?, ?, ?)""", (name, guests, time, date))
        db_conn.commit()
        print("Booking successful!")
    break

    
