import requests
import json

print("=" * 70)
print("Testing POST /login endpoint")
print("=" * 70)

url = "http://localhost:5000/login"
payload = {
    "username": "test_user",
    "password": "test_password"
}

print(f"\nSending POST request to {url}")
print(f"Payload: {json.dumps(payload)}")
print("\nWaiting for response...\n")

try:
    response = requests.post(url, json=payload, timeout=5)
    print(f"Response Status: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"Response Body: {response.text}")
except Exception as e:
    print(f"ERROR: {e}")

print("\n" + "=" * 70)
