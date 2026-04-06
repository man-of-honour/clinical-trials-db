# Clinical Trials Database

A portfolio project focused on relational database design, synthetic data generation, and analytical SQL queries for clinical-trial reporting.

This project demonstrates how to design a normalized database, populate it with generated data, validate analytical queries, and produce a final report in CSV format.

---

## Project Overview

The goal of the project is to build a small clinical-trials data pipeline from scratch:

- design a relational database for patients, trials, and measurements;
- create SQL scripts for schema creation;
- generate realistic test data with Python;
- write analytical SQL queries to compare placebo and active-drug results;
- produce a final aggregated report in CSV format.

The database uses **SQLite**, and the project includes both SQL and Python components.  
The connection string points to a local SQLite file.

---

## Tech Stack

- **SQL**
- **SQLite**
- **Python**
- **SQLAlchemy** (used in tests)
- **Pandas** (used to read the final CSV report in validation)

---

## Database Schema

The project contains three core tables:

### `patients`
Stores patient demographic and baseline condition data.

- `patient_id` — primary key  
- `name`  
- `age`  
- `gender`  
- `condition`  

### `trials`
Stores clinical-trial metadata.

- `trial_id` — primary key  
- `trial_name`  
- `start_date`  
- `end_date`  

### `measurements`
Stores patient measurements collected during trials.

- `measurement_id` — primary key  
- `patient_id` — foreign key → `patients`  
- `trial_id`   — foreign key → `trials`  
- `measurement_date`  
- `drug`  
- `condition_score` (0 – 100)

---

## Features

### 1. Database creation
`create.sql` defines the full schema, including primary / foreign keys and a constraint on `condition_score`.

### 2. Synthetic data generation
`generate_data.py` fills the database with randomized but structured data:

- 30 patients  
- 6 clinical trials  
- 360 measurements  
- placebo / active-drug groups in each trial  
- three measurements per patient over trial dates  

The generator adds a mild improvement trend for active drugs vs placebo, making the analytical queries meaningful.

### 3. Analytical SQL queries
`answers.py` contains two analytical tasks:

1. Average condition-score difference (active drug − placebo) per trial, ordered by start date.  
2. Difference in score change (first → last measurement) between active drug and placebo for each trial.

### 4. Final report generation
`report.sql` produces a trial-level CSV report including:

- number of participants  
- gender distribution  
- average age  
- average placebo score  
- average active-drug score  
- trial name  

---

## Repository Structure

```text
.
├── clinical_trials.db
├── conn.txt
├── create.sql
├── generate_data.py
├── answers.py
├── report.sql
├── test.py
├── trial_statistics.csv
└── README.md
```

---

## How to Run

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <your-repo-name>
```

### 2. Create the database schema

Run the SQL from `create.sql` against your SQLite database.

```bash
sqlite3 clinical_trials.db < create.sql
```

### 3. Generate test data

```bash
python generate_data.py
```

### 4. Run validation tests

Install dependencies first:

```bash
pip install pandas sqlalchemy
```

Then run:

```bash
python test.py
```

The test file checks:

- database connection  
- existence and usability of the schema  
- minimum number of patients and measurements  
- correctness of both analytical SQL queries  

---

## Analytical Tasks

### Task 1 — Average placebo vs active-drug difference
For each trial, calculate the difference between:

- average `condition_score` for the active drug  
- average `condition_score` for placebo  

Results are ordered by trial start date.

### Task 2 — First-to-last measurement comparison
For each trial:

- calculate the score change from the earliest to the latest measurement for placebo  
- calculate the same change for the active drug  
- subtract the placebo change from the active-drug change  

This yields a simple trial-level estimate of treatment effect relative to placebo.

---

## What This Project Demonstrates

- relational database design  
- SQL DDL and query writing  
- synthetic dataset generation  
- analytical thinking with SQL  
- test-driven validation of query results  
- transforming an educational task into portfolio-ready engineering work  

---

## Possible Improvements

- add Docker setup for easier reproducibility  
- include an ER diagram in the repository  
- add indexes and compare query performance  
- extend the report with per-trial outcome trends  
- add a Jupyter notebook for exploratory analysis and visualizations  
- support PostgreSQL in addition to SQLite  