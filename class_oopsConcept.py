class Booking:

    hotel_name = "IntelliStay"

    def __init__(self, booking_id, guest, amount):
        self.booking_id = booking_id
        self.guest = guest
        self.amount = amount

    def calculate_amount(self):
        return self.amount

    def show(self):
        print("----------------------")
        print("Hotel:", self.hotel_name)
        print("Booking ID:", self.booking_id)
        print("Guest:", self.guest)
        print("Original Amount:", self.amount)
        print("Final Amount:", self.calculate_amount())


class CorporateBooking(Booking):

    def calculate_amount(self):
        return self.amount * 0.90


class VIPBooking(Booking):

    def calculate_amount(self):
        return self.amount * 0.80


bookings = []


def add_booking():

    booking_id = input("Enter booking ID: ")
    guest = input("Enter guest name: ")

    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("Invalid amount!")
        return

    print("\nBooking Type")
    print("1. Normal")
    print("2. Corporate")
    print("3. VIP")

    booking_type = input("Choose: ")

    if booking_type == "1":

        booking = Booking(
            booking_id,
            guest,
            amount
        )

    elif booking_type == "2":

        booking = CorporateBooking(
            booking_id,
            guest,
            amount
        )

    elif booking_type == "3":

        booking = VIPBooking(
            booking_id,
            guest,
            amount
        )

    else:

        print("Invalid booking type")
        return

    bookings.append(booking)

    print("Booking created successfully!")


def show_bookings():

    if len(bookings) == 0:
        print("No bookings available")
        return

    for booking in bookings:
        booking.show()


while True:

    print("\n===== IntelliStay =====")
    print("1. Add Booking")
    print("2. Show Bookings")
    print("3. Exit")

    choice = input("Enter choice: ")

    if choice == "1":

        add_booking()

    elif choice == "2":

        show_bookings()

    elif choice == "3":

        print("Goodbye!")
        break

    else:

        print("Invalid choice")