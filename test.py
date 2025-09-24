import requests

url = 'http://127.0.0.1:8000/question'

payload = {
    "question": "Is the Lat Pulldown considered a strength training activity, and if so, why?"
}

response = requests.post(url, json=payload)  # <-- json= automatically sets the header

print(response)
print(response.status_code)
print(response.text)