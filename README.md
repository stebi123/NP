📦 Warehouse Inventory Management System
Built with FastAPI, SQLAlchemy, MySQL

This project is a complete warehouse inventory management system that handles:

Product lifecycle (product → batch → pallet → sales)

Staging (QC) process before goods enter inventory

Stock allocation to pallets

FIFO / FEFO sales deduction

Consumer tracking

Pricing system

Warehouse-level inventory control

It provides full traceability from incoming goods → QC → batch creation → pallet allocation → sales.

🚀 Tech Stack
Layer	Technology
Backend	FastAPI
ORM	SQLAlchemy
Database	MySQL
Auth	JWT
API Format	REST JSON
Testing	Any REST client (Postman, ThunderClient, etc.)
📑 Table of Contents

Prerequisites

Project Architecture

Data Flow Overview

Database Schema Overview

Core Logic Explained

API Flow Examples

FIFO / FEFO Logic

Error Handling & Validation

Future Enhancements

🛠 Prerequisites

Python 3.10+

MySQL Server running locally

Create a database:

CREATE DATABASE np;


Install dependencies:

pip install -r requirements.txt


Start the server:

uvicorn app.main:app --reload

🏗 Project Architecture
app/
 ├── core/
 │    ├── database.py
 │    ├── jwt.py
 │    └── security.py
 ├── models/
 │    ├── batch.py
 │    ├── batch_pallet.py
 │    ├── consumer.py
 │    ├── pallet.py
 │    ├── price.py
 │    ├── products.py
 │    ├── sales.py
 │    ├── staging.py
 │    └── warehouse.py
 ├── routers/
 │    ├── auth.py
 │    ├── batch.py
 │    ├── batch_pallet.py
 │    ├── consumer.py
 │    ├── pallet.py
 │    ├── price.py
 │    ├── products.py
 │    ├── sales.py
 │    ├── staging.py
 │    └── warehouse.py
 ├── schemas/
 └── main.py

🔄 Data Flow Overview
1️⃣ Staging → QC

Goods arrive → Stored temporarily in the staging table.
QC is performed.

If FAIL → goods rejected.

If PASS → moved to Batch creation.

2️⃣ Batch Creation

A batch represents:

manufacturing date

expiry date

batch number

total quantity

3️⃣ Assign Batches to Pallets

Example:

Batch B1 has 100 units

Pallet A → 60 units

Pallet B → 40 units

Stored in batch_pallet table.

4️⃣ Sales (FIFO / FEFO Deduction)

On sale:

System selects pallets based on algorithm:

FIFO → oldest stored pallet

FEFO → nearest expiry batch

Deducts from batch_pallet.quantity_left

Deducts from batch.quantity

Creates Sales rows

Removes pallet link if quantity becomes 0

🗄 Database Schema Overview
Main Tables
Table	Purpose
product	Product master data
warehouse	Warehouse locations
staging	Goods arrival before QC
batch	Batch metadata + quantity
pallet	Pallet metadata
batch_pallet	Maps batch → pallet with quantity_left
consumer	Customer info
price	MRP, MWP with historical dates
sales	Recorded sales history
🧠 Core Logic Explained
Staging & QC

Goods MUST pass QC before entering inventory.
QC creates clean traceability between arrival → batch.

Batch → Pallet Mapping

A batch can be split into multiple pallets.
Each pallet stores:

quantity_left

stored_on timestamp
This timestamp is key for FIFO deduction.

Sales Deduction Logic (EXTREMELY IMPORTANT)
FIFO (First-In-First-Out)

Select pallets ordered by:

stored_on ASC

FEFO (First-Expire-First-Out)

Select pallets ordered by:

batch.expiry_date ASC

Deduction Loop

For each selected pallet:

deduct = min(pallet.quantity_left, required_quantity)
pallet.quantity_left -= deduct
batch.quantity -= deduct
create sales row with deduct value
if pallet.quantity_left == 0:
    delete pallet entry from batch_pallet

🧪 API Flow Examples (Step-by-Step)
1️⃣ Create Warehouse
POST /warehouse/
{
  "name": "Central Storage",
  "location": "Cochin",
  "address": "NH Bypass"
}

2️⃣ Create Product
POST /products/
{
  "prod_id": "P-100",
  "name": "Wheat Flour",
  "sku": "WF-10KG"
}

3️⃣ Staging (goods arrive)
POST /staging/
{
  "product_id": 1,
  "warehouse_id": 1
}

4️⃣ Mark QC Completion
PUT /staging/1/qc
{
  "qc_done": true
}

5️⃣ Create a Batch
POST /batch/
{
  "batch_no": "B1",
  "product_id": 1,
  "manufacture_date": "2025-10-01",
  "expiry_date": "2026-10-01",
  "quantity": 100,
  "sku": "WF-10KG"
}

6️⃣ Create Pallets
POST /pallet/
{
  "pallet_id": "PALLET-A",
  "warehouse_id": 1
}


and

POST /pallet/
{
  "pallet_id": "PALLET-B",
  "warehouse_id": 1
}

7️⃣ Assign Batch to Pallets
POST /batch_pallet/
{
  "batch_id": 1,
  "pallet_id": 1,
  "quantity_left": 60
}

POST /batch_pallet/
{
  "batch_id": 1,
  "pallet_id": 2,
  "quantity_left": 40
}

8️⃣ Create Consumer
POST /consumer/
{
  "name": "ABC Retail",
  "phone": "9876543210"
}

9️⃣ Make a Sale
POST /sales/
{
  "product_id": 1,
  "consumer_id": 1,
  "quantity_sold": 70,
  "sale_price": 425.0,
  "fifo": true
}

Internally:

60 deducted from pallet A

10 deducted from pallet B

pallet A entry deleted

batch.quantity updated to 30

2 sale rows created

⚠ Error Handling & Validation

Batch cannot go negative

Pallet cannot be assigned more than batch quantity

Sale cannot exceed available stock

QC must be done before batch creation

Consumer must exist before sale

Once sale happens → deletion disabled (to prevent stock corruption)

🔮 Future Enhancements

Return-to-supplier (for QC FAIL)

Sales return / reverse stock movement

Multi-warehouse transfers

Barcode / QR integration

Web dashboard analytics

Pallet capacity validation

User activity logging

✅ Conclusion

This repository creates a complete warehouse management backend with:

✔ full stock traceability
✔ FIFO/FEFO inventory logic
✔ staging & QC
✔ pallet-level distribution
✔ clean sales deduction engine
✔ consumer & pricing support
