class Restaurant:
	
    hotel_name="Intellistay"
	
    def __init__(self,orderid, itemname, amount):
        self.orderid=orderid
        self.itemname=itemname
        self.amount=amount
            
    def calculate_amount(self):
            return self.amount
        
    def show(self):
            print("----------------------")
            print("Hotel:", self.hotel_name)
            print("Order ID:", self.orderid)
            print("ItemName:", self.itemname)
            print("Original Amount:", self.calculate_amount())

class threeStar(Restaurant):
        
        def calculate_amount(self):
            self.amount = (self.amount * 0.2) + self.amount
            return self.amount

class fiveStar(Restaurant):
        
        def calculate_amount(self):
            self.amount = (self.amount * 0.3) + self.amount
            return self.amount
            
            
orders=[]

def add_itemOrder():

        orderid=input("Enter the OrderID:")
        itemname=input("""Enter the ItemName:
                        1.Parotta
                        2.Curry
                        3.Panneer Button Masala
                        """)
        try:
            amount=int(input("Enter the Amount:"))
        except ValueError:
            print("Invalid amount. Please enter a valid number.")
            return

        restaurantType=input("""
                                Enter the RestaurantType:
                                1. Normal
                                2. 3-Star
                                3. 5-start
                             """)

        if restaurantType== "1":
                order=Restaurant(orderid, itemname, amount)
                
        elif restaurantType== "2":
                order=threeStar(orderid, itemname, amount)
                
        elif restaurantType== "3":
                order=fiveStar(orderid, itemname, amount)
                
        else:
              print("Select Valid RestaurantType")
              
              
        orders.append(order)
        
        print("Ordered Successfully")            
                
def show_itemOrder():

    if len(orders) == 0:
        print("No orders available")
        return

    for order in orders:
        order.show()



while True:

    print("\n===== IntelliStay =====")
    print("1. Add Order")
    print("2. Show Order")
    print("3. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        
        add_itemOrder()

    elif choice == "2":

        show_itemOrder()

    elif choice == "3":

        print("Goodbye!")
        break

    else:

        print("Invalid choice")              
                