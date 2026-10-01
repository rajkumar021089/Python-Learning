import requests

booking = {
    "guest": "Raj",
    "room": 101,
    "amount": 120,
    "status": "Confirmed"
}

response = requests.post(
    "https://jsonplaceholder.typicode.com/posts",
    json=booking
)

print("Status Code:", response.status_code)

data = response.json()

print("Guest:", data["guest"])
print("Room:", data["room"])
print("Amount:", data["amount"])
print("Generated ID:", data["id"])