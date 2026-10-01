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


while True:
    try:
        status=int(input("Enter the amount:"))
        break
    except ValueError:
        print("Please enter a valid Amount.")
        continue



def get_BookingCount_By_Status(Bookings, status):   
    count=0
    amount=0
    for Booking in Bookings:
        if (Booking["amount"] > 50):  
            amount=amount+Booking["amount"]
    return amount 


Amount=get_BookingCount_By_Status(Bookings,status)
print(f"TotalAmount={Amount}")    