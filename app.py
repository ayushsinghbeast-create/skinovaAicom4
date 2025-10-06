import streamlit as st
import pandas as pd
from PIL import Image
from io import StringIO, BytesIO
import random
from datetime import datetime, date, timedelta
import matplotlib.pyplot as plt
import numpy as np
import json
import time # For simulating API calls/loading

# --- 1. GLOBAL CONFIGURATION & HYPER-POLISHED UI SETUP ---

# Custom Colors & Theme Variables (Expanded Pallette)
SOFT_BLUE = "#6EC1E4"
DARK_ACCENT = "#3C8CB0"
LIGHT_BG = "#F9FCFF"
TEXT_COLOR = "#333333"
WHITE = "#FFFFFF"
ERROR_RED = "#E53935"
SUCCESS_GREEN = "#66BB6A"
WARNING_YELLOW = "#FFD54F"
NEUTRAL_GREY = "#90A4AE"
SKIN_TONE_WARM = "#FFDAB9"
SKIN_TONE_COOL = "#C0E0F0"
HEADER_COLOR = "#2A6D88"

# Page Configuration
st.set_page_config(
    page_title="SkinovaAI: 
    ,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Extensive Custom CSS for Theme, Fonts, and Hyper-Polish (Now significantly expanded CSS)
st.markdown(f"""
    <style>
    /* Global App Styling */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap');
    .stApp {{
        background-color: {LIGHT_BG};
        color: {TEXT_COLOR};
        font-family: 'Inter', sans-serif;
    }}
    
    /* Sidebar Styling */
    .css-1d391kg, .css-1lcbmhc {{ 
        background-color: {SOFT_BLUE};
        color: {LIGHT_BG};
        box-shadow: 2px 0 20px rgba(0, 0, 0, 0.3);
    }}
    .css-1oe2kgi a, .css-1oe2kgi div {{ /* Sidebar Links/Text */
        color: {HEADER_COLOR} !important;
        font-weight: 600;
        transition: all 0.2s;
        padding: 10px 15px;
        margin-bottom: 5px;
        border-radius: 8px;
    }}
    .css-1oe2kgi a:hover, .css-1oe2kgi div:hover {{
        color: {WHITE} !important;
        background-color: {DARK_ACCENT}; 
        transform: translateX(5px);
    }}
    .st-emotion-cache-1ft07x6.e1vs05j70 a[data-testid="stSidebarNavItemLink"] {{
        color: {WHITE} !important;
    }}
    .st-emotion-cache-1ft07x6.e1vs05j70 a[data-testid="stSidebarNavStartHome"] {{
        color: {WHITE} !important;
    }}
    
    /* Main Content Area Styling */
    .main .block-container {{
        padding-top: 2.5rem;
        padding-right: 4rem;
        padding-left: 4rem;
        padding-bottom: 3rem;
    }}
    
    /* Custom Card Styling (Hyper-Polished Look) */
    .skinova-card {{
        background-color: {WHITE};
        border-radius: 16px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
        padding: 25px;
        margin-bottom: 20px;
        border: 1px solid #E0E0E0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }}
    .skinova-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.15);
    }}
    .skinova-card-accent {{
        border-left: 5px solid {DARK_ACCENT};
        padding-left: 20px;
    }}

    /* KPI/Score Display Styling */
    .score-display {{
        text-align: center;
        padding: 20px;
        border-radius: 12px;
        font-weight: 700;
        color: {WHITE};
        margin-top: 10px;
        box-shadow: inset 0 0 15px rgba(0, 0, 0, 0.15);
        background: linear-gradient(135deg, {DARK_ACCENT}, {SOFT_BLUE});
    }}
    .score-value {{
        font-size: 4em;
        line-height: 1;
        margin-bottom: 5px;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
    }}

    /* Custom Button Styling */
    .stButton>button {{
        background-color: {DARK_ACCENT};
        color: {WHITE};
        border: none;
        border-radius: 10px;
        padding: 12px 25px;
        font-weight: 700;
        font-size: 1.1em;
        letter-spacing: 0.5px;
        transition: background-color 0.3s, transform 0.1s, box-shadow 0.3s;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    }}
    .stButton>button:hover {{
        background-color: {HEADER_COLOR}; 
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
    }}

    /* Header Styling */
    h1 {{
        color: {DARK_ACCENT};
        border-bottom: 4px solid {SOFT_BLUE};
        padding-bottom: 15px;
        font-weight: 900;
        letter-spacing: 1px;
    }}
    h2 {{
        color: {TEXT_COLOR};
        font-weight: 800;
        margin-top: 2rem;
        border-left: 5px solid {SOFT_BLUE};
        padding-left: 10px;
    }}
    h3 {{
        color: {DARK_ACCENT};
        font-weight: 700;
        margin-top: 1.5rem;
    }}
    
    /* Streamlit Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 30px;
    }}

    .stTabs [data-baseweb="tab"] {{
        height: 60px;
        white-space: nowrap;
        border-radius: 10px 10px 0 0;
        padding: 15px 20px;
        background-color: #EFEFEF;
        font-weight: 700;
        font-size: 1.1em;
    }}
    
    .stTabs [aria-selected="true"] {{
        background-color: {SOFT_BLUE};
        color: {WHITE};
        border-bottom: 5px solid {DARK_ACCENT};
    }}
    
    /* Routine Step Styling */
    .routine-step {{
        border: 2px solid {SOFT_BLUE};
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        background-color: {WHITE};
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }}
    .routine-step-title {{
        font-weight: 800;
        color: {DARK_ACCENT};
        font-size: 1.2em;
        margin-bottom: 5px;
    }}
    .routine-step-notes {{
        font-size: 0.9em;
        color: {NEUTRAL_GREY};
        margin-top: 10px;
        border-top: 1px dashed #DDD;
        padding-top: 5px;
    }}

    </style>
""", unsafe_allow_html=True)


# --- 2. GLOBAL STATE MANAGEMENT & HYPER-DATA MODELS (Massive Expansion) ---

# Global Application State Initialization
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'Login/Signup'
if 'onboarding_complete' not in st.session_state:
    st.session_state['onboarding_complete'] = False
if 'user_db' not in st.session_state:
    # Hyper-Database Structure (Expanded to hold complex user history and consultation data)
    st.session_state['user_db'] = {
        'guest_user': {
            'username': 'guest_user',
            'password': 'guest',
            'profile': {},
            'onboarding_complete': False,
            'history': {
                'score_log': [{'date': (date.today() - timedelta(days=30)).isoformat(), 'score': 70, 'delta': '+0'}], 
                'compliance_log': [], 
                'analytics_reports': [], 
                'routine_history': []
            },
            'current_routine': [],
            'skin_score': 70,
            'routine_streak': 0,
            'last_checkin_date': None,
            'consultation_history': [] # For Consult an Expert feature
        }
    }
if 'current_user' not in st.session_state:
    st.session_state['current_user'] = 'guest_user'
if 'current_routine_completed' not in st.session_state:
    st.session_state['current_routine_completed'] = False 

# --- HYPER-DETAILED MOCK DATA MODELS ---

# 2.1. Active Ingredient Profile Matrix (Expanded Conflicts and Delivery Systems)
ACTIVE_INGREDIENT_PROFILES = {
    "Hyaluronic Acid (HA)": {"function": "Hydration", "concerns": ["Dryness"], "conflict": [], "system": "Vehicle-Aqueous", "notes": "Multi-molecular weights used for deeper penetration."},
    "Niacinamide (Vitamin B3)": {"function": "Barrier, Oil Control", "concerns": ["Acne", "Redness"], "conflict": ["High concentration Vitamin C (use 30 min apart)"], "system": "Vehicle-Emulsion", "notes": "Minimizes pores and reduces inflammation."},
    "L-Ascorbic Acid (Vitamin C)": {"function": "Antioxidant, Brightening", "concerns": ["Pigmentation", "Aging"], "conflict": ["AHA/BHA (alternate), Benzoyl Peroxide (NEVER)"], "system": "Vehicle-LowPHSerum", "notes": "Crucial for morning routine. Highly unstable."},
    "Retinol (0.5% Encapsulated)": {"function": "Cell Turnover, Anti-Aging", "concerns": ["Aging", "Acne"], "conflict": ["AHA/BHA (Skin Cycling ONLY)", "Benzoyl Peroxide (NEVER)"], "system": "Vehicle-Oil", "notes": "Night use only. Encapsulation reduces irritation."},
    "Salicylic Acid (BHA 2%)": {"function": "Exfoliation (Oil-soluble)", "concerns": ["Acne", "Blackheads"], "conflict": ["Retinoids (alternate nights)"], "system": "Vehicle-Toner", "notes": "Deeply cleanses pores. Targets oil/clogged pores."},
    "Glycolic Acid (AHA 10%)": {"function": "Exfoliation (Water-soluble)", "concerns": ["Dullness", "Texture"], "conflict": ["Retinoids (alternate nights)"], "system": "Vehicle-Gel", "notes": "Increases sun sensitivity. Night use only."},
    "Benzoyl Peroxide (BP 5%)": {"function": "Acne Treatment", "concerns": ["Acne (Inflammatory)"], "conflict": ["Retinoids", "Vitamin C"], "system": "Vehicle-SpotTreatment", "notes": "Spot treatment. Mandatory patch test."},
    "Azelaic Acid (10%)": {"function": "Redness, Acne, Pigmentation", "concerns": ["Rosacea", "PIH"], "conflict": [], "system": "Vehicle-Cream", "notes": "Gentle, multi-tasking active. Can be used with Retinoids (if tolerant)."},
    "Ceramides (NP, AP, EOP)": {"function": "Barrier Repair", "concerns": ["Dryness", "Sensitive"], "conflict": [], "system": "Vehicle-Moisturizer", "notes": "Mimics skin's natural lipids for deep repair."}
}

# 2.2. Hyper-Product Catalog (Massively Expanded and Detailed for Marketplace)
MOCK_PRODUCTS = [
    {"id": 1001, "name": "Ceramide-Rich Hydrating Cleanser", "category": "Cleanser", "active_ing": ["Ceramides", "Glycerin"], "concern_match": ["Dryness", "Sensitive"], "budget": "Mid", "price": 1400, "rating": 4.8, "volume": "250ml", "type": "Cream"},
    {"id": 1002, "name": "5% L-Ascorbic Acid Day Serum", "category": "Active Serum", "active_ing": ["L-Ascorbic Acid", "Ferulic Acid"], "concern_match": ["Dullness", "Aging"], "budget": "High", "price": 4800, "rating": 4.9, "volume": "30ml", "type": "Oil-Free"},
    {"id": 1003, "name": "Advanced Barrier Repair Cream", "category": "Moisturizer", "active_ing": ["Ceramides", "Cholesterol", "Peptides"], "concern_match": ["All"], "budget": "High", "price": 3200, "rating": 4.7, "volume": "50g", "type": "Rich Balm"},
    {"id": 1004, "name": "0.3% Micro-Encapsulated Retinol", "category": "Active Night", "active_ing": ["Retinol"], "concern_match": ["Aging", "Acne"], "budget": "Mid", "price": 2800, "rating": 4.6, "volume": "30ml", "type": "Suspension"},
    {"id": 1005, "name": "Mineral Zinc Oxide SPF 50+", "category": "Sunscreen", "active_ing": ["Zinc Oxide"], "concern_match": ["Sensitive", "Pigmentation"], "budget": "Mid", "price": 1950, "rating": 4.9, "volume": "60ml", "type": "Tinted"},
    {"id": 1006, "name": "2% Salicylic Acid Acne Toner", "category": "Exfoliant", "active_ing": ["Salicylic Acid"], "concern_match": ["Acne", "Oiliness"], "budget": "Low", "price": 1100, "rating": 4.5, "volume": "150ml", "type": "Liquid"},
    {"id": 1007, "name": "10% Azelaic Acid Suspension", "category": "Active Serum", "active_ing": ["Azelaic Acid"], "concern_match": ["Rosacea", "Redness", "PIH"], "budget": "Low", "price": 950, "rating": 4.4, "volume": "30ml", "type": "Cream"},
    {"id": 1008, "name": "Squalane Oil Cleanser", "category": "Oil Cleanser", "active_ing": ["Squalane", "Polyglyceryl Oleate"], "concern_match": ["All"], "budget": "Mid", "price": 1600, "rating": 4.7, "volume": "100ml", "type": "Oil"},
    {"id": 1009, "name": "10% Glycolic Acid Overnight Gel", "category": "Exfoliant", "active_ing": ["Glycolic Acid"], "concern_match": ["Texture", "Dullness", "Aging"], "budget": "High", "price": 2500, "rating": 4.3, "volume": "50ml", "type": "Gel"},
    {"id": 1010, "name": "Hyaluronic Acid Layering Mist", "category": "Hydration", "active_ing": ["HA", "Niacinamide"], "concern_match": ["Dryness", "Barrier"], "budget": "Low", "price": 800, "rating": 4.6, "volume": "100ml", "type": "Mist"},
    # Adding 40 more detailed mock products (placeholder content for 5000 lines)
    *[
        {"id": 1011 + i, "name": f"Product Alpha {i}", "category": random.choice(["Cleanser", "Moisturizer", "Serum", "Sunscreen", "Exfoliant"]),
         "active_ing": [random.choice(list(ACTIVE_INGREDIENT_PROFILES.keys()))],
         "concern_match": [random.choice(["Acne", "Aging", "Dryness", "Sensitive", "Pigmentation"])],
         "budget": random.choice(["Low", "Mid", "High"]),
         "price": random.randint(500, 6000),
         "rating": round(random.uniform(4.0, 5.0), 1),
         "volume": f"{random.randint(30, 200)}ml", "type": random.choice(["Gel", "Cream", "Oil", "Serum"])
        } for i in range(40)
    ]
]
# Create DataFrame for easy querying in Marketplace
PRODUCT_DF = pd.DataFrame(MOCK_PRODUCTS)

# 2.3. Academy Content (Expanded Modules)
ACADEMY_CURRICULUM = {
    "Module 1: Foundation (The Skin Barrier)": [
        {"title": "Lesson 1.1: Anatomy of the Stratum Corneum (101)", "duration": "10 min", "status": "Completed", "type": "Video"},
        {"title": "Lesson 1.2: Essential Lipids: The Ceramide Story", "duration": "15 min", "status": "In Progress", "type": "Reading"},
        {"title": "Quiz 1: Barrier Basics", "duration": "5 min", "status": "Not Started", "type": "Quiz"}
    ],
    "Module 2: The Active Ingredient Deep Dive": [
        {"title": "Lesson 2.1: Retinoids: From Retinyl Palmitate to Tretinoin", "duration": "25 min", "status": "Not Started", "type": "Video"},
        {"title": "Lesson 2.2: The Acid Wars: AHA, BHA, and PHA (Uses & Misuses)", "duration": "20 min", "status": "Not Started", "type": "Reading"},
        {"title": "Lesson 2.3: Peptides and Growth Factors (Advanced Anti-Aging)", "duration": "18 min", "status": "Not Started", "type": "Reading"}
    ],
    "Module 3: Advanced Skincare Protocols": [
        {"title": "Lesson 3.1: Skin Cycling: The Expert Schedule", "duration": "15 min", "status": "Not Started", "type": "Video"},
        {"title": "Lesson 3.2: Managing Melasma & Post-Inflammatory Hyperpigmentation (PIH)", "duration": "30 min", "status": "Not Started", "type": "Video"},
        {"title": "Lesson 3.3: In-Office Treatments Integration (Lasers, Peels)", "duration": "20 min", "status": "Not Started", "type": "Reading"}
    ],
    "Module 4: Lifestyle and Internal Health": [
        {"title": "Lesson 4.1: The Gut-Skin Axis", "duration": "15 min", "status": "Not Started", "type": "Reading"},
        {"title": "Lesson 4.2: Stress and Cortisol's Impact on Acne", "duration": "12 min", "status": "Not Started", "type": "Reading"}
    ]
}

# 2.4. Community Forum Mock Data (Expanded Threads)
FORUM_THREADS = [
    {"id": 1, "title": "Retinol Purge: Normal or Too Strong? (0.3% Encapsulated)", "user": "AcneFighter23", "date": "2025-10-01", "replies": 15, "tags": ["Retinoids", "Acne"], "views": 350},
    {"id": 2, "title": "Best Tinted Mineral SPF for Fitzpatrick Type IV (Melanin-Rich)", "user": "SkintoneMatch", "date": "2025-09-28", "replies": 8, "tags": ["Sunscreen", "Pigmentation"], "views": 820},
    {"id": 3, "title": "Is Double Cleansing Necessary in Hot/Humid Climates?", "user": "HumidHater", "date": "2025-10-05", "replies": 3, "tags": ["Cleansing", "Climate"], "views": 110},
    {"id": 4, "title": "Help! My barrier is damaged after using BP and L-AA together.", "user": "DesperateSkin", "date": "2025-10-06", "replies": 22, "tags": ["Barrier", "Conflict", "HELP"], "views": 980},
    {"id": 5, "title": "Show Off Your SkinovaAI Routine Kit!", "user": "RoutineLover", "date": "2025-10-04", "replies": 5, "tags": ["Kit", "Review"], "views": 45}
]

# 2.5. Expert Consultation Profiles (For Consult an Expert feature)
EXPERT_PROFILES = [
    {"id": 1, "name": "Dr. Kavita Sharma, MD", "specialty": "Dermatology (Acne & Pigmentation)", "rating": 4.9, "experience": "12 Years", "cost": 1500, "availability": "Mon, Wed, Fri"},
    {"id": 2, "name": "Dr. Ethan Cole, PhD", "specialty": "Cosmetic Chemistry & Ingredient Science", "rating": 4.7, "experience": "18 Years", "cost": 2500, "availability": "Tue, Thu"},
    {"id": 3, "name": "Nurse Jane Doe, RN", "specialty": "Aesthetic Injectables & Barrier Health", "rating": 4.6, "experience": "8 Years", "cost": 1000, "availability": "All Week"}
]


# --- 3. CORE HYPER-LOGIC & HELPER FUNCTIONS (The Engine) ---

def calculate_age(dob):
    """Calculates age from date of birth string."""
    try:
        birth_date = datetime.strptime(dob, "%Y-%m-%d").date()
        today = date.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    except Exception:
        return 25 # Default

def navigate_to(page_name):
    """Updates the current page in session state."""
    st.session_state.current_page = page_name

def save_user_data(username, data_type, data):
    """Saves complex user data (profile or history) into the user_db."""
    if username in st.session_state.user_db:
        if data_type == 'profile':
            st.session_state.user_db[username]['profile'].update(data)
            st.session_state.user_db[username]['onboarding_complete'] = True
            # Recalculate everything on profile update
            st.session_state.user_db[username]['current_routine'], _ = generate_hyper_routine(st.session_state.user_db[username]['profile'])
            calculate_skin_score(st.session_state.user_db[username]['profile'], st.session_state.user_db[username]['history'])
        elif data_type in st.session_state.user_db[username]['history']:
            st.session_state.user_db[username]['history'][data_type].append(data)
        elif data_type == 'current_routine':
            st.session_state.user_db[username]['current_routine'] = data
        
        st.session_state.user_db[username]['history']['compliance_log'].append({
            'date': date.today().isoformat(),
            'activity': f'Data Updated: {data_type}',
            'timestamp': datetime.now().isoformat()
        })
    else:
        st.error("Error: User not found in database.")

def check_ingredient_conflict(routine_steps):
    """
    Hyper-Logic 1.1: Checks for ingredient conflicts within the current routine.
    More complex rules based on the ACTIVE_INGREDIENT_PROFILES matrix.
    """
    active_ingredients = [step['ingredient_key'] for step in routine_steps if 'ingredient_key' in step and 'Active' in step['type']]
    conflicts = []
    
    # Check for direct conflict pairs
    if "Retinol (0.5% Encapsulated)" in active_ingredients and "L-Ascorbic Acid (Vitamin C)" in active_ingredients:
        conflicts.append("⚠️ Retinol and L-AA should NEVER be used in the same routine (different pH, high irritation risk). Separate to Night (Retinol) and Morning (L-AA).")
    
    if "Benzoyl Peroxide (BP 5%)" in active_ingredients and ("Retinol (0.5% Encapsulated)" in active_ingredients or "L-Ascorbic Acid (Vitamin C)" in active_ingredients):
        conflicts.append("🚨 Severe Conflict: BP inactivates Retinol/L-AA and causes excessive irritation. AVOID using BP in the routine unless specifically targeted and separated.")

    # Check for over-exfoliation risk (AHA + BHA + Retinoid is the highest risk)
    exfoliators = [ing for ing in active_ingredients if ing in ["Retinol (0.5% Encapsulated)", "Glycolic Acid (AHA 10%)", "Salicylic Acid (BHA 2%)"]]
    if len(exfoliators) > 2:
        conflicts.append("🔥 Hyper-Warning: High risk of over-exfoliation. Ensure these are used on ALTERNATE nights (Skin Cycling protocol is mandatory).")
    
    # Check for multiple products with same key ingredient from different categories
    niacinamide_count = sum(1 for step in routine_steps if "Niacinamide" in step.get('ingredient_key', ''))
    if niacinamide_count > 1:
        conflicts.append("📌 Optimization: You have multiple Niacinamide products. Consider using only one high-concentration serum to save budget and avoid redundancy.")

    return conflicts

def get_product_for_routine_step(concern, active_ing, budget, type_filter, current_routine_product_ids):
    """
    Hyper-Logic 1.2: Finds the best product match based on multiple criteria.
    Prioritizes products the user hasn't used yet to expand options.
    """
    # 1. Base Filter by Category and Ingredient
    filtered_df = PRODUCT_DF[
        (PRODUCT_DF['category'].str.contains(type_filter.split(' ')[0], case=False, na=False)) |
        (PRODUCT_DF['active_ing'].apply(lambda x: active_ing in x))
    ].copy()
    
    if filtered_df.empty:
        return {"name": f"Recommended Product (AI: {active_ing} {type_filter})", "id": 0, "price": 0, "rating": 5.0}

    # 2. Budget Scoring
    budget_map = {'Low': 1, 'Mid': 2, 'High': 3}
    user_budget_score = budget_map.get(budget, 2)
    
    def score_product(row):
        score = row['rating'] * 10 
        
        # Budget Match Score (Closer to user's budget preference is better)
        prod_budget_score = budget_map.get(row['budget'], 2)
        score -= abs(prod_budget_score - user_budget_score) * 5 # Penalty for mismatch
        
        # Concern Match Bonus
        if any(c in row['concern_match'] for c in concern):
            score += 10
            
        # Preference to New Products (Avoid recommending existing kit products)
        if row['id'] in current_routine_product_ids:
            score -= 20
            
        return score

    filtered_df['score'] = filtered_df.apply(score_product, axis=1)
    
    # 3. Select the highest scoring product
    best_match = filtered_df.sort_values(by='score', ascending=False).iloc[0]
    
    return best_match.to_dict()


def generate_hyper_routine(profile):
    """
    Hyper-Logic 2: Generates a highly customized routine based on 10+ profile parameters.
    Implements Skin Cycling, Climate Adjustment, and Budget Optimization.
    """
    # 1. Extract Profile Data
    skin_type = profile.get('skin_type', 'Normal')
    concerns = profile.get('primary_concerns', [])
    climate = profile.get('climate', 'Temperate')
    budget = profile.get('budget', 'Mid')
    sensitivity = profile.get('skin_sensitivity', 'Low')
    
    current_routine_product_ids = [p['product_id'] for p in st.session_state.user_db.get(st.session_state.current_user, {}).get('current_routine', []) if p.get('product_id')]
    
    # 2. Routine Initialization
    morning_routine = []
    evening_routine = []
    
    # 3. Logic for Cleansing (MANDATORY STEPS)
    cleanser_active = "Ceramides"
    cleanser_type = "Creamy Cleanser" if skin_type in ['Dry', 'Sensitive'] else "Gel Cleanser"
    
    # Morning Cleanser (Adjusted for climate)
    if climate in ['Cold/Dry', 'Temperate']:
        morning_routine.append({"step": 1, "time": "Morning", "type": cleanser_type, "ingredient_key": cleanser_active, 
                                "product": get_product_for_routine_step(concerns, cleanser_active, budget, "Cleanser", current_routine_product_ids), 
                                "notes": "Gentle rinse with water or use a light cleanser."})
    else: # Hot/Humid
        morning_routine.append({"step": 1, "time": "Morning", "type": "Foaming Cleanser", "ingredient_key": "Salicylic Acid (BHA 2%)" if 'Oiliness' in skin_type else "Glycerin", 
                                "product": get_product_for_routine_step(concerns, "Cleanser", budget, "Cleanser", current_routine_product_ids),
                                "notes": "Use a deep, but non-stripping cleanse to manage morning oil."})
    
    # Evening Double Cleansing
    evening_routine.append({"step": 1, "time": "Evening", "type": "Oil Cleanser", "ingredient_key": "Squalane", 
                            "product": get_product_for_routine_step(concerns, "Oil Cleanser", budget, "Oil Cleanser", current_routine_product_ids), 
                            "notes": "MANDATORY first step to remove SPF/Makeup/Pollution."})
    evening_routine.append({"step": 2, "time": "Evening", "type": cleanser_type, "ingredient_key": cleanser_active, 
                            "product": get_product_for_routine_step(concerns, "Ceramides", budget, "Cleanser", current_routine_product_ids), 
                            "notes": "Second cleanse for skin purification."})

    # 4. Active Treatment (The Skin Cycling Protocol - Night Steps are 3-6)
    
    # Day Active (Morning - Antioxidant/Brightening)
    if 'Pigmentation' in concerns or 'Aging' in concerns:
        active_ing = "L-Ascorbic Acid (Vitamin C)"
    elif 'Redness' in concerns or 'Barrier' in concerns:
        active_ing = "Niacinamide (Vitamin B3)"
    else:
        active_ing = "Hyaluronic Acid (HA)"

    morning_routine.append({"step": 2, "time": "Morning", "type": "Antioxidant/Treatment Serum", "ingredient_key": active_ing, 
                            "product": get_product_for_routine_step(concerns, active_ing, budget, "Serum", current_routine_product_ids), 
                            "notes": "Shield against environmental damage. Apply to dry skin."})
    
    # Night Actives (Skin Cycling Logic)
    
    # NIGHT 1: Exfoliation (BHA/AHA)
    exfoliant_ing = "Salicylic Acid (BHA 2%)" if 'Acne' in concerns else "Glycolic Acid (AHA 10%)"
    if sensitivity == 'High': exfoliant_ing = "Azelaic Acid (10%)" # Gentle substitute

    evening_routine.append({"step": 3, "time": "Evening (NIGHT 1 - Exfoliation)", "type": "Exfoliant", "ingredient_key": exfoliant_ing, 
                            "product": get_product_for_routine_step(concerns, exfoliant_ing, budget, "Exfoliant", current_routine_product_ids), 
                            "notes": f"**Use only once every 4 nights.** Removes dead skin. Follow with a calming moisturizer."})

    # NIGHT 2: Retinoid
    retinoid_ing = "Retinol (0.5% Encapsulated)"
    if 'Acne' in concerns and sensitivity == 'Low': retinoid_ing = "Retinol (0.5% Encapsulated)"
    elif 'Aging' in concerns and sensitivity == 'High': retinoid_ing = "Azelaic Acid (10%)" # Gentler Retinoid Alternative

    evening_routine.append({"step": 4, "time": "Evening (NIGHT 2 - Retinoid)", "type": "Regenerative Treatment", "ingredient_key": retinoid_ing, 
                            "product": get_product_for_routine_step(concerns, retinoid_ing, budget, "Active Night", current_routine_product_ids), 
                            "notes": "**Use only once every 4 nights.** Anti-aging/Acne control. Apply pea-sized amount to dry skin."})
    
    # NIGHTS 3 & 4: Recovery/Hydration
    evening_routine.append({"step": 5, "time": "Evening (NIGHT 3 & 4 - Recovery)", "type": "Hydration/Barrier Serum", "ingredient_key": "Ceramides (NP, AP, EOP)", 
                            "product": get_product_for_routine_step(concerns, "Ceramides", budget, "Serum", current_routine_product_ids), 
                            "notes": "**Use on the 2 nights following Retinoid.** Focus on repairing the skin barrier after actives."})

    # 5. Moisturizer & Sunscreen (MANDATORY STEPS)
    moisturizer_ing = "Ceramides (NP, AP, EOP)"
    if skin_type in ['Dry', 'Sensitive']: moisturizer_type = "Barrier Repair Cream"
    else: moisturizer_type = "Lightweight Gel-Cream"

    # Morning Moisturizer
    morning_routine.append({"step": 3, "time": "Morning", "type": moisturizer_type, "ingredient_key": moisturizer_ing, 
                            "product": get_product_for_routine_step(concerns, moisturizer_ing, budget, "Moisturizer", current_routine_product_ids), 
                            "notes": "Locks in hydration. Apply before SPF."})
    
    # Evening Moisturizer (Last Step)
    evening_routine.append({"step": 6, "time": "Evening", "type": "Restorative Night Cream", "ingredient_key": "Peptides", 
                            "product": get_product_for_routine_step(concerns, "Moisturizer", budget, "Moisturizer", current_routine_product_ids), 
                            "notes": "Heavy occlusive layer to prevent trans-epidermal water loss (TEWL)."})
    
    # Sunscreen (Always last in AM)
    sunscreen_ing = "Zinc Oxide"
    if profile.get('fitzpatrick_type') in ['IV', 'V', 'VI']: sunscreen_type = "Tinted Mineral SPF 50+"
    else: sunscreen_type = "Mineral Zinc Oxide SPF 50+"
    
    morning_routine.append({"step": 4, "time": "Morning", "type": sunscreen_type, "ingredient_key": sunscreen_ing, 
                            "product": get_product_for_routine_step(concerns, sunscreen_ing, budget, "Sunscreen", current_routine_product_ids), 
                            "notes": "CRUCIAL. Apply liberally and reapply every 2 hours."})

    # 6. Final Routine Assembly and Conflict Check
    full_routine = morning_routine + evening_routine
    conflicts = check_ingredient_conflict(full_routine)
    
    return full_routine, conflicts


def calculate_skin_score(profile, history):
    """
    Hyper-Logic 3: Calculates a detailed Skin Score out of 100 based on complex factors.
    Includes compliance history, lifestyle weighting, and concern penalties.
    """
    score = 100 
    
    # 1. Base Penalties (Weighted by Severity)
    concern_penalties = {
        'Acne': 12, 'Pigmentation': 10, 'Aging': 8, 'Rosacea': 15, 'Texture': 5
    }
    for concern in profile.get('primary_concerns', []):
        score -= concern_penalties.get(concern, 0)
    
    # 2. Lifestyle Penalty/Bonus (Up to 15 points impact)
    stress_level = profile.get('lifestyle', {}).get('stress_level', 3) # 1 (Low) to 4 (High)
    sleep_quality = profile.get('lifestyle', {}).get('sleep_quality', 3) # 1 (Excellent) to 4 (Poor)
    
    score -= (stress_level - 1) * 3  # High stress -> max -9 penalty
    score -= (sleep_quality - 1) * 2 # Poor sleep -> max -6 penalty
    
    # 3. Compliance/Streak Bonus (Dynamic Impact - Up to 20 points impact)
    today = date.today()
    last_14_days_compliance = [log for log in history.get('compliance_log', []) if date.fromisoformat(log['date']) >= today - timedelta(days=14)]
    
    compliance_score = sum(1 for log in last_14_days_compliance if log.get('m_done') and log.get('e_done')) * 0.75
    score += min(15, int(compliance_score)) # Max 15 points
    
    streak = st.session_state.user_db.get(st.session_state.current_user, {}).get('routine_streak', 0)
    score += min(5, streak // 7) # Max 5 points for long streak
    
    # 4. Seasonal/Environmental Multiplier
    current_season = profile.get('climate', 'Temperate')
    if current_season in ['Hot/Humid'] and 'Oiliness' in profile.get('skin_type', 'Normal'):
        score *= 0.98 # Small penalty for climate challenge
    elif current_season in ['Cold/Dry'] and 'Dry' in profile.get('skin_type', 'Normal'):
        score *= 0.95 # Small penalty for climate challenge

    # 5. Final Clamping and Logging
    final_score = max(40, min(98, int(score))) 
    
    score_log = history.get('score_log', [])
    last_score = score_log[-1]['score'] if score_log else 75
    
    if not score_log or score_log[-1]['date'] != today.isoformat():
        score_log.append({
            'date': today.isoformat(),
            'score': final_score,
            'delta': f"{'+' if final_score >= last_score else '-'}{abs(final_score - last_score)}"
        })
    st.session_state.user_db[st.session_state.current_user]['skin_score'] = final_score
    st.session_state.user_db[st.session_state.current_user]['history']['score_log'] = score_log
    
    return final_score


def generate_mock_analysis_report(profile):
    """
    Hyper-Logic 4: Generates a highly detailed, mock Skin Analyzer report (Dermato-Pathology Simulation).
    """
    
    report_date = date.today().isoformat()
    analysis_data = {
        "report_id": f"SR-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "date": report_date,
        "assessment_summary": "Comprehensive AI assessment combining self-reported data, visual markers, and active treatment plan efficacy.",
        "metrics": {
            "hydration_level_pct": random.randint(30, 70), 
            "sebum_production_rate": random.randint(40, 90) if profile['skin_type'] == 'Oiliness' else random.randint(20, 50),
            "collagen_integrity_score_pct": random.randint(55, 85) if profile.get('age_group') == '30+' else random.randint(80, 95),
            "pigmentation_index": random.randint(10, 40) if 'Pigmentation' in profile['primary_concerns'] else random.randint(5, 15),
            "barrier_strength_index": random.randint(60, 95)
        },
        "pathology_breakdown": [],
        "environmental_impact": {
            "uv_exposure_risk": "High (Mandatory SPF use. Fitzpatrick Type V is highly susceptible to PIH).",
            "pollution_stress_index": 8.1,
            "climate_factor": f"{profile['climate']} - Requires adaptation for humidity/dryness."
        },
        "actionable_recommendations": [
            "Re-evaluate current active strength (may need to increase Retinoid concentration after 6 months).",
            "Implement **Facial Massage** daily for lymph drainage.",
            "Use only **non-comedogenic** products."
        ]
    }
    
    # Detailed Pathology Generation based on Concerns
    if 'Acne' in profile['primary_concerns']:
        analysis_data["pathology_breakdown"].append({
            "area": "Jawline & Cheeks",
            "finding": "High density of closed comedones and microcysts. Possible hormonal link (Simulated).",
            "severity": "Moderate-Severe",
            "root_cause": "Hormonal fluctuations and inflammation (elevated P. acnes)."
        })
    if 'Pigmentation' in profile['primary_concerns']:
        analysis_data["pathology_breakdown"].append({
            "area": "Forehead and Upper Lip",
            "finding": "Melasma-like patches with deep dermal component (AI Visual Assessment).",
            "severity": "High",
            "root_cause": "Historic UV damage and hormonal triggers."
        })
    if profile.get('age_group') == '30+':
        analysis_data["pathology_breakdown"].append({
            "area": "Periorbital Region",
            "finding": "Fine lines (static and dynamic) visible. Loss of elasticity.",
            "severity": "Mild-Moderate",
            "root_cause": "Natural aging and collagen degradation."
        })
    
    # Save the detailed report to history
    st.session_state.user_db[st.session_state.current_user]['history']['analytics_reports'].append(analysis_data)
    
    return analysis_data

def generate_personalized_kit(profile, routine):
    """
    Hyper-Logic 5: Generates a 6-product "Essential Kit" based on the full routine, budget, and product availability.
    """
    kit_products = []
    product_ids = [step['product']['id'] for step in routine if step['product']['id'] != 0]
    
    # Prioritized categories for the 6-product kit
    priorities = ["Cleanser", "Sunscreen", "Moisturizer", "Active Serum", "Active Night", "Exfoliant"]
    
    # Track categories already added to ensure balanced kit
    added_categories = set()
    
    for category in priorities:
        # Filter the full routine steps for this category
        candidate_steps = [step for step in routine if category in step['type']]
        
        if candidate_steps:
            # Get the recommended product ID from the routine step
            product_id = candidate_steps[0]['product']['id']
            
            # Find the full product detail from the main catalog
            product_detail = PRODUCT_DF[PRODUCT_DF['id'] == product_id].iloc[0].to_dict()
            
            if product_detail and category not in added_categories:
                kit_products.append(product_detail)
                added_categories.add(category)
                if len(kit_products) >= 6:
                    break

    # If the kit is still too small (e.g., no separate exfoliants recommended)
    while len(kit_products) < 6:
        # Fill remaining slots with the highest-rated product not yet in the kit
        unused_products = PRODUCT_DF[~PRODUCT_DF['id'].isin([p['id'] for p in kit_products])]
        
        if unused_products.empty:
            break
            
        best_filler = unused_products.sort_values(by='rating', ascending=False).iloc[0].to_dict()
        kit_products.append(best_filler)
        
    return kit_products


# --- 4. MODULAR UI RENDERING COMPONENTS ---

def render_kpi_card(title, value, unit, color_bg, icon, tooltip):
    """Renders a Key Performance Indicator (KPI) card."""
    st.markdown(f"""
        <div class="skinova-card" style="background-color: {color_bg}; color: {WHITE}; padding: 15px; text-align: center;">
            <div style="font-size: 1.2em; font-weight: 700; opacity: 0.8;">{title}</div>
            <div style="font-size: 2.5em; font-weight: 900; line-height: 1.2; margin-top: 5px;">{icon} {value} <span style="font-size: 0.5em; font-weight: 500;">{unit}</span></div>
            <p style="font-size: 0.8em; margin-top: 5px; opacity: 0.9;">{tooltip}</p>
        </div>
    """, unsafe_allow_html=True)

def render_routine_step(step_data, time_of_day, user_id):
    """Renders a single, detailed routine step with compliance checkbox."""
    step_key = f"{user_id}_{time_of_day}_{step_data['step']}_{date.today().isoformat()}"
    
    # Checkbox state management
    if step_key not in st.session_state:
        st.session_state[step_key] = False

    # Check for conflicts to display warning
    conflicts = check_ingredient_conflict(st.session_state.user_db[user_id]['current_routine'])
    is_conflict = any(step_data['ingredient_key'] in c for c in conflicts)
    
    product_info = step_data.get('product', {'name': 'N/A', 'price': 0, 'rating': 0})
    
    col1, col2 = st.columns([1, 4])
    with col1:
        st.session_state[step_key] = st.checkbox(f"**Step {step_data['step']}**", value=st.session_state[step_key], key=f"chk_{step_key}")

    with col2:
        st.markdown(f"""
            <div class="routine-step">
                <p class="routine-step-title">{step_data['type']} ({step_data['ingredient_key']})</p>
                <p style='font-size: 1em;'>
                    🛍️ **Recommended:** {product_info['name']} 
                    <span style='color: {DARK_ACCENT}; font-weight: 700;'>({product_info['rating']} ⭐)</span>
                    <span style='color: {NEUTRAL_GREY}; font-size: 0.9em;'>(₹{product_info['price']:,})</span>
                </p>
                <p class="routine-step-notes">
                    {step_data['notes']}
                    {f"<span style='color: {ERROR_RED}; font-weight: 700;'> 🚨 CONFLICT RISK! </span>" if is_conflict else ""}
                </p>
            </div>
        """, unsafe_allow_html=True)


def render_product_card(product):
    """Renders a beautiful product card for the Marketplace/Kit."""
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"""
            <div class="skinova-card skinova-card-accent" style="padding: 15px;">
                <h3 style="margin: 0; padding: 0; font-size: 1.5em; color: {DARK_ACCENT};">{product['name']}</h3>
                <p style="margin: 5px 0 10px 0; font-size: 0.9em; color: {NEUTRAL_GREY};">
                    **{product['category']}** | Active: **{', '.join(product['active_ing'])}**
                </p>
                <p style="font-size: 1.1em; font-weight: 600;">
                    Price: <span style='color: {SUCCESS_GREEN};'>₹{product['price']:,}</span> | Rating: {product['rating']} ⭐
                </p>
                <p style="font-size: 0.8em; margin-top: 10px;">
                    {product['volume']} - Type: {product['type']} - Budget: {product['budget']}
                </p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        st.button(f"Add to Cart", key=f"buy_{product['id']}", help=f"Add {product['name']} to your cart")
        st.button(f"View Details", key=f"det_{product['id']}", help=f"View ingredient list")


# --- 5. PAGE FUNCTIONS (The 8 Hyper-Features) ---

# --- LOGIN & ONBOARDING ---

def create_new_user(username, password):
    """Creates a new user session."""
    if username in st.session_state.user_db:
        return False
    
    st.session_state.user_db[username] = {
        'username': username,
        'password': password,
        'profile': {},
        'onboarding_complete': False,
        'history': {
            'score_log': [{'date': (date.today() - timedelta(days=30)).isoformat(), 'score': 75, 'delta': '+0'}],
            'compliance_log': [],
            'analytics_reports': [],
            'routine_history': []
        },
        'current_routine': [],
        'skin_score': 75,
        'routine_streak': 0,
        'last_checkin_date': None,
        'consultation_history': []
    }
    return True

def login_page():
    """Renders the Login/Signup page."""
    st.title("🧴 SkinovaAI: Your Hyper-Skincare Journey Starts Here")
    st.subheader("Login or Create an Account")
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        with st.form("login_form"):
            login_user = st.text_input("Username (e.g., guest_user)", key="login_user")
            login_pass = st.text_input("Password (e.g., guest)", type="password", key="login_pass")
            submit_login = st.form_submit_button("Login to Platform")

            if submit_login:
                if login_user in st.session_state.user_db and st.session_state.user_db[login_user]['password'] == login_pass:
                    st.session_state.logged_in = True
                    st.session_state.current_user = login_user
                    st.success(f"Welcome back, {login_user}!")
                    if st.session_state.user_db[login_user]['onboarding_complete']:
                        navigate_to('Dashboard')
                    else:
                        navigate_to('Onboarding')
                else:
                    st.error("Invalid Username or Password.")

    with tab2:
        with st.form("signup_form"):
            new_user = st.text_input("New Username", key="new_user")
            new_pass = st.text_input("New Password", type="password", key="new_pass")
            confirm_pass = st.text_input("Confirm Password", type="password", key="confirm_pass")
            submit_signup = st.form_submit_button("Create My Account")

            if submit_signup:
                if new_user in st.session_state.user_db:
                    st.error("Username already exists.")
                elif new_pass != confirm_pass:
                    st.error("Passwords do not match.")
                elif len(new_user) < 3 or len(new_pass) < 3:
                    st.error("Username and password must be at least 3 characters.")
                else:
                    if create_new_user(new_user, new_pass):
                        st.success(f"Account created for {new_user}! Please login now.")
                    else:
                        st.error("Could not create user.")


def onboarding_page():
    """Hyper-Detailed Onboarding to collect comprehensive user data."""
    st.title("🧬 SkinovaAI Hyper-Onboarding (Step 1 of 2)")
    st.markdown("### Let's create your Hyper-Personalized Skin Profile.")
    
    current_user_profile = st.session_state.user_db[st.session_state.current_user]['profile']
    
    with st.form("onboarding_form"):
        tab1, tab2, tab3 = st.tabs(["Personal Info", "Concerns & History", "Lifestyle & Goals"])

        # Tab 1: Personal Info
        with tab1:
            st.markdown("#### 👤 Basic Profile")
            col1, col2 = st.columns(2)
            with col1:
                dob = st.date_input("Date of Birth", value=date(2000, 1, 1), min_value=date(1920, 1, 1), max_value=date.today())
                skin_type = st.selectbox("Current Skin Type", ['Normal', 'Dry', 'Oily', 'Combination', 'Sensitive'])
            with col2:
                gender = st.selectbox("Gender", ['Female', 'Male', 'Other', 'Prefer Not to Say'])
                fitzpatrick_type = st.select_slider("Fitzpatrick Skin Type (Measures UV Sensitivity/Pigmentation Risk)", 
                                                    options=['I (Very Pale)', 'II (Pale)', 'III (Light Brown)', 'IV (Moderate Brown)', 'V (Dark Brown)', 'VI (Deeply Pigmented)'])

        # Tab 2: Concerns & History
        with tab2:
            st.markdown("#### 🎯 Primary Concerns & History")
            primary_concerns = st.multiselect("Primary Skin Concerns (Max 3 for best results)", 
                                               ['Acne', 'Aging/Wrinkles', 'Pigmentation (Sun Spots, PIH)', 'Melasma', 'Redness/Rosacea', 'Dryness/Eczema', 'Oiliness', 'Texture/Pores'],
                                               default=current_user_profile.get('primary_concerns', []))
            
            col3, col4 = st.columns(2)
            with col3:
                skin_sensitivity = st.select_slider("Skin Sensitivity Level", ['Low', 'Moderate', 'High'])
            with col4:
                allergies = st.text_input("Known Allergies (e.g., Fragrance, Sulfates)", value=current_user_profile.get('allergies', 'None'))
            
            st.info("💡 Fitzpatrick Type V & VI have higher risk of Post-Inflammatory Hyperpigmentation (PIH).")

        # Tab 3: Lifestyle & Goals
        with tab3:
            st.markdown("#### 🗺️ Lifestyle & Environment")
            col5, col6 = st.columns(2)
            with col5:
                climate = st.selectbox("Local Climate", ['Hot/Humid', 'Cold/Dry', 'Temperate', 'Desert'])
                stress_level = st.select_slider("Stress Level (1=Low, 4=High)", options=[1, 2, 3, 4])
            with col6:
                sleep_quality = st.select_slider("Sleep Quality (1=Excellent, 4=Poor)", options=[1, 2, 3, 4])
                water_intake = st.selectbox("Daily Water Intake", ['Low', 'Average', 'High'])
            
            st.markdown("#### 💰 Budget & Goals")
            col7, col8 = st.columns(2)
            with col7:
                budget = st.selectbox("Average Monthly Skincare Budget", ['Low (Below ₹1500)', 'Mid (₹1500 - ₹4000)', 'High (Above ₹4000)'])
            with col8:
                goal_date = st.date_input("Target Date for Major Improvement", value=date.today() + timedelta(days=90))

        submit_onboarding = st.form_submit_button("Finalize Profile & Get My Hyper-Routine")

        if submit_onboarding:
            age = calculate_age(dob.isoformat())
            profile_data = {
                'dob': dob.isoformat(),
                'age_group': '18-29' if age < 30 else ('30-49' if age < 50 else '50+'),
                'skin_type': skin_type,
                'gender': gender,
                'fitzpatrick_type': fitzpatrick_type,
                'primary_concerns': primary_concerns,
                'skin_sensitivity': skin_sensitivity,
                'allergies': allergies,
                'climate': climate,
                'budget': budget,
                'lifestyle': {'stress_level': stress_level, 'sleep_quality': sleep_quality, 'water_intake': water_intake},
                'goal_date': goal_date.isoformat()
            }
            
            with st.spinner("Analyzing 15+ variables and synthesizing routine..."):
                time.sleep(2) 
                save_user_data(st.session_state.current_user, 'profile', profile_data)
                
            st.session_state.user_db[st.session_state.current_user]['onboarding_complete'] = True
            navigate_to('Dashboard')
            st.experimental_rerun()


# --- DASHBOARD (Feature 1) ---

def dashboard_page():
    """Renders the main user dashboard with KPIs and analytics."""
    user_data = st.session_state.user_db[st.session_state.current_user]
    profile = user_data['profile']
    history = user_data['history']
    
    st.title("📊 Hyper-Dashboard: Your Skin Health Overview")
    
    st.markdown(f"## Welcome back, **{user_data['username'].capitalize()}**! Your current score is based on {profile.get('climate', 'Temperate')} climate and {len(profile.get('primary_concerns', []))} active concerns.")

    # 1. Main KPIs Section
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card("Skin Score", user_data['skin_score'], "PTS", DARK_ACCENT, "💡", "A weighted metric of skin health, compliance, and product efficacy.")
    with col2:
        streak_color = SUCCESS_GREEN if user_data['routine_streak'] >= 7 else WARNING_YELLOW
        render_kpi_card("Routine Streak", user_data['routine_streak'], "DAYS", streak_color, "🔥", "Consecutive days of checking in your AM/PM ritual.")
    with col3:
        # Calculate Compliance Rate
        total_days = 14
        compliant_days = sum(1 for log in history['compliance_log'] if date.fromisoformat(log['date']) >= date.today() - timedelta(days=total_days) and log.get('m_done') and log.get('e_done'))
        compliance_rate = round((compliant_days / total_days) * 100) if total_days > 0 else 0
        render_kpi_card("14-Day Compliance", compliance_rate, "%", SOFT_BLUE, "✅", "Percentage of days you followed your full routine.")
    with col4:
        days_to_goal = (datetime.strptime(profile.get('goal_date', date.today().isoformat()), "%Y-%m-%d").date() - date.today()).days
        goal_color = SUCCESS_GREEN if days_to_goal > 0 else NEUTRAL_GREY
        render_kpi_card("Goal Deadline", days_to_goal, "DAYS", goal_color, "📅", "Days remaining until your target skin improvement date.")
    
    st.markdown("---")
    
    # 2. Score History Chart (Hyper-Analytics)
    st.header("📈 Skin Score 30-Day Trend & Projection")
    
    df_score = pd.DataFrame(history['score_log']).tail(30)
    df_score['date'] = pd.to_datetime(df_score['date'])
    
    # Simple linear projection for 7 days
    if len(df_score) > 1:
        x = np.arange(len(df_score))
        y = df_score['score'].values
        slope, intercept = np.polyfit(x, y, 1)
        
        future_dates = [df_score['date'].iloc[-1] + timedelta(days=i) for i in range(1, 8)]
        future_x = np.arange(len(df_score), len(df_score) + 7)
        future_scores = [intercept + slope * fx for fx in future_x]
        
        df_projection = pd.DataFrame({
            'date': future_dates,
            'score': [min(98, s) for s in future_scores], # Clamp projection score
            'type': 'Projection'
        })
        df_score['type'] = 'Actual'
        df_chart = pd.concat([df_score[['date', 'score', 'type']], df_projection], ignore_index=True)
        
    else:
        df_chart = df_score.copy()
        df_chart['type'] = 'Actual'
        
    
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df_chart[df_chart['type'] == 'Actual']['date'], df_chart[df_chart['type'] == 'Actual']['score'], marker='o', linestyle='-', color=DARK_ACCENT, label='Actual Score')
    if 'Projection' in df_chart['type'].unique():
        ax.plot(df_chart[df_chart['type'] == 'Projection']['date'], df_chart[df_chart['type'] == 'Projection']['score'], linestyle='--', color=SOFT_BLUE, label='7-Day Projection')
    
    ax.set_title("Skin Score Trend", fontsize=16, color=TEXT_COLOR)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Score (PTS)", fontsize=12)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("---")
    
    # 3. Quick Tips and Next Steps
    st.header("💡 Personalized Action Plan")
    st.markdown("""
        <div class="skinova-card" style="background-color: #F0F8FF;">
        <h3 style="color: #3C8CB0; margin-top: 0;">Your Top Priority This Week:</h3>
        <ul>
            <li>**Compliance:** You missed **2** evening routines last week. Consistency is key for actives!</li>
            <li>**Active Focus:** Your Hyper-Routine includes **Skin Cycling**. Ensure you use the Retinoid and Exfoliant on separate nights to prevent barrier damage.</li>
            <li>**Re-analyze:** Run the **Hyper-Analyzer** for a simulated deep-dive report and fresh recommendations.</li>
        </ul>
        </div>
    """, unsafe_allow_html=True)

# --- MY DAILY RITUAL (Feature 2) ---

def my_routine_page():
    """Renders the user's daily ritual (AM/PM Routine) with compliance check."""
    user_data = st.session_state.user_db[st.session_state.current_user]
    
    st.title("✅ My Daily Ritual")
    st.markdown("### Your Hyper-Personalized Skincare Routine")
    st.info(f"📅 **Today's Date:** {date.today().strftime('%A, %B %d, %Y')}")

    routine = user_data['current_routine']
    if not routine:
        st.warning("Your Hyper-Routine is not yet generated. Please complete the **Onboarding** or try clicking 'Get New Routine' on the Dashboard.")
        return

    # Check for daily routine reset and update streak/score
    today = date.today().isoformat()
    if user_data['last_checkin_date'] != today:
        # Reset checkmark states for a new day
        for key in list(st.session_state.keys()):
            if key.startswith(f"{st.session_state.current_user}_Morning") or key.startswith(f"{st.session_state.current_user}_Evening"):
                del st.session_state[key]
        st.session_state.user_db[st.session_state.current_user]['last_checkin_date'] = None # Ensure it runs the check below
        st.session_state['current_routine_completed'] = False


    # Tabbed Routine Display
    tab1, tab2, tab3 = st.tabs(["🌞 Morning Ritual", "🌙 Evening Ritual", "⚠️ Routine Conflicts"])
    
    morning_routine = sorted([s for s in routine if s['time'] == 'Morning'], key=lambda x: x['step'])
    evening_routine = sorted([s for s in routine if 'Evening' in s['time']], key=lambda x: x['step'])

    with tab1:
        st.header("🌞 Morning Steps (Antioxidant & Protection)")
        for step in morning_routine:
            render_routine_step(step, "Morning", st.session_state.current_user)

    with tab2:
        st.header("🌙 Evening Steps (Double Cleanse & Regeneration)")
        st.markdown(f"""
            <div style='background-color: {SKIN_TONE_COOL}; padding: 10px; border-radius: 8px;'>
            **NIGHT CYCLING TIP:** Today is **NIGHT {((date.today() - datetime.strptime(user_data['profile'].get('dob', date.today().isoformat()), '%Y-%m-%d').date()).days % 4) + 1}** in your 4-day Skin Cycle.
            <br>Focus on the corresponding night step (Exfoliation, Retinoid, or Recovery).
            </div>
        """, unsafe_allow_html=True)
        for step in evening_routine:
            render_routine_step(step, "Evening", st.session_state.current_user)

    with tab3:
        st.header("⚠️ Ingredient Conflict and Optimization Alerts")
        conflicts = check_ingredient_conflict(routine)
        if conflicts:
            for conflict in conflicts:
                st.error(conflict)
        else:
            st.success("🎉 No major ingredient conflicts detected in your Hyper-Routine.")
            st.info("Your active ingredients are properly sequenced for maximum benefit and minimal irritation.")

    st.markdown("---")
    
    # 3. Daily Compliance Check
    st.header("✨ Daily Check-in")
    
    col_c1, col_c2 = st.columns(2)
    morning_steps_done = all(st.session_state.get(f"{st.session_state.current_user}_Morning_{step['step']}_{today}", False) for step in morning_routine)
    evening_steps_done = all(st.session_state.get(f"{st.session_state.current_user}_Evening_{step['step']}_{today}", False) for step in evening_routine)

    if col_c1.button("Check-in Morning Routine", disabled=morning_steps_done or st.session_state['current_routine_completed']):
        st.session_state['Morning_Check'] = True
        st.toast("Morning Check-in recorded!")
        
    if col_c2.button("Check-in Evening Routine", disabled=evening_steps_done or st.session_state['current_routine_completed']):
        st.session_state['Evening_Check'] = True
        st.toast("Evening Check-in recorded!")

    if morning_steps_done and evening_steps_done and not st.session_state['current_routine_completed']:
        st.balloons()
        st.success("Daily Ritual Complete! Updating Skin Score and Streak...")
        
        # Update Compliance Log and Streak
        user_data['history']['compliance_log'].append({
            'date': today,
            'activity': 'Daily Ritual Check-in',
            'm_done': True,
            'e_done': True
        })
        
        # Streak Logic
        last_checkin = datetime.strptime(user_data['last_checkin_date'], "%Y-%m-%d").date() if user_data['last_checkin_date'] else None
        
        if last_checkin is None or last_checkin == date.today() - timedelta(days=1):
            user_data['routine_streak'] += 1
            st.session_state.user_db[st.session_state.current_user]['routine_streak'] = user_data['routine_streak']
            st.toast(f"🔥 Streak increased to {user_data['routine_streak']} days!")
        elif last_checkin != date.today():
            user_data['routine_streak'] = 1 # Reset if non-consecutive
            st.session_state.user_db[st.session_state.current_user]['routine_streak'] = 1
            st.warning("Streak reset. Keep up the consistency!")
            
        st.session_state.user_db[st.session_state.current_user]['last_checkin_date'] = today
        st.session_state['current_routine_completed'] = True
        calculate_skin_score(user_data['profile'], user_data['history'])
        st.experimental_rerun()


# --- HYPER-ANALYZER (Feature 3) ---

def skin_analyzer_page():
    """Renders the Skin Analyzer for deep dermatological assessment simulation."""
    st.title("🔬 Hyper-Analyzer: Deep Dermatological Assessment (Simulated)")
    st.markdown("### Run a new analysis to get a 360° report based on your profile and compliance history.")

    if st.button("Run New Hyper-Analysis", type="primary"):
        with st.spinner("Processing over 20 internal and external factors via AI Pathology Engine..."):
            time.sleep(3)
            report = generate_mock_analysis_report(st.session_state.user_db[st.session_state.current_user]['profile'])
            st.session_state['latest_report'] = report
        st.success(f"Analysis Complete! Report ID: {report['report_id']}")

    if 'latest_report' not in st.session_state and st.session_state.user_db[st.session_state.current_user]['history']['analytics_reports']:
        st.session_state['latest_report'] = st.session_state.user_db[st.session_state.current_user]['history']['analytics_reports'][-1]
    
    if 'latest_report' in st.session_state:
        report = st.session_state['latest_report']
        st.markdown("---")
        st.header(f"Report: {report['date']} | ID: {report['report_id']}")
        
        st.subheader("Summary Assessment")
        st.info(report['assessment_summary'])
        
        # Metrics Visualizer
        st.subheader("Key Biometric Markers (AI Simulation)")
        m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)
        
        def display_metric(col, name, value, unit, color):
            with col:
                st.markdown(f"""
                    <div class="skinova-card" style="border: 2px solid {color}; text-align: center; padding: 10px;">
                        <p style="font-size: 0.8em; color: {NEUTRAL_GREY}; margin: 0;">{name}</p>
                        <p style="font-size: 1.5em; font-weight: 800; color: {color}; margin: 5px 0 0 0;">{value} {unit}</p>
                    </div>
                """, unsafe_allow_html=True)
                
        metrics = report['metrics']
        display_metric(m_col1, "Hydration Level", metrics['hydration_level_pct'], "%", SOFT_BLUE)
        display_metric(m_col2, "Sebum Rate", metrics['sebum_production_rate'], "µg/cm²", WARNING_YELLOW)
        display_metric(m_col3, "Collagen Integrity", metrics['collagen_integrity_score_pct'], "%", DARK_ACCENT)
        display_metric(m_col4, "Pigmentation Index", metrics['pigmentation_index'], "AU", ERROR_RED)
        display_metric(m_col5, "Barrier Strength", metrics['barrier_strength_index'], "%", SUCCESS_GREEN)

        
        # Detailed Pathology
        st.subheader("Dermato-Pathology Breakdown")
        for breakdown in report['pathology_breakdown']:
            st.markdown(f"""
                <div class="skinova-card" style="background-color: #FFF3F3; border: 1px solid {ERROR_RED}44;">
                    <p style="font-weight: 700; color: {ERROR_RED}; margin-bottom: 5px;">📍 {breakdown['area']} (Severity: {breakdown['severity']})</p>
                    <p style="font-size: 0.9em;">**Finding:** {breakdown['finding']}</p>
                    <p style="font-size: 0.9em;">**Root Cause:** {breakdown['root_cause']}</p>
                </div>
            """, unsafe_allow_html=True)

        # Actionable Recommendations
        st.subheader("Actionable Hyper-Recommendations")
        for rec in report['actionable_recommendations']:
            st.markdown(f"**➡️ {rec}**")

    # History
    st.markdown("---")
    st.subheader("Analysis History")
    if len(st.session_state.user_db[st.session_state.current_user]['history']['analytics_reports']) > 0:
        for i, h_report in enumerate(reversed(st.session_state.user_db[st.session_state.current_user]['history']['analytics_reports'])):
            if st.button(f"View Report from {h_report['date']}", key=f"hist_report_{i}"):
                st.session_state['latest_report'] = h_report
                st.experimental_rerun()
    else:
        st.info("No prior reports available.")


# --- PERSONALIZED KIT (Feature 4) ---

def personalized_kit_page():
    """Renders the essential 6-product kit based on routine and budget."""
    st.title("🎁 Your Personalized Hyper-Kit")
    st.markdown("### This is your essential 6-product system, optimized for efficacy, budget, and minimal conflicts.")

    user_data = st.session_state.user_db[st.session_state.current_user]
    routine = user_data['current_routine']
    
    if not routine:
        st.warning("Please complete the Onboarding and ensure your routine is generated first.")
        return

    if 'personalized_kit' not in st.session_state:
        st.session_state['personalized_kit'] = generate_personalized_kit(user_data['profile'], routine)
        
    kit = st.session_state['personalized_kit']
    total_cost = sum(p['price'] for p in kit)
    
    st.markdown(f"""
        <div class="skinova-card" style="text-align: center; background-color: {SKIN_TONE_WARM};">
            <h3 style='margin: 0; color: {DARK_ACCENT};'>Total Estimated Kit Cost: <span style='font-size: 1.5em;'>₹{total_cost:,}</span></h3>
            <p style='margin: 5px 0 0 0;'>Based on your '{user_data['profile'].get('budget', 'Mid')}' budget preference.</p>
        </div>
    """, unsafe_allow_html=True)

    st.subheader("The 6 Pillars of Your Routine")
    
    # Display the kit in two columns
    cols = st.columns(2)
    for i, product in enumerate(kit):
        with cols[i % 2]:
            render_product_card(product)
            

# --- MARKETPLACE (Feature 5) ---

def product_marketplace_page():
    """Renders a fully searchable and filterable product catalog."""
    st.title("🛍️ Product Marketplace: Shop by Science")
    st.markdown("### Browse highly-rated products vetted by SkinovaAI ingredient science.")

    # Filtering/Searching UI
    col1, col2, col3 = st.columns(3)
    search_query = col1.text_input("Search by Name or Ingredient", "")
    category_filter = col2.selectbox("Filter by Category", ['All'] + list(PRODUCT_DF['category'].unique()))
    concern_filter = col3.selectbox("Filter by Primary Concern", ['All'] + ['Acne', 'Aging', 'Dryness', 'Sensitive', 'Pigmentation'])
    
    df = PRODUCT_DF.copy()
    
    # Apply Filters
    if search_query:
        df = df[df['name'].str.contains(search_query, case=False, na=False) | 
                df['active_ing'].apply(lambda x: search_query.lower() in ' '.join(x).lower())]
    
    if category_filter != 'All':
        df = df[df['category'] == category_filter]
        
    if concern_filter != 'All':
        df = df[df['concern_match'].apply(lambda x: concern_filter in x)]

    st.subheader(f"Found {len(df)} Matching Products")

    # Sort Products
    sort_by = st.selectbox("Sort By", ['Rating (High to Low)', 'Price (Low to High)', 'Name (A-Z)'])
    if sort_by == 'Rating (High to Low)':
        df = df.sort_values(by='rating', ascending=False)
    elif sort_by == 'Price (Low to High)':
        df = df.sort_values(by='price', ascending=True)
    elif sort_by == 'Name (A-Z)':
        df = df.sort_values(by='name', ascending=True)

    # Display Results
    if df.empty:
        st.warning("No products match your current filters.")
        return

    cols = st.columns(2)
    for i, row in df.iterrows():
        with cols[i % 2]:
            render_product_card(row.to_dict())


# --- SKINCARE ACADEMY (Feature 6) ---

def skincare_academy_page():
    """Renders educational content structured into modules."""
    st.title("👩‍🎓 Skincare Academy: Become Your Own Expert")
    st.markdown("### Deep-dive into the science behind your skin and your routine.")

    for module_title, lessons in ACADEMY_CURRICULUM.items():
        st.subheader(module_title)
        st.markdown(f"""
            <div class="skinova-card" style="padding: 10px 20px;">
                <p style="font-size: 0.9em; font-style: italic; color: {NEUTRAL_GREY};">
                {len([l for l in lessons if l['status'] == 'Completed'])} of {len(lessons)} lessons completed.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Display each lesson
        for lesson in lessons:
            icon = "▶️" if lesson['type'] == 'Video' else ("📖" if lesson['type'] == 'Reading' else "📝")
            status_color = SUCCESS_GREEN if lesson['status'] == 'Completed' else (DARK_ACCENT if lesson['status'] == 'In Progress' else NEUTRAL_GREY)
            
            col1, col2, col3 = st.columns([0.5, 4, 1.5])
            with col1:
                st.markdown(f"<h1 style='font-size: 1.5em; color: {status_color};'>{icon}</h1>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"**{lesson['title']}** <br> <span style='font-size: 0.9em; color: {NEUTRAL_GREY};'>{lesson['duration']}</span>", unsafe_allow_html=True)
            with col3:
                st.button(lesson['status'], key=f"lesson_{lesson['title']}", disabled=lesson['status'] == 'Completed', help=f"Start this {lesson['type']}")

        st.markdown("---")


# --- COMMUNITY FORUM (Feature 7) ---

def community_forum_page():
    """Renders a simple community forum simulation with threads."""
    st.title("💬 Community Forum: SkinovaTalk")
    st.markdown("### Connect with other users, ask questions, and share your journey.")

    tab1, tab2 = st.tabs(["Hot Topics", "Start New Thread"])
    
    with tab1:
        st.subheader("Active Threads")
        for thread in sorted(FORUM_THREADS, key=lambda x: x['views'], reverse=True):
            st.markdown(f"""
                <div class="skinova-card" style="padding: 15px;">
                    <h3 style="margin-top: 0; color: {DARK_ACCENT}; font-size: 1.2em;">{thread['title']}</h3>
                    <p style="font-size: 0.9em; color: {NEUTRAL_GREY}; margin: 5px 0;">
                        Posted by **{thread['user']}** on {thread['date']} | 
                        Replies: **{thread['replies']}** | Views: **{thread['views']}**
                    </p>
                    <p style="font-size: 0.8em; margin: 0;">Tags: {' '.join([f'<span style="background-color: #E0F7FA; padding: 2px 5px; border-radius: 5px; color: {DARK_ACCENT};">{tag}</span>' for tag in thread['tags']])}</p>
                </div>
            """, unsafe_allow_html=True)
            
    with tab2:
        st.subheader("Create a New Discussion")
        with st.form("new_thread_form"):
            thread_title = st.text_input("Thread Title (e.g., Best serum for PIH?)")
            thread_content = st.text_area("Your Question / Content")
            thread_tags = st.multiselect("Tags (Max 3)", ["Acne", "Aging", "Retinoids", "Sunscreen", "Budget", "Conflict", "Review"])
            submit_thread = st.form_submit_button("Publish Thread")
            
            if submit_thread and thread_title and thread_content:
                new_id = len(FORUM_THREADS) + 1
                FORUM_THREADS.append({
                    "id": new_id,
                    "title": thread_title,
                    "user": st.session_state.current_user.capitalize(),
                    "date": date.today().isoformat(),
                    "replies": 0,
                    "tags": thread_tags,
                    "views": 1
                })
                st.success("Thread published successfully! Check 'Hot Topics'.")


# --- CONSULT AN EXPERT (Feature 8) ---

def consult_expert_page():
    """Renders the expert consultation booking and history page."""
    st.title("👩‍⚕️ Consult an Expert")
    st.markdown("### Book a one-on-one virtual consultation with a certified professional.")

    tab1, tab2 = st.tabs(["Book Consultation", "My History"])

    with tab1:
        st.subheader("Available Specialists")
        
        # Expert Filtering
        specialty_filter = st.selectbox("Filter by Specialty", ['All', 'Dermatology (Acne & Pigmentation)', 'Cosmetic Chemistry & Ingredient Science', 'Aesthetic Injectables & Barrier Health'])
        
        filtered_experts = EXPERT_PROFILES
        if specialty_filter != 'All':
            filtered_experts = [e for e in EXPERT_PROFILES if e['specialty'] == specialty_filter]
            
        cols = st.columns(3)
        for i, expert in enumerate(filtered_experts):
            with cols[i % 3]:
                st.markdown(f"""
                    <div class="skinova-card" style="text-align: center; background-color: {SKIN_TONE_COOL}33;">
                        <h3 style="margin-top: 0; color: {HEADER_COLOR};">{expert['name']}</h3>
                        <p style="font-weight: 700; color: {DARK_ACCENT}; margin: 5px 0;">{expert['specialty']}</p>
                        <p style="font-size: 0.9em; margin: 5px 0;">Rating: **{expert['rating']} ⭐** | Fee: **₹{expert['cost']:,}**</p>
                        <p style="font-size: 0.8em; color: {NEUTRAL_GREY};">Available: {expert['availability']}</p>
                        {st.button("Book Now", key=f"book_{expert['id']}", help="Select a time slot")}
                    </div>
                """, unsafe_allow_html=True)
                
        st.markdown("---")
        st.subheader("Virtual Booking Form (Mock)")
        expert_name = st.selectbox("Select Expert to Book", [e['name'] for e in filtered_experts])
        date_book = st.date_input("Select Date", min_value=date.today() + timedelta(days=1), max_value=date.today() + timedelta(days=30))
        time_slot = st.selectbox("Select Time Slot", ['10:00 AM', '11:00 AM', '2:00 PM', '4:00 PM', '7:00 PM'])
        
        consult_concern = st.text_area("Briefly describe your main concern for the consult.")
        
        if st.button("Confirm Booking (Simulated)", type="primary"):
            if expert_name and consult_concern:
                st.session_state.user_db[st.session_state.current_user]['consultation_history'].append({
                    "expert": expert_name,
                    "date": date_book.isoformat(),
                    "time": time_slot,
                    "concern": consult_concern,
                    "status": "Pending"
                })
                st.success(f"Consultation booked with {expert_name} on {date_book.isoformat()} at {time_slot}. Check your history.")
            else:
                st.error("Please fill in all details.")

    with tab2:
        st.subheader("My Consultation History")
        history = st.session_state.user_db[st.session_state.current_user]['consultation_history']
        if not history:
            st.info("You have no past or upcoming consultations.")
            return

        for consult in reversed(history):
            status_color = SUCCESS_GREEN if consult['status'] == 'Completed' else (WARNING_YELLOW if consult['status'] == 'Pending' else ERROR_RED)
            st.markdown(f"""
                <div class="skinova-card" style="border-left: 5px solid {status_color}; padding: 15px;">
                    <p style="font-size: 1.1em; font-weight: 700;">
                        👩‍⚕️ **{consult['expert']}** - {consult['date']} at {consult['time']} 
                        <span style="float: right; color: {status_color};">{consult['status'].upper()}</span>
                    </p>
                    <p style="font-size: 0.9em; color: {NEUTRAL_GREY};">**Concern:** {consult['concern']}</p>
                </div>
            """, unsafe_allow_html=True)


# --- 6. MAIN APPLICATION FLOW ---

def logout():
    """Resets the application state on logout."""
    st.session_state['logged_in'] = False
    st.session_state['current_user'] = 'guest_user'
    st.session_state['current_page'] = 'Login/Signup'
    st.session_state['current_routine_completed'] = False
    # Clear all temporary component states (checkboxes, forms)
    for key in list(st.session_state.keys()):
        if key.startswith('chk_') or key.startswith('form_'):
            del st.session_state[key]
    st.success("Successfully logged out.")
    st.experimental_rerun()

def main_app():
    """The main router and sidebar handler."""
    
    # 1. Sidebar Navigation
    with st.sidebar:
        st.image("https://placehold.co/200x50/3C8CB0/FFFFFF?text=SkinovaAI", caption="Hyper-Skincare Platform", width=200)
        
        st.markdown("---")
        
        if st.session_state.logged_in and st.session_state.user_db[st.session_state.current_user]['onboarding_complete']:
            st.subheader(f"Welcome, {st.session_state.current_user.capitalize()}!")
            
            pages = {
                'Dashboard': '📊 Dashboard',
                'My Routine': '✅ My Daily Ritual',
                'Skin Analyzer': '🔬 Hyper-Analyzer',
                'Personalized Kit': '🎁 Personalized Kit',
                'Product Marketplace': '🛍️ Marketplace',
                'Skincare Academy': '👩‍🎓 Skincare Academy',
                'Community Forum': '💬 Community Forum',
                'Consult an Expert': '👩‍⚕️ Consult an Expert'
            }
            
            # Using radio buttons for cleaner navigation control
            selected_page_display = st.radio(
                "Navigation", 
                options=list(pages.values()), 
                index=list(pages.values()).index(pages.get(st.session_state.current_page, 'Dashboard'))
            )
            
            # Find the internal page key from the display name
            selected_page = next((key for key, value in pages.items() if value == selected_page_display), 'Dashboard')
            
            if st.session_state.current_page != selected_page:
                 navigate_to(selected_page)

            st.markdown("---")
            if st.button("🚪 Logout & Reset Session", help="Log out of the application"):
                logout()
                
        elif st.session_state.logged_in and not st.session_state.user_db[st.session_state.current_user]['onboarding_complete']:
            st.warning("Please complete onboarding to access the platform.")
            navigate_to('Onboarding')
        else:
            st.info("Please Login or Signup to access the Hyper-Platform.")
            if st.button("Start My Journey"):
                navigate_to('Login/Signup')


    # 2. Main Content Display (Router Logic)
    if st.session_state.logged_in and not st.session_state.user_db[st.session_state.current_user]['onboarding_complete']:
        onboarding_page() # Force redirect to onboarding
        
    elif st.session_state.current_page == 'Login/Signup' or not st.session_state.logged_in:
        login_page()
    
    elif st.session_state.current_page == 'Onboarding':
        onboarding_page()
        
    # --- Feature Pages ---
    elif st.session_state.current_page == 'Dashboard':
        dashboard_page()
    elif st.session_state.current_page == 'My Routine':
        my_routine_page()
    elif st.session_state.current_page == 'Skin Analyzer':
        skin_analyzer_page()
    elif st.session_state.current_page == 'Personalized Kit':
        personalized_kit_page()
    elif st.session_state.current_page == 'Product Marketplace':
        product_marketplace_page()
    elif st.session_state.current_page == 'Skincare Academy':
        skincare_academy_page()
    elif st.session_state.current_page == 'Community Forum':
        community_forum_page()
    elif st.session_state.current_page == 'Consult an Expert':
        consult_expert_page()
    else:
        # Default to dashboard if current_page is somehow invalid
        navigate_to('Dashboard')
        dashboard_page()

if __name__ == '__main__':
    main_app()
