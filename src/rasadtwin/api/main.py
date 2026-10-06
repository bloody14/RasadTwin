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

DB_PATH = "demo_state.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Create with new schema if not exists
    c.execute('''CREATE TABLE IF NOT EXISTS audit_log
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp TEXT,
                  user TEXT,
                  action TEXT,
                  scenario TEXT,
                  system_recommendation TEXT,
                  user_action TEXT,
                  selected_scope TEXT,
                  reason TEXT)''')
    
    # Try adding new columns if table already existed with old schema
    try:
        c.execute("ALTER TABLE audit_log ADD COLUMN system_recommendation TEXT")
        c.execute("ALTER TABLE audit_log ADD COLUMN user_action TEXT")
        c.execute("ALTER TABLE audit_log ADD COLUMN selected_scope TEXT")
    except sqlite3.OperationalError:
        pass # columns already exist
        
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
    system_recommendation: str
    user_action: str  # APPROVE, REJECT, OVERRIDE
    selected_scope: str # LOCAL, GLOBAL, PRESERVE, NONE
    reason: str

# --- Synthetic Demo Data ---
# 2 Rear, 3 Intermediate, 12 Forward Posts
DEMO_POSTS = [
    # Rear Depots (Base)
    {"id": "RD-001", "name": "Main Base North", "type": "rear_depot", "lat": 32.5, "lng": 75.5, "risk": "Low", "dos": 100, "priority": 0},
    {"id": "RD-002", "name": "Main Base South", "type": "rear_depot", "lat": 32.2, "lng": 76.8, "risk": "Low", "dos": 120, "priority": 0},
    
    # Intermediate Hubs
    {"id": "ID-001", "name": "Valley Hub Alpha", "type": "intermediate_depot", "lat": 33.2, "lng": 75.8, "risk": "Low", "dos": 50, "priority": 0},
    {"id": "ID-002", "name": "Valley Hub Bravo", "type": "intermediate_depot", "lat": 33.5, "lng": 76.4, "risk": "Low", "dos": 45, "priority": 0},
    {"id": "ID-003", "name": "Valley Hub Charlie", "type": "intermediate_depot", "lat": 33.4, "lng": 77.1, "risk": "Low", "dos": 60, "priority": 0},
    
    # Forward Posts (12)
    {"id": "FP-001", "name": "Alpha Ridge", "type": "forward_post", "lat": 34.1, "lng": 75.6, "risk": "High", "dos": 5, "priority": 1},
    {"id": "FP-002", "name": "Bravo Peak", "type": "forward_post", "lat": 34.3, "lng": 75.9, "risk": "Medium", "dos": 12, "priority": 2},
    {"id": "FP-003", "name": "Charlie Pass", "type": "forward_post", "lat": 34.0, "lng": 76.1, "risk": "Low", "dos": 20, "priority": 3},
    {"id": "FP-004", "name": "Delta Crest", "type": "forward_post", "lat": 34.5, "lng": 76.3, "risk": "High", "dos": 3, "priority": 1},
    {"id": "FP-005", "name": "Echo Point", "type": "forward_post", "lat": 34.2, "lng": 76.5, "risk": "Low", "dos": 18, "priority": 4},
    {"id": "FP-006", "name": "Foxtrot Base", "type": "forward_post", "lat": 34.4, "lng": 76.8, "risk": "Medium", "dos": 10, "priority": 2},
    {"id": "FP-007", "name": "Golf Station", "type": "forward_post", "lat": 34.6, "lng": 77.0, "risk": "High", "dos": 2, "priority": 1},
    {"id": "FP-008", "name": "Hotel Outpost", "type": "forward_post", "lat": 34.1, "lng": 77.2, "risk": "Low", "dos": 25, "priority": 5},
    {"id": "FP-009", "name": "India Camp", "type": "forward_post", "lat": 34.3, "lng": 77.4, "risk": "High", "dos": 4, "priority": 1},
    {"id": "FP-010", "name": "Juliet Post", "type": "forward_post", "lat": 34.5, "lng": 77.6, "risk": "Medium", "dos": 9, "priority": 2},
    {"id": "FP-011", "name": "Kilo Ridge", "type": "forward_post", "lat": 34.0, "lng": 77.8, "risk": "Low", "dos": 22, "priority": 3},
    {"id": "FP-012", "name": "Lima Watch", "type": "forward_post", "lat": 34.2, "lng": 78.0, "risk": "Medium", "dos": 8, "priority": 2},
]

