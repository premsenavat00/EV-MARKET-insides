"""
Database initialization and SQL Operations Module for
Electric Vehicle Market Performance & Insights
"""

import sqlite3
import os
from contextlib import contextmanager
from typing import Dict, Any, List, Optional, Tuple, Generator

DATABASE_NAME = "database.db"

def get_db_path() -> str:
    """Returns the absolute path to the SQLite database file."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, DATABASE_NAME)

@contextmanager
def get_connection() -> Generator[sqlite3.Connection, None, None]:
    """Context manager that creates a database connection with Row factory and ensures it is closed."""
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db(force: bool = False) -> None:
    """Initializes the SQLite database with schema and comprehensive EV dataset."""
    db_path = get_db_path()
    if os.path.exists(db_path) and not force:
        # Check if table has rows
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='vehicles'")
            if cursor.fetchone():
                cursor.execute("SELECT COUNT(*) FROM vehicles")
                if cursor.fetchone()[0] > 0:
                    return

    with get_connection() as conn:
        cursor = conn.cursor()

        # Drop existing table if force is True
        if force:
            cursor.execute("DROP TABLE IF EXISTS vehicles")

        # Create vehicles table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            manufacturer TEXT NOT NULL,
            model TEXT NOT NULL,
            vehicle_category TEXT NOT NULL CHECK(vehicle_category IN ('Hatchback', 'Sedan', 'SUV', 'Two-Wheeler')),
            battery_technology TEXT NOT NULL CHECK(battery_technology IN ('LFP', 'NMC', 'NCA', 'Solid-State')),
            battery_capacity REAL NOT NULL,     -- in kWh
            driving_range INTEGER NOT NULL,      -- in km
            price REAL NOT NULL,                 -- in USD
            charging_speed INTEGER NOT NULL,     -- in kW (Peak DC Fast Charge)
            manufacturing_country TEXT NOT NULL,
            customer_rating REAL NOT NULL,       -- 1.0 to 5.0
            annual_sales INTEGER NOT NULL,       -- Annual units sold
            efficiency REAL NOT NULL,            -- kWh per 100 km
            release_year INTEGER NOT NULL
        );
        """)

        # Create useful analytical indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_battery ON vehicles(battery_technology);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_category ON vehicles(vehicle_category);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_country ON vehicles(manufacturing_country);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_manufacturer ON vehicles(manufacturer);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_price ON vehicles(price);")

        # Curated, realistic, high-fidelity dataset representing real-world EVs and next-gen market dynamics
        sample_vehicles = [
            # --- SUVs ---
            ("Tesla", "Model Y Long Range", "SUV", "NMC", 81.0, 533, 48990, 250, "USA", 4.7, 485000, 15.2, 2024),
            ("Tesla", "Model Y RWD", "SUV", "LFP", 60.0, 455, 42990, 170, "China", 4.6, 395000, 13.2, 2024),
            ("BYD", "Atto 3 (Yuan Plus)", "SUV", "LFP", 60.5, 420, 34500, 88, "China", 4.5, 340000, 14.4, 2023),
            ("BYD", "Song Plus EV", "SUV", "LFP", 87.0, 520, 37800, 140, "China", 4.6, 290000, 16.7, 2024),
            ("Volkswagen", "ID.4 Pro", "SUV", "NMC", 77.0, 525, 45200, 175, "Germany", 4.3, 192000, 14.7, 2023),
            ("Hyundai", "Ioniq 5 AWD", "SUV", "NMC", 84.0, 507, 49800, 350, "South Korea", 4.8, 168000, 16.6, 2024),
            ("Kia", "EV6 Long Range AWD", "SUV", "NMC", 77.4, 506, 52600, 350, "South Korea", 4.7, 145000, 15.3, 2023),
            ("Kia", "EV9 GT-Line 7-Seater", "SUV", "NMC", 99.8, 505, 73900, 210, "South Korea", 4.8, 78000, 19.8, 2024),
            ("Volvo", "EX30 Single Motor", "SUV", "LFP", 51.0, 344, 34950, 134, "China", 4.4, 98000, 14.8, 2024),
            ("Volvo", "EX90 Twin Motor", "SUV", "NMC", 111.0, 600, 79995, 250, "Sweden", 4.8, 42000, 18.5, 2024),
            ("BMW", "iX xDrive50", "SUV", "NMC", 111.5, 630, 87100, 195, "Germany", 4.7, 65000, 17.7, 2024),
            ("Audi", "Q4 e-tron 45", "SUV", "NMC", 82.0, 530, 55200, 175, "Germany", 4.4, 82000, 15.5, 2023),
            ("Ford", "Mustang Mach-E Ext Range", "SUV", "NCA", 91.0, 500, 54995, 150, "USA", 4.4, 115000, 18.2, 2024),
            ("Ford", "F-150 Lightning Extended", "SUV", "NMC", 131.0, 515, 69995, 155, "USA", 4.5, 72000, 25.4, 2023),
            ("Rivian", "R1S Dual-Motor Large", "SUV", "NCA", 135.0, 645, 74900, 220, "USA", 4.8, 54000, 20.9, 2024),
            ("Chevrolet", "Blazer EV RS AWD", "SUV", "NMC", 85.0, 449, 53200, 150, "USA", 4.2, 49000, 18.9, 2024),
            ("NIO", "ES6 100kWh", "SUV", "NMC", 100.0, 625, 52000, 180, "China", 4.7, 85000, 16.0, 2024),
            ("NIO", "EL8 Ultra Solid-State 150k", "SUV", "Solid-State", 150.0, 930, 89500, 360, "China", 4.9, 18500, 16.1, 2025),
            ("MG", "ZS EV Long Range", "SUV", "LFP", 72.6, 440, 32900, 92, "China", 4.1, 74000, 16.5, 2023),
            ("Tata", "Nexon EV Max", "SUV", "LFP", 40.5, 453, 21500, 50, "India", 4.3, 56000, 8.9, 2024),
            ("Mahindra", "XUV400 Pro", "SUV", "NMC", 39.4, 456, 19900, 50, "India", 4.2, 38000, 8.6, 2024),
            ("Porsche", "Macan 4 Electric", "SUV", "NMC", 100.0, 613, 78800, 270, "Germany", 4.9, 39000, 16.3, 2024),
            ("Toyota", "bZ4X AWD", "SUV", "NMC", 71.4, 411, 44420, 150, "Japan", 3.8, 43000, 17.4, 2023),
            ("Nissan", "Ariya Evolve+", "SUV", "NMC", 87.0, 500, 48500, 130, "Japan", 4.3, 58000, 17.4, 2023),

            # --- Sedans ---
            ("Tesla", "Model 3 Highland RWD", "Sedan", "LFP", 60.0, 513, 38990, 170, "China", 4.8, 385000, 11.7, 2024),
            ("Tesla", "Model 3 Long Range AWD", "Sedan", "NMC", 78.1, 629, 47740, 250, "USA", 4.8, 290000, 12.4, 2024),
            ("Tesla", "Model S Plaid", "Sedan", "NCA", 100.0, 600, 89990, 250, "USA", 4.9, 41000, 16.7, 2023),
            ("BYD", "Seal Excellence AWD", "Sedan", "LFP", 82.5, 570, 44000, 150, "China", 4.7, 210000, 14.5, 2024),
            ("BYD", "Han EV Flagship", "Sedan", "LFP", 85.4, 605, 42500, 120, "China", 4.6, 185000, 14.1, 2023),
            ("BMW", "i4 eDrive40 Gran Coupe", "Sedan", "NMC", 83.9, 590, 57300, 205, "Germany", 4.7, 94000, 14.2, 2024),
            ("BMW", "i7 xDrive60", "Sedan", "NMC", 105.7, 625, 105700, 195, "Germany", 4.8, 28000, 16.9, 2024),
            ("Hyundai", "Ioniq 6 Long Range RWD", "Sedan", "NMC", 77.4, 614, 45500, 350, "South Korea", 4.7, 112000, 12.6, 2024),
            ("NIO", "ET7 100kWh", "Sedan", "NMC", 100.0, 675, 68000, 180, "China", 4.8, 48000, 14.8, 2024),
            ("NIO", "ET7 Solid-State Edition", "Sedan", "Solid-State", 150.0, 1050, 94500, 360, "China", 4.9, 14000, 14.3, 2025),
            ("Mercedes-Benz", "EQS 450+ Luxury", "Sedan", "NMC", 118.0, 780, 104400, 200, "Germany", 4.7, 36000, 15.1, 2024),
            ("Porsche", "Taycan Turbo S", "Sedan", "NMC", 105.0, 630, 145000, 320, "Germany", 4.9, 31000, 16.7, 2024),
            ("Polestar", "Polestar 2 Long Range", "Sedan", "NMC", 82.0, 655, 49900, 205, "Sweden", 4.6, 52000, 12.5, 2024),
            ("Lucid", "Air Pure RWD", "Sedan", "NCA", 88.0, 660, 69900, 250, "USA", 4.7, 23000, 13.3, 2024),
            ("Toyota", "Crown EV Concept (Solid-State)", "Sedan", "Solid-State", 90.0, 800, 72000, 350, "Japan", 4.8, 12000, 11.2, 2025),

            # --- Hatchbacks ---
            ("BYD", "Dolphin Standard", "Hatchback", "LFP", 44.9, 340, 27500, 60, "China", 4.5, 360000, 13.2, 2023),
            ("BYD", "Seagull Mini (Dolphin Mini)", "Hatchback", "LFP", 38.8, 305, 11900, 40, "China", 4.6, 420000, 12.7, 2024),
            ("Volkswagen", "ID.3 Pro S", "Hatchback", "NMC", 77.0, 559, 39900, 170, "Germany", 4.3, 142000, 13.8, 2024),
            ("MG", "MG4 EV Trophy Long Range", "Hatchback", "NMC", 64.0, 450, 31500, 135, "China", 4.6, 175000, 14.2, 2024),
            ("Renault", "5 E-Tech Electric", "Hatchback", "NMC", 52.0, 400, 26900, 100, "France", 4.7, 89000, 13.0, 2024),
            ("Peugeot", "e-208 GT", "Hatchback", "NMC", 51.0, 410, 33500, 100, "France", 4.4, 76000, 12.4, 2023),
            ("Fiat", "500e Icon", "Hatchback", "NMC", 42.0, 320, 32500, 85, "Italy", 4.3, 62000, 13.1, 2023),
            ("Chevrolet", "Bolt EV Premier", "Hatchback", "NMC", 65.0, 416, 27800, 55, "USA", 4.2, 95000, 15.6, 2023),
            ("Nissan", "Leaf SV PLUS", "Hatchback", "NMC", 60.0, 342, 36195, 100, "Japan", 4.0, 51000, 17.5, 2023),
            ("Tata", "Tiago EV Long Range", "Hatchback", "LFP", 24.0, 315, 11200, 25, "India", 4.4, 71000, 7.6, 2024),
            ("Mini", "Cooper SE Electric", "Hatchback", "NMC", 54.2, 402, 36000, 95, "UK", 4.5, 48000, 13.5, 2024),
            ("QuantumScape / VW", "Solid-State E-Golf Prototype", "Hatchback", "Solid-State", 70.0, 680, 41000, 320, "Germany", 4.8, 15000, 10.3, 2025),

            # --- Two-Wheelers ---
            ("Ola Electric", "S1 Pro Gen 2", "Two-Wheeler", "NMC", 4.0, 195, 1850, 6, "India", 4.5, 280000, 2.1, 2024),
            ("Ola Electric", "S1 X 3kWh", "Two-Wheeler", "LFP", 3.0, 143, 1100, 4, "India", 4.3, 220000, 2.1, 2024),
            ("Ather Energy", "450X Gen 3", "Two-Wheeler", "NMC", 3.7, 150, 1950, 6, "India", 4.7, 135000, 2.5, 2024),
            ("Ather Energy", "450 Apex Flagship", "Two-Wheeler", "NMC", 3.7, 157, 2350, 6, "India", 4.8, 38000, 2.4, 2024),
            ("Ather Energy", "Rizta Family Scooter", "Two-Wheeler", "LFP", 3.7, 160, 1490, 5, "India", 4.6, 82000, 2.3, 2024),
            ("TVS Motor", "iQube ST 5.1kWh", "Two-Wheeler", "NMC", 5.1, 150, 2150, 5, "India", 4.5, 115000, 3.4, 2024),
            ("Zero Motorcycles", "DSR/X Electric Adventure", "Two-Wheeler", "NMC", 17.3, 290, 22995, 12, "USA", 4.8, 14000, 6.0, 2024),
            ("Zero Motorcycles", "SR/F Naked Roadster", "Two-Wheeler", "NMC", 17.3, 275, 19795, 12, "USA", 4.7, 18000, 6.3, 2023),
            ("LiveWire", "S2 Del Mar (Harley)", "Two-Wheeler", "NMC", 10.5, 181, 15499, 10, "USA", 4.6, 12000, 5.8, 2024),
            ("NIU Technologies", "NQi GTS Pro", "Two-Wheeler", "LFP", 4.2, 130, 3990, 4, "China", 4.3, 165000, 3.2, 2023),
            ("Super Soco", "TC Max Cafe Racer", "Two-Wheeler", "LFP", 3.2, 110, 4200, 3, "China", 4.2, 85000, 2.9, 2023),
            ("BMW Motorrad", "CE 04 Urban Cruiser", "Two-Wheeler", "NMC", 8.9, 130, 12195, 7, "Germany", 4.6, 21000, 6.8, 2024),
            ("Ultraviolette", "F77 Mach 2 Recon", "Two-Wheeler", "NMC", 10.3, 323, 4950, 8, "India", 4.7, 24000, 3.2, 2024),
            ("Solidion Tech", "Titan Next-Gen Two-Wheeler", "Two-Wheeler", "Solid-State", 6.5, 380, 5400, 15, "South Korea", 4.8, 8500, 1.7, 2025)
        ]

        cursor.executemany("""
        INSERT INTO vehicles (
            manufacturer, model, vehicle_category, battery_technology,
            battery_capacity, driving_range, price, charging_speed,
            manufacturing_country, customer_rating, annual_sales, efficiency, release_year
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, sample_vehicles)

        conn.commit()
    print(f"Database successfully initialized with {len(sample_vehicles)} records.")

# ==========================================
# SQL Operations and Analytical Query Engine
# ==========================================

def build_filter_clauses(filters: Optional[Dict[str, Any]] = None) -> Tuple[str, List[Any]]:
    """Builds parameterized SQL WHERE clause based on dynamic filter dictionary."""
    if not filters:
        return "", []

    clauses = []
    params = []

    if filters.get("battery_technology"):
        val = filters["battery_technology"]
        if val != "All":
            clauses.append("battery_technology = ?")
            params.append(val)

    if filters.get("vehicle_category"):
        val = filters["vehicle_category"]
        if val != "All":
            clauses.append("vehicle_category = ?")
            params.append(val)

    if filters.get("manufacturing_country"):
        val = filters["manufacturing_country"]
        if val != "All":
            clauses.append("manufacturing_country = ?")
            params.append(val)

    if filters.get("min_price") is not None and str(filters["min_price"]).strip():
        clauses.append("price >= ?")
        params.append(float(filters["min_price"]))

    if filters.get("max_price") is not None and str(filters["max_price"]).strip():
        clauses.append("price <= ?")
        params.append(float(filters["max_price"]))

    if filters.get("search") and str(filters["search"]).strip():
        search_term = f"%{filters['search'].strip()}%"
        clauses.append("(manufacturer LIKE ? OR model LIKE ?)")
        params.extend([search_term, search_term])

    where_sql = ("WHERE " + " AND ".join(clauses)) if clauses else ""
    return where_sql, params

def get_kpis(filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Calculates top-level KPI metrics for the dashboard."""
    where_sql, params = build_filter_clauses(filters)

    query = f"""
    SELECT
        COUNT(*) as total_models,
        COALESCE(SUM(annual_sales), 0) as total_sales,
        COALESCE(AVG(driving_range), 0) as avg_range,
        COALESCE(AVG(customer_rating), 0) as avg_rating,
        COALESCE(AVG(price), 0) as avg_price,
        COALESCE(AVG(charging_speed), 0) as avg_charging_speed
    FROM vehicles
    {where_sql};
    """

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()

        # Find top manufacturer by annual sales under current filters
        top_mfg_query = f"""
        SELECT manufacturer, SUM(annual_sales) as mfg_sales
        FROM vehicles
        {where_sql}
        GROUP BY manufacturer
        ORDER BY mfg_sales DESC
        LIMIT 1;
        """
        cursor.execute(top_mfg_query, params)
        top_mfg_row = cursor.fetchone()
        top_manufacturer = top_mfg_row["manufacturer"] if top_mfg_row else "N/A"
        top_mfg_sales = top_mfg_row["mfg_sales"] if top_mfg_row else 0

        # Find top battery technology by share
        top_bat_query = f"""
        SELECT battery_technology, SUM(annual_sales) as bat_sales
        FROM vehicles
        {where_sql}
        GROUP BY battery_technology
        ORDER BY bat_sales DESC
        LIMIT 1;
        """
        cursor.execute(top_bat_query, params)
        top_bat_row = cursor.fetchone()
        top_battery = top_bat_row["battery_technology"] if top_bat_row else "N/A"

    return {
        "total_models": row["total_models"],
        "total_sales": row["total_sales"],
        "avg_range": round(row["avg_range"], 1),
        "avg_rating": round(row["avg_rating"], 2),
        "avg_price": round(row["avg_price"], 2),
        "avg_charging_speed": round(row["avg_charging_speed"], 1),
        "top_manufacturer": top_manufacturer,
        "top_mfg_sales": top_mfg_sales,
        "top_battery": top_battery
    }

def get_top_manufacturers_by_sales(limit: int = 10, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Returns top manufacturers sorted by total annual sales."""
    where_sql, params = build_filter_clauses(filters)
    query = f"""
    SELECT
        manufacturer,
        SUM(annual_sales) as total_sales,
        COUNT(*) as model_count,
        ROUND(AVG(customer_rating), 2) as avg_rating,
        ROUND(AVG(price), 2) as avg_price
    FROM vehicles
    {where_sql}
    GROUP BY manufacturer
    ORDER BY total_sales DESC
    LIMIT ?;
    """
    params.append(limit)
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return [dict(r) for r in cursor.fetchall()]

def get_range_by_battery_type(filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Returns average driving range, charging speed, and sales grouped by battery technology."""
    where_sql, params = build_filter_clauses(filters)
    query = f"""
    SELECT
        battery_technology,
        COUNT(*) as model_count,
        ROUND(AVG(driving_range), 1) as avg_range,
        MIN(driving_range) as min_range,
        MAX(driving_range) as max_range,
        ROUND(AVG(battery_capacity), 1) as avg_capacity,
        ROUND(AVG(charging_speed), 1) as avg_charging_speed,
        ROUND(AVG(price), 2) as avg_price,
        SUM(annual_sales) as total_sales
    FROM vehicles
    {where_sql}
    GROUP BY battery_technology
    ORDER BY total_sales DESC;
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return [dict(r) for r in cursor.fetchall()]

def get_country_distribution(filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Returns vehicle production volume, total sales, and market metrics by manufacturing country."""
    where_sql, params = build_filter_clauses(filters)
    query = f"""
    SELECT
        manufacturing_country,
        COUNT(*) as total_models,
        SUM(annual_sales) as total_sales,
        ROUND(AVG(price), 2) as avg_price,
        ROUND(AVG(driving_range), 1) as avg_range,
        ROUND(AVG(customer_rating), 2) as avg_rating
    FROM vehicles
    {where_sql}
    GROUP BY manufacturing_country
    ORDER BY total_sales DESC;
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return [dict(r) for r in cursor.fetchall()]

def get_category_breakdown(filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Returns performance breakdown by vehicle category."""
    where_sql, params = build_filter_clauses(filters)
    query = f"""
    SELECT
        vehicle_category,
        COUNT(*) as count,
        SUM(annual_sales) as total_sales,
        ROUND(AVG(price), 2) as avg_price,
        ROUND(AVG(driving_range), 1) as avg_range,
        ROUND(AVG(customer_rating), 2) as avg_rating
    FROM vehicles
    {where_sql}
    GROUP BY vehicle_category
    ORDER BY total_sales DESC;
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return [dict(r) for r in cursor.fetchall()]

# ==========================================
# Specialized Problem Scenario Queries
# ==========================================

def get_emily_johnson_insights(filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Scenario 1: Emily Johnson (EV Market Strategy Director)
    Focus: Battery tech adoption, market share, capacity trade-offs, and fast charging trends.
    """
    where_sql, params = build_filter_clauses(filters)

    with get_connection() as conn:
        cursor = conn.cursor()

        # 1. Total sales and battery market share
        cursor.execute(f"""
        SELECT
            battery_technology,
            SUM(annual_sales) as sales_volume,
            ROUND(AVG(battery_capacity), 1) as avg_capacity,
            ROUND(AVG(charging_speed), 1) as avg_charging_speed,
            ROUND(AVG(price), 2) as avg_price,
            ROUND(AVG(driving_range), 1) as avg_range
        FROM vehicles
        {where_sql}
        GROUP BY battery_technology
        ORDER BY sales_volume DESC;
        """, params)
        battery_stats = [dict(r) for r in cursor.fetchall()]

        # 2. Battery tech vs Category distribution
        cursor.execute(f"""
        SELECT
            battery_technology,
            vehicle_category,
            SUM(annual_sales) as category_sales,
            COUNT(*) as models
        FROM vehicles
        {where_sql}
        GROUP BY battery_technology, vehicle_category
        ORDER BY battery_technology, category_sales DESC;
        """, params)
        tech_category = [dict(r) for r in cursor.fetchall()]

        # 3. High-efficiency charging leaders (Charging Speed >= 150kW)
        cursor.execute(f"""
        SELECT
            manufacturer, model, battery_technology, charging_speed, battery_capacity, driving_range, annual_sales
        FROM vehicles
        {where_sql}
        {"AND" if where_sql else "WHERE"} charging_speed >= 150
        ORDER BY charging_speed DESC, annual_sales DESC
        LIMIT 6;
        """, params)
        fast_chargers = [dict(r) for r in cursor.fetchall()]

    return {
        "battery_stats": battery_stats,
        "tech_category": tech_category,
        "fast_chargers": fast_chargers
    }

def get_david_chen_insights(filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Scenario 2: David Chen (Business Intelligence Manager)
    Focus: Manufacturing distribution, country-wise volume, top manufacturer dominance, export pricing.
    """
    where_sql, params = build_filter_clauses(filters)

    with get_connection() as conn:
        cursor = conn.cursor()

        # 1. Country aggregate metrics
        cursor.execute(f"""
        SELECT
            manufacturing_country,
            SUM(annual_sales) as total_country_sales,
            COUNT(DISTINCT manufacturer) as distinct_manufacturers,
            COUNT(*) as total_models,
            ROUND(AVG(price), 2) as avg_country_price,
            ROUND(AVG(driving_range), 1) as avg_range
        FROM vehicles
        {where_sql}
        GROUP BY manufacturing_country
        ORDER BY total_country_sales DESC;
        """, params)
        country_summary = [dict(r) for r in cursor.fetchall()]

        # 2. Manufacturer footprint across manufacturing countries
        cursor.execute(f"""
        SELECT
            manufacturer,
            manufacturing_country,
            SUM(annual_sales) as regional_sales,
            COUNT(*) as models_produced
        FROM vehicles
        {where_sql}
        GROUP BY manufacturer, manufacturing_country
        ORDER BY regional_sales DESC
        LIMIT 10;
        """, params)
        mfg_footprint = [dict(r) for r in cursor.fetchall()]

        # 3. Price tier distribution per country
        cursor.execute(f"""
        SELECT
            manufacturing_country,
            ROUND(MIN(price), 2) as min_price,
            ROUND(MAX(price), 2) as max_price,
            ROUND(AVG(price), 2) as avg_price
        FROM vehicles
        {where_sql}
        GROUP BY manufacturing_country
        ORDER BY avg_price DESC;
        """, params)
        country_pricing = [dict(r) for r in cursor.fetchall()]

    return {
        "country_summary": country_summary,
        "mfg_footprint": mfg_footprint,
        "country_pricing": country_pricing
    }

def get_sarah_williams_insights(filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Scenario 3: Dr. Sarah Williams (Sustainable Mobility Research Analyst)
    Focus: Driving range analysis, price-to-range value, customer satisfaction correlation.
    """
    where_sql, params = build_filter_clauses(filters)

    with get_connection() as conn:
        cursor = conn.cursor()

        # 1. Scatter points for Driving Range vs Price vs Rating
        cursor.execute(f"""
        SELECT
            id, manufacturer, model, vehicle_category, battery_technology,
            driving_range, price, customer_rating, battery_capacity, annual_sales,
            ROUND(price / NULLIF(driving_range, 0), 2) as cost_per_km_range
        FROM vehicles
        {where_sql}
        ORDER BY driving_range DESC;
        """, params)
        scatter_points = [dict(r) for r in cursor.fetchall()]

        # 2. Customer rating brackets and average driving range
        cursor.execute(f"""
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
            ROUND(AVG(price), 2) as avg_price,
            SUM(annual_sales) as bracket_sales
        FROM vehicles
        {where_sql}
        GROUP BY rating_bracket
        ORDER BY avg_range DESC;
        """, params)
        rating_correlation = [dict(r) for r in cursor.fetchall()]

        # 3. Top value leaders (Lowest cost per km of driving range)
        cursor.execute(f"""
        SELECT
            manufacturer, model, vehicle_category, battery_technology,
            driving_range, price, customer_rating,
            ROUND(price / NULLIF(driving_range, 0), 2) as cost_per_km_range
        FROM vehicles
        {where_sql}
        {"AND" if where_sql else "WHERE"} vehicle_category != 'Two-Wheeler' -- Compare full-size 4-wheelers fairly
        ORDER BY cost_per_km_range ASC
        LIMIT 5;
        """, params)
        value_leaders = [dict(r) for r in cursor.fetchall()]

    return {
        "scatter_points": scatter_points,
        "rating_correlation": rating_correlation,
        "value_leaders": value_leaders
    }

def get_filtered_vehicles(
    filters: Optional[Dict[str, Any]] = None,
    page: int = 1,
    per_page: int = 12,
    sort_by: str = "annual_sales",
    sort_order: str = "desc"
) -> Dict[str, Any]:
    """Returns paginated, sorted vehicle records with total count."""
    valid_sort_cols = {
        "annual_sales": "annual_sales",
        "driving_range": "driving_range",
        "price": "price",
        "customer_rating": "customer_rating",
        "charging_speed": "charging_speed",
        "battery_capacity": "battery_capacity",
        "manufacturer": "manufacturer",
        "model": "model"
    }
    sort_col = valid_sort_cols.get(sort_by, "annual_sales")
    order = "DESC" if str(sort_order).lower() == "desc" else "ASC"

    where_sql, params = build_filter_clauses(filters)

    with get_connection() as conn:
        cursor = conn.cursor()

        # Count total matching rows
        count_query = f"SELECT COUNT(*) FROM vehicles {where_sql};"
        cursor.execute(count_query, params)
        total_count = cursor.fetchone()[0]

        # Calculate offset
        offset = max(0, (page - 1) * per_page)
        data_params = list(params)
        data_params.extend([per_page, offset])

        query = f"""
        SELECT
            id, manufacturer, model, vehicle_category, battery_technology,
            battery_capacity, driving_range, price, charging_speed,
            manufacturing_country, customer_rating, annual_sales, efficiency, release_year
        FROM vehicles
        {where_sql}
        ORDER BY {sort_col} {order}
        LIMIT ? OFFSET ?;
        """
        cursor.execute(query, data_params)
        vehicles = [dict(r) for r in cursor.fetchall()]

    total_pages = max(1, (total_count + per_page - 1) // per_page)

    return {
        "vehicles": vehicles,
        "total_count": total_count,
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages
    }

def get_filter_options() -> Dict[str, Any]:
    """Returns unique filter dropdown options and min/max ranges for UI sliders."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT battery_technology FROM vehicles ORDER BY battery_technology;")
        batteries = [r[0] for r in cursor.fetchall()]

        cursor.execute("SELECT DISTINCT vehicle_category FROM vehicles ORDER BY vehicle_category;")
        categories = [r[0] for r in cursor.fetchall()]

        cursor.execute("SELECT DISTINCT manufacturing_country FROM vehicles ORDER BY manufacturing_country;")
        countries = [r[0] for r in cursor.fetchall()]

        cursor.execute("SELECT MIN(price), MAX(price), MIN(driving_range), MAX(driving_range) FROM vehicles;")
        price_range = cursor.fetchone()

    return {
        "battery_technologies": batteries,
        "vehicle_categories": categories,
        "manufacturing_countries": countries,
        "min_price": price_range[0] or 0,
        "max_price": price_range[1] or 150000,
        "min_range": price_range[2] or 0,
        "max_range": price_range[3] or 1200
    }

def get_vehicle_by_id(vehicle_id: int) -> Optional[Dict[str, Any]]:
    """Retrieves a single vehicle by its primary key ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vehicles WHERE id = ?;", (vehicle_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

if __name__ == "__main__":
    init_db(force=True)
    kpis = get_kpis()
    print("Initial KPIs:", kpis)
