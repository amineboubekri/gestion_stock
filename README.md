# Gestion Stock

<p align="center"><i>Streamlining Inventory Management with Django Excellence</i></p>

<p align="center">
  <img src="https://img.shields.io/github/last-commit/amineboubekri/gestion_stock?style=for-the-badge" alt="last commit"/>
  <img src="https://img.shields.io/badge/last%20update-March%202024-blue?style=for-the-badge" alt="last update"/>
  <img src="https://img.shields.io/badge/language-Python-blue?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/framework-Django-green?style=for-the-badge"/>
  <img src="https://img.shields.io/github/languages/count/amineboubekri/gestion_stock?style=for-the-badge" alt="language count"/>
</p>

---

<p align="center"><i><b>Built with the tools and technologies:</b></i></p>
<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" />
  <img src="https://img.shields.io/badge/MySQL-00000F?style=for-the-badge&logo=mysql&logoColor=white" />
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" />
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" />
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" />
  <br/>
  <img src="https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white" />
  <img src="https://img.shields.io/badge/ReportLab-000000?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Pillow-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/PDF-FF0000?style=for-the-badge&logo=pdf&logoColor=white" />
</p>

---

## 📌 Overview

**Gestion Stock** is a comprehensive inventory management system designed to help organizations efficiently manage their stock, track orders, and handle employee requests. The system features role-based access control for administrators, employees, and warehouse managers.

### 🔍 Key Features

- 👤 **Role-Based Access Control:** Secure login system with different roles (Admin, Employee, Warehouse Manager)
- 📦 **Inventory Management:** Track product quantities and manage stock levels
- 📝 **Order Management:** Create and track orders with validation workflow
- 👥 **Employee Management:** Add, modify, and manage employee accounts
- 📊 **Order History:** View and track order history
- 📄 **PDF Generation:** Generate order receipts and reports
- 🛒 **Shopping Cart:** Add multiple items to cart before placing orders

---

## 🚀 Getting Started

### Prerequisites

This project requires the following dependencies:
- Python 3.x
- Django
- MySQL
- ReportLab
- Pillow

---

### Installation

Clone the repository:
```bash
git clone https://github.com/amineboubekri/gestion_stock
cd gestion_stock
```

Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Configure the database in `gestion_stock/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'gestion_stock',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

Run migrations:
```bash
python manage.py migrate
```

### ▶️ Usage

Run the development server:
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

### ✅ Features

- **User Management:**
  - Role-based authentication (Admin, Employee, Warehouse Manager)
  - Secure login and registration
  - Profile management

- **Inventory Management:**
  - Add new products
  - Update product information
  - Track stock levels
  - View product history

- **Order Management:**
  - Create new orders
  - Track order status
  - Validate/reject orders
  - Generate order receipts
  - Shopping cart functionality

- **Employee Management:**
  - Add new employees
  - Modify employee information
  - View employee list
  - Manage employee roles

- **Reporting:**
  - Generate PDF receipts
  - View order history
  - Track stock movements

<p align="center"><a href="#">⬆ Return to Top</a></p>
