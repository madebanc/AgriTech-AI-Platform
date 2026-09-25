"""
predictor.py
AgriTech AI Platform — Prediction Engine
Author : Daniel Oyanogbezina
Purpose: Loads the Day 3 trained model and exposes one clean
         function: predict_and_advise()
         Called by app.py for every /api/predict request
"""

import pickle
import os
import pandas as pd
from advisory import (
    CROP_ADVICE, SUPPORTED_CROPS,
    rainfall_advice, soil_ph_advice, get_risk_flags,
)

# ── Load model once when the module is imported ───────────────────────
# Loading once = fast responses (no re-loading per request)

BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH   = os.path.join(BASE_DIR, "models", "yield_predictor_v1.pkl")
FEATURES_PATH= os.path.join(BASE_DIR, "models", "feature_cols.pkl")

try:
    with open(MODEL_PATH, "rb") as f:
        _model = pickle.load(f)
    with open(FEATURES_PATH, "rb") as f:
        _feature_cols = pickle.load(f)
    MODEL_LOADED = True
    print(f"[predictor] Model loaded — {len(_feature_cols)} features")
except FileNotFoundError as e:
    _model        = None
    _feature_cols = []
    MODEL_LOADED  = False
    print(f"[predictor] WARNING: model not found — {e}")
    print("[predictor] Run Day 3 notebook Cell 8 to create the model file.")


# ── Core prediction function ──────────────────────────────────────────

def predict_and_advise(crop: str,
                       rainfall_mm: float,
                       soil_ph: float,
                       fertilizer_kg: float,
                       improved_seeds: bool,
                       irrigation: bool,
                       farm_size_ha: float) -> dict:
    """
    Given a farmer's conditions, returns:
      - predicted yield (tons)
      - income range (low / mid / high)
      - personalised farming advice
      - risk flags
      - what-if yield if farmer upgrades inputs
      - crop calendar for current month

    Returns a dict — app.py converts it to JSON.
    """

    # ── Validate crop ──
    crop = crop.strip().title()
    if crop not in SUPPORTED_CROPS:
        return {
            "error": f"Crop '{crop}' not supported.",
            "supported_crops": SUPPORTED_CROPS,
        }

    # ── Validate model ──
    if not MODEL_LOADED:
        return {
            "error": "Prediction model not loaded. "
                     "Run Day 3 notebook Cell 8 to create it.",
        }

    # ── Validate numeric inputs ──
    errors = []
    if not (300 <= rainfall_mm <= 3000):
        errors.append("rainfall_mm must be between 300 and 3000")
    if not (4.0 <= soil_ph <= 9.0):
        errors.append("soil_ph must be between 4.0 and 9.0")
    if not (0 <= fertilizer_kg <= 500):
        errors.append("fertilizer_kg must be between 0 and 500")
    if not (0.1 <= farm_size_ha <= 100):
        errors.append("farm_size_ha must be between 0.1 and 100")
    if errors:
        return {"error": "Validation failed", "details": errors}

    # ── Build input row ──
    row = {col: 0 for col in _feature_cols}
    row["rainfall_mm"]    = rainfall_mm
    row["soil_ph"]        = soil_ph
    row["fertilizer_kg"]  = fertilizer_kg
    row["improved_seeds"] = int(improved_seeds)
    row["irrigation"]     = int(irrigation)
    row["farm_size_ha"]   = farm_size_ha
    crop_col = f"crop_{crop}"
    if crop_col in row:
        row[crop_col] = 1

    input_df  = pd.DataFrame([row])
    yield_hat = round(max(1.0, _model.predict(input_df)[0]), 2)

    # ── Income estimates ──
    advice_db              = CROP_ADVICE[crop]
    price_low, price_high  = advice_db["price_range"]
    price_mid              = (price_low + price_high) / 2

    # ── What-if: full inputs ──
    row_best = row.copy()
    row_best["improved_seeds"]  = 1
    row_best["irrigation"]      = 1
    row_best["fertilizer_kg"]   = max(fertilizer_kg, 100)
    df_best        = pd.DataFrame([row_best])
    yield_best     = round(max(1.0, _model.predict(df_best)[0]), 2)
    uplift_pct     = round((yield_best - yield_hat) / yield_hat * 100, 1)

    # ── Risk flags ──
    risks = get_risk_flags(
        crop, rainfall_mm, soil_ph,
        fertilizer_kg, improved_seeds, irrigation
    )

    return {
        "crop":             crop,
        "farm_size_ha":     farm_size_ha,
        "prediction": {
            "yield_tons":       yield_hat,
            "income_low_ngn":   round(yield_hat * price_low),
            "income_mid_ngn":   round(yield_hat * price_mid),
            "income_high_ngn":  round(yield_hat * price_high),
        },
        "advice": {
            "season":           advice_db["season"],
            "spacing":          advice_db["spacing"],
            "harvest":          advice_db["harvest"],
            "fertilizer_tip":   advice_db["fertilizer"],
            "water":            rainfall_advice(rainfall_mm),
            "soil":             soil_ph_advice(soil_ph),
            "disease_watch":    advice_db["disease_watch"],
            "market_tip":       advice_db["market_tip"],
        },
        "risk_flags":       risks,
        "what_if": {
            "description":      "Yield with improved seeds + irrigation + 100 kg fertilizer",
            "yield_tons":       yield_best,
            "uplift_percent":   uplift_pct,
        },
    }