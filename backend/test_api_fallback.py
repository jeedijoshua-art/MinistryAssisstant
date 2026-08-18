import sys
from fastapi.testclient import TestClient
from app.main import app
from app.database.session import SessionLocal

client = TestClient(app)

def run_tests():
    # Test 1: get_books without translation_code (should fallback to TEST)
    response = client.get("/api/v1/bible/books")
    print("GET /bible/books:", response.status_code)
    if response.status_code == 200:
        books = response.json()
        print(f"  Returned {len(books)} books")
    else:
        print(f"  Error: {response.text}")
        
    # Test 2: resolve_verse without translation_code (should fallback to TEST)
    response = client.get("/api/v1/bible/verse?reference=John 3:16")
    print("GET /bible/verse (John 3:16):", response.status_code)
    if response.status_code == 200:
        verses = response.json()
        print(f"  Returned {len(verses)} verses")
    else:
        print(f"  Error: {response.text}")

    # Test 3: daily_verse fallback
    # Because daily verse rotates, it might return 404 if the verse is not Genesis or John 3:16
    response = client.get("/api/v1/bible/daily-verse")
    print("GET /bible/daily-verse:", response.status_code)
    if response.status_code == 200:
        print(f"  Returned: {response.json().get('text')}")
    else:
        print(f"  Error: {response.text}")

if __name__ == "__main__":
    run_tests()
