# Rohith Sagar Karnala

**Senior Data Engineer | Cloud Architect | Healthcare & FinTech Specialist**
<br/>
[<img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" />](https://www.linkedin.com/in/rohithsagar) &nbsp;
[<img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" />](https://github.com/rohitsagar363) &nbsp;
[<img src="https://img.shields.io/badge/View_Resume-PDF-D14836?style=for-the-badge&logo=adobeacrobatreader&logoColor=white" />](https://github.com/rohitsagar363/rohitsagar363.github.io/blob/main/Rohith_Karnala_Data_Engineer.pdf) *(Note: Upload your PDF resume to this repository and link it here)*

---

### About Me

I am a Data Engineer with over 4 years of specialized experience building scalable data ecosystems, particularly in complex, regulated domains like healthcare and finance.

My expertise is in architecting end-to-end data solutions, from ingestion and processing to modeling and visualization. I have architected HIPAA-compliant lakehouses on **Azure** for clients like Humana, and I've led large-scale migrations on **AWS** for Bristol Myers Squibb.

My core technical strength is in building metadata-driven frameworks using **PySpark**, and then modeling that data for high-performance analytics using tools like **dbt** and **Snowflake**. I am passionate about building robust, reliable, and cost-efficient platforms that turn complex data into actionable insights.

---

## 1. Enterprise Case Studies (Proprietary Work)

This section details my architectural contributions to large-scale, enterprise-grade data platforms. Code is proprietary, but the architecture and problem-solving process are my own.

---

### Case Study 1: Enterprise Healthcare Analytics Lakehouse

* **Client:** A Major US Healthcare Provider
* **Technologies:** Azure (Databricks, ADF, Synapse), Snowflake, dbt, PySpark, Power BI, Terraform

**The Business Problem:**
The client had over 5 terabytes of critical healthcare data (claims, provider, patient) locked in siloed, on-premise systems. Analytics was slow, data governance was difficult, and the business had no way to get real-time insights on key metrics like "cost-of-care" or provider performance.

**My Role:**
As the lead data engineer, I architected and co-built a new, HIPAA-compliant data lakehouse on Azure. My responsibility was to design the end-to-end data flow, from raw ingestion to the final Power BI dashboard.

**The Architectural Solution:**



[Image of an Azure Data Lakehouse Medallion Architecture]


I designed and implemented a **Medallion Architecture** to ensure data quality and traceability:
1.  **Ingestion (Bronze):** Used **Azure Data Factory (ADF)** to ingest raw data from 40+ sources (SQL, SFTP, APIs) into Azure Data Lake Storage (ADLS) as the "Bronze" layer.
2.  **Transformation (Silver):** Developed **PySpark** jobs in **Databricks** to clean, validate, and conform the raw data. This is where I implemented critical **SCD Type-2 logic** (using Delta MERGE) to track historical changes for claims and providers.
3.  **Modeling (Gold):** The conformed "Silver" data was loaded into **Snowflake**. I then used **dbt** to build the "Gold" layer—a series of high-performance, business-ready star-schema data models.
4.  **CI/CD:** The entire platform was built using **Terraform** (Infrastructure-as-Code) and deployed via **GitHub Actions** for a fully automated, testable, and reliable process.

**The Business Impact:**
The new platform **improved query performance by 40%** and provided the business with a single source of truth. The dbt-modeled data in Snowflake allowed business analysts to get **real-time, interactive insights** on their most important KPIs for the first time.

---

### Case Study 2: Large-Scale ETL Migration & Framework (In Progress)

* **Client:** A Global Pharmaceutical Company
* **Technologies:** AWS, PySpark, PostgreSQL, Oracle
* **The Problem:** The client had 450+ brittle, legacy ETL pipelines that were slow and difficult to maintain.
* **My Solution:** I led the migration of all 450+ pipelines to a modern PySpark-based platform. To do this, I **engineered a config-driven PySpark framework** that dynamically generated ETL code from metadata. This framework reduced manual development by **60%** and allowed our 15-member team to complete the migration with 100% accuracy.

---

### Case Study 3: Secure FinTech API & Data Platform (In Progress)

* **Client:** A Major Financial Institution
* **Technologies:** Python (FastAPI), PySpark, AWS, OAuth2
* **The Problem:** The client needed to securely ingest and unify data from dozens of banking schemas (transactions, KYC, credit) via APIs.
* **My Solution:** I designed and built a series of **secure FastAPI microservices** for data ingestion, handling OAuth2/JWT authentication. I also engineered a **metadata-driven schema mapping framework** in PySpark that cut data reconciliation effort by **40%**.

---

## 2. Public Prototypes & Tech Labs

This section contains my open-source projects, built to demonstrate specific technical concepts and coding standards.

---

### Project 1: Resilient Asynchronous API Ingestion Framework

This project demonstrates a production-ready solution for a common data engineering challenge: fetching large amounts of data from a rate-limited API, fast and reliably.

* **Problem:** How do you reliably ingest data from an API that requires token refreshes and will rate-limit you (`429` errors) if you're too aggressive?
* **Solution:** This prototype is a Python framework using **`asyncio`** for high-concurrency I/O. It features a thread-safe `TokenManager` class to automatically handle **OAuth 2.0 token refreshes** and a robust **retry mechanism** with exponential backoff for `429` and `5xx` errors.
* **[View on GitHub](https://github.com/rohitsagar363/talkdesk-async-etl)**

---

### Project 2: Low-Latency Machine Learning Inference

This project explores real-time audio processing and machine learning classification, focusing on high-throughput, low-latency architecture.

* **Problem:** How do you build a system that can ingest a real-time stream of data (like audio) and run an ML model on it with minimal delay?
* **Solution:** This prototype uses a queue-based architecture to process audio signals, run classification, and disambiguate sounds in real-time. It's an exploration of the systems design required for real-time ML inference.
* **[View on GitHub](https://github.com/rohitsagar363/Low-latency-Sound-Disambiguator)**

---

### Future Prototypes (Coming Soon)

I am always building. This is where I will add new, focused prototypes to showcase skills in:
* `dbt`: Building a complete dbt project from scratch.
* `Snowflake`: Advanced stream processing and data sharing.
* `FastAPI`: Building a secure, documented API for an ML model.

---
