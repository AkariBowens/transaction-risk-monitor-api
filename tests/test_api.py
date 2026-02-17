import pytest
from fastapi.testclient import TestClient
from main import app
import uuid
import redis

@pytest.fixture(autouse=True)
def clear_redis():
    r = redis.Redis(host='localhost', port=6379, db=0, socket_connect_timeout=1)
    r.flushall()
    print("/----- Redis Flushed -----/")
    # Runs the test
    yield

client = TestClient(app)

def test_velocity_check():
    # Runs 1000 transactions; some failing the check and some passing the check

    for i in range(1000):
        amount = 500.00 if i % 2 == 0 else 15000.00

        payload = {
            "transaction_id": str(uuid.uuid4()),
            "account_id": "ACC123456",
            "amount": str(amount),
            "currency": "USD",
            "merchant_id": "SAFE_SHOP",
            "merchant_category_code": "5411",
            "ip_address": "127.0.0.1"
        }

        response = client.post("/v1/assess-risk", json=payload)
        assert response.status_code == 200

        data = response.json()
        if amount > 10000:
            assert data["decision"] in ["DENY", "REVIEW"]
            assert "LARGE_TRANSACTION_DETECTION" in data["triggered_rules"] 
        else:
            assert data["decision"] == "ALLOW"

def test_invalid_data_rejection():
    
    # Ensures "bad" data is caught
    bad_payload = {"amount" : "Not a number"}
    response = client.post("/v1/assess-risk", json=bad_payload)
    assert response.status_code == 422

