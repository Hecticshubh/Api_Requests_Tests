# test_order_response.py

import copy
import allure
import pytest


# Verify the order response for all supported payment methods
@pytest.mark.response
@pytest.mark.regression
@pytest.mark.parametrize(
    "payment_method",
    ["UPI", "CARD", "COD", "NET_BANKING"]
)
@allure.title("Verify order response for supported payment method")
def test_create_order_response(
    api_url,
    api_headers,
    valid_order_payload,
    api_client,
    payment_method
):
    payload = copy.deepcopy(valid_order_payload)
    payload["payment_method"] = payment_method

    url = f"{api_url}/api/v1/orders/"

    with allure.step("Create order"):
        response = api_client.post(
            url,
            headers=api_headers,
            json=payload
        )

    with allure.step("Verify response status"):
        assert response.status_code == 201

    response_data = response.json()

    with allure.step("Verify response structure"):
        assert response_data["success"] is True
        assert response_data["message"] == "Order created successfully"
        assert "order" in response_data

        order = response_data["order"]

        assert "order_id" in order
        assert "customer_id" in order
        assert "items" in order
        assert "shipping_address" in order
        assert "payment_method" in order
        assert "status" in order

    with allure.step("Verify order response values"):
        assert order["customer_id"] == 101
        assert order["payment_method"] == payment_method
        assert order["status"] == "PLACED"


# Verify the data types of all order response fields
@pytest.mark.response
@pytest.mark.regression
@allure.title("Verify order response data types")
def test_create_order_response_data_types(
    api_url,
    api_headers,
    valid_order_payload,
    api_client
):
    url = f"{api_url}/api/v1/orders/"

    with allure.step("Create order"):
        response = api_client.post(
            url,
            headers=api_headers,
            json=valid_order_payload
        )

    with allure.step("Verify response status"):
        assert response.status_code == 201

    response_data = response.json()
    order = response_data["order"]

    with allure.step("Verify response data types"):
        assert isinstance(response_data["success"], bool)
        assert isinstance(response_data["message"], str)

        assert isinstance(order["order_id"], str)
        assert isinstance(order["customer_id"], int)
        assert isinstance(order["items"], list)
        assert isinstance(order["shipping_address"], dict)
        assert isinstance(order["payment_method"], str)
        assert isinstance(order["status"], str)


# Verify that the response order data matches the request data
@pytest.mark.response
@pytest.mark.regression
@allure.title("Verify request and response data match")
def test_create_order_request_response_match(
    api_url,
    api_headers,
    valid_order_payload,
    api_client
):
    payload = copy.deepcopy(valid_order_payload)

    url = f"{api_url}/api/v1/orders/"

    with allure.step("Create order"):
        response = api_client.post(
            url,
            headers=api_headers,
            json=payload
        )

    with allure.step("Verify response status"):
        assert response.status_code == 201

    order = response.json()["order"]

    with allure.step("Verify response matches request"):
        assert order["customer_id"] == payload["customer_id"]
        assert order["items"] == payload["items"]
        assert order["shipping_address"] == payload["shipping_address"]
        assert order["payment_method"] == payload["payment_method"]
        assert order["status"] == "PLACED"
        assert order["order_id"]


# Verify that the API returns a JSON response
@pytest.mark.response
@pytest.mark.regression
@allure.title("Verify order response content type")
def test_create_order_response_headers(
    api_url,
    api_headers,
    valid_order_payload,
    api_client
):
    url = f"{api_url}/api/v1/orders/"

    with allure.step("Create order"):
        response = api_client.post(
            url,
            headers=api_headers,
            json=valid_order_payload
        )

    with allure.step("Verify response status"):
        assert response.status_code == 201

    with allure.step("Verify JSON content type"):
        assert response.headers["content-type"].startswith(
            "application/json"
        )