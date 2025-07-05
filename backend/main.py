from fastapi import FastAPI
from backend.databases import engine, Base
from backend import admin, customer, payment, auth # All directly imported from backend
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI()

# Ensure the static directory exists
os.makedirs("frontend/static/css", exist_ok=True)
os.makedirs("frontend/static/js", exist_ok=True)
os.makedirs("frontend/static/images", exist_ok=True)
os.makedirs("frontend/static/Qrs", exist_ok=True) # For QR codes

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Serve your frontend HTML files
@app.get("/")
async def read_customer_index():
    return FileResponse("frontend/templates/customer.html")

@app.get("/admin")
async def read_admin_panel():
    return FileResponse("frontend/templates/admin.html")

@app.get("/login")
async def read_login_page():
    return FileResponse("frontend/templates/login.html")

@app.get("/register")
async def read_register_page():
    return FileResponse("frontend/templates/register.html")

@app.get("/cart")
async def read_cart_page():
    return FileResponse("frontend/templates/cart.html")

@app.get("/checkout")
async def read_checkout_page():
    return FileResponse("frontend/templates/checkout.html")

@app.get("/payment-success")
async def read_payment_success_page():
    return FileResponse("frontend/templates/payment_success.html")

@app.get("/payment-cancelled")
async def read_payment_cancel_page():
    return FileResponse("frontend/templates/payment_cancel.html")

# Synchronous table creation
@app.on_event("startup")
def startup_db():
    Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(admin.router)
app.include_router(customer.router)
app.include_router(payment.router)
app.include_router(auth.router)

