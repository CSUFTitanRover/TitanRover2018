import sqlite3
from sqlite3 import Error


def storeMessage(time, distance, messageType):
  conn = sqlite3.connect('telemetry.db', check_same_thread=False)
  c = conn.cursor()
  try:
    c.execute('''CREATE TABLE IF NOT EXISTS telemetry 
    (time double PRIMARY KEY,
    distance double NOT NULL,
    messageType integer NOT NULL)''')
    args = [time, distance, messageType]
    c.execute('''INSERT INTO telemetry (time, distance, messageType) VALUES (?, ?, ?)''', args)
    conn.commit()
    except Error as e:
      print(e)
