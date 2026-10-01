import  json

with open('Booking.json', 'r') as file:
    data=json.load(file)

print(data)
