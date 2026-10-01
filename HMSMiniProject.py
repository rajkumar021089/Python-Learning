username=input("Enter your username: ")
password=input("Enter your password: ")
count=0

while True:
    if count>=3:
        print("You have exceeded the maximum number of login attempts. Please try again later.")
        break
    if username=="admin" and password=="admin":
        print("Login Successful")
        break
    else:
        print("Invalid username or password. Please try again.")
        username=input("Enter your username: ")
        password=input("Enter your password: ") 
        count=count+1


Bookings= [
  {
        "booking_id": "B001",
        "guest": "Raj",
        "room": 101,
        "amount": 120,
        "status": "Checked In",
        "Date": "2023-06-01"
    },
    {
        "booking_id": "B002",
        "guest": "Priya",
        "room": 205,
        "amount": 200,
        "status": "Checked In",
        "Date": "2023-06-02"
    },
    {
        "booking_id": "B003",
        "guest": "Vikaan",
        "room": 310,
        "amount": 95,
        "status": "Cancelled",
        "payment": "Pending",
        "Date": "2023-06-03"
    }
]

def get_details(Bookings, status):   
    count=0
    amount=0
    for Booking in Bookings:
        if (Booking["status"]==status):  
            count=count+1
            amount=amount+Booking["amount"]
    return count,amount

def get_details_by_date(Bookings, date):
    count=0
    amount=0
    for Booking in Bookings:
        if (Booking["Date"]==date):  
            count=count+1
            amount=amount+Booking["amount"]
    return count,amount 


status=input("Enter the status to get booking details: ")
date=input("Enter the date to get booking details: ")   

count,amount=get_details(Bookings,status)
print(f"Booking Count for status '{status}': {count}")
count,amount=get_details_by_date(Bookings,date)
print(f"Booking Count for date '{date}': {count}")  
