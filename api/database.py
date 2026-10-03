"""
database.py — AgriTech AI Platform
Author : Daniel Oyanogbezina
Purpose: Logs every prediction to SQLite
         Powers the analytics dashboard
"""

import sqlite3
import os
from datetime import datetime

# Database lives in the project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH  = os.path.join(BASE_DIR, "agritech_analytics.db")


def get_connection():
    """Open a database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row   # rows behave like dicts
    return conn


def init_database():
    """Create tables if they don't exist yet"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp     TEXT    NOT NULL,
            crop          TEXT    NOT NULL,
            state         TEXT,
            farm_size_ha  REAL,
            rainfall_mm   REAL,
            soil_ph       REAL,
            fertilizer_kg REAL,
            improved_seeds INTEGER,
            irrigation     INTEGER,
            yield_tons     REAL,
            income_mid_ngn REAL,
            risk_count     INTEGER DEFAULT 0,
            uplift_percent REAL
        )
    """)

    conn.commit()
    conn.close()
    print("[database] Tables ready")


def log_prediction(data: dict, result: dict):
    """
    Save one prediction to the database.
    Called from app.py after every successful /api/predict
    """
    try:
        conn   = get_connection()
        cursor = conn.cursor()

        prediction = result.get("prediction", {})
        risk_flags = result.get("risk_flags", [])
        what_if    = result.get("what_if", {})

        cursor.execute("""
            INSERT INTO predictions (
                timestamp, crop, state, farm_size_ha,
                rainfall_mm, soil_ph, fertilizer_kg,
                improved_seeds, irrigation,
                yield_tons, income_mid_ngn,
                risk_count, uplift_percent
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.utcnow().isoformat(),
            data.get("crop"),
            data.get("state", "Unknown"),
            data.get("farm_size_ha"),
            data.get("rainfall_mm"),
            data.get("soil_ph"),
            data.get("fertilizer_kg"),
            int(data.get("improved_seeds", False)),
            int(data.get("irrigation", False)),
            prediction.get("yield_tons"),
            prediction.get("income_mid_ngn"),
            len(risk_flags),
            what_if.get("uplift_percent"),
        ))

        conn.commit()
        conn.close()

    except Exception as e:
        # Never let a logging error break the main prediction
        print(f"[database] Logging error (non-critical): {e}")


def get_analytics() -> dict:
    """
    Returns all analytics data for the dashboard.
    Handles empty database gracefully.
    """
    conn   = get_connection()
    cursor = conn.cursor()

    try:
        # Total predictions
        cursor.execute("SELECT COUNT(*) FROM predictions")
        total = cursor.fetchone()[0]

        if total == 0:
            return _empty_analytics()

        # Predictions by crop
        cursor.execute("""
            SELECT crop, COUNT(*) as count
            FROM predictions
            GROUP BY crop
            ORDER BY count DESC
        """)
        by_crop = [dict(row) for row in cursor.fetchall()]

        # Predictions by state (top 10)
        cursor.execute("""
            SELECT state, COUNT(*) as count
            FROM predictions
            WHERE state IS NOT NULL AND state != 'Unknown'
            GROUP BY state
            ORDER BY count DESC
            LIMIT 10
        """)
        by_state = [dict(row) for row in cursor.fetchall()]

        # Predictions over last 14 days
        cursor.execute("""
            SELECT DATE(timestamp) as day, COUNT(*) as count
            FROM predictions
            WHERE timestamp >= DATE('now', '-14 days')
            GROUP BY DATE(timestamp)
            ORDER BY day ASC
        """)
        over_time = [dict(row) for row in cursor.fetchall()]

        # Average yield by crop
        cursor.execute("""
            SELECT crop,
                   ROUND(AVG(yield_tons), 1)  as avg_yield,
                   ROUND(AVG(income_mid_ngn)) as avg_income
            FROM predictions
            WHERE yield_tons IS NOT NULL
            GROUP BY crop
            ORDER BY avg_yield DESC
        """)
        avg_yield = [dict(row) for row in cursor.fetchall()]

        # Risk flag summary
        cursor.execute("""
            SELECT
              SUM(CASE WHEN risk_count = 0 THEN 1 ELSE 0 END) as no_risk,
              SUM(CASE WHEN risk_count = 1 THEN 1 ELSE 0 END) as one_risk,
              SUM(CASE WHEN risk_count = 2 THEN 1 ELSE 0 END) as two_risk,
              SUM(CASE WHEN risk_count >= 3 THEN 1 ELSE 0 END) as three_plus
            FROM predictions
        """)
        risk_row    = cursor.fetchone()
        risk_summary = dict(risk_row) if risk_row else {}

        # Key metrics
        cursor.execute("""
            SELECT
              ROUND(AVG(yield_tons), 1)         as avg_yield,
              ROUND(AVG(income_mid_ngn))         as avg_income,
              ROUND(AVG(uplift_percent), 1)      as avg_uplift,
              SUM(CASE WHEN improved_seeds = 1
                  THEN 1 ELSE 0 END) * 100.0
                  / COUNT(*)                     as pct_improved_seeds,
              SUM(CASE WHEN irrigation = 1
                  THEN 1 ELSE 0 END) * 100.0
                  / COUNT(*)                     as pct_irrigation
            FROM predictions
        """)
        metrics = dict(cursor.fetchone() or {})

        conn.close()

        return {
            "total_predictions": total,
            "by_crop":           by_crop,
            "by_state":          by_state,
            "over_time":         over_time,
            "avg_yield_by_crop": avg_yield,
            "risk_summary":      risk_summary,
            "key_metrics":       metrics,
        }

    except Exception as e:
        conn.close()
        print(f"[database] Analytics error: {e}")
        return _empty_analytics()


def _empty_analytics() -> dict:
    """Returns when no data exists yet"""
    return {
        "total_predictions": 0,
        "by_crop":           [],
        "by_state":          [],
        "over_time":         [],
        "avg_yield_by_crop": [],
        "risk_summary":      {},
        "key_metrics":       {},
        "message":           "No predictions yet. Make some predictions to see analytics!"
    }


# Initialise on import
init_database()