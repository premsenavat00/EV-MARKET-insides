"""
Electric Vehicle Market Performance & Insights
Flask Web Application Backend
"""

import csv
import io
from flask import Flask, render_template, request, jsonify, Response
import db

app = Flask(__name__)

# Ensure database is initialized on startup
with app.app_context():
    db.init_db()

def parse_filters(req_args) -> dict:
    """Helper to extract and sanitize query filters from request arguments."""
    filters = {}
    battery_tech = req_args.get("battery_technology", "").strip()
    if battery_tech and battery_tech != "All":
        filters["battery_technology"] = battery_tech

    category = req_args.get("vehicle_category", "").strip()
    if category and category != "All":
        filters["vehicle_category"] = category

    country = req_args.get("manufacturing_country", "").strip()
    if country and country != "All":
        filters["manufacturing_country"] = country

    min_price = req_args.get("min_price", "").strip()
    if min_price and min_price.replace(".", "", 1).isdigit():
        filters["min_price"] = float(min_price)

    max_price = req_args.get("max_price", "").strip()
    if max_price and max_price.replace(".", "", 1).isdigit():
        filters["max_price"] = float(max_price)

    search = req_args.get("search", "").strip()
    if search:
        filters["search"] = search

    return filters

@app.route("/")
def dashboard():
    """Home Dashboard summarizing overall EV Market Insights."""
    filters = parse_filters(request.args)
    filter_options = db.get_filter_options()
    kpis = db.get_kpis(filters)
    top_manufacturers = db.get_top_manufacturers_by_sales(limit=8, filters=filters)
    battery_tech_data = db.get_range_by_battery_type(filters=filters)
    country_data = db.get_country_distribution(filters=filters)
    category_data = db.get_category_breakdown(filters=filters)

    return render_template(
        "index.html",
        kpis=kpis,
        top_manufacturers=top_manufacturers,
        battery_tech_data=battery_tech_data,
        country_data=country_data,
        category_data=category_data,
        filter_options=filter_options,
        active_filters=filters
    )

@app.route("/personas")
def personas():
    """Dedicated analytical views for Emily Johnson, David Chen, and Dr. Sarah Williams."""
    filters = parse_filters(request.args)
    filter_options = db.get_filter_options()

    emily_insights = db.get_emily_johnson_insights(filters)
    david_insights = db.get_david_chen_insights(filters)
    sarah_insights = db.get_sarah_williams_insights(filters)
    kpis = db.get_kpis(filters)

    # Determine default active tab if specified
    active_tab = request.args.get("tab", "emily")
    if active_tab not in ["emily", "david", "sarah"]:
        active_tab = "emily"

    return render_template(
        "personas.html",
        active_tab=active_tab,
        emily=emily_insights,
        david=david_insights,
        sarah=sarah_insights,
        kpis=kpis,
        filter_options=filter_options,
        active_filters=filters
    )

@app.route("/vehicles")
def vehicles():
    """Interactive Vehicle Catalog & Data Explorer with pagination and sorting."""
    filters = parse_filters(request.args)
    filter_options = db.get_filter_options()

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 12, type=int)
    sort_by = request.args.get("sort_by", "annual_sales")
    sort_order = request.args.get("sort_order", "desc")

    result = db.get_filtered_vehicles(
        filters=filters,
        page=page,
        per_page=per_page,
        sort_by=sort_by,
        sort_order=sort_order
    )

    return render_template(
        "vehicles.html",
        vehicles=result["vehicles"],
        total_count=result["total_count"],
        page=result["page"],
        total_pages=result["total_pages"],
        per_page=per_page,
        sort_by=sort_by,
        sort_order=sort_order,
        filter_options=filter_options,
        active_filters=filters
    )

@app.route("/sql-console")
def sql_console():
    """Documentation and interactive preview of SQL queries used across the project."""
    return render_template("sql_console.html")

# ==========================================
# REST API Endpoints for Asynchronous UI
# ==========================================

@app.route("/api/analytics")
def api_analytics():
    """Returns real-time analytics data in JSON format for dynamic Chart.js updates."""
    filters = parse_filters(request.args)
    kpis = db.get_kpis(filters)
    top_manufacturers = db.get_top_manufacturers_by_sales(limit=10, filters=filters)
    battery_tech_data = db.get_range_by_battery_type(filters=filters)
    country_data = db.get_country_distribution(filters=filters)
    category_data = db.get_category_breakdown(filters=filters)

    emily = db.get_emily_johnson_insights(filters)
    david = db.get_david_chen_insights(filters)
    sarah = db.get_sarah_williams_insights(filters)

    return jsonify({
        "status": "success",
        "kpis": kpis,
        "top_manufacturers": top_manufacturers,
        "battery_tech_data": battery_tech_data,
        "country_data": country_data,
        "category_data": category_data,
        "emily": emily,
        "david": david,
        "sarah": sarah
    })

@app.route("/api/vehicle/<int:vehicle_id>")
def api_vehicle_detail(vehicle_id):
    """Returns single vehicle specification details."""
    vehicle = db.get_vehicle_by_id(vehicle_id)
    if not vehicle:
        return jsonify({"status": "error", "message": "Vehicle not found"}), 404
    return jsonify({"status": "success", "vehicle": vehicle})

@app.route("/api/export-csv")
def export_csv():
    """Exports filtered dataset as downloadable CSV file."""
    filters = parse_filters(request.args)
    where_sql, params = db.build_filter_clauses(filters)

    query = f"""
    SELECT
        id, manufacturer, model, vehicle_category, battery_technology,
        battery_capacity, driving_range, price, charging_speed,
        manufacturing_country, customer_rating, annual_sales, efficiency, release_year
    FROM vehicles
    {where_sql}
    ORDER BY annual_sales DESC;
    """

    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()

    output = io.StringIO()
    writer = csv.writer(output)

    # Header
    writer.writerow([
        "ID", "Manufacturer", "Model", "Category", "Battery Tech",
        "Capacity (kWh)", "Range (km)", "Price (USD)", "Charging Speed (kW)",
        "Manufacturing Country", "Customer Rating", "Annual Sales", "Efficiency (kWh/100km)", "Release Year"
    ])

    for row in rows:
        writer.writerow(list(row))

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=ev_market_insights.csv"}
    )

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
