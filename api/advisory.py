"""
advisory.py
AgriTech AI Platform — Crop Advisory Knowledge Base
Author : Daniel Oyanogbezina
Purpose: Encodes Nigerian agricultural expertise as reusable data
         Called by predictor.py and app.py
"""

import datetime

# ── Crop advisory database ────────────────────────────────────────────
CROP_ADVICE = {
    "Cassava": {
        "season":        "Plant: March-April or August-September",
        "soil_ph":       "Best pH: 5.5 - 6.5",
        "spacing":       "Spacing: 1m x 1m (10,000 stands/ha)",
        "harvest":       "Harvest: 9-12 months after planting",
        "fertilizer":    "Apply NPK 15-15-15 at 6 weeks after planting",
        "water_need":    "Moderate — tolerates short dry spells",
        "disease_watch": "Watch for: Cassava Mosaic Disease, Brown Streak",
        "market_tip":    "Best selling months: December - February",
        "price_range":   [40_000, 80_000],   # Naira per ton
    },
    "Yam": {
        "season":        "Plant: January-March (before first rains)",
        "soil_ph":       "Best pH: 5.5 - 6.0",
        "spacing":       "Spacing: 1m x 1m on ridges or mounds",
        "harvest":       "Harvest: 7-10 months after planting",
        "fertilizer":    "Apply NPK at planting + top-dress at 8 weeks",
        "water_need":    "High in first 3 months",
        "disease_watch": "Watch for: Yam Anthracnose, Dry Rot",
        "market_tip":    "Best selling months: August - October (New Yam Festival)",
        "price_range":   [200_000, 400_000],
    },
    "Maize": {
        "season":        "Plant: March-April (1st) or July-August (2nd season)",
        "soil_ph":       "Best pH: 5.8 - 7.0",
        "spacing":       "Spacing: 75cm x 25cm (2 seeds per hole)",
        "harvest":       "Harvest: 90-120 days after planting",
        "fertilizer":    "NPK at planting + Urea top-dress at 6 weeks",
        "water_need":    "Critical during tasselling — prevent drought stress",
        "disease_watch": "Watch for: Fall Armyworm (inspect weekly at night)",
        "market_tip":    "Best selling months: November - January",
        "price_range":   [150_000, 250_000],
    },
    "Rice": {
        "season":        "Plant: May-June (wet season)",
        "soil_ph":       "Best pH: 5.5 - 6.5",
        "spacing":       "Spacing: 20cm x 20cm (transplanting method)",
        "harvest":       "Harvest: 100-140 days after planting",
        "fertilizer":    "Apply Urea in splits — at planting and at tillering",
        "water_need":    "Very high — paddy field needs standing water",
        "disease_watch": "Watch for: Rice Blast, Bacterial Leaf Blight",
        "market_tip":    "Best selling months: January - March (dry season)",
        "price_range":   [180_000, 320_000],
    },
    "Groundnut": {
        "season":        "Plant: April-May with first reliable rains",
        "soil_ph":       "Best pH: 6.0 - 6.5",
        "spacing":       "Spacing: 45cm x 15cm",
        "harvest":       "Harvest: 90-120 days after planting",
        "fertilizer":    "Phosphorus only — fixes own nitrogen",
        "water_need":    "Moderate — sensitive to waterlogging",
        "disease_watch": "Watch for: Rosette Virus, Leaf Spot",
        "market_tip":    "Best selling months: November - December",
        "price_range":   [120_000, 220_000],
    },
    "Cocoa": {
        "season":        "Plant: April-June under shade trees",
        "soil_ph":       "Best pH: 6.0 - 7.0",
        "spacing":       "Spacing: 3m x 3m with shade trees",
        "harvest":       "First harvest: 3-5 years after planting",
        "fertilizer":    "Annual NPK + micronutrients application",
        "water_need":    "High and consistent — not drought tolerant",
        "disease_watch": "Watch for: Black Pod Disease, Swollen Shoot Virus",
        "market_tip":    "Sell through co-operatives for better price",
        "price_range":   [800_000, 1_500_000],
    },
}

