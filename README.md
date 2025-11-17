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

It handles:

- 📦 Product creation  
- 🧪 Staging/QC  
- 🔢 Batch creation  
- 📦 Pallet allocation  
- 🎯 FIFO/FEFO sales deduction  
- 🧹 Auto pallet cleanup  
- 🧍 Consumer tracking  
- 💸 Pricing (MRP, MWP)  
- 🏬 Warehouse-level stock control  

Fully traceable from **incoming goods → QC → batch → pallet → sales**.

---

# 🏗️ **Architecture Diagram**

```mermaid
flowchart LR
    A[Staging (QC)] --> B[Batch Creation]
    B --> C[Pallet Allocation]
    C --> D[Inventory Database]
    D --> E[Sales API]
    E --> F[FIFO / FEFO Deduction]
    F --> G[Auto Pallet Cleaner]
    G --> H[Reports & Traceability]
📘 ER Diagram
mermaid
Copy code
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
bash
Copy code
pip install -r requirements.txt
Create MySQL database:
sql
Copy code
CREATE DATABASE warehouse_system;
Create .env file:
ini
Copy code
DB_USER=root
DB_PASS=yourpassword
DB_HOST=localhost
DB_PORT=3306
DB_NAME=warehouse_system
JWT_SECRET=supersecret
🗂️ Folder Structure
css
Copy code
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

System will automatically:

Deduct using FIFO/FEFO

Update batch + pallet

Auto-clean empty pallets

🚀 Future Enhancements
AI-powered stock forecasting

Barcode / QR code printing

Warehouse-to-warehouse transfer

Expiry alerts & notifications

<div align="center">
⭐ If this project helps you, please give it a GitHub Star!
Your support motivates future updates 😊

</div> ```
