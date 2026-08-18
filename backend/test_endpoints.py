from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

print("--- Testing /api/v1/bible/books ---")
response = client.get("/api/v1/bible/books?translation_code=TEST")
print(response.status_code)
print(len(response.json()), "books found.")

print("\n--- Testing /api/v1/bible/verse ---")
response = client.get("/api/v1/bible/verse?translation_code=TEST&reference=Genesis%201:1")
print(response.status_code)
if response.status_code == 200:
    print([v["text"] for v in response.json()])
else:
    print(response.json())

print("\n--- Testing /api/v1/bible/search ---")
response = client.get("/api/v1/bible/search?translation_code=TEST&query=beginning")
print(response.status_code)
if response.status_code == 200:
    print([v["text"] for v in response.json()])
else:
    print(response.json())

print("\n--- Testing /api/v1/bible/daily-verse ---")
# To make daily-verse work, we need a daily verse to exist.
# Let's just pass translation_code=TEST
response = client.get("/api/v1/bible/daily-verse?translation_code=TEST")
print(response.status_code)
if response.status_code == 200:
    print(response.json().get("text"))
else:
    print(response.json())
