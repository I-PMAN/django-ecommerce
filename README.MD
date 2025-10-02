# Django E-Commerce Project

[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-5.x-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

---

## 🚀 Project Overview

A **full-featured e-commerce backend** built with **Django REST Framework**.  
Supports **user registration, products, shopping cart, checkout, payment simulation, orders, reviews, and wishlist**.  
Designed to be **modular, scalable, and production-ready** with JWT authentication and admin management.

---

## 🌟 Features

### User Management

- JWT Authentication (register/login)
- Profile view & update

### Products

- CRUD operations (admin)
- Product listing & detail
- Reviews & average rating
- Wishlist functionality

### Cart & Orders

- Add/update/remove cart items
- Checkout & address management
- Payment simulation
- Admin order management

### Admin Features

- Update order status
- Moderate reviews
- View users, products, orders
- Dashboard metrics (planned)

---

## ⚡ Tech Stack

- Python 3.11
- Django 5.x
- Django REST Framework
- SQLite (default)
- JWT Authentication (`djangorestframework-simplejwt`)

---

## 📁 Project Structure

django_ecommerce/
├── ecommerce/ # Project settings & URLs
├── users/ # User registration, login, profile
├── products/ # Products, reviews, wishlist
├── orders/ # Cart, checkout, payment, orders
├── manage.py
├── db.sqlite3
├── requirements.txt

---

## 🛠️ Setup & Run

1. **Clone repository**

```bash
git clone https://github.com/<username>/django-ecommerce.git
cd django-ecommerce
```

2. **Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run migrations**

```bash
python manage.py migrate
```

5. **Create a superuser**

```bash
python manage.py createsuperuser
```

6. **Run the development server**

```bash
python manage.py runserver
```

- Admin panel: http://127.0.0.1:8000/admin/

- API base: http://127.0.0.1:8000/

🔗 API Endpoints (Highlights)

Authentication

| Method | Endpoint              | Description                          |
| ------ | --------------------- | ------------------------------------ |
| POST   | `/api/token/`         | Obtain JWT access and refresh tokens |
| POST   | `/api/token/refresh/` | Refresh JWT access token             |

Users

| Method | Endpoint           | Description                   |
| ------ | ------------------ | ----------------------------- |
| POST   | `/users/register/` | Register a new user           |
| GET    | `/users/profile/`  | Retrieve current user profile |
| PUT    | `/users/profile/`  | Update user profile           |

Products

| Method | Endpoint          | Description                  |
| ------ | ----------------- | ---------------------------- |
| GET    | `/products/`      | List all products            |
| GET    | `/products/{id}/` | Retrieve product details     |
| POST   | `/products/`      | Create a new product (Admin) |
| PUT    | `/products/{id}/` | Update a product (Admin)     |
| DELETE | `/products/{id}/` | Delete a product (Admin)     |

Reviews

| Method | Endpoint                  | Description                    |
| ------ | ------------------------- | ------------------------------ |
| POST   | `/products/{id}/reviews/` | Add a review for a product     |
| GET    | `/products/{id}/reviews/` | List all reviews for a product |
| PUT    | `/reviews/{id}/`          | Update a review                |
| DELETE | `/reviews/{id}/`          | Delete a review                |

Wishlist

| Method | Endpoint                 | Description                  |
| ------ | ------------------------ | ---------------------------- |
| POST   | `/wishlist/add/`         | Add product to wishlist      |
| GET    | `/wishlist/`             | List wishlist items          |
| DELETE | `/wishlist/{id}/remove/` | Remove product from wishlist |

Cart

| Method | Endpoint           | Description               |
| ------ | ------------------ | ------------------------- |
| POST   | `/cart/add/`       | Add item to cart          |
| GET    | `/cart/`           | View cart items           |
| PUT    | `/cart/item/{id}/` | Update cart item quantity |
| DELETE | `/cart/item/{id}/` | Remove item from cart     |

Checkout & Orders

| Method | Endpoint                      | Description                       |
| ------ | ----------------------------- | --------------------------------- |
| POST   | `/checkout/`                  | Checkout cart and create an order |
| POST   | `/orders/{id}/pay/`           | Simulate payment for an order     |
| GET    | `/orders/`                    | List all orders (user/admin)      |
| GET    | `/orders/{id}/`               | Retrieve order details            |
| POST   | `/orders/{id}/update_status/` | Update order status (Admin only)  |

Addresses

| Method | Endpoint                       | Description         |
| ------ | ------------------------------ | ------------------- |
| POST   | `/addresses/`                  | Add a new address   |
| GET    | `/addresses/`                  | List user addresses |
| PUT    | `/addresses/{id}/`             | Update an address   |
| POST   | `/addresses/{id}/set-default/` | Set default address |

✅ Running Tests

```bash
python manage.py test
```

Covers users, products, cart, checkout, payment, reviews, wishlist endpoints.

🌐 Future Enhancements

- Email notifications for orders/payments

- Advanced product filtering & search

- Admin dashboard with analytics

- Real payment gateway integration

integration

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

---
