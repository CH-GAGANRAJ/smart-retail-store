from fastapi import APIRouter, UploadFile, File, Form, HTTPException  # Import Form
from backend.models import product
from backend.databases import SessionLocal
from backend.qr_generator import generate_qr_code
import os

router=APIRouter(prefix="/admin")

@router.post('/add-product')
async def add_product(
    name: str = Form(...), # Use Form() for each field
    price: float = Form(...),
    product_url: str = Form(...)
):
    """
    Adds a new product to the database and generates a QR code for it.
    Expects form data for name, price, and product_url.
    """
    db = SessionLocal()
    try:
        # Create the directory for QR codes if it doesn't exist
        qr_dir = "frontend/static/Qrs"
        os.makedirs(qr_dir, exist_ok=True)

        # Generate a safe filename for the QR code
        # Replace spaces with underscores and ensure it's unique enough
        qr_filename = f"{name.replace(' ', '_')}_{db.query(product).count() + 1}.png"
        qr_path_full = os.path.join(qr_dir, qr_filename)
        qr_path_relative_to_static = f"Qrs/{qr_filename}" # Path to be stored in DB and used by frontend

        generate_qr_code(product_url, qr_path_full)

        item = product(
            name=name,
            price=price,
            product_url=product_url,
            QR=qr_path_relative_to_static # Store the relative path
        )
        db.add(item)
        db.commit()
        db.refresh(item) # Refresh to get the generated ID if needed
        return {"message": "Product added successfully", "qr_path": qr_path_relative_to_static}
    except Exception as e:
        db.rollback() # Rollback in case of error
        raise HTTPException(status_code=500, detail=f"Failed to add product: {str(e)}")
    finally:
        db.close()

