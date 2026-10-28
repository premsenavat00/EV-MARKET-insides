# Electric Vehicle Market Performance & Insights

A complete, production-ready, full-stack web analytics platform designed to evaluate global electric vehicle performance, manufacturing distribution, battery technology adoption, and customer satisfaction.

Built with **Python**, **Flask**, **SQLite**, **Bootstrap 5**, and **Chart.js**.

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Problem Scenarios & Personas](#problem-scenarios--personas)
3. [Architecture & Project Structure](#architecture--project-structure)
4. [Database Schema & Design](#database-schema--design)
5. [SQL Operations & Analytical Queries](#sql-operations--analytical-queries)
6. [Web Application Features](#web-application-features)
7. [Installation & Setup](#installation--setup)
8. [Running the Application](#running-the-application)
9. [Running Verification Tests](#running-verification-tests)
10. [REST API Documentation](#rest-api-documentation)

---

## Project Overview

The global transition to electric mobility involves complex trade-offs between battery chemistry, manufacturing geography, driving range, vehicle pricing, and consumer satisfaction. This application serves as an executive decision platform that bridges raw data with strategic insights across three key business disciplines.

---

## Problem Scenarios & Personas

The application addresses three distinct stakeholder personas:

### 1. Emily Johnson — EV Market Strategy Director
* **Core Focus:** Battery technology adoption, chemistry market share, charging infrastructure readiness.
* **Key Questions Addressed:**
  - What is the market share of **LFP**, **NMC**, **NCA**, and emerging **Solid-State** batteries?
  - How does battery chemistry correlate with average driving range, capacity, and DC fast-charging speeds?
  - Which battery tech provides the optimal trade-off between price and fleet scalability?
* **Application Features:**
  - Battery Chemistry Sales Share Doughnut chart.
  - Peak Fast-Charging (kW) vs. Battery Capacity (kWh) grouped analysis.
  - High-Efficiency Fleet Leaders table (DC Fast Charge $\ge 150\text{ kW}$).

### 2. David Chen — Business Intelligence Manager
* **Core Focus:** Global manufacturing distribution, regional production scale, OEM market share, export pricing.
* **Key Questions Addressed:**
  - Which nations dominate global EV output (China, USA, Germany, South Korea, India, Japan, France)?
  - How do top automotive OEMs (BYD, Tesla, Volkswagen, Hyundai, Ola Electric) divide production across domestic and international gigafactories?
  - What are the average price tiers by manufacturing country?
* **Application Features:**
  - Top 10 Manufacturers by Annual Sales volume bar chart.
  - Manufacturing Country Output distribution chart.
  - Country Manufacturing Intelligence Matrix & OEM Footprint table.

### 3. Dr. Sarah Williams — Sustainable Mobility Research Analyst
* **Core Focus:** Driving range economics, range-anxiety mitigation, customer satisfaction ratings.
* **Key Questions Addressed:**
  - What is the empirical relationship between vehicle MSRP and certified driving range?
  - Does higher driving range or fast charging directly drive higher customer ratings?
  - Which EVs deliver the best "Range-per-Dollar" value (lowest cost per km of range)?
* **Application Features:**
  - Interactive **Driving Range (km) vs. Price (USD)** Scatter Plot with per-model inspection.
  - Customer Satisfaction Brackets vs. Average Range analysis.
  - Top 5 "Range-per-Dollar" Value Champions table.

---

## Architecture & Project Structure

```
EV MARKET/
├── app.py              # Flask backend application with routing & API endpoints
├── db.py               # SQLite database setup, seeding & SQL query operations
├── database.db         # SQLite database file (indexed)
├── test_app.py         # Automated test suite (9 test cases covering DB & Web APIs)
├── requirements.txt    # Project dependencies
├── README.md           # Full project documentation
├── templates/          # Jinja2 HTML templates (Bootstrap 5 UI)
│   ├── base.html       # Base layout with navbar, footer & theme scripts
│   ├── index.html      # Executive Dashboard with high-level KPIs & multi-metric charts
│   ├── personas.html   # Dedicated analytical views for Emily, David, and Sarah
│   ├── vehicles.html   # Interactive Vehicle Catalog with search, filters & spec modal
│   └── sql_console.html# SQL queries documentation & database schema reference
└── static/             # Client-side static assets
    ├── css/
    │   └── style.css   # Modern cyber-electric glassmorphism styling
    └── js/
        └── dashboard.js# Chart.js defaults & UI helpers
```

---

## Database Schema & Design

The platform uses a relational SQLite database (`database.db`) with an optimized `vehicles` table:

```sql
CREATE TABLE vehicles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    manufacturer TEXT NOT NULL,
    model TEXT NOT NULL,
    vehicle_category TEXT NOT NULL CHECK(vehicle_category IN ('Hatchback', 'Sedan', 'SUV', 'Two-Wheeler')),
    battery_technology TEXT NOT NULL CHECK(battery_technology IN ('LFP', 'NMC', 'NCA', 'Solid-State')),
    battery_capacity REAL NOT NULL,     -- Battery pack size in kWh
    driving_range INTEGER NOT NULL,      -- Real-world rated range in km
    price REAL NOT NULL,                 -- MSRP base retail price in USD
    charging_speed INTEGER NOT NULL,     -- Peak DC fast charge in kW
    manufacturing_country TEXT NOT NULL,
    customer_rating REAL NOT NULL,       -- Verified owner rating (1.0 to 5.0)
    annual_sales INTEGER NOT NULL,       -- Annual units sold
    efficiency REAL NOT NULL,            -- Consumption in kWh per 100 km
    release_year INTEGER NOT NULL
);

-- Analytical Indexes
CREATE INDEX idx_battery ON vehicles(battery_technology);
CREATE INDEX idx_category ON vehicles(vehicle_category);
CREATE INDEX idx_country ON vehicles(manufacturing_country);
CREATE INDEX idx_manufacturer ON vehicles(manufacturer);
CREATE INDEX idx_price ON vehicles(price);
```

### Dataset Composition
The database includes **65 realistic and diverse records** modeled after real-world production EVs and next-gen prototypes across:
- **Categories:** SUVs (Tesla Model Y, BYD Atto 3, Hyundai Ioniq 5, Rivian R1S), Sedans (Tesla Model 3, BYD Seal, BMW i4, Lucid Air, Mercedes EQS), Hatchbacks (BYD Dolphin, VW ID.3, MG4 EV, Renault 5, Tata Tiago EV), Two-Wheelers (Ola S1 Pro, Ather 450X, Zero DSR/X, BMW CE 04).
- **Chemistries:** LFP (Lithium Iron Phosphate), NMC (Nickel Manganese Cobalt), NCA (Nickel Cobalt Aluminum), Solid-State.
- **Hubs:** China, USA, Germany, South Korea, India, Japan, Sweden, France, UK, Italy.

---

## SQL Operations & Analytical Queries

The `db.py` module encapsulates clean, parameterized, SQL-injection-safe queries:

### 1. Key Performance Indicators (KPIs)
```sql
SELECT
    COUNT(*) as total_models,
    COALESCE(SUM(annual_sales), 0) as total_sales,
    COALESCE(AVG(driving_range), 0) as avg_range,
    COALESCE(AVG(customer_rating), 0) as avg_rating,
    COALESCE(AVG(price), 0) as avg_price,
    COALESCE(AVG(charging_speed), 0) as avg_charging_speed
FROM vehicles;
```

### 2. Battery Tech Adoption & Metrics (Emily Johnson)
```sql
SELECT
    battery_technology,
    COUNT(*) as model_count,
    ROUND(AVG(driving_range), 1) as avg_range,
    ROUND(AVG(battery_capacity), 1) as avg_capacity,
    ROUND(AVG(charging_speed), 1) as avg_charging_speed,
    ROUND(AVG(price), 2) as avg_price,
    SUM(annual_sales) as total_sales
FROM vehicles
GROUP BY battery_technology
ORDER BY total_sales DESC;
```

### 3. Manufacturing Country Output (David Chen)
```sql
SELECT
    manufacturing_country,
    COUNT(DISTINCT manufacturer) as distinct_manufacturers,
    COUNT(*) as total_models,
    SUM(annual_sales) as total_sales,
    ROUND(AVG(price), 2) as avg_price,
    ROUND(AVG(driving_range), 1) as avg_range
FROM vehicles
GROUP BY manufacturing_country
ORDER BY total_sales DESC;
```

### 4. Satisfaction Brackets & Range Economics (Dr. Sarah Williams)
```sql
SELECT
    CASE
        WHEN customer_rating >= 4.7 THEN '4.7 - 5.0 (Elite)'
        WHEN customer_rating >= 4.4 THEN '4.4 - 4.6 (Very High)'
        WHEN customer_rating >= 4.0 THEN '4.0 - 4.3 (Good)'
        ELSE 'Under 4.0 (Moderate)'
    END as rating_bracket,
    COUNT(*) as model_count,
    ROUND(AVG(driving_range), 1) as avg_range,
    ROUND(AVG(charging_speed), 1) as avg_charging,
    SUM(annual_sales) as bracket_sales
FROM vehicles
GROUP BY rating_bracket
ORDER BY avg_range DESC;
```

---

## Web Application Features

1. **Executive Dashboard (`/`):**
   - KPI counters for global sales, range, ratings, top manufacturer, and peak charging.
   - Interactive Chart.js charts with real-time tooltips and legend controls.
   - Quick filter toolbar with live parameter propagation.

2. **Persona Workspaces (`/personas`):**
   - Interactive tabbed interface dedicated to **Emily Johnson**, **David Chen**, and **Dr. Sarah Williams**.
   - Tailored charts, comparative metrics tables, and strategic insight callouts.

3. **Vehicle Catalog (`/vehicles`):**
   - Dynamic multi-parameter filtering (Battery Tech, Category, Country, Max Price, Search).
   - Multi-column sorting (Sales, Range, Price, Rating, Charging Speed, Capacity).
   - Pagination controls with responsive layout.
   - Specification modal popup for deep-dive technical specs.
   - Instant "Export to CSV" button.

4. **SQL Operations Reference (`/sql-console`):**
   - Detailed schema reference table and exact SQL statements mapped to each problem scenario.

---

## Installation & Setup

### Prerequisites
- Python 3.10, 3.11, 3.12, or 3.13
- Git (optional)

### Step 1: Clone or Navigate to the Workspace
```bash
cd "c:\Users\prems\OneDrive\Desktop\EV MARKET"
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Initialize the SQLite Database
```bash
python db.py
```
*(The database will also automatically initialize on first launch if not already present.)*

---

## Running the Application

Start the Flask development server:
```bash
python app.py
```

Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## Running Verification Tests

To run the automated test suite verifying database logic, analytical queries, and Flask routes:
```bash
python test_app.py
```

Expected output:
```
Ran 9 tests in 0.129s

OK
```

---

## REST API Documentation

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/analytics` | Returns real-time KPI metrics, chart datasets, and persona insights in JSON format. Supports filter query params (`battery_technology`, `vehicle_category`, `manufacturing_country`, `max_price`, `search`). |
| `GET` | `/api/vehicle/<id>` | Returns detailed technical specifications for a single EV by primary key ID. |
| `GET` | `/api/export-csv` | Generates and downloads a CSV export of the currently filtered dataset. |
