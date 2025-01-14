import requests
import time

def generate_traffic():
    url = "http://127.0.0.1:8080/api"
    headers = {"Content-Type": "application/json"}
    data = {"key": "value"}

    for _ in range(10):
        response = requests.post(url, json=data, headers=headers)
        print(f"Sent request, received response: {response.status_code}")
        time.sleep(1)

if __name__ == "__main__":
    generate_traffic()