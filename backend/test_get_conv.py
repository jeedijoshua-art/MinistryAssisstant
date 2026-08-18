from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

res = client.post("/api/v1/conversations", json={"title": "Test GET"})
conv_id = res.json()["id"]
print(f"Created {conv_id}")

res2 = client.get(f"/api/v1/conversations/{conv_id}")
print(f"GET Status: {res2.status_code}")
print(f"GET Body: {res2.json()}")
