import sys
from fastapi.testclient import TestClient
from app.main import app
import traceback

client = TestClient(app, raise_server_exceptions=False)

def test_post_conversations():
    print("Testing POST /api/v1/conversations")
    response = client.post("/api/v1/conversations", json={
        "title": "Test Conversation"
    })
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
    
    # Let's also check if it works when we hit it directly bypassing TestClient's exception handling
    try:
        direct_client = TestClient(app, raise_server_exceptions=True)
        direct_client.post("/api/v1/conversations", json={"title": "Test Conversation"})
    except Exception as e:
        print("\n--- TRACEBACK ---")
        traceback.print_exc()

if __name__ == "__main__":
    test_post_conversations()
