bookings = [
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


for booking in bookings:
    if booking["status"] == "Checked In":
        print(f"Booking ID: {booking['booking_id']}, Guest: {booking['guest']}, Room: {booking['room']}, Amount: {booking['amount']}, Status: {booking['status']}") 

    if booking["status"] == "Cancelled":
        print(f"Booking ID: {booking['booking_id']}, Guest: {booking['guest']}, Room: {booking['room']}, Amount: {booking['amount']}, Status: {booking['status']}, Payment: {booking['payment']}")

    if booking.get("payment", "N/A") == "Pending":     
        print(f"Booking ID: {booking['booking_id']}, Guest: {booking['guest']}, Room: {booking['room']}, Amount: {booking['amount']}, Status: {booking['status']}, Payment: {booking['payment']}")