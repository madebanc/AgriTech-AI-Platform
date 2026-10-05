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
    # ── Nigerian state coordinates for weather lookup ─────────────────────
# Coordinates for the main farming area of each state
NIGERIAN_STATES = {
    "Abia":          {"lat": 5.4527,  "lon": 7.5248,  "region": "south_east"},
    "Adamawa":       {"lat": 9.3265,  "lon": 12.3984, "region": "north_east"},
    "Akwa Ibom":     {"lat": 5.0079,  "lon": 7.8497,  "region": "south_south"},
    "Anambra":       {"lat": 6.2104,  "lon": 7.0688,  "region": "south_east"},
    "Bauchi":        {"lat": 10.3158, "lon": 9.8442,  "region": "north_east"},
    "Bayelsa":       {"lat": 4.7719,  "lon": 6.0699,  "region": "south_south"},
    "Benue":         {"lat": 7.3369,  "lon": 8.7404,  "region": "north_central"},
    "Borno":         {"lat": 11.8846, "lon": 13.1571, "region": "north_east"},
    "Cross River":   {"lat": 5.8702,  "lon": 8.5988,  "region": "south_south"},
    "Delta":         {"lat": 5.8904,  "lon": 5.6801,  "region": "south_south"},
    "Ebonyi":        {"lat": 6.2649,  "lon": 8.0137,  "region": "south_east"},
    "Edo":           {"lat": 6.5659,  "lon": 5.7153,  "region": "south_south"},
    "Ekiti":         {"lat": 7.7190,  "lon": 5.3110,  "region": "south_west"},
    "Enugu":         {"lat": 6.4584,  "lon": 7.5464,  "region": "south_east"},
    "FCT Abuja":     {"lat": 9.0579,  "lon": 7.4951,  "region": "north_central"},
    "Gombe":         {"lat": 10.2897, "lon": 11.1673, "region": "north_east"},
    "Imo":           {"lat": 5.4921,  "lon": 7.0299,  "region": "south_east"},
    "Jigawa":        {"lat": 12.2280, "lon": 9.5615,  "region": "north_west"},
    "Kaduna":        {"lat": 10.5264, "lon": 7.4384,  "region": "north_west"},
    "Kano":          {"lat": 12.0022, "lon": 8.5920,  "region": "north_west"},
    "Katsina":       {"lat": 12.9908, "lon": 7.6018,  "region": "north_west"},
    "Kebbi":         {"lat": 12.4539, "lon": 4.1975,  "region": "north_west"},
    "Kogi":          {"lat": 7.7337,  "lon": 6.6906,  "region": "north_central"},
    "Kwara":         {"lat": 8.4966,  "lon": 4.5421,  "region": "north_central"},
    "Lagos":         {"lat": 6.5244,  "lon": 3.3792,  "region": "south_west"},
    "Nasarawa":      {"lat": 8.4996,  "lon": 8.1997,  "region": "north_central"},
    "Niger":         {"lat": 9.9309,  "lon": 5.5983,  "region": "north_central"},
    "Ogun":          {"lat": 7.1601,  "lon": 3.3497,  "region": "south_west"},
    "Ondo":          {"lat": 7.2508,  "lon": 5.2103,  "region": "south_west"},
    "Osun":          {"lat": 7.5629,  "lon": 4.5200,  "region": "south_west"},
    "Oyo":           {"lat": 7.3775,  "lon": 3.9470,  "region": "south_west"},
    "Plateau":       {"lat": 9.2182,  "lon": 9.5179,  "region": "north_central"},
    "Rivers":        {"lat": 4.8156,  "lon": 7.0498,  "region": "south_south"},
    "Sokoto":        {"lat": 13.0059, "lon": 5.2476,  "region": "north_west"},
    "Taraba":        {"lat": 7.8700,  "lon": 11.3696, "region": "north_east"},
    "Yobe":          {"lat": 12.2938, "lon": 11.7467, "region": "north_east"},
    "Zamfara":       {"lat": 12.1700, "lon": 6.6600,  "region": "north_west"},
}

# Expected annual rainfall by region (mm) — used as fallback
REGION_RAINFALL = {
    "south_south":  2000,
    "south_east":   1500,
    "south_west":   1300,
    "north_central": 1100,
    "north_east":    800,
    "north_west":    600,
}

