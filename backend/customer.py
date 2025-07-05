from fastapi import APIRouter, HTTPException, Query
from backend.models import product, cart
from backend.databases import SessionLocal
from backend.ai_review import ai_review
from sqlalchemy.orm import joinedload
from pydantic import BaseModel # Ensure BaseModel is imported

router = APIRouter(prefix="/customer")

# Pydantic model for the Add to Cart request body
class AddToCartRequest(BaseModel):
    user_id: int
    product_id: int
    quantity: int = 1 # Default value as in the original function

# Pydantic model for the Update Cart request body
class UpdateCartRequest(BaseModel):
    cart_item_id: int
    quantity: int

@router.get("/product-by-url")
async def get_product_by_url(product_url: str = Query(..., description="The URL of the product")):
    db = SessionLocal()
    item = db.query(product).filter(product.product_url == product_url).first()

    if not item:
        db.close()
        raise HTTPException(status_code=404, detail="Product not found for the given URL")

    ai_content = ai_review(item.product_url)
    db.close()
    return {
        "product": item,
        "ai_review": ai_content
    }

@router.post("/add-to-cart")
async def add_to_cart(request: AddToCartRequest):
    db = SessionLocal()
    print(f"Attempting to add to cart: user_id={request.user_id}, product_id={request.product_id}, quantity={request.quantity}")
    try:
        existing_cart_item = db.query(cart).filter(
            cart.user_id == request.user_id,
            cart.product_id == request.product_id
        ).first()

        if existing_cart_item:
            existing_cart_item.quantity += request.quantity
            print(f"Updated existing cart item: ID={existing_cart_item.id}, New Quantity={existing_cart_item.quantity}")
        else:
            cart_item = cart(
                user_id=request.user_id,
                product_id=request.product_id,
                quantity=request.quantity
            )
            db.add(cart_item)
            print(f"Added new cart item for user {request.user_id}, product {request.product_id}")
        db.commit()
        db.close()
        print("Cart operation committed successfully.")
        return {"message": "Added to cart"}
    except Exception as e:
        db.rollback()
        db.close()
        print(f"Error adding to cart: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to add to cart: {str(e)}")

@router.get("/cart/{user_id}")
async def get_cart_items(user_id: int):
    db = SessionLocal()
    cart_items = db.query(cart).options(joinedload(cart.product)).filter(cart.user_id == user_id).all()

    serialized_cart_items = []
    for item in cart_items:
        serialized_cart_items.append({
            "id": item.id,
            "user_id": item.user_id,
            "product_id": item.product_id,
            "quantity": item.quantity,
            "product": {
                "id": item.product.id,
                "name": item.product.name,
                "price": item.product.price,
                "product_url": item.product.product_url,
                "QR": item.product.QR
            }
        })
    db.close()
    return {"cart_items": serialized_cart_items}

@router.put("/update-cart")
async def update_cart_item(request: UpdateCartRequest): # Changed to accept Pydantic model
    db = SessionLocal()
    print(f"Attempting to update cart item: cart_item_id={request.cart_item_id}, quantity={request.quantity}") # Debugging print
    try:
        cart_item = db.query(cart).filter(cart.id == request.cart_item_id).first()

        if not cart_item:
            db.close()
            raise HTTPException(status_code=404, detail="Cart item not found")

        if request.quantity <= 0:
            db.delete(cart_item) # Remove if quantity is 0 or less
            db.commit()
            db.close()
            print(f"Removed cart item: ID={request.cart_item_id}") # Debugging print
            return {"message": "Cart item removed"}
        else:
            cart_item.quantity = request.quantity
            db.commit()
            db.refresh(cart_item)
            db.close()
            print(f"Updated cart item: ID={request.cart_item_id}, New Quantity={request.quantity}") # Debugging print
            return {"message": "Cart item updated", "cart_item": cart_item}
    except Exception as e:
        db.rollback()
        db.close()
        print(f"Error updating cart item: {e}") # Print the actual exception
        raise HTTPException(status_code=500, detail=f"Failed to update cart item: {str(e)}")


@router.delete("/remove-from-cart/{cart_item_id}")
async def remove_from_cart(cart_item_id: int): # This one remains a path parameter
    db = SessionLocal()
    print(f"Attempting to remove cart item: cart_item_id={cart_item_id}") # Debugging print
    try:
        cart_item = db.query(cart).filter(cart.id == cart_item_id).first()

        if not cart_item:
            db.close()
            raise HTTPException(status_code=404, detail="Cart item not found")

        db.delete(cart_item)
        db.commit()
        db.close()
        print(f"Removed cart item: ID={cart_item_id} successfully.") # Debugging print
        return {"message": "Cart item removed successfully"}
    except Exception as e:
        db.rollback()
        db.close()
        print(f"Error removing cart item: {e}") # Print the actual exception
        raise HTTPException(status_code=500, detail=f"Failed to remove cart item: {str(e)}")

