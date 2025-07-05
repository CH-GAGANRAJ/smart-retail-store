import os
import stripe
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
from starlette.responses import FileResponse
from backend.databases import SessionLocal
from sqlalchemy.orm import Session
from backend.models import cart, product
from typing import List
from pydantic import BaseModel

load_dotenv()

router = APIRouter(prefix="/payments")

# Configure Stripe (test mode)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
DOMAIN = "http://localhost:8000"

class CreateCheckoutRequest(BaseModel):
    user_id: int

@router.post("/create-checkout-session")
async def create_checkout_session(request_body: CreateCheckoutRequest):
    db = SessionLocal()
    user_id = request_body.user_id
    try:
        cart_items = db.query(cart).filter(cart.user_id == user_id).all()

        if not cart_items:
            raise HTTPException(status_code=400, detail="Cart is empty")

        # Prepare line items for Stripe
        line_items = []
        for item in cart_items:
            Product = db.query(product).filter(product.id == item.product_id).first()
            line_items.append({
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": Product.name,
                        "description": f"Product URL: {Product.product_url}",
                    },
                    "unit_amount": int(Product.price * 100),  # Convert to cents
                },
                "quantity": item.quantity,
            })

        # Create Stripe checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url=f"{DOMAIN}/payment-success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{DOMAIN}/payment-cancelled",
            metadata={
                "user_id": str(user_id),
                "cart_items": str([item.id for item in cart_items])
            }
        )

        return {"url": session.url}

    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


@router.post("/payment-success")
async def read_payment_success_page():
    return FileResponse("frontend/templates/payment_success.html")


@router.post("/payment-cancelled")
async def read_payment_cancel_page():
    return FileResponse("frontend/templates/payment_cancel.html")

