# conftest.py

import os
from copy import deepcopy

import pytest
import requests
from dotenv import load_dotenv


# Load environment variables
load_dotenv()


# Define the API base URL
BASE_URL = "http://127.0.0.1:8000"


# Load the authentication token from environment variables
AUTH_TOKEN = os.getenv("AUTH_TOKEN")


# Define common API headers
COMMON_HEADERS = {
    "Content-Type": "application/json"
}


# Define the valid order payload
VALID_ORDER_PAYLOAD = {
    "customer_id": 101,
    "items": [
        {
            "product_id": 2,
            "quantity": 2
        }
    ],
    "shipping_address": {
        "name": "Rahul Sharma",
        "phone": "9876543210",
        "address": "123 Main Road",
        "city": "Lucknow",
        "state": "Uttar Pradesh",
        "pincode": "226001"
    },
    "payment_method": "UPI"
}


# Provide the API base URL
@pytest.fixture
def api_url():
    return BASE_URL


# Provide authenticated API headers
@pytest.fixture
def api_headers():
    return {
        **COMMON_HEADERS,
        "Authorization": f"Bearer {AUTH_TOKEN}"
    }


# Provide a fresh deep copy of the valid order payload
@pytest.fixture
def valid_order_payload():
    return deepcopy(VALID_ORDER_PAYLOAD)


# Provide the requests library for API calls
@pytest.fixture
def api_client():
    return requests