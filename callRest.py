import requests

response = requests.get(
    "https://jsonplaceholder.typicode.com/users/1"
)

print("Status Code:", response.status_code)

data = response.json()

print("Name:", data["name"])
print("Email:", data["email"])
print("City:", data["address"]["city"])