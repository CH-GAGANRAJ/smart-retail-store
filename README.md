# Smart Retail Store

![Screenshot 2025-07-05 172113](https://github.com/user-attachments/assets/ace69c52-359e-4abf-83fb-d82b97aeea07)
*A modern solution to reduce retail checkout queues*

## ✨ Features

| Feature | Description |
|---------|-------------|
| **QR Self-Checkout** | Customers scan products and pay without cashier assistance |
| **AI Product Assistant** | Generates product summaries and usage tips automatically |
| **Admin Dashboard** | Manage products, generate QR codes, and view analytics |
| **Digital Receipts** | Paperless receipts with purchase details |

## 🛠 Tech Stack

**Backend**:
- Python (FastAPI)
- PostgreSQL
- Stripe API (test mode)

**Frontend**:
- HTML5/CSS3
- JavaScript (ES6+)
- Bootstrap 5
- QR Scanner JS

**AI Components**:
- Google Gemini API
- Web Scraping (BeautifulSoup)

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- PostgreSQL 12+
- Node.js (for frontend assets)

### Installation
```bash
# Clone repository
git clone https://github.com/yourusername/smart-retail-system.git
cd smart-retail-system

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

# Install dependencies
pip install -r req.txt
```
### Configuration
Create .env file:
```bash
DATABASE_URL=postgresql://user:password@localhost:5432/smart_retail
STRIPE_SECRET_KEY=sk_test_yourkey
GEMINI_API_KEY=your-ai-key
DOMAIN=http://localhost:8000
```
### Running the System
```bash
# Start backend server
uvicorn backend.main:app --reload
```
### Testing Payments
Use Stripe test cards:
Card Number	Scenario
4242 4242 4242 4242	Successful payment
4000 0000 0000 0002	Declined payment

## 📺 Demo Video
[![Smart Retail System Demo](https://img.youtube.com/vi/FzKuPeYQEY4/0.jpg)](https://www.youtube.com/watch?v=FzKuPeYQEY4)

