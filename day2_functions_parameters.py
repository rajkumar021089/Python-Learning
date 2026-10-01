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


def count_check_in(Bookings, status):
    count=0
    for Booking in Bookings:
        if (Booking["status"]==status):
            count=count+1
    return count
           
 
Count=count_check_in(Bookings,"Checked In")
print(f"Checked In Count={Count}")

Count=count_check_in(Bookings,"Cancelled")
print(f"Cancelled={Count}")