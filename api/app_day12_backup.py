"""
app.py — AgriTech AI Platform
Author : Daniel Oyanogbezina
Day 11 : Added /api/diseases endpoints
"""

import sys
import os
import urllib.request
import json as json_lib
import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask      import Flask, request, jsonify
from flask_cors import CORS

from advisory import (
    SUPPORTED_CROPS,
    CROP_ADVICE,
    get_calendar,
    MONTH_NAMES,
    NIGERIAN_STATES,
    REGION_RAINFALL,
    get_state_list,
    CROP_DISEASES,
    SEVERITY_COLORS,
    get_diseases,
    get_all_diseases,
)
from predictor import predict_and_advise, MODEL_LOADED
from database  import log_prediction, get_analytics

app = Flask(__name__)
CORS(app)


def error_response(message: str, code: int = 400):
    return jsonify({"success": False, "error": message}), code


def ok_response(data: dict):
    return jsonify({"success": True, **data})


# ── 1: Home ────────────────────────────────────────────────
@app.route("/", methods=["GET"])
def home():
    return ok_response({
        "name":    "AgriTech AI Platform API",
        "version": "1.1.0",
        "author":  "Daniel Oyanogbezina",
        "mission": "AI-powered farming advice for Nigerian farmers",
        "endpoints": {
            "GET  /":                       "API information",
            "GET  /health":                 "Health check",
            "GET  /api/crops":              "List supported crops",
            "POST /api/predict":            "Predict yield + advice",
            "GET  /api/calendar/<crop>":    "Monthly crop calendar",
            "GET  /api/advice/<crop>":      "Full advice for a crop",
            "GET  /api/weather/<state>":    "Rainfall for a state",
            "GET  /api/states":             "List Nigerian states",
            "GET  /api/analytics":          "Dashboard analytics",
            "GET  /api/diseases/<crop>":    "Diseases for a crop",
            "GET  /api/diseases":           "All disease counts",
        },
        "supported_crops": SUPPORTED_CROPS,
    })


# ── 2: Health ──────────────────────────────────────────────
@app.route("/health", methods=["GET"])
def health():
    return ok_response({
        "status":       "online",
        "model_loaded": MODEL_LOADED,
        "timestamp":    datetime.datetime.now().isoformat(),
        "server":       "AgriTech AI Platform v1.1",
    })


# ── 3: List crops ──────────────────────────────────────────
@app.route("/api/crops", methods=["GET"])
def list_crops():
    crops_info = []
    for crop in SUPPORTED_CROPS:
        info = CROP_ADVICE[crop]
        crops_info.append({
            "crop":         crop,
            "season":       info["season"],
            "harvest_time": info["harvest"],
            "market_tip":   info["market_tip"],
            "disease_count": len(CROP_DISEASES.get(crop, [])),
            "price_range_ngn_per_ton": {
                "low":  info["price_range"][0],
                "high": info["price_range"][1],
            },
        })
    return ok_response({"count": len(crops_info), "crops": crops_info})


# ── 4: Predict (main endpoint) ─────────────────────────────
@app.route("/api/predict", methods=["POST"])
def predict():
    body = request.get_json(silent=True)
    if not body:
        return error_response(
            "Request body must be JSON. "
            "Set Content-Type: application/json header."
        )

    required = [
        "crop", "rainfall_mm", "soil_ph",
        "fertilizer_kg", "improved_seeds",
        "irrigation", "farm_size_ha",
    ]
    missing = [f for f in required if f not in body]
    if missing:
        return error_response(f"Missing required fields: {missing}")

    try:
        crop           = str(body["crop"])
        rainfall_mm    = float(body["rainfall_mm"])
        soil_ph        = float(body["soil_ph"])
        fertilizer_kg  = float(body["fertilizer_kg"])
        improved_seeds = bool(body["improved_seeds"])
        irrigation     = bool(body["irrigation"])
        farm_size_ha   = float(body["farm_size_ha"])
        state          = str(body.get("state", "Unknown"))
    except (ValueError, TypeError) as e:
        return error_response(f"Invalid field type: {e}")

    result = predict_and_advise(
        crop=crop, rainfall_mm=rainfall_mm, soil_ph=soil_ph,
        fertilizer_kg=fertilizer_kg, improved_seeds=improved_seeds,
        irrigation=irrigation, farm_size_ha=farm_size_ha,
    )

    if "error" in result:
        return error_response(result["error"])

    try:
        log_prediction({
            "crop": crop, "state": state,
            "farm_size_ha": farm_size_ha, "rainfall_mm": rainfall_mm,
            "soil_ph": soil_ph, "fertilizer_kg": fertilizer_kg,
            "improved_seeds": improved_seeds, "irrigation": irrigation,
        }, result)
    except Exception as e:
        print(f"[app] Logging error (non-critical): {e}")

    return ok_response({"result": result})


# ── 5: Crop calendar ───────────────────────────────────────
@app.route("/api/calendar/<crop>", methods=["GET"])
def crop_calendar(crop):
    crop = crop.strip().title()
    if crop not in SUPPORTED_CROPS:
        return error_response(f"Crop '{crop}' not supported.")
    try:
        month = int(request.args.get(
            "month", datetime.datetime.now().month))
        if not 1 <= month <= 12:
            return error_response("month must be between 1 and 12")
    except ValueError:
        return error_response("month must be an integer (1-12)")
    return ok_response({"calendar": get_calendar(crop, month)})


