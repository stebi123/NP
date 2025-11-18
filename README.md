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