# ── Crop calendar: 6 crops x 12 months ───────────────────────────────
CROP_CALENDAR = {
    "Cassava": {
        1:  "Prepare land, clear and till. Source improved cuttings.",
        2:  "Continue land preparation. Apply pre-planting fertilizer.",
        3:  "PLANT. Use 25-30 cm cuttings. Space 1m x 1m.",
        4:  "First weeding. Monitor for whitefly (mosaic vector).",
        5:  "Apply NPK fertilizer. Second weeding.",
        6:  "Monitor for disease. Remove infected plants immediately.",
        7:  "Weed if needed. Canopy should be closing.",
        8:  "SECOND SEASON PLANTING. Inspect for stem borers.",
        9:  "Apply foliar spray if needed. Monitor field.",
        10: "Begin harvesting early-maturing varieties.",
        11: "Peak harvest season. Negotiate with processors early.",
        12: "Harvest and process. Best market prices this month.",
    },
    "Yam": {
        1:  "PLANT. Use 200-500 g seed yams on mounds 1m apart.",
        2:  "Stake plants as they emerge. First weeding.",
        3:  "Apply NPK fertilizer. Ensure stakes are firm.",
        4:  "Monitor for mealybugs and beetles.",
        5:  "Top-dress fertilizer. Mulch around mounds.",
        6:  "Weed carefully — roots are near the surface.",
        7:  "Monitor tuber development. Do not harvest yet.",
        8:  "Begin harvesting early varieties. New Yam Festival period.",
        9:  "PEAK HARVEST. Best prices of the year.",
        10: "Final harvest. Cure tubers in shade for 1-2 weeks.",
        11: "Store cured yams. Inspect weekly for rot.",
        12: "Market stored yams. Plan next season seed yams.",
    },
    "Maize": {
        1:  "Plan season. Source certified seeds from agro-dealer.",
        2:  "Prepare land. Test soil pH.",
        3:  "PLANT first season. Apply basal NPK fertilizer.",
        4:  "First weeding. Inspect nightly for Fall Armyworm.",
        5:  "Top-dress with Urea. Critical tasselling period.",
        6:  "Harvest first season. Dry grain to 13% moisture.",
        7:  "PLANT second season immediately after first harvest.",
        8:  "Weed and fertilize second season crop.",
        9:  "Watch for disease. Apply fungicide if needed.",
        10: "Harvest second season. Store properly.",
        11: "BEST PRICES this month. Sell stored grain now.",
        12: "Market and plan next year. Rotate with legume crop.",
    },
    "Rice": {
        1:  "Best prices for stored rice. Sell now.",
        2:  "Prepare paddy fields. Repair bunds and channels.",
        3:  "Source certified seeds. Prepare nursery beds.",
        4:  "Nursery sowing. Soak seeds 24 hours before sowing.",
        5:  "TRANSPLANT to main field. Apply basal fertilizer.",
        6:  "Maintain water level. First Urea application.",
        7:  "Second Urea at tillering stage. Manage weeds.",
        8:  "Panicle initiation — maintain water level strictly.",
        9:  "Monitor for blast disease. Drain field 2 weeks pre-harvest.",
        10: "HARVEST when 80% of grains turn golden.",
        11: "Dry and mill. Store in sealed bags.",
        12: "Market. Prices rising — consider holding stock.",
    },
    "Groundnut": {
        1:  "Prepare land. Source certified seeds.",
        2:  "Till to 20 cm depth. Apply phosphorus fertilizer.",
        3:  "Wait for reliable rains before planting.",
        4:  "PLANT with first reliable rains. Space 45 x 15 cm.",
        5:  "First weeding. Earth up around plants.",
        6:  "Watch for Rosette virus. Remove infected plants.",
        7:  "Stop weeding — pegs entering soil. Do not disturb.",
        8:  "Monitor maturity. Yellowing leaves signal readiness.",
        9:  "HARVEST. Dry in windrows for 2 weeks.",
        10: "Shell and grade. Sell premium grade first.",
        11: "BEST PRICES November-December. Market now.",
        12: "Market remaining stock. Plan next season.",
    },
    "Cocoa": {
        1:  "Prune trees. Remove dead wood and mistletoe.",
        2:  "Apply potassium fertilizer to established trees.",
        3:  "Monitor for Black Pod. Apply copper-based fungicide.",
        4:  "MAIN PLANTING SEASON for new cocoa farms.",
        5:  "Fertilize established farms. Clear undergrowth.",
        6:  "Harvest mid-crop pods. Ferment 6 days precisely.",
        7:  "Monitor Black Pod intensively (wet season peak).",
        8:  "Continue mid-crop harvest. Apply fungicide.",
        9:  "Prepare for main crop. Clear harvesting paths.",
        10: "MAIN CROP starts. Harvest ripe pods every 2 weeks.",
        11: "Peak main crop harvest. Ferment and dry carefully.",
        12: "Final main crop. Grade carefully and sell to co-ops.",
    },
}

