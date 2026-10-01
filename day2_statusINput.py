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


def get_BookingCount_By_Status(Bookings, status):
    count=0
    amount=0
    for Booking in Bookings:
        if (Booking["status"]==status):
            count=count+1
            amount=amount+Booking["amount"]
    return count,amount
           


status=input("Enter the status to get the count and amount:")
Count,Amount=get_BookingCount_By_Status(Bookings,status)
print(f"{status}={Count}",
      f"{status} Amount={Amount}")    