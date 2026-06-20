# Fintech Portfolio Pipeline

Hey there! Welcome to my end-to-end data engineering pipeline. I built this project to simulate how modern fintech platforms ingest market data, organize it in a robust relational database, and run complex analytical transformations to extract actual portfolio insights. 

Instead of just building a simple script, I wanted to tackle the whole lifecycle: dealing with API data structures, managing state dependencies in an orchestrator, handling database injection, and writing heavy-hitting analytical SQL.

---

## The Architecture (How It Works)

The pipeline is split into three clean, modular phases:

1. **Extract (`extract/api_extractor.py`)**: Pulls raw market and financial data from live endpoints, validates the payloads, and stages them locally.
2. **Load (`database/db_loader.py` & `main.py`)**: Initializes a PostgreSQL engine using SQLAlchemy, sets up our tracking schemas, and handles bulk loading. If something breaks halfway through, custom exception handling keeps it from corrupting the state.
3. **Transform (`sql/transforms/`)**: Once the raw data is safely in Postgres, this is where the real analytical heavy lifting happens.

---

## The Tech Stack

* **Language:** Python 3.x
* **Database:** PostgreSQL
* **Libraries:** SQLAlchemy, Pandas, Requests
* **Version Control:** Git (managed via a strict feature-branching strategy)

---

## The SQL Deep Dive (The Analytical Engine)

I didn't want to just do basic `SELECT *` queries here. Inside `sql/transforms/`, I implemented advanced SQL patterns to mimic real-world financial calculations:

* **`window_functions.sql`**: Handles running totals, moving averages, and asset ranking using `PARTITION BY` and `OVER` clauses to capture portfolio velocity.
* **`regular_cte.sql`**: Breaks down highly complex multi-stage financial calculations into clean, readable logical blocks.
* **`recursive_cte.sql`**: Simulates hierarchical data tracking—perfect for looking at layered portfolio fee structures or compounding returns over iterative periods.
* **`olap_queries.sql`**: Uses multidimensional aggregations (`ROLLUP`, `CUBE`) to generate instant summary slices across different sectors and timeframes.

---

## How to Spin It Up Locally

If you want to pull this down and run it on your machine, here's the quick start:

1. **Clone the repo:**
```bash
   git clone [https://github.com/YOUR_USERNAME/fintech_pipeline.git](https://github.com/YOUR_USERNAME/fintech_pipeline.git)
   cd fintech_pipeline