SUPPORTED_CROPS = list(CROP_ADVICE.keys())

MONTH_NAMES = [
    "", "January", "February", "March", "April",
    "May", "June", "July", "August", "September",
    "October", "November", "December",
]

# ── Helper functions ──────────────────────────────────────────────────

def rainfall_advice(mm: float) -> str:
    if mm < 600:
        return "Very dry — irrigation is ESSENTIAL for any crop."
    if mm < 900:
        return "Dry — supplement with irrigation. Mulch to retain moisture."
    if mm < 1200:
        return "Moderate — good for most crops. Monitor soil moisture weekly."
    if mm < 1600:
        return "Good rainfall — focus on drainage and disease prevention."
    return "Very wet — high flood/fungal risk. Ensure drainage channels are clear."


def soil_ph_advice(ph: float) -> str:
    if ph < 5.0:
        return "Very acidic — apply agricultural lime before planting."
    if ph < 5.5:
        return "Slightly acidic — lime application recommended."
    if ph <= 6.5:
        return "Optimal pH range — most crops will thrive."
    if ph <= 7.0:
        return "Slightly alkaline — suitable for maize and groundnut."
    return "Too alkaline — sulphur application may be needed."


def get_risk_flags(crop, rainfall_mm, soil_ph,
                   fertilizer_kg, improved_seeds, irrigation) -> list:
    flags = []
    if rainfall_mm < 800 and not irrigation:
        flags.append("LOW RAINFALL + NO IRRIGATION: yield at serious risk — add water source.")
    if soil_ph < 5.5:
        flags.append("LOW SOIL pH: apply agricultural lime before planting.")
    if fertilizer_kg < 20:
        flags.append("LOW FERTILIZER: apply at least 50 kg/ha NPK for meaningful yield.")
    if not improved_seeds:
        flags.append("TRADITIONAL SEEDS: improved varieties typically add 15-25% yield.")
    if rainfall_mm > 1800 and crop == "Groundnut":
        flags.append("HIGH RAINFALL + GROUNDNUT: plant on ridges to prevent waterlogging.")
    if crop == "Rice" and not irrigation and rainfall_mm < 1000:
        flags.append("RICE NEEDS WATER: irrigation or paddy system strongly recommended.")
    return flags


def get_calendar(crop: str, month: int = None) -> dict:
    if month is None:
        month = datetime.datetime.now().month
    crop = crop.strip().title()
    if crop not in CROP_CALENDAR:
        return {"error": f"Crop '{crop}' not found."}
    prev_m = 12 if month == 1  else month - 1
    next_m = 1  if month == 12 else month + 1
    return {
        "crop":          crop,
        "month":         MONTH_NAMES[month],
        "last_month":    {"month": MONTH_NAMES[prev_m], "task": CROP_CALENDAR[crop][prev_m]},
        "this_month":    {"month": MONTH_NAMES[month],  "task": CROP_CALENDAR[crop][month]},
        "next_month":    {"month": MONTH_NAMES[next_m], "task": CROP_CALENDAR[crop][next_m]},
    }