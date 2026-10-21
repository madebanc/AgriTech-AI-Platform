/**
 * translations.js — AgriTech AI Platform
 * Author : Daniel Oyanogbezina
 * Purpose: All UI text in 4 Nigerian languages
 *          English (EN), Yoruba (YO), Hausa (HA), Igbo (IG)
 *
 * Usage:
 *   LANG.setLanguage('yo')   — switches to Yoruba
 *   LANG.t('btn_predict')    — returns translated string
 *   LANG.current             — current language code
 */

const TRANSLATIONS = {

  /* ── English (default) ──────────────────────────────── */
  en: {
    /* Header */
    app_name:          "AgriTech AI",
    app_sub:           "Farmer Advisory Platform",

    /* Hero */
    hero_title:        "AI-Powered Crop Yield Prediction",
    hero_sub:          "Select your state and crop. Our AI analyses your conditions to predict yield, estimate income, and flag risks — in seconds.",
    stat_crops:        "Crops Supported",
    stat_states:       "Nigerian States",
    stat_ai:           "Risk Detection",

    /* Form labels */
    form_title:        "Enter Your Farm Details",
    label_crop:        "Crop Type",
    label_state:       "Nigerian State",
    label_farm_size:   "Farm Size (hectares)",
    label_rainfall:    "Annual Rainfall (mm)",
    label_soil_ph:     "Soil pH",
    label_fertilizer:  "Fertilizer (kg/ha)",
    label_seeds:       "Improved Seeds?",
    label_irrigation:  "Irrigation Available?",
    seeds_yes:         "Yes",
    seeds_no:          "No",
    irrigation_yes:    "Yes",
    irrigation_no:     "No (rain-fed)",
    btn_predict:       "Get AI Prediction",

    /* Placeholders */
    ph_crop:           "-- Select your crop --",
    ph_state:          "-- Select your state --",
    ph_farm_size:      "e.g. 2.5",
    ph_rainfall:       "Select state above to auto-fill",
    ph_soil_ph:        "e.g. 6.2",
    ph_fertilizer:     "e.g. 100",

    /* Hints */
    hint_soil_ph:      "Optimal: 5.5 – 6.5 for most crops",
    hint_rainfall:     "Auto-filled from weather data when you select a state",
    hint_seeds:        "Modern varieties from IITA / NASC",
    autofill_badge:    "Auto-filled",
    action_title: "What to do now",
    action_now: "Do this now",
    action_plan: "Get ready",
    action_month_task: "Your {crop} task for {month}",
    action_next_task: "Next month: {task}",
    action_sell: "Best time to sell",
    urg_now: "Do this now",
    urg_plant: "Time to plant",
    urg_harvest: "Time to harvest",
    urg_spray: "Time to spray",
    urg_weed: "Time to weed",
    urg_fert: "Time to fertilise",
    market_title: "Market timing and money",
    market_best: "Best selling months",
    market_bag_price: "Price per 50 kg bag",
    market_your_bags: "Your expected bags",
    market_money: "Expected money if you sell",
    market_note: "Prices are indicative. Check the local market before selling.",
    market_offline: "Market prices need internet. Connect to see prices.",
    unit_hectare: "Hectare",
    unit_acre: "Acre",
    unit_plot: "Plot (648 sqm Lagos standard)",
    soil_prompt: "What is your soil like? Pick one",
    soil_sandy: "Sandy, water drains fast, light colour",
    soil_loamy: "Loamy, soft and dark, holds water well",
    soil_clay: "Clay, sticky when wet, hard when dry",
    soil_unknown: "Not sure",
    confirm_check: "Please check before we predict:",
    confirm_ask: "Is this correct? Press OK to predict, Cancel to fix.",
    plain_template: "Your {crop} on {ha} hectare may give about {tons} tons, which is about {bags} bags of 50 kg. This is an estimate for planning, not a promise. Weather and pests can change it.",
    size_template: "{v} {unit} is about {ha} hectare for the model.",
    bags_template: "{kg} kg per hectare is about {bags} bags of 50 kg.",
    helper_size_full: "15 plots is about 1 hectare. 6 plots is about 1 acre. Plot sizes differ by town, confirm with extension officer if unsure.",

    /* Results */
    result_title:      "Prediction Results",
    unit_tons:         "tons predicted",
    income_low:        "Low Estimate",
    income_mid:        "Mid Estimate",
    income_high:       "High Estimate",
    risk_title:        "Risk Flags",
    no_risk:           "No risk flags detected — your farm setup looks good!",
    whatif_title:      "What If You Upgraded?",
    whatif_current:    "Current Yield",
    whatif_best:       "With Full Inputs",
    whatif_desc:       "Improved seeds + irrigation + 100 kg/ha fertilizer",
    advice_title:      "Personalised Farming Advice",
    calendar_title:    "This Month's Actions",
    last_month:        "Last Month",
    this_month:        "This Month",
    next_month:        "Next Month",
    now_badge:         "This Month",

    /* Advice labels */
    adv_season:        "Planting Season",
    adv_spacing:       "Spacing",
    adv_harvest:       "Harvest",
    adv_fertilizer:    "Fertilizer",
    adv_water:         "Water",
    adv_soil:          "Soil",
    adv_disease:       "Disease Watch",
    adv_market:        "Market Timing",

    /* Errors */
    err_server:        "The AI server is warming up. Please wait 30 seconds and try again.",
    err_no_crop:       "Please select a crop type.",
    err_no_state:      "Please select your Nigerian state.",
    err_farm_size:     "Farm size must be at least 0.1 hectares.",
    err_rainfall:      "Rainfall must be at least 300mm. Select a state to auto-fill.",
    err_soil_ph:       "Soil pH must be between 4.0 and 9.0.",
    err_fertilizer:    "Please enter fertilizer amount (enter 0 if none used).",

    /* Status */
    status_connecting: "Connecting...",
    status_online:     "AI Online",
    status_offline:    "Server offline",
    status_waking:     "Waking up...",

    /* Footer */
    footer_built:      "Built by",
    footer_mission:    "Empowering Nigerian farmers with AI",
    uplift_text:       "potential uplift with better inputs",
  },

  /* ── Yoruba (south-west Nigeria) ────────────────────── */
  yo: {
    app_name:          "AgriTech AI",
    app_sub:           "Ipele Imọran fun Agbẹ",

    hero_title:        "Asọtẹlẹ Irugbin pẹlu Imọ-ẹrọ AI",
    hero_sub:          "Yan ipinle rẹ ati irugbin rẹ. AI wa yoo ṣe atupale awọn ipo rẹ lati ṣe asọtẹlẹ èso, owo to n bọ, ati awọn eewu.",
    stat_crops:        "Irugbin Ti a Ṣatilẹyin",
    stat_states:       "Awọn Ipinle Naijiria",
    stat_ai:           "Iwari Ewu AI",

    form_title:        "Tẹ Alaye Oko Rẹ Sii",
    label_crop:        "Iru Irugbin",
    label_state:       "Ipinle Naijiria",
    label_farm_size:   "Iwọn Oko (hektari)",
    label_rainfall:    "Omi Ojo Odun (mm)",
    label_soil_ph:     "pH Ile",
    label_fertilizer:  "Ajile (kg/ha)",
    label_seeds:       "Irugbin Ilọsiwaju?",
    label_irrigation:  "Omi Oko Wa?",
    seeds_yes:         "Bẹẹni",
    seeds_no:          "Rara",
    irrigation_yes:    "Bẹẹni",
    irrigation_no:     "Rara (ojo nikan)",
    btn_predict:       "🤖 Gba Asọtẹlẹ AI",

    ph_crop:           "-- Yan irugbin rẹ --",
    ph_state:          "-- Yan ipinle rẹ --",
    ph_farm_size:      "fun apẹẹrẹ 2.5",
    ph_rainfall:       "Yan ipinle loke lati kun aaye yii",
    ph_soil_ph:        "fun apẹẹrẹ 6.2",
    ph_fertilizer:     "fun apẹẹrẹ 100",

    hint_soil_ph:      "Ti o dara julọ: 5.5 – 6.5 fun ọpọlọpọ irugbin",
    hint_rainfall:     "A yoo kun aaye yii lẹyin ti o ba yan ipinle rẹ",
    hint_seeds:        "Awọn oriṣiiriṣi tuntun lati IITA / NASC",
    autofill_badge:    "Ti kun",
    action_title: "Ohun tí o ṣe níbi",
    action_now: "Ṣe é lẹ́ẹ̀kansí",
    action_plan: "Pẹ̀lú re",
    action_month_task: "Ọ̀rọ̀ ẹ tìlẹ̀ ẹni {crop} ní {month}",
    action_next_task: "Oṣù tí ó tẹ̀lé: {task}",
    action_sell: "Àkókò tí a tà jẹ́",
    urg_now: "Ṣe é lẹ́ẹ̀kansí",
    urg_plant: "Ìgbà ìtù",
    urg_harvest: "Ìgbà ọjà",
    urg_spray: "Ìgbà ilẹ̀",
    urg_weed: "Ìgbà ẹ̀fọ̀",
    urg_fert: "Ìgbà oṣán",
    market_title: "Ìjì Ìtajà àti Owó",
    market_best: "Oṣù tàbí nípa tàbí jẹ́",
    market_bag_price: "Iyá ọjọ́ 50 kg",
    market_your_bags: "Àpò apá ọjọ́ rẹ",
    market_money: "Owó tí o yẹ̀ kí o tà",
    market_note: "Iye owó yí ni àtúnṣe. Ṣàyẹ̀wò ọjà ilé rẹ kí o tà.",
    market_offline: "Iye owó ọjà nílò internet. Sopọ̀ ọjọ́ kan kí o rí i.",
    unit_hectare: "Hektari",
    unit_acre: "Eka",
    unit_plot: "Plot (648 sqm, iwon Lagos)",
    soil_prompt: "Iru ile re bawo? Yan okan",
    soil_sandy: "Iyanrin, omi nsan yarayara, awo feere",
    soil_loamy: "Alemo, riro ati dudu, o dan omi duro daradara",
    soil_clay: "Amo, o lemo nigbati o tutu, o le nigbati o gbe",
    soil_unknown: "Ko da loju",
    confirm_check: "Jowo sayewo saju ki a to sotele:",
    confirm_ask: "Se eyi to? Te OK lati sotele, Cancel lati satunse.",
    plain_template: "Irugbin {crop} re lori hektari {ha} le fun ni to {tons} toonu, eyi ti o je to apo {bags} ti 50 kg. Eyi je isiro fun eto, kii se ileri. Oju ojo ati kokoro le yi i pada.",
    size_template: "{v} {unit} je to {ha} hektari fun awose.",
    bags_template: "{kg} kg fun hektari kan je to apo {bags} ti 50 kg.",
    helper_size_full: "Plot 15 je to hektari 1. Plot 6 je to eka 1. Iwon plot yato si ilu si ilu, beere lowo osise itesiwaju ti o ko ba da loju.",

    result_title:      "Abajade Asọtẹlẹ",
    unit_tons:         "toonu ni asọtẹlẹ",
    income_low:        "Owo Kekere",
    income_mid:        "Owo Aarin",
    income_high:       "Owo Giga",
    risk_title:        "Awọn Ewu",
    no_risk:           "Ko si ewu ti a ri — eto oko rẹ dara!",
    whatif_title:      "Ti O Ba Siwaju Sii?",
    whatif_current:    "Èso Lọwọlọwọ",
    whatif_best:       "Pẹlu Ohun Gbogbo",
    whatif_desc:       "Irugbin ilọsiwaju + omi oko + ajile 100 kg/ha",
    advice_title:      "Imọran Ogbin Ti o Yẹ fun Ọ",
    calendar_title:    "Ohun Ti O Gbọdọ Ṣe Oṣu Yii",
    last_month:        "Oṣu Sẹhin",
    this_month:        "Oṣu Yii",
    next_month:        "Oṣu To Nbọ",
    now_badge:         "Oṣu Yii",

    adv_season:        "Akoko Dida",
    adv_spacing:       "Aaye Laarin",
    adv_harvest:       "Ikore",
    adv_fertilizer:    "Ajile",
    adv_water:         "Omi",
    adv_soil:          "Ile",
    adv_disease:       "Arun Irugbin",
    adv_market:        "Akoko Tita",

    err_server:        "Ẹrọ AI n ji dậy. Jọwọ duro iṣẹju 30 ki o tun gbiyanju.",
    err_no_crop:       "Jọwọ yan iru irugbin.",
    err_no_state:      "Jọwọ yan ipinle rẹ.",
    err_farm_size:     "Iwọn oko gbọdọ jẹ o kere hektari 0.1.",
    err_rainfall:      "Omi ojo gbọdọ jẹ o kere 300mm. Yan ipinle rẹ lati kun.",
    err_soil_ph:       "pH ile gbọdọ wa laarin 4.0 ati 9.0.",
    err_fertilizer:    "Jọwọ tẹ iye ajile (tẹ 0 ti o ko lo).",

    status_connecting: "N sopọ...",
    status_online:     "AI Wa Online",
    status_offline:    "Ẹrọ Ko Wa",
    status_waking:     "N ji dậy...",

    footer_built:      "Ti kọ nipasẹ",
    footer_mission:    "Ṣiṣe agbara agbẹ Naijiria pẹlu AI",
    uplift_text:       "dide ti o ṣeeṣe pẹlu awọn ohun elo to dara",
  },

  /* ── Hausa (northern Nigeria) ───────────────────────── */
  ha: {
    app_name:          "AgriTech AI",
    app_sub:           "Dandalin Shawarar Manomi",

    hero_title:        "Hasashen Amfanin Gona da Fasahar AI",
    hero_sub:          "Zaɓi jiharku da amfanin gonakku. AI ɗinmu zai nazarci yanayin gonakku don hasashe amfanin, kuɗin shigarwa, da gargaɗi.",
    stat_crops:        "Amfanin Gona Da Ake Tallafawa",
    stat_states:       "Jihohin Najeriya",
    stat_ai:           "AI Na Gano Haɗari",

    form_title:        "Shigar da Bayanan Gonarka",
    label_crop:        "Nau'in Amfanin Gona",
    label_state:       "Jihar Najeriya",
    label_farm_size:   "Girman Gona (hekta)",
    label_rainfall:    "Ruwan Sama Na Shekara (mm)",
    label_soil_ph:     "pH Na Ƙasa",
    label_fertilizer:  "Takin Zamani (kg/ha)",
    label_seeds:       "Ingantattun Iri?",
    label_irrigation:  "Akwai Ban Ruwa?",
    seeds_yes:         "Eh",
    seeds_no:          "A'a",
    irrigation_yes:    "Eh",
    irrigation_no:     "A'a (ruwan sama kawai)",
    btn_predict:       "🤖 Samu Hasashen AI",

    ph_crop:           "-- Zaɓi amfanin gonarka --",
    ph_state:          "-- Zaɓi jiharku --",
    ph_farm_size:      "misali 2.5",
    ph_rainfall:       "Zaɓi jiha don cike wannan filin",
    ph_soil_ph:        "misali 6.2",
    ph_fertilizer:     "misali 100",

    hint_soil_ph:      "Mafi kyau: 5.5 – 6.5 don yawancin amfanin gona",
    hint_rainfall:     "Zai cika ta atomatik bayan ka zaɓi jiha",
    hint_seeds:        "Nau'o'i na zamani daga IITA / NASC",
    autofill_badge:    "An Cika",
    action_title: "Abin da za ka yi",
    action_now: "Yi shi yanzu",
    action_plan: "Shirya",
    action_month_task: "Aikin {crop} na {month}",
    action_next_task: "Wata na farko: {task}",
    action_sell: "Mafi kyau don saye",
    urg_now: "Yi shi yanzu",
    urg_plant: "Lokacin planting",
    urg_harvest: "Lokacin harvesting",
    urg_spray: "Lokacin fesawa",
    urg_weed: "Lokacin tsuma",
    urg_fert: "Lokacin fertilizer",
    market_title: "Kasuwanni da kuɗi",
    market_best: "Wata mafi kyau ga saye",
    market_bag_price: "Kudin jiga 50 kg",
    market_your_bags: "Jigajinkin da za ka yi",
    market_money: "Kudinka da za ka samu idan ka saye",
    market_note: "Kudin wannan ana nuna ne kawai. Duba kasuwanninka kafin ka saye.",
    market_offline: "Kudin kasuwanni yana buƙatar intanet. Haɗa don gan shi.",
    unit_hectare: "Hekta",
    unit_acre: "Eka",
    unit_plot: "Fili (648 sqm, ma'aunin Legas)",
    soil_prompt: "Kasarka fa ta ke? Zabi daya",
    soil_sandy: "Yashi, ruwa yana tafiya da sauri, launi mai haske",
    soil_loamy: "Laka, mai laushi da duhu, tana rike ruwa da kyau",
    soil_clay: "Yumbu, tana likewa da jika, tana tauri da bushewa",
    soil_unknown: "Ban da tabbas",
    confirm_check: "Da fatan a duba kafin a yi hasashe:",
    confirm_ask: "Shin daidai ne? Danna OK don hasashe, Cancel don gyarawa.",
    plain_template: "Amfanin gonarka {crop} a kan hekta {ha} na iya ba da kusan tan {tons}, wanda kusan jaka {bags} ne na 50 kg. Wannan kiyasi ne don tsarawa, ba alkawari ba. Yanayi da kwari na iya canza shi.",
    size_template: "{v} {unit} kusan {ha} hekta ne don tsarin.",
    bags_template: "{kg} kg a kowace hekta kusan jaka {bags} ne na 50 kg.",
    helper_size_full: "Fili 15 kusan hekta 1 ne. Fili 6 kusan eka 1 ne. Girman fili ya bambanta da gari zuwa gari, tambayi ma'aikacin extension idan ba ka da tabbas.",

    result_title:      "Sakamakon Hasashe",
    unit_tons:         "tan an hasashen",
    income_low:        "Ƙananan Kuɗi",
    income_mid:        "Kuɗi Na Tsakiya",
    income_high:       "Babban Kuɗi",
    risk_title:        "Gargaɗin Haɗari",
    no_risk:           "Babu haɗari da aka gano — tsarin gonarka yana da kyau!",
    whatif_title:      "Idan Ka Inganta?",
    whatif_current:    "Amfanin Yanzu",
    whatif_best:       "Da Kayan Aiki Duka",
    whatif_desc:       "Ingantattun iri + ban ruwa + taki 100 kg/ha",
    advice_title:      "Shawara Ta Noma Ta Musamman Gare Ka",
    calendar_title:    "Ayyukan Wannan Watan",
    last_month:        "Watan Da Ya Wuce",
    this_month:        "Wannan Watan",
    next_month:        "Watan Mai Zuwa",
    now_badge:         "Wannan Watan",

    adv_season:        "Lokacin Shuka",
    adv_spacing:       "Nisan Tsakanin",
    adv_harvest:       "Girbi",
    adv_fertilizer:    "Taki",
    adv_water:         "Ruwa",
    adv_soil:          "Ƙasa",
    adv_disease:       "Cutar Amfanin Gona",
    adv_market:        "Lokacin Sayarwa",

    err_server:        "Ana farfado da uwar garken AI. Jira daƙiƙa 30 sannan a sake gwadawa.",
    err_no_crop:       "Don Allah zaɓi nau'in amfanin gona.",
    err_no_state:      "Don Allah zaɓi jiharku.",
    err_farm_size:     "Girman gona dole ne ya zama aƙalla hekta 0.1.",
    err_rainfall:      "Ruwan sama dole ne ya zama aƙalla 300mm. Zaɓi jiha don cika.",
    err_soil_ph:       "pH na ƙasa dole ne ya kasance tsakanin 4.0 da 9.0.",
    err_fertilizer:    "Don Allah shigar da adadin taki (shigar 0 idan ba a yi amfani da shi).",

    status_connecting: "Ana haɗawa...",
    status_online:     "AI Yana Aiki",
    status_offline:    "Uwar Garke Ba Ya Aiki",
    status_waking:     "Ana farfaɗo...",

    footer_built:      "An gina ta",
    footer_mission:    "Ƙarfafa manoman Najeriya da AI",
    uplift_text:       "karuwar da za a iya samu da ingantattun kayan aiki",
  },

  /* ── Igbo (south-east Nigeria) ──────────────────────── */
  ig: {
    app_name:          "AgriTech AI",
    app_sub:           "Ikpo Ọkọ Ndụmọdụ Maka Ndị Ọrụ Ugbo",

    hero_title:        "Nhọpụta Ihe Ọ Na-Aghọta Ugbo Site na AI",
    hero_sub:          "Họrọ steeti gị na ihe ị na-akọ. AI anyị ga-nyochaa ọnọdụ gị iji kwuo ihe ọ ga-aghọta, ego ị ga-enweta, na ihe ize ndụ.",
    stat_crops:        "Ihe A Na-Akọ",
    stat_states:       "Steeti Naịjịrịa",
    stat_ai:           "AI Na-Achọpụta Ihe Ize Ndụ",

    form_title:        "Tinye Nkọwa Ugbo Gị",
    label_crop:        "Ụdị Ihe Ọ Na-Akọ",
    label_state:       "Steeti Naịjịrịa",
    label_farm_size:   "Ogo Ugbo (hekta)",
    label_rainfall:    "Mmiri Ozuzo Nke Afọ (mm)",
    label_soil_ph:     "pH Ala",
    label_fertilizer:  "Nri Ala (kg/ha)",
    label_seeds:       "Mkpụrụ Dị Mma?",
    label_irrigation:  "Mmiri Ugbo Dị?",
    seeds_yes:         "Ee",
    seeds_no:          "Mba",
    irrigation_yes:    "Ee",
    irrigation_no:     "Mba (ozuzo naanị)",
    btn_predict:       "🤖 Nweta Nhọpụta AI",

    ph_crop:           "-- Họrọ ihe ị na-akọ --",
    ph_state:          "-- Họrọ steeti gị --",
    ph_farm_size:      "dịka 2.5",
    ph_rainfall:       "Họrọ steeti ka e wee kwuo ya",
    ph_soil_ph:        "dịka 6.2",
    ph_fertilizer:     "dịka 100",

    hint_soil_ph:      "Kacha mma: 5.5 – 6.5 maka ihe a na-akọ ọtụtụ",
    hint_rainfall:     "A ga-akwụso ya ozigbo mgbe ị họọrọ steeti gị",
    hint_seeds:        "Ụdị ọhụrụ si IITA / NASC",
    autofill_badge:    "Akwụsọla",
    action_title: "Ọrụ ị ga-eji taa",
    action_now: "Ya mere",
    action_plan: "Kwadebe",
    action_month_task: "Ọrụ gị maka {crop} na {month}",
    action_next_task: "Ọnwa na-abịa: {task}",
    action_sell: "Oge kachịrị ire",
    urg_now: "Ya mere",
    urg_plant: "Oge planting",
    urg_harvest: "Oge harvesting",
    urg_spray: "Oge spraying",
    urg_weed: "Oge ikpeazụ",
    urg_fert: "Obe fertilizer",
    market_title: "Ozi ahụ ọrụ na ego",
    market_best: "Ọnwa kachịrị ihe niile",
    market_bag_price: "Ọnọda obi 50 kg",
    market_your_bags: "Akwụụ obi ị ga-atụta",
    market_money: "Ego ị ga-ahụ maka ị rere",
    market_note: "Ọnọdụ ego a dị n'akụkụ mere. Lelee ọka ahụ tupu ị rere.",
    market_offline: "Ọnọdụ ego ahụ chọrọ internet. Jiri ikpeazụka ka ị hụ ya.",
    unit_hectare: "Hekta",
    unit_acre: "Eka",
    unit_plot: "Plot (648 sqm, okoloto Lagos)",
    soil_prompt: "Ala gi di ka gini? Horo otu",
    soil_sandy: "Aja, mmiri na-agbapu ngwa ngwa, ocha",
    soil_loamy: "Udavuu, di nro ma gbaa ochichiri, na-ejide mmiri nke oma",
    soil_clay: "Uro, na-arapara mgbe mmiri di, na-esi ike mgbe o kporo nku",
    soil_unknown: "Amaghi m",
    confirm_check: "Biko lelee anya tupu anyi ebuo amuma:",
    confirm_ask: "Nke a o ziri ezi? Pia OK iji buo amuma, Cancel iji mezie.",
    plain_template: "Ihe ubi {crop} gi na hekta {ha} nwere ike inye ihe di ka tan {tons}, nke di ka akpa {bags} nke 50 kg. Nke a bu atumatu maka nhazi, obughi nkwa. Ihu igwe na pests nwere ike igbanwe ya.",
    size_template: "{v} {unit} di ka {ha} hekta maka model.",
    bags_template: "{kg} kg kwa hekta di ka akpa {bags} nke 50 kg.",
    helper_size_full: "Plot 15 di ka hekta 1. Plot 6 di ka eka 1. Ogo plot di iche site n'obodo ruo n'obodo, juo onye oru extension ma oburu na imaghi.",

    result_title:      "Nsonaazụ Nhọpụta",
    unit_tons:         "tọn e kwupụtara",
    income_low:        "Ego Dị Ala",
    income_mid:        "Ego Etiti",
    income_high:       "Ego Dị Elu",
    risk_title:        "Ihe Ize Ndụ",
    no_risk:           "Achọpụtabeghị ihe ize ndụ — nhazi ugbo gị dị mma!",
    whatif_title:      "Ọ Bụrụ Na Ị Melite?",
    whatif_current:    "Ihe Ọ Na-Aghọta Ugbu a",
    whatif_best:       "Na Ngwaọrụ Niile",
    whatif_desc:       "Mkpụrụ dị mma + mmiri ugbo + nri ala 100 kg/ha",
    advice_title:      "Ndụmọdụ Ọrụ Ugbo Maka Gị",
    calendar_title:    "Ihe Ị Ga-Eme Ọnwa a",
    last_month:        "Ọnwa Gara Aga",
    this_month:        "Ọnwa a",
    next_month:        "Ọnwa Na-abịa",
    now_badge:         "Ọnwa a",

    adv_season:        "Oge Ịkọ",
    adv_spacing:       "Oge Nkezi",
    adv_harvest:       "Ịhịa",
    adv_fertilizer:    "Nri Ala",
    adv_water:         "Mmiri",
    adv_soil:          "Ala",
    adv_disease:       "Ọrịa Ihe A Na-Akọ",
    adv_market:        "Oge Ire Ahịa",

    err_server:        "Sava AI na-amalite. Biko chere sekọnd 30 wee nwaa ọzọ.",
    err_no_crop:       "Biko họrọ ụdị ihe ị na-akọ.",
    err_no_state:      "Biko họrọ steeti gị.",
    err_farm_size:     "Ogo ugbo ga-abụrịrị ọ dịkarịa ala hekta 0.1.",
    err_rainfall:      "Mmiri ozuzo ga-abụrịrị ọ dịkarịa ala 300mm. Họrọ steeti iji kwuo ya.",
    err_soil_ph:       "pH ala ga-abụrịrị n'etiti 4.0 na 9.0.",
    err_fertilizer:    "Biko tinye oke nri ala (tinye 0 ọ bụrụ na ị jughị).",

    status_connecting: "Na-ejikọ...",
    status_online:     "AI Dị Online",
    status_offline:    "Sava Adịghị Arụ Ọrụ",
    status_waking:     "Na-amalite...",

    footer_built:      "Wuru site na",
    footer_mission:    "Na-enyere ndị ọrụ ugbo Naịjịrịa ike site na AI",
    uplift_text:       "ọlụlụ nwere ike nweta na ngwaọrụ dị mma",
  },
};

/* ── Language manager ───────────────────────────────────── */
const LANG = {
  current: 'en',

  setLanguage(code) {
    if (!TRANSLATIONS[code]) return;
    this.current = code;
    // Persist choice in localStorage so it survives refresh
    try { localStorage.setItem('agritech_lang', code); } catch {}
    this.applyAll();
  },

  t(key) {
    return TRANSLATIONS[this.current][key]
        || TRANSLATIONS['en'][key]
        || key;
  },

  /* Update every element with data-i18n attribute */
  applyAll() {
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      const val = this.t(key);
      if (el.tagName === 'INPUT' && el.placeholder !== undefined) {
        // For inputs, only update placeholder
        el.placeholder = val;
      } else if (el.tagName === 'OPTION') {
        el.textContent = val;
      } else {
        el.textContent = val;
      }
    });

    /* Update active language button */
    document.querySelectorAll('.lang-btn').forEach(btn => {
      btn.classList.toggle('lang-active',
        btn.getAttribute('data-lang') === this.current);
    });
  },

  /* Load saved preference on startup */
  init() {
    try {
      const saved = localStorage.getItem('agritech_lang');
      if (saved && TRANSLATIONS[saved]) this.current = saved;
    } catch {}
    this.applyAll();
  }
};