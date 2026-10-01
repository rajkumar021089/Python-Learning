from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app=FastAPI()

class Booking(BaseModel):
    bookingid: str
    guest: str
    amount: int
    room: int
    status: str
    
    
def createtable():
    connection = sqlite3.connect("bookings.db")
    
    cursor = connection.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS BOOKINGS(
            booking_id TEXT PRIMARY KEY,
            guest TEXT,
            amount INTEGER,
            room INTEGER,
            STATUS TEXT
        )
    """)
    
    connection.commit()
    
    connection.close()
    
createtable()
 
 
 
@app.get("/bookings")
def get_bookings():
    connection=sqlite3.connect("bookings.db")
    connection.row_factory=sqlite3.Row
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM BOOKINGS")

    bookingslist= cursor.fetchall()
    bookings=[dict(booking) for booking in bookingslist ]
    connection.close()
    return bookings
    
 
@app.post("/bookings")
def create_bookings(bookings: list[Booking]):
    connection = sqlite3.connect("bookings.db")
    cursor = connection.cursor()
    for booking in bookings:
        cursor.execute("""
        INSERT INTO BOOKINGS (booking_id,guest,amount,room,status) 
        VALUES (?,?,?,?,?)
        """,
    (
    booking.bookingid,
    booking.guest,
    booking.amount,
    booking.room,
    booking.status
    ))
    
    connection.commit()
    
    connection.close()
    
    return bookings 