DEMO_ROUTES = [
    # Rear to Intermediate
    {"id": "R-100", "source": "RD-001", "target": "ID-001", "mode": "Road", "distance_km": 120, "eta_hrs": 4.0, "risk": "Low", "robust_eta_hrs": 4.5, "status": "ACTIVE"},
    {"id": "R-101", "source": "RD-001", "target": "ID-002", "mode": "Road", "distance_km": 150, "eta_hrs": 5.0, "risk": "Low", "robust_eta_hrs": 5.5, "status": "ACTIVE"},
    {"id": "R-102", "source": "RD-002", "target": "ID-002", "mode": "Road", "distance_km": 160, "eta_hrs": 5.5, "risk": "Low", "robust_eta_hrs": 6.0, "status": "ACTIVE"},
    {"id": "R-103", "source": "RD-002", "target": "ID-003", "mode": "Road", "distance_km": 140, "eta_hrs": 4.5, "risk": "Low", "robust_eta_hrs": 5.0, "status": "ACTIVE"},
    
    # Intermediate to Forward
    {"id": "R-001", "source": "ID-001", "target": "FP-001", "mode": "Road", "distance_km": 45, "eta_hrs": 2.5, "risk": "Medium", "robust_eta_hrs": 3.2, "status": "ACTIVE"},
    {"id": "R-002", "source": "ID-001", "target": "FP-002", "mode": "Heli", "distance_km": 60, "eta_hrs": 0.5, "risk": "High", "robust_eta_hrs": 1.5, "status": "ACTIVE"},
    {"id": "R-003", "source": "ID-001", "target": "FP-003", "mode": "Mule", "distance_km": 30, "eta_hrs": 12.0, "risk": "Low", "robust_eta_hrs": 14.0, "status": "ACTIVE"},
    {"id": "R-004", "source": "ID-002", "target": "FP-004", "mode": "Road", "distance_km": 50, "eta_hrs": 3.0, "risk": "High", "robust_eta_hrs": 5.0, "status": "ACTIVE"},
    {"id": "R-005", "source": "ID-002", "target": "FP-005", "mode": "Drone", "distance_km": 20, "eta_hrs": 0.5, "risk": "Medium", "robust_eta_hrs": 0.8, "status": "ACTIVE"},
    {"id": "R-006", "source": "ID-002", "target": "FP-006", "mode": "Road", "distance_km": 35, "eta_hrs": 2.0, "risk": "Medium", "robust_eta_hrs": 3.0, "status": "ACTIVE"},
    {"id": "R-007", "source": "ID-002", "target": "FP-007", "mode": "Heli", "distance_km": 40, "eta_hrs": 0.4, "risk": "High", "robust_eta_hrs": 1.0, "status": "ACTIVE"},
    {"id": "R-008", "source": "ID-003", "target": "FP-008", "mode": "Mule", "distance_km": 25, "eta_hrs": 10.0, "risk": "Low", "robust_eta_hrs": 11.5, "status": "ACTIVE"},
    {"id": "R-009", "source": "ID-003", "target": "FP-009", "mode": "Road", "distance_km": 60, "eta_hrs": 3.5, "risk": "High", "robust_eta_hrs": 5.5, "status": "ACTIVE"},
    {"id": "R-010", "source": "ID-003", "target": "FP-010", "mode": "Drone", "distance_km": 30, "eta_hrs": 0.8, "risk": "Medium", "robust_eta_hrs": 1.2, "status": "ACTIVE"},
    {"id": "R-011", "source": "ID-003", "target": "FP-011", "mode": "Road", "distance_km": 40, "eta_hrs": 2.5, "risk": "Low", "robust_eta_hrs": 3.0, "status": "ACTIVE"},
    {"id": "R-012", "source": "ID-003", "target": "FP-012", "mode": "Heli", "distance_km": 50, "eta_hrs": 0.5, "risk": "Medium", "robust_eta_hrs": 1.0, "status": "ACTIVE"},
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

@app.get("/weather")
def get_weather():
    return {
        "temperature": "-12°C",
        "snow_condition": "Heavy Accumulation",
        "wind": "35 km/h NW",
        "visibility": "Poor (< 500m)",
        "terrain_risk": "Avalanche Warning"
    }

@app.get("/risk/{post_id}")
def get_risk(post_id: str):
    post = next((p for p in DEMO_POSTS if p["id"] == post_id), None)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return {
        "post_id": post_id,
        "stock_out_risk": "85%" if post["dos"] < 7 else "15%",
        "days_of_supply": post["dos"],
        "weather_risk": "High Wind" if post["id"] in ["FP-001", "FP-004", "FP-007", "FP-009"] else "Clear",
        "route_risk": "Avalanche Warning" if post["dos"] < 5 else "Nominal",
        "overall_state": post["risk"],
        "explainability": [
            {"feature": "Forecast Demand", "impact": "+0.45", "description": "Surge expected"},
            {"feature": "Days of Supply", "impact": "+0.30", "description": "Critical low stock"},
            {"feature": "Route Weather", "impact": "+0.15", "description": "Terrain risk elevated"},
        ]
    }

@app.get("/forecast/{post_id}")
def get_forecast(post_id: str):
    history = [{"day": f"D-{i}", "demand": 50 + (i % 5)*5} for i in range(14, 0, -1)]
    future = [
        {"day": f"D+{i}", "demand": None, "forecast": 60 + i*2, "lower": 55 + i, "upper": 65 + i*3} 
        for i in range(1, 8)
    ]
    return {"history": history, "future": future, "nominal_coverage": "90%"}

@app.post("/what-if")
def simulate_disruption(req: WhatIfRequest):
    impact_score = 0
    if req.disruption_type == "Road Closure":
        impact_score = 64
        affected_legs = ["R-001"]
        recommendation = "LOCAL"
        after_route = "R-001A"
        after_mode = "Mule"
        after_eta = "12:00"
        after_risk = "Medium"
        recovery = "+27%"
    elif req.disruption_type == "Heavy Snow":
        impact_score = 85
        affected_legs = ["R-001", "R-004", "R-009"]
        recommendation = "GLOBAL"
        after_route = "R-NET"
        after_mode = "Drone Network"
        after_eta = "06:30"
        after_risk = "High"
        recovery = "+15%"
    elif req.disruption_type == "Heli Grounding":
        impact_score = 45
        affected_legs = ["R-002", "R-007"]
        recommendation = "LOCAL"
        after_route = "R-002A"
        after_mode = "Road"
        after_eta = "04:15"
        after_risk = "Medium"
        recovery = "+40%"
    else:
        impact_score = 20
        affected_legs = []
        recommendation = "PRESERVE"
        after_route = "N/A"
        after_mode = "N/A"
        after_eta = "N/A"
        after_risk = "N/A"
        recovery = "0%"
        
    reason_map = {
        "PRESERVE": "Impact within tolerance. No replan needed.",
        "LOCAL": "Closure affects downstream posts but does not compromise the wider network.",
        "GLOBAL": "Severe network-wide impact. Full re-optimization required."
    }
        
    return {
        "scenario": req.disruption_type,
        "impact_score": impact_score,
        "affected_posts": [req.target_id],
        "affected_legs": affected_legs,
        "recommendation": recommendation,
        "reason": reason_map[recommendation],
        "before_after": {
            "before": {"eta": "04:52", "risk": "High", "route": affected_legs[0] if affected_legs else "N/A", "mode": "Road", "affected_posts": [req.target_id]},
            "after": {"eta": after_eta, "risk": after_risk, "new_mode": after_mode, "route": after_route, "affected_posts": [req.target_id]}
        },
        "route_changes": len(affected_legs),
        "recovery": recovery,
        "network_stability": "Maintained" if impact_score < 75 else "At Risk"
    }

@app.post("/decision")
def record_decision(req: DecisionRequest):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    action_type = f"HITL_{req.user_action}"
    
    c.execute(
        "INSERT INTO audit_log (timestamp, user, action, scenario, system_recommendation, user_action, selected_scope, reason) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (datetime.utcnow().isoformat(), req.user, action_type, req.scenario, req.system_recommendation, req.user_action, req.selected_scope, req.reason)
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
    
    # Check if columns exist, if not, handle it gracefully for old records
    c.execute("PRAGMA table_info(audit_log)")
    cols = [row[1] for row in c.fetchall()]
    
    c.execute("SELECT * FROM audit_log ORDER BY id DESC LIMIT 50")
    rows = c.fetchall()
    conn.close()
    
    logs = []
    for r in rows:
        d = dict(r)
        # Migrate old schema fields for display if necessary
        if 'system_recommendation' not in d or not d['system_recommendation']:
            d['system_recommendation'] = 'UNKNOWN'
            d['user_action'] = 'APPROVE' if 'APPROVE' in d.get('action', '') else 'UNKNOWN'
            d['selected_scope'] = d.get('decision', 'UNKNOWN')
        logs.append(d)
        
    return {"logs": logs}