def get_state_list():
    """Returns sorted list of all Nigerian states"""
    return sorted(NIGERIAN_STATES.keys())

# ─────────────────────────────────────────────────────────────────────
# CROP DISEASE ENCYCLOPEDIA
# Added Day 11 — Daniel Oyanogbezina
# 14 diseases across 6 crops with symptoms, treatment, prevention
# ─────────────────────────────────────────────────────────────────────

CROP_DISEASES = {
    "Cassava": [
        {
            "name":     "Cassava Mosaic Disease (CMD)",
            "pathogen": "Begomovirus — spread by whiteflies",
            "severity": "critical",
            "symptoms": [
                "Yellow-green mosaic patterns on leaves",
                "Distorted and twisted young leaves",
                "Stunted plant growth",
                "Reduced root size and quality"
            ],
            "treatment": [
                "Remove and destroy all infected plants immediately",
                "Do not use cuttings from infected plants",
                "Plant resistant varieties: TME 419, IITA TMS",
                "Control whitefly vectors with neem-based insecticide",
                "Maintain field hygiene — clear all crop debris"
            ],
            "prevention": [
                "Always use certified disease-free planting material",
                "Plant resistant varieties from IITA or NASC",
                "Monitor fields weekly for early detection",
                "Control whitefly population proactively"
            ],
            "yield_loss": "20 - 95%",
            "local_names": {
                "yoruba": "Arun Kasava",
                "hausa":  "Cuta rogo",
                "igbo":   "Oria ji oyibo"
            }
        },
        {
            "name":     "Cassava Brown Streak Disease (CBSD)",
            "pathogen": "Ipomovirus — spread by whiteflies",
            "severity": "critical",
            "symptoms": [
                "Yellow blotches along leaf veins",
                "Brown streaks on green stems",
                "Dry brown rot inside storage roots",
                "Roots look healthy outside but rotten inside"
            ],
            "treatment": [
                "Remove and burn all infected plants completely",
                "Never reuse planting material from infected farm",
                "Plant CBSD-resistant varieties from IITA",
                "Contact nearest agricultural extension office"
            ],
            "prevention": [
                "Use only certified clean planting material",
                "Avoid moving planting material from infected areas",
                "Plant tolerant varieties where disease is present",
                "Practice strict field sanitation"
            ],
            "yield_loss": "70 - 100%",
            "local_names": {
                "yoruba": "Arun gbongbo kasava",
                "hausa":  "Cutar tushen rogo",
                "igbo":   "Orịa cassava"
            }
        },
        {
            "name":     "Cassava Anthracnose Disease (CAD)",
            "pathogen": "Colletotrichum gloeosporioides (fungus)",
            "severity": "medium",
            "symptoms": [
                "Die-back of shoot tips and young stems",
                "Dark brown lesions on stems",
                "Cankers that girdle the stem",
                "Leaves wilt and fall prematurely"
            ],
            "treatment": [
                "Prune and destroy affected plant parts",
                "Apply copper-based fungicide to cut wounds",
                "Improve air circulation by wider spacing",
                "Avoid overhead irrigation"
            ],
            "prevention": [
                "Use disease-free planting material",
                "Avoid wounding plants during weeding",
                "Apply preventive copper fungicide spray",
                "Ensure good field drainage"
            ],
            "yield_loss": "10 - 30%",
            "local_names": {
                "yoruba": "Arun igi kasava",
                "hausa":  "Cutar bawon rogo",
                "igbo":   "Orịa ụgbọ cassava"
            }
        },
        {
            "name":     "Cassava Bacterial Blight (CBB)",
            "pathogen": "Xanthomonas axonopodis (bacteria)",
            "severity": "high",
            "symptoms": [
                "Angular water-soaked spots on leaves",
                "Wilting of leaves and shoot tips",
                "Gummy bacterial exudate on stems",
                "Systemic wilting in severe cases"
            ],
            "treatment": [
                "Remove infected plant material immediately",
                "Apply copper-based bactericide spray",
                "Avoid working in field when plants are wet",
                "Disinfect farm tools between plants"
            ],
            "prevention": [
                "Plant resistant varieties",
                "Use pathogen-free planting material",
                "Practice crop rotation",
                "Avoid water stress during dry periods"
            ],
            "yield_loss": "15 - 50%",
            "local_names": {
                "yoruba": "Arun kokoro kasava",
                "hausa":  "Cuta ta kwayoyin cuta rogo",
                "igbo":   "Orịa bacteria cassava"
            }
        },
    ],

    "Maize": [
        {
            "name":     "Fall Armyworm (FAW)",
            "pathogen": "Spodoptera frugiperda (insect pest)",
            "severity": "critical",
            "symptoms": [
                "Ragged holes in whorl leaves",
                "Sawdust-like frass (droppings) in whorl",
                "Larvae visible inside whorl at night",
                "Severe defoliation of young plants"
            ],
            "treatment": [
                "Apply emamectin benzoate or spinetoram insecticide",
                "Spray early morning or late evening",
                "Use neem-based biopesticide for mild infestations",
                "Remove and destroy heavily infested plants",
                "Apply sand mixed with ash into the whorl"
            ],
            "prevention": [
                "Monitor fields twice weekly from plant emergence",
                "Plant early to avoid peak pest season",
                "Use pheromone traps to monitor adult moths",
                "Encourage natural predators: birds and wasps"
            ],
            "yield_loss": "20 - 100%",
            "local_names": {
                "yoruba": "Kokoro aginju agbado",
                "hausa":  "Tsutsatsin masara",
                "igbo":   "Ochịchọ ọka"
            }
        },
        {
            "name":     "Maize Streak Virus (MSV)",
            "pathogen": "Mastrevirus — spread by leafhoppers",
            "severity": "high",
            "symptoms": [
                "Pale yellow streaks running along leaf veins",
                "Streaks appear on young leaves first",
                "Severely stunted plant growth",
                "Ear formation greatly reduced"
            ],
            "treatment": [
                "No cure — remove infected plants early",
                "Control leafhopper vectors with insecticide",
                "Replant with resistant varieties immediately"
            ],
            "prevention": [
                "Plant streak-resistant maize varieties",
                "Early planting to avoid leafhopper peak season",
                "Remove infected plants before virus spreads",
                "Keep field surroundings clear of weeds"
            ],
            "yield_loss": "10 - 100%",
            "local_names": {
                "yoruba": "Arun ila agbado",
                "hausa":  "Cutar layin masara",
                "igbo":   "Orịa ọka"
            }
        },
        {
            "name":     "Maize Rust",
            "pathogen": "Puccinia sorghi (fungus)",
            "severity": "medium",
            "symptoms": [
                "Small reddish-brown pustules on leaves",
                "Pustules appear on both leaf surfaces",
                "Severe infection causes leaf yellowing",
                "Premature leaf death in late stages"
            ],
            "treatment": [
                "Apply propiconazole or mancozeb fungicide",
                "Spray at first sign of infection",
                "Repeat application after 14 days if needed"
            ],
            "prevention": [
                "Plant rust-resistant maize varieties",
                "Avoid excessive nitrogen fertilizer",
                "Ensure adequate plant spacing for airflow",
                "Destroy crop debris after harvest"
            ],
            "yield_loss": "10 - 40%",
            "local_names": {
                "yoruba": "Arun pupa agbado",
                "hausa":  "Tsatsa masara",
                "igbo":   "Orịa ọcha ọka"
            }
        },
    ],

    "Yam": [
        {
            "name":     "Yam Anthracnose",
            "pathogen": "Colletotrichum gloeosporioides (fungus)",
            "severity": "high",
            "symptoms": [
                "Irregular brown-black lesions on leaves",
                "Die-back of stem tips",
                "Dark sunken spots on tubers",
                "Premature defoliation of plant"
            ],
            "treatment": [
                "Apply mancozeb or copper oxychloride fungicide",
                "Spray every 14 days during wet season",
                "Remove and destroy infected plant material",
                "Treat seed yams with fungicide before planting"
            ],
            "prevention": [
                "Use disease-free seed yams only",
                "Treat seed yams with wood ash before planting",
                "Ensure good drainage in yam plots",
                "Rotate crops — avoid replanting in same spot"
            ],
            "yield_loss": "20 - 80%",
            "local_names": {
                "yoruba": "Arun ijisu",
                "hausa":  "Cutar doya",
                "igbo":   "Orịa ji"
            }
        },
        {
            "name":     "Yam Mosaic Virus",
            "pathogen": "Potyvirus — spread by aphids",
            "severity": "medium",
            "symptoms": [
                "Yellow mosaic patterns on young leaves",
                "Leaf distortion and curling",
                "Reduced plant vigour",
                "Smaller tubers at harvest"
            ],
            "treatment": [
                "Remove and destroy infected plants",
                "Control aphid vectors with insecticide",
                "Do not propagate from infected tubers"
            ],
            "prevention": [
                "Use certified virus-free seed yams",
                "Control aphid populations early in season",
                "Remove infected plants promptly",
                "Avoid planting near infected fields"
            ],
            "yield_loss": "15 - 60%",
            "local_names": {
                "yoruba": "Arun aworan isu",
                "hausa":  "Cutar mosaic doya",
                "igbo":   "Orịa mosaic ji"
            }
        },
        {
            "name":     "Dry Rot (Yam Storage Rot)",
            "pathogen": "Botryodiplodia theobromae (fungus)",
            "severity": "high",
            "symptoms": [
                "Dark discolouration under tuber skin",
                "Dry shrunken internal tissue",
                "White fungal growth on stored yams",
                "Rapid spread to healthy tubers in storage"
            ],
            "treatment": [
                "Remove all rotting tubers from store immediately",
                "Disinfect storage facility thoroughly",
                "Apply wood ash to remaining healthy tubers",
                "Improve ventilation in storage facility"
            ],
            "prevention": [
                "Cure yams properly before storage (shade dry 1-2 weeks)",
                "Never store damaged or bruised tubers",
                "Treat storage facility with lime wash",
                "Inspect stored yams weekly"
            ],
            "yield_loss": "20 - 70% post-harvest",
            "local_names": {
                "yoruba": "Ibaje ibi ipamo isu",
                "hausa":  "Rubewar doya",
                "igbo":   "Orịa ji n'onodu"
            }
        },
    ],

    "Rice": [
        {
            "name":     "Rice Blast",
            "pathogen": "Magnaporthe oryzae (fungus)",
            "severity": "critical",
            "symptoms": [
                "Diamond-shaped grey-brown spots on leaves",
                "White to grey lesions with brown borders",
                "Neck rot — panicle neck turns brown and breaks",
                "Empty or half-filled grains at harvest"
            ],
            "treatment": [
                "Apply tricyclazole or isoprothiolane fungicide",
                "Spray at tillering and panicle initiation stages",
                "Drain field and reduce nitrogen application",
                "Repeat spray after 7-10 days if severe"
            ],
            "prevention": [
                "Plant blast-resistant rice varieties",
                "Avoid excessive nitrogen fertilizer",
                "Maintain healthy plant population density",
                "Use certified disease-free seeds only"
            ],
            "yield_loss": "10 - 100%",
            "local_names": {
                "yoruba": "Arun iresi",
                "hausa":  "Cutar shinkafa",
                "igbo":   "Orịa osịkapa"
            }
        },
        {
            "name":     "Bacterial Leaf Blight (BLB)",
            "pathogen": "Xanthomonas oryzae pv. oryzae",
            "severity": "high",
            "symptoms": [
                "Water-soaked to yellowish stripes on leaf edges",
                "Leaf margin turns yellow then brown and dies",
                "Milky bacterial ooze on infected tissue",
                "Wilting of young plants in kresek phase"
            ],
            "treatment": [
                "Apply copper-based bactericide spray",
                "Drain the paddy field temporarily",
                "Remove and destroy severely infected plants",
                "Avoid excessive nitrogen during infection period"
            ],
            "prevention": [
                "Use resistant rice varieties",
                "Maintain proper irrigation — avoid water stress",
                "Use balanced fertilizer — not excess nitrogen",
                "Disinfect seeds before planting"
            ],
            "yield_loss": "20 - 50%",
            "local_names": {
                "yoruba": "Arun kokoro iresi",
                "hausa":  "Cutar bala shinkafa",
                "igbo":   "Orịa bacteria osịkapa"
            }
        },
    ],

    "Groundnut": [
        {
            "name":     "Groundnut Rosette Disease",
            "pathogen": "Groundnut Rosette Virus — spread by aphids",
            "severity": "critical",
            "symptoms": [
                "Stunted plants with small clustered leaves",
                "Mosaic and mottling patterns on leaves",
                "Chlorotic rosette — leaves turn pale yellow",
                "No pod formation in severely infected plants"
            ],
            "treatment": [
                "Remove and destroy infected plants immediately",
                "Control aphid vectors urgently with insecticide",
                "Apply imidacloprid for rapid aphid control",
                "No effective chemical cure — prevention is critical"
            ],
            "prevention": [
                "Plant rosette-resistant varieties: SAMNUT series",
                "Plant early at start of rains to avoid aphid peak",
                "Maintain high plant population — border rows sacrificed",
                "Apply insecticide at emergence to protect young plants"
            ],
            "yield_loss": "50 - 100%",
            "local_names": {
                "yoruba": "Arun epa",
                "hausa":  "Cutar gyada",
                "igbo":   "Orịa ahịhịa"
            }
        },
        {
            "name":     "Early Leaf Spot",
            "pathogen": "Cercospora arachidicola (fungus)",
            "severity": "medium",
            "symptoms": [
                "Circular dark spots on upper leaf surface",
                "Yellow halo surrounding the spots",
                "Premature defoliation in severe cases",
                "Spots appear 30-40 days after planting"
            ],
            "treatment": [
                "Apply chlorothalonil or mancozeb fungicide",
                "Spray every 14 days from 30 days after emergence",
                "Remove and bury heavily infected leaves"
            ],
            "prevention": [
                "Plant resistant groundnut varieties",
                "Avoid overhead irrigation if possible",
                "Ensure good air movement through proper spacing",
                "Rotate crops — never groundnut after groundnut"
            ],
            "yield_loss": "10 - 50%",
            "local_names": {
                "yoruba": "Arun abawon epa",
                "hausa":  "Cutar batsa gyada",
                "igbo":   "Orịa akwụkwọ ahịhịa"
            }
        },
    ],

    "Cocoa": [
        {
            "name":     "Black Pod Disease",
            "pathogen": "Phytophthora megakarya (fungus-like organism)",
            "severity": "critical",
            "symptoms": [
                "Brown to black water-soaked spots on pods",
                "Rapid spread covering entire pod within days",
                "White mycelium visible on pod surface in humid conditions",
                "Beans inside rot completely — total pod loss"
            ],
            "treatment": [
                "Remove and destroy all infected pods immediately",
                "Apply copper hydroxide or metalaxyl fungicide",
                "Spray every 2-3 weeks during wet season",
                "Clear vegetation beneath trees to reduce humidity"
            ],
            "prevention": [
                "Prune trees regularly for good air circulation",
                "Remove mistletoe and epiphytes from trees",
                "Harvest ripe pods promptly — never leave on tree",
                "Apply preventive copper fungicide before rainy season"
            ],
            "yield_loss": "30 - 90%",
            "local_names": {
                "yoruba": "Arun pod cocoa",
                "hausa":  "Cutar bakar kwayar cocoa",
                "igbo":   "Orịa oji ojii cocoa"
            }
        },
        {
            "name":     "Cocoa Swollen Shoot Virus (CSSV)",
            "pathogen": "Badnavirus — spread by mealybugs",
            "severity": "critical",
            "symptoms": [
                "Swelling and distortion of root and stem tips",
                "Red vein banding on young leaves",
                "Yellowing and premature leaf fall",
                "Severe stunting and eventual tree death"
            ],
            "treatment": [
                "No cure exists — infected trees must be cut down",
                "Cut and destroy infected trees completely",
                "Control mealybug vectors on remaining trees",
                "Report outbreak to State Agricultural Department"
            ],
            "prevention": [
                "Use certified disease-free planting material only",
                "Control mealybug population proactively",
                "Inspect new farms for CSSV before planting nearby",
                "Maintain buffer zones around infected areas"
            ],
            "yield_loss": "25 - 50% per year until tree death",
            "local_names": {
                "yoruba": "Arun wiwu cocoa",
                "hausa":  "Cutar kumburi cocoa",
                "igbo":   "Orịa onụnụ cocoa"
            }
        },
    ],
}

SEVERITY_COLORS = {
    "critical": "#d94f3d",
    "high":     "#e07b00",
    "medium":   "#f4a900",
    "low":      "#1a6b3c",
}


def get_diseases(crop: str) -> list:
    """Returns disease list for a crop"""
    crop = crop.strip().title()
    return CROP_DISEASES.get(crop, [])


def get_all_diseases() -> dict:
    """Returns disease count per crop"""
    return {crop: len(diseases)
            for crop, diseases in CROP_DISEASES.items()}