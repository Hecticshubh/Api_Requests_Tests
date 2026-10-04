# test_order_auth_request.py

import allure
import pytest


# Verify that an order cannot be created without an authorization token
@pytest.mark.auth
@pytest.mark.regression
@allure.title("Create order without authorization token")
def test_create_order_without_token(
    api_url,
    valid_order_payload,
    api_client
):
    url = f"{api_url}/api/v1/orders/"

    with allure.step("Send POST request without authorization token"):
        response = api_client.post(
            url,
            json=valid_order_payload
        )

    with allure.step("Verify unauthorized response"):
        assert response.status_code == 401
        assert response.json()["detail"] == "Authorization header is required"


# Verify that an order cannot be created with an invalid authorization token
@pytest.mark.auth
@pytest.mark.regression
@allure.title("Create order with invalid authorization token")
def test_create_order_with_wrong_token(
    api_url,
    api_headers,
    valid_order_payload,
    api_client
):
    url = f"{api_url}/api/v1/orders/"

    headers = {
        **api_headers,
        "Authorization": "Bearer wrong-token-123"
    }

    with allure.step("Send POST request with invalid authorization token"):
        response = api_client.post(
            url,
            headers=headers,
            json=valid_order_payload
        )

    with allure.step("Verify unauthorized response"):
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid or expired token"