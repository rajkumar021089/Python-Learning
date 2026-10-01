Bookings= [
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
        "status": "Cancelled",
        "payment": "Pending"
    }
]

count = 0
BookedCount=0
BookingAmount=0
CheckedInAmount=0
for booking in Bookings:
    count = count + 1
    BookingAmount = BookingAmount + booking["amount"]
    if booking["status"] == "Checked In":
        BookedCount = BookedCount + 1
        CheckedInAmount = CheckedInAmount + booking["amount"]
       

print(
    f"Total Bookings: {count}",
    f"Total Booked Count: {BookedCount}",
    f"Total Booking Amount: {BookingAmount}",
    f"Total Checked In Amount: {CheckedInAmount}")
