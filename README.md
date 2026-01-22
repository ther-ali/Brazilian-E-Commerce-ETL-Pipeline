# Brazilian E-Commerce ETL Pipeline

This project implements an **Extract, Transform, Load (ETL)** data engineering pipeline for the **Brazilian E-Commerce Public Dataset by Olist**. Ideally suited for Linux environments, this project processes over 100k anonymized order records, normalizes the data, and loads it into a relational SQLite database.

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

## 📂 Project Structure

The project is organized into the following directory structure:

```text
.
├── dataset/                     # Directory for source CSV files
├── python/
│   └── etl_pipeline.py          # Python script for extraction and loading 
├── sql/
│   └── db_creation.sql          # SQL script for database schema and DDL 
├── scheduler/
│   └── schedule_steps.txt       # Instructions for automating the job via Cron
├── ETL_log.log                  # Execution logs 
└── olist_db                     # Target SQLite database
