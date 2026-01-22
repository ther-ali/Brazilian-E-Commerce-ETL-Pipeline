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
