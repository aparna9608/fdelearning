from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_get_customers():
    response = client.get("/customers")

    assert response.status_code == 200


def test_create_customer():
    customer_data = {
        "name": "Test User",
        "role": "SDET"
    }

    response = client.post("/customers", json=customer_data)

    assert response.status_code == 201

    response_data = response.json()

    assert response_data["name"] == "Test User"
    assert response_data["role"] == "SDET"
    assert "id" in response_data

def test_create_and_fetch_customer():
    customer_data = {
        "name": "Integration User",
        "role": "FDE"
    }

    # Create customer
    post_response = client.post("/customers", json=customer_data)

    assert post_response.status_code == 201

    created_customer = post_response.json()
    customer_id = created_customer["id"]

    # Fetch customers
    get_response = client.get("/customers")

    assert get_response.status_code == 200

    customers = get_response.json()

    # Find the customer we just created
    customer = next(
        customer for customer in customers
        if customer["id"] == customer_id
    )

    # Validate
    assert customer["name"] == "Integration User"
    assert customer["role"] == "FDE"

def test_create_customer_missing_role():
    customer_data = {
        "name": "Invalid User"
    }

    response = client.post("/customers", json=customer_data)

    assert response.status_code == 422

def test_create_customer_empty_values():
    customer_data = {
        "name": "",
        "role": ""
    }

    response = client.post("/customers", json=customer_data)

    assert response.status_code == 422