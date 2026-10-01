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

try:

    amount = int(input("Enter the amount:"))
    for booking in Bookings:
     if (booking["amount"]>=amount):
        print(f"Booking Id={booking['booking_id']}",
              f"Guest={booking['guest']}",
              f"Room={booking['room']}",
              f"Amount={booking['amount']}",
              f"Status={booking['status']}")


except ValueError:
    print("Please enter a valid integer amount.")
    exit()


        