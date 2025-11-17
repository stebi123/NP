🏭⚡ Warehouse Inventory Management System
A Complete FastAPI + SQLAlchemy + MySQL Inventory & Sales Engine with FIFO/FEFO Logic
<p align="center"> <img src="https://img.shields.io/badge/FastAPI-00A489?style=for-the-badge&logo=fastapi&logoColor=white"/> <img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=python&logoColor=white"/> <img src="https://img.shields.io/badge/MySQL-00618A?style=for-the-badge&logo=mysql&logoColor=white"/> <img src="https://img.shields.io/badge/JWT%20Auth-Security-blueviolet?style=for-the-badge"/> <img src="https://img.shields.io/badge/Architecture-Clean%20MVC-orange?style=for-the-badge"/> </p> <p align="center"> <img width="800" src="https://raw.githubusercontent.com/github/explore/master/topics/warehouse/warehouse.png"/> </p>
🌟 Overview

This system is a complete warehouse lifecycle engine that manages:

📦 Product → 🧪 Staging (QC) → 🔢 Batch → 📦 Pallet → 💰 Sales

with full traceability.

Includes:

✨ FIFO/FEFO auto-deduction
✨ Pallet auto-cleaner
✨ Price engine
✨ Consumer tracking
✨ Full warehouse stock visibility
✨ Razor-sharp API design (FastAPI)

🔥 Top Features
(Styled with Neon Icons & Modern Layout)
Feature	Description
🧪 Staging / QC Layer	Incoming goods undergo quality check before being accepted into inventory.
🔢 Batch Management	Products grouped into batches with expiry, dates, quantity tracking.
📦 Pallet Allocation	Automatic distribution of batch stock into pallets.
🎯 FIFO / FEFO Sales Engine	Auto-deducts stock from the correct pallet & batch.
🧻 Pallet Auto-Cleaner	When pallet stock hits zero → system auto-flags as empty.
🧍 Consumer Tracking	Sales linked with full consumer info (phone, company, address).
💸 Dynamic Pricing Engine	Per-product MRP / MWP with historical price support.
🏬 Warehouse-Level Segregation	Every item strictly belongs to a warehouse.
🏗️ Project Architecture (Visual Diagram)
flowchart LR
    A[🧪 Staging (QC)] --> B[🔢 Batch Creation]
    B --> C[📦 Pallet Allocation]
    C --> D[🗄 Inventory Database]
    D --> E[💰 Sales API]
    E --> F[🔁 FIFO / FEFO Stock Deduction]
    F --> G[🧹 Pallet Auto-Cleaner]
    G --> H[📊 Reports & Traceability]

🗄️ ER Diagram (Entity Relationship Model)
erDiagram
    PRODUCT ||--|{ BATCH : has
    BATCH ||--|{ BATCH_PALLET : mapped_to
    PALLET ||--|{ BATCH_PALLET : contains
    SALES }|--|| PRODUCT : sells
    SALES }|--|| CONSUMER : bought_by
    PRICE ||--|| PRODUCT : priced_for
    WAREHOUSE ||--|{ PRODUCT : stores
    WAREHOUSE ||--|{ PALLET : holds

🛠️ Tech Stack
💻 Backend

FastAPI

SQLAlchemy ORM

Pydantic v2

Uvicorn

🗄 Database

MySQL

Alembic (optional migrations)

🔐 Auth

JWT-Based Access Control

⚙️ Prerequisites

🚀 Install the basics:

Python 3.10+  
MySQL Server  
pip install -r requirements.txt


Create your DB:

CREATE DATABASE warehouse_system;


Update .env:

DB_USER=root
DB_PASS=yourpassword
DB_NAME=warehouse_system
DB_HOST=localhost
DB_PORT=3306
JWT_SECRET=supersecret

📦 Project Folder Structure
app/
 ├── core/
 │    ├── database.py
 │    ├── security.py
 │    ├── jwt.py
 ├── models/
 │    ├── products.py
 │    ├── batch.py
 │    ├── pallet.py
 │    ├── batch_pallet.py
 │    ├── consumer.py
 │    ├── price.py
 │    ├── sales.py
 │    ├── warehouse.py
 │    └── ...
 ├── routers/
 │    ├── products.py
 │    ├── batch.py
 │    ├── pallet.py
 │    ├── staging.py
 │    ├── price.py
 │    ├── sales.py
 │    └── ...
 └── main.py

🔥 System Workflow (Step-by-Step)
1️⃣ Staging (QC Entry)

Goods enter → marked as pending inspection.

2️⃣ Batch Creation

After QC approval → batches created with:
✔ quantity
✔ expiry
✔ manufacturing date
✔ product link

3️⃣ Pallet Allocation

Stock is placed into pallets.
Example:
100 units → pallet A (60) + pallet B (40)

4️⃣ Sales Processing

Sales request contains:

product_id

quantity

consumer_id

sale_price

5️⃣ FIFO / FEFO Deduction

System selects correct batch/pallet automatically:
✔ first expiring batch (FEFO)
✔ first created batch (FIFO)

6️⃣ Auto-Clean Pallet

If pallet reaches 0 stock → system marks it empty.

🧪 Testing the Complete Flow
👉 Create Product

POST /products/

👉 Create Batch

POST /batch/

👉 Allocate to Pallet

POST /batch_pallet/

👉 Add Price

POST /price/

👉 Add Consumer

POST /consumer/

👉 Perform Sale

POST /sales/

System automatically:
✔ Deducts correct stock
✔ Logs sale
✔ Updates pallet
✔ Triggers auto-cleaner

🎯 Screenshots (Placeholder – add yours)
/assets/screens/dashboard.png  
/assets/screens/fifo_flow.png
/assets/screens/sales_entry.png

🚀 Future Enhancements

Automated QR label printing

Warehouse-to-warehouse transfers

Stock forecasting (AI/ML)

Expiry alerts & batch recall

⭐ Show Some Love!

If this project helped you, consider giving it a ⭐ on GitHub 😊