# ── 6: Crop advice ─────────────────────────────────────────
@app.route("/api/advice/<crop>", methods=["GET"])
def crop_advice(crop):
    crop = crop.strip().title()
    if crop not in SUPPORTED_CROPS:
        return error_response(f"Crop '{crop}' not supported.")
    info = CROP_ADVICE[crop]
    return ok_response({
        "crop": crop,
        "advice": {
            "season":        info["season"],
            "soil_ph":       info["soil_ph"],
            "spacing":       info["spacing"],
            "harvest":       info["harvest"],
            "fertilizer":    info["fertilizer"],
            "water_need":    info["water_need"],
            "disease_watch": info["disease_watch"],
            "market_tip":    info["market_tip"],
            "price_range_ngn_per_ton": {
                "low":  info["price_range"][0],
                "high": info["price_range"][1],
            },
        },
    })


# ── 7: State weather ───────────────────────────────────────
@app.route("/api/weather/<state>", methods=["GET"])
def get_state_weather(state):
    matched_state = None
    for s in NIGERIAN_STATES:
        if s.lower() == state.lower() or \
           s.lower().replace(" ", "") == state.lower().replace(" ", ""):
            matched_state = s
            break

    if not matched_state:
        return error_response(
            f"State '{state}' not found. Use /api/states for the list."
        )

    coords = NIGERIAN_STATES[matched_state]
    lat, lon, region = coords["lat"], coords["lon"], coords["region"]

    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&daily=precipitation_sum"
            f"&timezone=Africa%2FLagos&past_days=30&forecast_days=1"
        )
        req = urllib.request.Request(url,
              headers={"User-Agent": "AgriTechAI/1.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            wdata = json_lib.loads(resp.read().decode())

        daily_rain = wdata.get("daily", {}).get("precipitation_sum", [])
        rain_30    = sum(r for r in daily_rain if r is not None)
        annual_est = round(rain_30 * 12)
        regional   = REGION_RAINFALL[region]
        blended    = round((annual_est * 0.4) + (regional * 0.6))

        return ok_response({
            "state": matched_state, "region": region,
            "coordinates": {"lat": lat, "lon": lon},
            "weather": {
                "rainfall_30_days_mm":   round(rain_30, 1),
                "annual_estimate_mm":    annual_est,
                "recommended_input_mm":  blended,
                "source": "Open-Meteo + regional data",
            },
        })

    except Exception:
        regional = REGION_RAINFALL[region]
        return ok_response({
            "state": matched_state, "region": region,
            "weather": {
                "recommended_input_mm": regional,
                "source": "regional historical average",
            },
        })


# ── 8: List states ─────────────────────────────────────────
@app.route("/api/states", methods=["GET"])
def list_states():
    return ok_response({
        "count":  len(NIGERIAN_STATES),
        "states": get_state_list(),
    })


# ── 9: Analytics ───────────────────────────────────────────
@app.route("/api/analytics", methods=["GET"])
def analytics():
    return ok_response({"analytics": get_analytics()})


# ── 10: Diseases for one crop ──────────────────────────────
@app.route("/api/diseases/<crop>", methods=["GET"])
def crop_diseases(crop):
    crop = crop.strip().title()
    if crop not in SUPPORTED_CROPS:
        return error_response(
            f"Crop '{crop}' not supported. "
            f"Supported: {SUPPORTED_CROPS}"
        )
    diseases = get_diseases(crop)
    return ok_response({
        "crop":            crop,
        "disease_count":   len(diseases),
        "diseases":        diseases,
        "severity_colors": SEVERITY_COLORS,
    })


# ── 11: All disease counts ─────────────────────────────────
@app.route("/api/diseases", methods=["GET"])
def all_diseases():
    return ok_response({
        "summary":         get_all_diseases(),
        "total_diseases":  sum(get_all_diseases().values()),
        "severity_colors": SEVERITY_COLORS,
    })


# ── Error handlers ─────────────────────────────────────────
@app.errorhandler(404)
def not_found(e):
    return error_response(
        "Endpoint not found. Visit / for all endpoints.", 404)

@app.errorhandler(405)
def method_not_allowed(e):
    return error_response("Method not allowed.", 405)

@app.errorhandler(500)
def server_error(e):
    return error_response("Internal server error.", 500)


# ── Run ────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  AgriTech AI Platform — Farmer Advisory API v1.1")
    print("  Author: Daniel Oyanogbezina")
    print("=" * 60)
    print(f"  Model loaded    : {MODEL_LOADED}")
    print(f"  Supported crops : {SUPPORTED_CROPS}")
    print(f"  Nigerian states : {len(NIGERIAN_STATES)}")
    print(f"  Diseases loaded : {sum(get_all_diseases().values())}")
    print()
    print("  Endpoints (11 total):")
    print("  GET  http://127.0.0.1:5001/")
    print("  GET  http://127.0.0.1:5001/health")
    print("  GET  http://127.0.0.1:5001/api/crops")
    print("  POST http://127.0.0.1:5001/api/predict")
    print("  GET  http://127.0.0.1:5001/api/calendar/<crop>")
    print("  GET  http://127.0.0.1:5001/api/advice/<crop>")
    print("  GET  http://127.0.0.1:5001/api/weather/<state>")
    print("  GET  http://127.0.0.1:5001/api/states")
    print("  GET  http://127.0.0.1:5001/api/analytics")
    print("  GET  http://127.0.0.1:5001/api/diseases/<crop>  <- NEW")
    print("  GET  http://127.0.0.1:5001/api/diseases         <- NEW")
    print()
    print("  Press CTRL+C to stop")
    print("=" * 60 + "\n")

    app.run(host="127.0.0.1", port=5001, debug=True)