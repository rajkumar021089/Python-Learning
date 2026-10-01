from fastapi import FastAPI

app=FastAPI()

from pydantic import BaseModel

class Booking(BaseModel):
    booking_id: str
    guest: str
    room: int
    amount: int
    status: str

bookings=[
 {
        "booking_id": "B001",
        "guest": "Raj",
        "room": 101,
        "amount": 120,
        "status": "Checked In"
    },
    {
        "booking_id": "B002",
        "guest": "Priya",
        "room": 205,
        "amount": 200,
        "status": "Checked In"
    },
    {
        "booking_id": "B003",
        "guest": "Vikaan",
        "room": 310,
        "amount": 95,
        "status": "Cancelled"
    }
]

@app.get("/")
def	home_page():
	return "Welcome to Python world"


@app.get("/booking")
def get_bookings():
	
	
	return bookings 

    
@app.get("/bookings/{id}")
def get_bookings_by_id(id):
    
    for booking in bookings:
        if booking["booking_id"]==id:
            return booking
            break

@app.post("/bookings")
def create_Bookings(booking: Booking):
    bookings.append(booking.model_dump())
    return booking