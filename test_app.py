"""
Comprehensive Verification and Test Suite for
Electric Vehicle Market Performance & Insights Application
"""

import unittest
from app import app
import db

class TestEVMarketApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        db.init_db(force=True)
        cls.client = app.test_client()
        cls.client.testing = True

    def test_database_kpis(self):
        kpis = db.get_kpis()
        self.assertGreater(kpis["total_models"], 50)
        self.assertGreater(kpis["total_sales"], 1000000)
        self.assertGreater(kpis["avg_range"], 100)
        self.assertGreater(kpis["avg_rating"], 3.5)
        self.assertIn("top_manufacturer", kpis)
        self.assertIn("top_battery", kpis)

    def test_emily_insights(self):
        emily = db.get_emily_johnson_insights()
        self.assertTrue(len(emily["battery_stats"]) >= 4)
        tech_names = [b["battery_technology"] for b in emily["battery_stats"]]
        self.assertIn("LFP", tech_names)
        self.assertIn("NMC", tech_names)
        self.assertIn("Solid-State", tech_names)
        self.assertTrue(len(emily["fast_chargers"]) > 0)

    def test_david_insights(self):
        david = db.get_david_chen_insights()
        self.assertTrue(len(david["country_summary"]) >= 5)
        country_names = [c["manufacturing_country"] for c in david["country_summary"]]
        self.assertIn("China", country_names)
        self.assertIn("USA", country_names)
        self.assertIn("Germany", country_names)
        self.assertTrue(len(david["mfg_footprint"]) > 0)

    def test_sarah_insights(self):
        sarah = db.get_sarah_williams_insights()
        self.assertTrue(len(sarah["scatter_points"]) >= 50)
        self.assertTrue(len(sarah["rating_correlation"]) > 0)
        self.assertTrue(len(sarah["value_leaders"]) > 0)
        # Check value leaders cost per km
        for val in sarah["value_leaders"]:
            self.assertIsNotNone(val["cost_per_km_range"])
            self.assertGreater(val["cost_per_km_range"], 0)

    def test_filtered_vehicles(self):
        # Filter by LFP
        res = db.get_filtered_vehicles(filters={"battery_technology": "LFP"}, per_page=100)
        for v in res["vehicles"]:
            self.assertEqual(v["battery_technology"], "LFP")

        # Filter by SUV
        res_suv = db.get_filtered_vehicles(filters={"vehicle_category": "SUV"}, per_page=100)
        for v in res_suv["vehicles"]:
            self.assertEqual(v["vehicle_category"], "SUV")

        # Filter by max price
        res_price = db.get_filtered_vehicles(filters={"max_price": 30000}, per_page=100)
        for v in res_price["vehicles"]:
            self.assertLessEqual(v["price"], 30000)

    def test_routes_status_code(self):
        routes = ["/", "/personas", "/vehicles", "/sql-console"]
        for r in routes:
            resp = self.client.get(r)
            self.assertEqual(resp.status_code, 200, f"Route {r} failed with status {resp.status_code}")

    def test_api_analytics(self):
        resp = self.client.get("/api/analytics?battery_technology=LFP")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data["status"], "success")
        self.assertIn("kpis", data)
        self.assertIn("battery_tech_data", data)
        self.assertIn("emily", data)
        self.assertIn("david", data)
        self.assertIn("sarah", data)

    def test_api_vehicle_detail(self):
        resp = self.client.get("/api/vehicle/1")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["vehicle"]["id"], 1)

    def test_api_export_csv(self):
        resp = self.client.get("/api/export-csv")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, "text/csv; charset=utf-8")
        text = resp.data.decode("utf-8")
        self.assertIn("ID,Manufacturer,Model,Category", text)
        self.assertIn("Tesla", text)
        self.assertIn("BYD", text)

if __name__ == "__main__":
    unittest.main()
