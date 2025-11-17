🏭 Warehouse Inventory Management System
Powered by FastAPI • SQLAlchemy • MySQL

A complete backend system that manages:

✔ Product lifecycle
✔ Staging (QC) workflow
✔ Batch management
✔ Pallet allocation
✔ FIFO / FEFO stock deduction
✔ Consumer tracking
✔ Sales tracking
✔ Pricing system
✔ Warehouse-level inventory

✨ Features
📌 Inventory Management

Products → Batches → Pallets → Sales

Real-time stock tracking

Prevents negative inventory

Auto-remove empty pallet allocations

🧪 Staging (QC) Flow

Goods arrive → placed in staging

QC approval required before entering inventory

Ensures clean traceability

🎯 Sales Engine

FIFO (First In First Out) support

FEFO (First Expire First Out) support

Multi-pallet quantity deduction

Automatic batch & pallet adjustments

👥 Consumer Management

Stores consumer details (name, contact, company, address)

Links each sale to a consumer

💰 Pricing Module

MRP & MWP per product

Supports historical price updates

🛠 Tech Stack
Layer	Technology
Backend	FastAPI
ORM	SQLAlchemy
DB	MySQL
Auth	JWT
Format	REST JSON
Testing Tools	Postman / ThunderClient
📁 Project Structure
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
 ├── schemas/
 └── main.py

🔄 System Flow (High-Level)
Goods Arrive
    ↓
Staging → QC
    ↓ (QC pass)
Create Batch
    ↓
Assign to Pallets
    ↓
Make Sale (FIFO / FEFO)
    ↓
Auto-deduct from pallets + batch

🧩 Core Logic Explained
🟦 1. Staging → QC

Goods first enter staging.
QC must be marked passed before a batch can be created.

🟨 2. Batch Creation

Batch includes:

batch_no

manufacture_date

expiry_date

total quantity

product reference

🟥 3. Pallet Allocation

Batch quantity can be split across pallets:
Example:

Pallet	Qty
A	60
B	40

Stored in batch_pallet.

🟩 4. Sales Engine (FIFO / FEFO)
FIFO = stock stored earlier is sold first

Sorted by:

stored_on ASC

FEFO = stock expiring earlier is sold first

Sorted by:

expiry_date ASC

Deduction Loop Automatically:

Deduct from batch_pallet.quantity_left

Deduct from batch.quantity

Create multiple sales rows (if needed)

Remove pallet link if empty

🔌 API Testing Flow (Sample)
1️⃣ Create Warehouse
POST /warehouse/
{
  "name": "Main Warehouse",
  "location": "Cochin",
  "address": "NH-47"
}

2️⃣ Create Product
POST /products/
{
  "prod_id": "P100",
  "name": "Wheat Flour",
  "sku": "WF-10KG"
}

3️⃣ Staging Entry
POST /staging/
{
  "product_id": 1,
  "warehouse_id": 1
}

4️⃣ QC Approval
PUT /staging/1/qc
{
  "qc_done": true
}

5️⃣ Create Batch
POST /batches/
{
  "batch_no": "B1",
  "product_id": 1,
  "manufacture_date": "2025-01-01",
  "expiry_date": "2026-01-01",
  "quantity": 100,
  "sku": "WF-10KG"
}

6️⃣ Create Pallets
POST /pallets/
{
  "pallet_id": "PAL-A",
  "warehouse_id": 1
}

POST /pallets/
{
  "pallet_id": "PAL-B",
  "warehouse_id": 1
}

7️⃣ Allocate Quantity
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

8️⃣ Add Consumer
POST /consumer/
{
  "name": "ABC Retailer",
  "phone": "9876543210"
}

9️⃣ Make a Sale
POST /sales/
{
  "product_id": 1,
  "consumer_id": 1,
  "quantity_sold": 70,
  "sale_price": 450,
  "fifo": true
}

Backend does:

✔ 60 from PAL-A
✔ 10 from PAL-B
✔ Auto remove empty PAL-A entry
✔ Batch quantity becomes 30
✔ Creates 2 sales rows

🛡 Error Prevention

❌ Prevents negative stock
❌ Prevents deleting sales (to avoid corruption)
❌ Validates consumer, batch, pallet before sale
❌ Validates QC before batch creation

🚀 Future Improvements

Sales return module

Warehouse transfer module

QR/Barcode inventory scanning

Admin analytics dashboard

Pallet capacity validation
