# test_order_request.py

import copy
import allure
import pytest


@pytest.mark.request
@pytest.mark.smoke
@pytest.mark.regression
@allure.title("Create order successfully")
def test_create_order_success(
    api_url,
    api_headers,
    valid_order_payload,
    api_client
):
    url = f"{api_url}/api/v1/orders/"

    with allure.step("Send valid POST order request"):
        response = api_client.post(
            url,
            headers=api_headers,
            json=valid_order_payload
        )

    with allure.step("Verify successful response"):
        assert response.status_code == 201


@pytest.mark.request
@pytest.mark.regression
@pytest.mark.parametrize(
    "payment_method",
    ["UPI", "CARD", "COD", "NET_BANKING"]
)
@allure.title("Create order with supported payment method")
def test_create_order_with_payment_methods(
    api_url,
    api_headers,
    valid_order_payload,
    api_client,
    payment_method
):
    payload = copy.deepcopy(valid_order_payload)
    payload["payment_method"] = payment_method

    url = f"{api_url}/api/v1/orders/"

    response = api_client.post(
        url,
        headers=api_headers,
        json=payload
    )

    assert response.status_code == 201


@pytest.mark.request
@pytest.mark.regression
@pytest.mark.parametrize(
    "customer_id",
    [-5, 0, -100]
)
@allure.title("Reject order with invalid customer ID")
def test_create_order_invalid_customer_id(
    api_url,
    api_headers,
    valid_order_payload,
    api_client,
    customer_id
):
    payload = copy.deepcopy(valid_order_payload)
    payload["customer_id"] = customer_id

    url = f"{api_url}/api/v1/orders/"

    response = api_client.post(
        url,
        headers=api_headers,
        json=payload
    )

    assert response.status_code == 422


@pytest.mark.request
@pytest.mark.regression
@pytest.mark.parametrize(
    "product_id",
    [-2, 0, -100]
)
@allure.title("Reject order with invalid product ID")
def test_create_order_invalid_product_id(
    api_url,
    api_headers,
    valid_order_payload,
    api_client,
    product_id
):
    payload = copy.deepcopy(valid_order_payload)
    payload["items"][0]["product_id"] = product_id

    url = f"{api_url}/api/v1/orders/"

    response = api_client.post(
        url,
        headers=api_headers,
        json=payload
    )

    assert response.status_code == 422


@pytest.mark.request
@pytest.mark.regression
@pytest.mark.parametrize(
    "quantity",
    [0, -1, -10]
)
@allure.title("Reject order with invalid quantity")
def test_create_order_invalid_quantity(
    api_url,
    api_headers,
    valid_order_payload,
    api_client,
    quantity
):
    payload = copy.deepcopy(valid_order_payload)
    payload["items"][0]["quantity"] = quantity

    url = f"{api_url}/api/v1/orders/"

    response = api_client.post(
        url,
        headers=api_headers,
        json=payload
    )

    assert response.status_code == 422


@pytest.mark.request
@pytest.mark.regression
@allure.title("Reject order with empty items")
def test_create_order_empty_items(
    api_url,
    api_headers,
    valid_order_payload,
    api_client
):
    payload = copy.deepcopy(valid_order_payload)
    payload["items"] = []

    url = f"{api_url}/api/v1/orders/"

    response = api_client.post(
        url,
        headers=api_headers,
        json=payload
    )

    assert response.status_code == 422


@pytest.mark.request
@pytest.mark.regression
@pytest.mark.parametrize(
    "payment_method",
    ["BITCOIN", "PAYPAL", "ABC", ""]
)
@allure.title("Reject order with invalid payment method")
def test_create_order_invalid_payment_method(
    api_url,
    api_headers,
    valid_order_payload,
    api_client,
    payment_method
):
    payload = copy.deepcopy(valid_order_payload)
    payload["payment_method"] = payment_method

    url = f"{api_url}/api/v1/orders/"

    response = api_client.post(
        url,
        headers=api_headers,
        json=payload
    )

    assert response.status_code == 422


@pytest.mark.request
@pytest.mark.regression
@pytest.mark.parametrize(
    "phone",
    [
        "12345",
        "123456789",
        "12345678901",
        "abcdefghij"
    ]
)
@allure.title("Reject order with invalid phone number")
def test_create_order_invalid_phone(
    api_url,
    api_headers,
    valid_order_payload,
    api_client,
    phone
):
    payload = copy.deepcopy(valid_order_payload)
    payload["shipping_address"]["phone"] = phone

    url = f"{api_url}/api/v1/orders/"

    response = api_client.post(
        url,
        headers=api_headers,
        json=payload
    )

    assert response.status_code == 422


@pytest.mark.request
@pytest.mark.regression
@pytest.mark.parametrize(
    "pincode",
    [
        "123",
        "12345",
        "1234567",
        "abcdef"
    ]
)
@allure.title("Reject order with invalid pincode")
def test_create_order_invalid_pincode(
    api_url,
    api_headers,
    valid_order_payload,
    api_client,
    pincode
):
    payload = copy.deepcopy(valid_order_payload)
    payload["shipping_address"]["pincode"] = pincode

    url = f"{api_url}/api/v1/orders/"

    response = api_client.post(
        url,
        headers=api_headers,
        json=payload
    )

    assert response.status_code == 422


@pytest.mark.request
@pytest.mark.regression
@allure.title("Reject order with missing customer ID")
def test_create_order_missing_customer_id(
    api_url,
    api_headers,
    valid_order_payload,
    api_client
):
    payload = copy.deepcopy(valid_order_payload)
    payload.pop("customer_id")

    url = f"{api_url}/api/v1/orders/"

    response = api_client.post(
        url,
        headers=api_headers,
        json=payload
    )

    assert response.status_code == 422