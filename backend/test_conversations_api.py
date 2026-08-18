from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def run():
    print("Testing POST /api/v1/conversations")
    response = client.post("/api/v1/conversations", json={"title": "Test Chat"})
    print(response.status_code, response.text)
    
if __name__ == "__main__":
    run()
