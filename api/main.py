from enum import Enum
import json
import os
import logging
from pathlib import Path

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field

from api.database import get_connection


# Load environment variables
load_dotenv()


# Configure logging
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(message)s",
    datefmt="%Y-%m-%d %I:%M:%S %p",
    handlers=[
        logging.FileHandler(LOG_DIR / "api_test.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


# Configure application settings
class Config:
    AUTH_TOKEN = os.getenv("AUTH_TOKEN")


# Initialize the FastAPI application
app = FastAPI(
    title="Ecommerce API",
    version="1.0.0"
)


# Configure the order API router
router = APIRouter(
    prefix="/api/v1/orders",
    tags=["Orders"]
)


# Configure bearer token authentication
security = HTTPBearer(auto_error=False)


# Define order item validation
class OrderItem(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)


# Define shipping address validation
class ShippingAddress(BaseModel):
    name: str
    phone: str = Field(pattern=r"^[0-9]{10}$")
    address: str
    city: str
    state: str
    pincode: str = Field(pattern=r"^[0-9]{6}$")


# Define supported payment methods
class PaymentMethod(str, Enum):
    UPI = "UPI"
    CARD = "CARD"
    COD = "COD"
    NET_BANKING = "NET_BANKING"


# Define order request validation
class OrderCreate(BaseModel):
    customer_id: int = Field(gt=0)
    items: list[OrderItem] = Field(min_length=1)
    shipping_address: ShippingAddress
    payment_method: PaymentMethod


# Create a new order
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_order(
    order: OrderCreate,
    credentials: HTTPAuthorizationCredentials | None = Depends(security)
):

    logger.info("Order creation request received")

    # Validate authentication credentials
    if credentials is None:
        logger.warning("Order creation failed: authorization header is missing")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header is required"
        )

    # Validate the authentication token
    if credentials.credentials != Config.AUTH_TOKEN:
        logger.warning("Order creation failed: invalid authentication token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    # Create a database connection
    connection = get_connection()
    cursor = connection.cursor()

    # Get the current order count
    cursor.execute("""
        SELECT COUNT(*) FROM orders
    """)

    order_count = cursor.fetchone()[0]
    order_id = f"ORD-{10001 + order_count}"

    # Insert the order into the database
    cursor.execute("""
        INSERT INTO orders (
            order_id,
            customer_id,
            items,
            shipping_address,
            payment_method,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        order_id,
        order.customer_id,
        json.dumps([item.model_dump() for item in order.items]),
        json.dumps(order.shipping_address.model_dump()),
        order.payment_method.value,
        "PLACED"
    ))

    # Save and close the database connection
    connection.commit()
    connection.close()

    logger.info("Order created successfully: %s", order_id)

    # Return the created order response
    return {
        "success": True,
        "message": "Order created successfully",
        "order": {
            "order_id": order_id,
            "customer_id": order.customer_id,
            "items": order.items,
            "shipping_address": order.shipping_address,
            "payment_method": order.payment_method,
            "status": "PLACED"
        }
    }


# Register the order routes
app.include_router(router)


# Define the API health endpoint
@app.get("/")
def root():
    logger.info("Health check endpoint called")

    return {
        "success": True,
        "message": "Ecommerce API is running"
    }