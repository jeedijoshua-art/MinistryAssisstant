from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def run():
    # 1. Create Conversation
    print("\n--- 1. Create Conversation ---")
    res = client.post("/api/v1/conversations", json={"title": "Mission 3 Test"})
    assert res.status_code == 201, f"Failed to create conversation: {res.text}"
    conv = res.json()
    conv_id = conv["id"]
    print(f"Created conversation {conv_id}")

    # 2. Assistant Chat - Hello
    print("\n--- 2. Assistant Chat (Hello) ---")
    payload = {
        "conversation_id": conv_id,
        "message": "Hello",
        "church_id": "b21b6c81-b3bc-4797-bf54-91d1f7e416bf",
        "user_id": "00000000-0000-0000-0000-000000000000"
    }
    res = client.post("/api/v1/assistant/chat", json=payload)
    if res.status_code != 200:
        print(f"Error: {res.status_code} {res.text}")
        return
    print(res.json()["message"]["content"])

    # 3. Explain John 3:16
    print("\n--- 3. Explain John 3:16 ---")
    payload["message"] = "Explain John 3:16"
    res = client.post("/api/v1/assistant/chat", json=payload)
    if res.status_code != 200:
        print(f"Error: {res.status_code} {res.text}")
        return
    print(res.json()["message"]["content"])

    # 4. Summarize it
    print("\n--- 4. Summarize it ---")
    payload["message"] = "Summarize it."
    res = client.post("/api/v1/assistant/chat", json=payload)
    if res.status_code != 200:
        print(f"Error: {res.status_code} {res.text}")
        return
    print(res.json()["message"]["content"])

    # 5. Create a prayer based on it
    print("\n--- 5. Create a prayer based on it ---")
    payload["message"] = "Create a prayer based on it."
    res = client.post("/api/v1/assistant/chat", json=payload)
    if res.status_code != 200:
        print(f"Error: {res.status_code} {res.text}")
        return
    print(res.json()["message"]["content"])

if __name__ == "__main__":
    run()
