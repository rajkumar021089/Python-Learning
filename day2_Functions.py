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



def count_check_in(Bookings):
    count=0
    for Booking in Bookings:
        if (Booking["status"]=="Checked In"):
            count=count+1
    return count

def amount_check_in(Bookings):
    amount=0
    for Booking in Bookings:
        if (Booking["status"]=="Checked In"):
            amount=amount+Booking["amount"]
    return amount

CheckedInCount=count_check_in(Bookings)
CheckedInAmount=amount_check_in(Bookings)
print(f"Checked In Count={CheckedInCount}")
print(f"Checked In Amount={CheckedInAmount}")         