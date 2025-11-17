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

---

# 🏗️ **Architecture Diagram**

```mermaid
flowchart LR
    A[🧪 Staging (QC)] --> B[🔢 Batch Creation]
    B --> C[📦 Pallet Allocation]
    C --> D[🗄 Inventory Database]
    D --> E[💰 Sales API]
    E --> F[🎯 FIFO / FEFO Deduction]
    F --> G[🧹 Auto Pallet Cleaner]
    G --> H[📊 Reports & Traceability]

erDiagram
    PRODUCT ||--|{ BATCH : contains
    BATCH ||--|{ BATCH_PALLET : stored_in
    PALLET ||--|{ BATCH_PALLET : holds
    SALES }|--|| PRODUCT : sold_as
    SALES }|--|| CONSUMER : purchased_by
    PRICE ||--|| PRODUCT : price_for
    WAREHOUSE ||--|{ PALLET : located_in
    WAREHOUSE ||--|{ PRODUCT : available_in

🧰 Tech Stack
Backend

FastAPI

SQLAlchemy ORM

Pydantic v2

Uvicorn

Database

MySQL

Security

JWT Authentication

⚙️ Prerequisites

Install dependencies:

pip install -r requirements.txt


Create database:

CREATE DATABASE warehouse_system;


Create .env:

DB_USER=root
DB_PASS=yourpassword
DB_HOST=localhost
DB_PORT=3306
DB_NAME=warehouse_system
JWT_SECRET=supersecret

🗂️ Folder Structure
app/
 ├── core/
 ├── models/
 ├── routers/
 ├── schemas/
 ├── main.py

🔥 Complete Workflow
1️⃣ Create Product

POST /products/

2️⃣ Send Goods to Staging

POST /staging/

3️⃣ Approve & Create Batch

POST /batch/

4️⃣ Allocate Batch to Pallet

POST /batch_pallet/

5️⃣ Add Pricing

POST /price/

6️⃣ Add Consumer

POST /consumer/

7️⃣ Make a Sale

POST /sales/

System will:

Deduct using FIFO/FEFO

Update batch + pallet

Auto clean empty pallets

🚀 Future Enhancements

AI-based stock forecasting

Barcode/QR label printing

Warehouse-to-warehouse transfer

Expiry alerts

<div align="center">
⭐ If this project helps you, please give it a GitHub Star!

Your support motivates future updates 😊

</div> ```
