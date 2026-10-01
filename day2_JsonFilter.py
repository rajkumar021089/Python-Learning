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

for booking in Bookings:
    if booking["amount"] > 150:
        print(
        f"Guest:{booking['guest']} - High Value Booking")
    elif booking["amount"] < 100 and booking["amount"] > 50:
        print(
        f"Guest:{booking['guest']} - moderate Value Booking")  
    else:
        print(
        f"Guest:{booking['guest']} - Low Value Booking")


        