"""FastAPI Backend for RasadTwin Prototype."""
from __future__ import annotations

import sqlite3
import json
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

app = FastAPI(title="RasadTwin Command Dashboard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SQLite Database for offline-first and audit
DB_PATH = "demo_state.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS audit_log
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp TEXT,
                  user TEXT,
                  action TEXT,
                  scenario TEXT,
                  decision TEXT,
                  reason TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS cache_state
                 (key TEXT PRIMARY KEY,
                  data TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- Models ---
class WhatIfRequest(BaseModel):
    disruption_type: str
    target_id: str

class DecisionRequest(BaseModel):
    user: str
    scenario: str
    decision: str  # PRESERVE, LOCAL, GLOBAL
    reason: str

# --- Synthetic Demo Data ---
# 8 Forward Posts, 3 Intermediate, 2 Rear
DEMO_POSTS = [
    {"id": "FP-001", "name": "Alpha Ridge", "type": "forward_post", "lat": 34.1, "lng": 77.2, "risk": "High", "dos": 5, "priority": 1},
    {"id": "FP-002", "name": "Bravo Peak", "type": "forward_post", "lat": 34.2, "lng": 77.3, "risk": "Medium", "dos": 12, "priority": 2},
    {"id": "FP-003", "name": "Charlie Pass", "type": "forward_post", "lat": 34.0, "lng": 77.1, "risk": "Low", "dos": 20, "priority": 3},
    {"id": "FP-004", "name": "Delta Crest", "type": "forward_post", "lat": 34.3, "lng": 77.4, "risk": "High", "dos": 3, "priority": 1},
    {"id": "FP-005", "name": "Echo Point", "type": "forward_post", "lat": 34.15, "lng": 77.25, "risk": "Low", "dos": 18, "priority": 4},
    {"id": "FP-006", "name": "Foxtrot Base", "type": "forward_post", "lat": 34.05, "lng": 77.15, "risk": "Medium", "dos": 10, "priority": 2},
    {"id": "FP-007", "name": "Golf Station", "type": "forward_post", "lat": 34.4, "lng": 77.5, "risk": "High", "dos": 2, "priority": 1},
    {"id": "FP-008", "name": "Hotel Outpost", "type": "forward_post", "lat": 33.9, "lng": 77.0, "risk": "Low", "dos": 25, "priority": 5},
    
    {"id": "ID-001", "name": "Valley Hub 1", "type": "intermediate_depot", "lat": 33.5, "lng": 76.5, "risk": "Low", "dos": 50, "priority": 0},
    {"id": "ID-002", "name": "Valley Hub 2", "type": "intermediate_depot", "lat": 33.6, "lng": 76.8, "risk": "Low", "dos": 45, "priority": 0},
    {"id": "ID-003", "name": "Valley Hub 3", "type": "intermediate_depot", "lat": 33.7, "lng": 76.6, "risk": "Low", "dos": 60, "priority": 0},
    
    {"id": "RD-001", "name": "Main Base North", "type": "rear_depot", "lat": 32.5, "lng": 75.5, "risk": "Low", "dos": 100, "priority": 0},
    {"id": "RD-002", "name": "Main Base South", "type": "rear_depot", "lat": 32.0, "lng": 75.0, "risk": "Low", "dos": 120, "priority": 0},
]

DEMO_ROUTES = [
    {"id": "R-001", "source": "ID-001", "target": "FP-001", "mode": "Road", "distance_km": 45, "eta_hrs": 2.5, "risk": "Medium", "robust_eta_hrs": 3.2},
    {"id": "R-002", "source": "ID-001", "target": "FP-002", "mode": "Heli", "distance_km": 60, "eta_hrs": 0.5, "risk": "High", "robust_eta_hrs": 1.5},
    {"id": "R-003", "source": "ID-002", "target": "FP-003", "mode": "Mule", "distance_km": 15, "eta_hrs": 6.0, "risk": "Low", "robust_eta_hrs": 6.5},
    {"id": "R-004", "source": "ID-002", "target": "FP-004", "mode": "Drone", "distance_km": 20, "eta_hrs": 0.3, "risk": "Medium", "robust_eta_hrs": 0.5},
    {"id": "R-005", "source": "ID-003", "target": "FP-005", "mode": "Road", "distance_km": 30, "eta_hrs": 1.5, "risk": "Low", "robust_eta_hrs": 1.8},
    {"id": "R-006", "source": "RD-001", "target": "ID-001", "mode": "Road", "distance_km": 120, "eta_hrs": 4.0, "risk": "Low", "robust_eta_hrs": 4.5},
    {"id": "R-007", "source": "RD-001", "target": "ID-002", "mode": "Road", "distance_km": 110, "eta_hrs": 3.5, "risk": "Low", "robust_eta_hrs": 4.0},
    {"id": "R-008", "source": "RD-002", "target": "ID-003", "mode": "Road", "distance_km": 150, "eta_hrs": 5.0, "risk": "Low", "robust_eta_hrs": 5.5},
]

# --- Endpoints ---
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "RasadTwin Backend Online"}

@app.get("/posts")
def get_posts():
    return {"posts": DEMO_POSTS}

@app.get("/routes")
def get_routes():
    return {"routes": DEMO_ROUTES}

@app.get("/risk/{post_id}")
def get_risk(post_id: str):
    post = next((p for p in DEMO_POSTS if p["id"] == post_id), None)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return {
        "post_id": post_id,
        "stock_out_risk": "85%" if post["dos"] < 7 else "15%",
        "days_of_supply": post["dos"],
        "weather_risk": "High Wind" if post["id"] in ["FP-001", "FP-004"] else "Clear",
        "route_risk": "Avalanche Warning" if post["dos"] < 5 else "Nominal",
        "overall_state": post["risk"],
        # SHAP explanation mock
        "explainability": [
            {"feature": "Forecast Demand", "impact": "+0.45", "description": "Surge expected"},
            {"feature": "Days of Supply", "impact": "+0.30", "description": "Critical low stock"},
            {"feature": "Route Weather", "impact": "+0.15", "description": "Heli grounding risk"},
        ]
    }

@app.get("/forecast/{post_id}")
def get_forecast(post_id: str):
    # Synthetic mock forecast for the UI chart
    history = [{"day": f"D-{i}", "demand": 50 + (i % 5)*5} for i in range(14, 0, -1)]
    future = [
        {"day": f"D+{i}", "demand": None, "forecast": 60 + i*2, "lower": 55 + i, "upper": 65 + i*3} 
        for i in range(1, 8)
    ]
    return {"history": history, "future": future, "nominal_coverage": "90%"}

@app.post("/what-if")
def simulate_disruption(req: WhatIfRequest):
    # Mocking impact analysis
    impact_score = 0
    if req.disruption_type == "Road Closure":
        impact_score = 64 # Medium-High to trigger LOCAL replan
    elif req.disruption_type == "Heavy Snow":
        impact_score = 85 # High to trigger GLOBAL replan
    elif req.disruption_type in ["Heli Grounding", "Drone Grounding"]:
        impact_score = 45 # Medium
    else:
        impact_score = 20 # Low
        
    recommendation = "PRESERVE"
    if impact_score > 75:
        recommendation = "GLOBAL"
    elif impact_score > 30:
        recommendation = "LOCAL"
        
    reason_map = {
        "PRESERVE": "Impact within tolerance. No replan needed.",
        "LOCAL": "Closure affects downstream posts but does not compromise the wider network.",
        "GLOBAL": "Severe network-wide impact. Full re-optimization required."
    }
        
    return {
        "scenario": req.disruption_type,
        "impact_score": impact_score,
        "affected_posts": ["FP-001", "FP-002"] if impact_score > 50 else ["FP-002"],
        "affected_legs": ["R-001"] if req.disruption_type == "Road Closure" else (["R-001", "R-005"] if impact_score > 50 else ["R-002"]),
        "recommendation": recommendation,
        "reason": reason_map[recommendation],
        "before_after": {
            "before": {"eta": "04:52", "risk": "High", "route": "R-001", "mode": "Road", "affected_posts": ["FP-001"]},
            "after": {"eta": "05:21", "risk": "Medium", "new_mode": "Mule", "route": "R-001A", "affected_posts": ["FP-001"]}
        },
        "route_changes": 1,
        "recovery": "+27%",
        "network_stability": "Maintained"
    }

@app.post("/decision")
def record_decision(req: DecisionRequest):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO audit_log (timestamp, user, action, scenario, decision, reason) VALUES (?, ?, ?, ?, ?, ?)",
        (datetime.utcnow().isoformat(), req.user, "HITL_OVERRIDE" if req.decision == "OVERRIDE" else "HITL_APPROVE", req.scenario, req.decision, req.reason)
    )
    conn.commit()
    log_id = c.lastrowid
    conn.close()
    return {"status": "success", "audit_id": log_id}

@app.get("/audit")
def get_audit_log():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM audit_log ORDER BY id DESC LIMIT 50")
    rows = c.fetchall()
    conn.close()
    return {"logs": [dict(r) for r in rows]}
