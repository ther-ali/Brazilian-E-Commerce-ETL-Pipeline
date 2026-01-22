# Brazilian E-Commerce ETL Data Pipeline

This project implements a robust **Extract, Transform, Load (ETL)** pipeline for the Olist Brazilian E-Commerce dataset. Designed for Linux-based environments, it processes over 100k anonymized order records, normalizes them, and warehouses them into a relational SQLite database.

## 📖 Dataset Description

**Source:** Brazilian E-Commerce Public Dataset by Olist

This dataset contains information on 100k orders from 2016 to 2018 made at multiple marketplaces in Brazil. Its features allow viewing an order from multiple dimensions: order status, price, payment, freight performance, customer location, product attributes, and reviews.

**Context:**
* **Real Commercial Data:** Provided by Olist, the largest department store in Brazilian marketplaces.
* **Anonymization:** Real commercial data has been anonymized. Company and partner names in review texts were replaced with names of *Game of Thrones* great houses.
* **Workflow:** When a customer purchases from the Olist Store, a seller is notified to fulfill the order. The customer receives a satisfaction survey via email upon delivery.

**Key Constraints:**
1.  An order might have multiple items.
2.  Each item might be fulfilled by a distinct seller.

---

## ✅ Requirements

To successfully run this pipeline, ensure your environment meets the following criteria:

* [cite_start]**Operating System:** Linux-based system (Ubuntu, Debian, CentOS, etc.) 
* **Python:** Version 3.x
* **Database:** SQLite3 (Pre-installed on most Linux distros)
* **Python Libraries:**
    * [cite_start]`pandas` (For data manipulation) 
    * [cite_start]`sqlite3` (Standard library for database connection) 
    * [cite_start]`logging` (Standard library for tracking execution) 
    * [cite_start]`glob`, `os`, `pathlib` (Standard libraries for file handling) 

## 📦 Setup & Installation

**Note:** This repository contains the source code for the ETL pipeline. The raw data files and the generated SQLite database file are **not included** due to size restrictions. You must generate the database locally by following these steps.

### 1. Prepare the Data
1.  Download the dataset (e.g., from Kaggle or your source).
2.  Place the CSV files into the `dataset/` folder in the project root.
    * *Ensure the folder contains:* `dataset/olist_orders_dataset.csv`, `dataset/olist_customers_dataset.csv`, etc.

### 2. Create the Database Schema
The repository includes an SQL script to generate the empty database schema with all necessary tables and relationships. Run this command in your terminal:

```bash
sqlite3 olist_db < sql/SQL_script.sql
