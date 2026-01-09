<div align="center">

# 🏭⚡ **Warehouse Inventory Management System**  
### *FastAPI + SQLAlchemy + MySQL — Complete Warehouse Engine with FIFO/FEFO Sales Logic*

<br/>

<p>
  <img src="https://img.shields.io/badge/FastAPI-00A489?style=for-the-badge&logo=fastapi&logoColor=white"/>
  <img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/MySQL-00618A?style=for-the-badge&logo=mysql&logoColor=white"/>
  <img src="https://img.shields.io/badge/JWT-Auth-blueviolet?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/REST-API-orange?style=for-the-badge"/>
</p>

<br/>

📦 **Product → 🧪 QC/Staging → 🔢 Batch → 📦 Pallet → 💰 Sales**  
A fully traceable, enterprise-ready warehouse flow.

</div>

---

# 🌟 **Overview**

This project is a **complete warehouse lifecycle management system** built with **FastAPI**, **SQLAlchemy**, and **MySQL**.

It handles the entire flow:

- 📦 **Product creation**
- 🧪 **Staging (QC) before accepting stock**
- 🔢 **Batch creation & expiry tracking**
- 📦 **Pallet allocation & stock distribution**
- 🎯 **Accurate FIFO/FEFO auto-deduction during sales**
- 🧹 **Auto pallet cleaning — removes pallet link when empty**
- 🧍 **Consumer tracking**
- 💸 **Product pricing (MRP/MWP)**
- 🏬 **Warehouse-level stock control**

The system ensures **full traceability** from *incoming goods → QC → batch → pallet → sales*.

---

# 🚀 **Features at a Glance**

### 🧪 **Staging (QC)**
Incoming goods are first placed into **staging** for quality control before entering real inventory.

### 🔢 **Batch Management**
Each batch contains:
- Quantity  
- Expiry date  
- Manufacturing date  
- Linked product  

### 📦 **Pallet Allocation**
Distribute batch stock into multiple pallets.

Example:  
Batch of **100 units**  
→ Pallet A (60)  
→ Pallet B (40)

### 🎯 **FIFO / FEFO Auto Deduction**
During sales:
- FIFO = First In First Out  
- FEFO = First Expiry First Out  

System automatically selects correct **batch + pallet**.

### 🧹 **Auto Pallet Cleaner**
When pallet stock reaches **0**, system automatically removes the pallet entry.

### 🧍 **Consumer Tracking**
Sales are linked to consumers:
- name  
- phone  
- address  
- company  

### 💸 **Dynamic Pricing System**
MRP, MWP — with optional **price history**.

=====================================================================

LOCAL DEVELOPMENT SETUP (FROM SCRATCH)

=====================================================================

PREREQUISITES

Install the following on your system:

- Python 3.11 or higher
- MySQL 8.0 or higher
- Git

Verify installation:

python --version
mysql --version
git --version

=====================================================================

CLONE THE REPOSITORY

git clone <REPO_URL>
cd <PROJECT_FOLDER>

=====================================================================

CREATE AND ACTIVATE VIRTUAL ENVIRONMENT

Windows:
python -m venv virtual
virtual\Scripts\activate

macOS / Linux:
python3 -m venv virtual
source virtual/bin/activate

You should now see (virtual) in your terminal.

=====================================================================

INSTALL DEPENDENCIES

pip install --upgrade pip
pip install -r requirements.txt

=====================================================================

MYSQL SETUP

Start MySQL Service

Windows:
net start MySQL80

Linux / macOS:
sudo service mysql start

Login to MySQL as root:

mysql -u root -p

Create database:

CREATE DATABASE warehouse_db;

Create application user:

CREATE USER 'warehouse_user'@'localhost' IDENTIFIED BY 'warehouse123';

Grant permissions:

GRANT ALL PRIVILEGES ON warehouse_db.* TO 'warehouse_user'@'localhost';
FLUSH PRIVILEGES;

Verify database access:

Exit MySQL, then run:
mysql -u warehouse_user -p warehouse_db

If login succeeds, database setup is correct.

=====================================================================

ENVIRONMENT VARIABLES

Create a file named .env in the project root.

Ask the developer for .env content

NOTE:
.env is ignored via .gitignore and must never be committed.

=====================================================================

RUN THE APPLICATION

Database tables are created automatically on startup.

uvicorn app.main:app --reload

=====================================================================

ACCESS THE APPLICATION

Backend API:
http://127.0.0.1:8000

Swagger API Docs:
http://127.0.0.1:8000/docs

=====================================================================

COMMON ISSUES

Database access denied:
- Check database name in .env
- Check MySQL GRANT permissions

Module not found:
- Ensure virtual environment is activated

Environment variables not loading:
- Ensure .env exists in project root

=====================================================================

STOP THE SERVER

CTRL + C

=====================================================================

SETUP COMPLETE

The backend is now running locally.
