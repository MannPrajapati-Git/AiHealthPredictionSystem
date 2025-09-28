# with graphs

import os
import pickle
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

# Set page configuration
st.set_page_config(
    page_title="Health Prediction System",
    layout="wide",
    page_icon="🏥",
    initial_sidebar_state="expanded"
)

# FIXED: Comprehensive CSS with proper selectbox targeting + Graph Styling + No Active Links
def load_css():
    st.markdown("""
    <style>
    /* Import modern fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Main app background - Clean White */
    .stApp {
        background-color: #ffffff;
        font-family: 'Poppins', sans-serif;
        color: #000000;
    }
    
     /* CRITICAL: Disable all sidebar toggle functionality */
    [data-testid="collapsedControl"] {
        display: none !important;
        visibility: hidden !important;
        pointer-events: none !important;
        opacity: 0 !important;
    }
    
    /* Hide hamburger menu icons completely */
    .css-1dp5vir,
    .css-1rs6os,
    .css-17lntkn {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Force sidebar to always be visible and stable */
    .css-1d391kg, 
    [data-testid="stSidebar"] {
        background-color: #f8f9fa !important;
        border-right: 2px solid #1e40af !important;
        transform: translateX(0px) !important;
        transition: none !important;
        position: relative !important;
        width: 300px !important;
        min-width: 300px !important;
        max-width: 300px !important;
    }
    
    /* Ensure sidebar content is always visible */
    .css-1d391kg .css-1v0mbdj,
    [data-testid="stSidebar"] > div {
        display: block !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    
    /* Disable any collapse animations */
    .css-1lcbmhc {
        transform: none !important;
        transition: none !important;
        width: 300px !important;
        min-width: 300px !important;
    }
    
    /* Main content area - adjust for stable sidebar */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background-color: transparent;
        margin-left: 0 !important;
    }
    
    /* Blue titles */
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        color: #1e40af !important;
        margin-bottom: 2rem;
        padding: 1.5rem;
        background-color: #f0f4ff;
        border-radius: 15px;
        border: 2px solid #1e40af;
        box-shadow: 0 4px 15px rgba(30, 64, 175, 0.1);
    }
    
    /* Section headers - Blue */
    .section-header {
        color: #1e40af !important;
        font-size: 2.5rem;
        font-weight: 600;
        text-align: center;
        margin-bottom: 2rem;
        padding: 1.2rem;
        background-color: #f0f4ff;
        border-radius: 12px;
        border: 2px solid #1e40af;
    }
    
    /* Info box styling */
    .info-box {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        border: 2px solid #1e40af;
        color: #000000;
    }
    
    .info-box h4 {
        color: #1e40af !important;
        margin-bottom: 0.8rem;
        font-weight: 600;
    }
    
    .info-box p {
        color: #000000;
        margin-bottom: 0;
        line-height: 1.6;
        font-size: 16px;
    }
    
    /* Graph container styling - NO ACTIVE LINKS */
    .plotly-graph-div {
        border-radius: 15px !important;
        box-shadow: 0 6px 20px rgba(30, 64, 175, 0.1) !important;
        margin: 1.5rem 0 !important;
        border: 2px solid #e5e7eb !important;
        background-color: #ffffff !important;
        pointer-events: none !important; /* Disable all interactions */
    }
    
    /* Disable Plotly interactions */
    .plotly .modebar {
        display: none !important;
    }
    
    /* Tab styling */
    .stTabs > div > div > div > div {
        background-color: #f8f9fa;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 2px solid #1e40af;
    }
    
    /* Tab button styling - ONLY COLOR CHANGE, NO LINKS */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f0f4ff;
        padding: 8px;
        border-radius: 10px;
        border: 2px solid #1e40af;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #ffffff !important;
        border: 1px solid #1e40af !important;
        border-radius: 8px !important;
        color: #1e40af !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #f0f4ff !important;
        transform: translateY(-1px) !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #1e40af !important;
        color: #ffffff !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(30, 64, 175, 0.3) !important;
    }
    
    /* Input field styling - Dark Blue Borders */
    .stTextInput > div > div > input {
        background-color: #ffffff;
        border: 2px solid #1e40af !important;
        border-radius: 10px;
        padding: 0.8rem;
        font-size: 16px;
        color: #000000;
        transition: all 0.3s ease;
        font-weight: 400;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6 !important;
        outline: none;
        box-shadow: 0 0 10px rgba(30, 64, 175, 0.2);
        background-color: #f0f4ff;
    }
    
    /* Input labels - Black Text */
    .stTextInput > label {
        color: #000000 !important;
        font-weight: 500;
        margin-bottom: 0.5rem;
        font-size: 16px;
    }
    
    /* Red Buttons */
    .stButton > button {
        background-color: #dc2626 !important;
        color: #ffffff !important;
        border: none;
        padding: 1rem 2rem;
        font-size: 18px;
        font-weight: 600;
        border-radius: 10px;
        transition: all 0.3s ease;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        background-color: #b91c1c !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(220, 38, 38, 0.3);
    }
    
    /* COMPREHENSIVE SELECTBOX FIX - All possible CSS targets */
    .stSelectbox > label {
        color: #000000 !important;
        font-weight: 500;
        margin-bottom: 0.5rem;
        font-size: 16px;
    }
    
    /* Main selectbox container - Multiple selectors for compatibility */
    .stSelectbox > div > div,
    .stSelectbox div[data-baseweb="select"],
    .stSelectbox div[data-testid="stSelectbox"] > div > div {
        background-color: #ffffff !important;
        border: 2px solid #1e40af !important;
        border-radius: 10px !important;
        color: #000000 !important;
        padding: 0.5rem;
    }
    
    /* CRITICAL FIX: Target the actual displayed text in selectbox */
    .stSelectbox div[data-baseweb="select"] > div > div,
    .stSelectbox div[data-baseweb="select"] span,
    .stSelectbox div[data-baseweb="select"] > div,
    .stSelectbox [data-baseweb="select"] > div {
        color: #000000 !important;
        background-color: transparent !important;
    }
    
    /* Target the selected value display */
    .stSelectbox [data-baseweb="select"] .css-1wa3eu0-placeholder,
    .stSelectbox [data-baseweb="select"] .css-1uccc91-singleValue,
    .stSelectbox [data-baseweb="select"] div[role="button"] > div,
    .stSelectbox [data-baseweb="select"] div[role="button"] span {
        color: #000000 !important;
    }
    
    /* Additional targeting for text visibility */
    .stSelectbox select,
    .stSelectbox input,
    .stSelectbox input[type="text"] {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    /* Force text color on all child elements */
    .stSelectbox * {
        color: #000000 !important;
    }
    
    /* Dropdown options styling */
    .stSelectbox [role="option"],
    .stSelectbox div[role="listbox"] li,
    .stSelectbox ul[role="listbox"] li {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    /* Hover states for dropdown */
    .stSelectbox [role="option"]:hover,
    .stSelectbox div[role="listbox"] li:hover,
    .stSelectbox ul[role="listbox"] li:hover {
        background-color: #f0f4ff !important;
        color: #000000 !important;
    }
    
    /* Force override any inherited styles */
    .stSelectbox div,
    .stSelectbox span,
    .stSelectbox p {
        color: #000000 !important;
    }
    
    /* Green Success Messages */
    .stSuccess {
        background-color: #16a34a !important;
        color: #ffffff !important;
        border-radius: 10px;
        padding: 1.2rem;
        border: none;
        font-size: 16px;
        font-weight: 500;
    }
    
    /* Red Error Messages */
    .stError {
        background-color: #dc2626 !important;
        color: #ffffff !important;
        border-radius: 10px;
        padding: 1.2rem;
        border: none;
        font-size: 16px;
        font-weight: 500;
    }
    
    /* Blue Info Messages */
    .stInfo {
        background-color: #1e40af !important;
        color: #ffffff !important;
        border-radius: 10px;
        padding: 1.2rem;
        border: none;
        font-size: 16px;
        font-weight: 500;
    }
    
    /* Model selection section */
    .model-section {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        border: 2px solid #1e40af;
    }
    
    .model-section h3 {
        color: #1e40af !important;
        margin-bottom: 1rem;
        font-weight: 600;
        font-size: 1.5rem;
    }
    
    /* All headers - Blue */
    h1, h2, h3, h4, h5, h6 {
        color: #1e40af !important;
        font-weight: 600;
    }
    
    /* All text elements - Black */
    p, div, span, .stMarkdown {
        color: #000000 !important;
    }
    
    /* Subsection headers - Black */
    .subsection-header {
        color: #000000 !important;
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 1rem;
        padding: 0.8rem;
        background-color: #f8f9fa;
        border-radius: 8px;
        border-left: 4px solid #1e40af;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #000000;
        border-top: 2px solid #1e40af;
        margin-top: 2rem;
        background-color: #f8f9fa;
        border-radius: 10px;
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Sidebar option menu styling */
    .nav-link {
        color: #000000 !important;
    }
    
    /* Column styling */
    .stColumn {
        padding: 0.5rem;
    }
    
    /* Radio and checkbox styling */
    .stRadio > label, .stCheckbox > label {
        color: #000000 !important;
        font-weight: 500;
    }
    
    /* Metric styling */
    .metric-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid #1e40af;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Load CSS
load_css()

# FIXED: Define the correct directory paths according to your folder structure
working_dir = os.path.dirname(os.path.abspath(__file__))
dataset_dir = os.path.join(working_dir, 'dataset')
models_dir = os.path.join(working_dir, 'saved_models')

# Load the models with correct path
@st.cache_resource
def load_models():
    try:
        diabetes_logistic = pickle.load(open(f'{models_dir}/logistic_regression.pkl', 'rb'))
        diabetes_rf = pickle.load(open(f'{models_dir}/random_forest.pkl', 'rb'))
        diabetes_svm = pickle.load(open(f'{models_dir}/svm.pkl', 'rb'))
        
        heart_logistic = pickle.load(open(f'{models_dir}/logistic_regression1.pkl', 'rb'))
        heart_rf = pickle.load(open(f'{models_dir}/random_forest1.pkl', 'rb'))
        heart_svm = pickle.load(open(f'{models_dir}/svm1.pkl', 'rb'))
        
        return {
            'diabetes': {'Logistic Regression': diabetes_logistic, 'Random Forest': diabetes_rf, 'SVM': diabetes_svm},
            'heart': {'Logistic Regression': heart_logistic, 'Random Forest': heart_rf, 'SVM': heart_svm}
        }
    except Exception as e:
        st.error(f"Error loading models: {str(e)}")
        return None

models = load_models()

# FIXED: Load datasets with correct path from dataset folder
@st.cache_data
def load_datasets():
    try:
        # Load the datasets with proper separator from dataset folder
        diabetes_path = os.path.join(dataset_dir, 'diabetes.csv')
        heart_path = os.path.join(dataset_dir, 'heart.csv')
        
        diabetes_df = pd.read_csv(diabetes_path, sep=';')
        heart_df = pd.read_csv(heart_path, sep=';')
        
        return diabetes_df, heart_df
    except Exception as e:
        st.error(f"Error loading datasets: {str(e)}")
        st.error(f"Looking for files at: {diabetes_path} and {heart_path}")
        return None, None

# Function to show detailed diabetes suggestions using st.html
def show_diabetes_suggestions(prediction_result):
    if prediction_result == 1:  # High Risk
        st.html("""
        <div style="
            background-color: #f0f9ff;
            padding: 2rem;
            border-radius: 15px;
            margin: 2rem 0;
            border: 2px solid #0ea5e9;
            color: #000000;
        ">
            <h4 style="color: #0ea5e9; margin-bottom: 1rem; font-weight: 600; font-size: 1.4rem;">
                📋 DETAILED RECOMMENDATIONS FOR DIABETES MANAGEMENT
            </h4>
            
            <h5 style="color: #1e40af; margin-top: 1.5rem; margin-bottom: 0.8rem; font-weight: 600;">
                🏥 Immediate Actions Required:
            </h5>
            <ul style="margin-bottom: 1rem;">
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Consult an Endocrinologist or Primary Care Doctor immediately</strong>
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    Schedule comprehensive blood tests (HbA1c, fasting glucose, glucose tolerance test)
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    Get regular blood pressure and cholesterol screenings
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    Consider continuous glucose monitoring if recommended by doctor
                </li>
            </ul>
            
            <h5 style="color: #1e40af; margin-top: 1.5rem; margin-bottom: 0.8rem; font-weight: 600;">
                🍽️ Dietary Guidelines:
            </h5>
            <ul style="margin-bottom: 1rem;">
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Choose complex carbohydrates:</strong> Whole grains, quinoa, oats instead of white rice/bread
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Increase fiber intake:</strong> Vegetables, legumes, berries (aim for 25-30g daily)
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Portion control:</strong> Use smaller plates, measure portions, eat slowly
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Avoid:</strong> Sugary drinks, processed foods, refined sugars, trans fats
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Timing:</strong> Eat smaller, frequent meals every 3-4 hours
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Hydration:</strong> Drink 8-10 glasses of water daily, avoid fruit juices
                </li>
            </ul>
            
            <h5 style="color: #1e40af; margin-top: 1.5rem; margin-bottom: 0.8rem; font-weight: 600;">
                🏃‍♂️ Exercise Recommendations:
            </h5>
            <ul style="margin-bottom: 1rem;">
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Aerobic Exercise:</strong> 150 minutes moderate activity per week (brisk walking, swimming)
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Strength Training:</strong> 2-3 sessions per week with resistance exercises
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Post-meal walks:</strong> 10-15 minutes after each meal to control blood sugar spikes
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Monitor during exercise:</strong> Check blood glucose before and after physical activity
                </li>
            </ul>
            
            <h5 style="color: #1e40af; margin-top: 1.5rem; margin-bottom: 0.8rem; font-weight: 600;">
                📊 Monitoring & Lifestyle:
            </h5>
            <ul style="margin-bottom: 1rem;">
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Daily blood glucose monitoring</strong> as prescribed by healthcare provider
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Weight management:</strong> Aim for 5-10% weight loss if overweight
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Stress management:</strong> Practice yoga, meditation, or deep breathing exercises
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Sleep hygiene:</strong> 7-9 hours of quality sleep nightly
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Quit smoking and limit alcohol</strong> consumption
                </li>
            </ul>
            
            <p style="color: #000000; line-height: 1.6; margin-bottom: 1rem;">
                <strong>⚠️ Warning Signs to Watch:</strong> Excessive thirst, frequent urination, blurred vision, fatigue, slow-healing wounds. Contact healthcare provider immediately if these occur.
            </p>
        </div>
        """)
    else:  # Low Risk
        st.html("""
        <div style="
            background-color: #f0f9ff;
            padding: 2rem;
            border-radius: 15px;
            margin: 2rem 0;
            border: 2px solid #0ea5e9;
            color: #000000;
        ">
            <h4 style="color: #0ea5e9; margin-bottom: 1rem; font-weight: 600; font-size: 1.4rem;">
                ✅ DIABETES PREVENTION RECOMMENDATIONS
            </h4>
            
            <h5 style="color: #1e40af; margin-top: 1.5rem; margin-bottom: 0.8rem; font-weight: 600;">
                🍎 Maintain Healthy Lifestyle:
            </h5>
            <ul style="margin-bottom: 1rem;">
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Balanced diet:</strong> Include plenty of vegetables, fruits, whole grains, and lean proteins
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Regular meals:</strong> Maintain consistent eating schedule, avoid skipping meals
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Limit processed foods:</strong> Reduce intake of packaged snacks, sugary beverages
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Portion awareness:</strong> Use smaller plates and practice mindful eating
                </li>
            </ul>
            
            <h5 style="color: #1e40af; margin-top: 1.5rem; margin-bottom: 0.8rem; font-weight: 600;">
                🏋️‍♀️ Stay Physically Active:
            </h5>
            <ul style="margin-bottom: 1rem;">
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Regular exercise:</strong> 30 minutes of moderate activity, 5 days a week
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Daily movement:</strong> Take stairs, walk during breaks, park farther away
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Variety:</strong> Mix cardio, strength training, and flexibility exercises
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Find enjoyable activities:</strong> Dancing, cycling, hiking, sports
                </li>
            </ul>
            
            <h5 style="color: #1e40af; margin-top: 1.5rem; margin-bottom: 0.8rem; font-weight: 600;">
                🔍 Regular Health Monitoring:
            </h5>
            <ul style="margin-bottom: 1rem;">
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Annual health checkups</strong> including blood glucose screening
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Maintain healthy weight:</strong> BMI between 18.5-24.9
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Monitor blood pressure</strong> and cholesterol levels regularly
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Family history awareness:</strong> Inform doctor about diabetes family history
                </li>
            </ul>
            
            <h5 style="color: #1e40af; margin-top: 1.5rem; margin-bottom: 0.8rem; font-weight: 600;">
                🌟 Lifestyle Optimization:
            </h5>
            <ul style="margin-bottom: 1rem;">
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Stress management:</strong> Practice relaxation techniques, maintain work-life balance
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Quality sleep:</strong> 7-9 hours per night with consistent sleep schedule
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Stay hydrated:</strong> Drink water throughout the day
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Avoid smoking and limit alcohol</strong> consumption
                </li>
            </ul>
            
            <p style="color: #000000; line-height: 1.6; margin-bottom: 1rem;">
                <strong>🎯 Prevention Goal:</strong> Continue healthy habits to maintain low diabetes risk. Consider annual screening, especially after age 35 or if risk factors develop.
            </p>
        </div>
        """)

# Function to show detailed heart disease suggestions using st.html
def show_heart_disease_suggestions(prediction_result):
    if prediction_result == 1:  # High Risk
        st.html("""
        <div style="
            background-color: #f0f9ff;
            padding: 2rem;
            border-radius: 15px;
            margin: 2rem 0;
            border: 2px solid #0ea5e9;
            color: #000000;
        ">
            <h4 style="color: #0ea5e9; margin-bottom: 1rem; font-weight: 600; font-size: 1.4rem;">
                💓 COMPREHENSIVE HEART DISEASE MANAGEMENT PLAN
            </h4>
            
            <h5 style="color: #1e40af; margin-top: 1.5rem; margin-bottom: 0.8rem; font-weight: 600;">
                🏥 Immediate Medical Care:
            </h5>
            <ul style="margin-bottom: 1rem;">
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Consult a Cardiologist immediately</strong> for comprehensive evaluation
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Complete cardiac workup:</strong> ECG, echocardiogram, stress test, cardiac catheterization if needed
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Blood work:</strong> Lipid profile, cardiac enzymes, inflammatory markers
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Regular monitoring:</strong> Blood pressure, cholesterol, heart rhythm
                </li>
            </ul>
            
            <h5 style="color: #1e40af; margin-top: 1.5rem; margin-bottom: 0.8rem; font-weight: 600;">
                💊 Medication Compliance:
            </h5>
            <ul style="margin-bottom: 1rem;">
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Take prescribed medications exactly as directed</strong> (blood thinners, statins, ACE inhibitors)
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Never skip doses</strong> and don't stop medications without doctor consultation
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Monitor for side effects</strong> and report to healthcare provider
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Keep emergency medications</strong> (like nitroglycerin) accessible if prescribed
                </li>
            </ul>
            
            <h5 style="color: #1e40af; margin-top: 1.5rem; margin-bottom: 0.8rem; font-weight: 600;">
                🥗 Heart-Healthy Diet (DASH/Mediterranean):
            </h5>
            <ul style="margin-bottom: 1rem;">
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Reduce sodium:</strong> Less than 2,300mg daily (ideally 1,500mg)
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Increase omega-3:</strong> Fatty fish 2-3 times weekly (salmon, mackerel, sardines)
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Choose healthy fats:</strong> Olive oil, avocados, nuts instead of saturated fats
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Limit cholesterol:</strong> Less than 200mg daily, avoid trans fats completely
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Eat more:</strong> Fruits, vegetables, whole grains, lean proteins, legumes
                </li>
            </ul>
            
            <h5 style="color: #1e40af; margin-top: 1.5rem; margin-bottom: 0.8rem; font-weight: 600;">
                🏃‍♂️ Cardiac Rehabilitation Exercise:
            </h5>
            <ul style="margin-bottom: 1rem;">
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Doctor-supervised exercise program</strong> initially, then gradually increase activity
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Start slowly:</strong> 5-10 minutes daily, gradually work up to 30-45 minutes
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Monitor heart rate:</strong> Stay within target zones as prescribed
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Warning signs during exercise:</strong> Stop if chest pain, dizziness, or shortness of breath
                </li>
            </ul>
            
            <h5 style="color: #1e40af; margin-top: 1.5rem; margin-bottom: 0.8rem; font-weight: 600;">
                🚨 Emergency Preparedness:
            </h5>
            <ul style="margin-bottom: 1rem;">
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Know heart attack symptoms:</strong> Chest pain, arm/jaw pain, nausea, sweating
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Keep emergency contacts</strong> readily available
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Have action plan</strong> for cardiac emergencies
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Regular follow-ups</strong> with cardiologist as scheduled
                </li>
            </ul>
            
            <p style="color: #000000; line-height: 1.6; margin-bottom: 1rem;">
                <strong>⚠️ Seek Immediate Help If:</strong> Chest pain, severe shortness of breath, irregular heartbeat, dizziness, or fainting. Call emergency services immediately - don't wait!
            </p>
        </div>
        """)
    else:  # Low Risk
        st.html("""
        <div style="
            background-color: #f0f9ff;
            padding: 2rem;
            border-radius: 15px;
            margin: 2rem 0;
            border: 2px solid #0ea5e9;
            color: #000000;
        ">
            <h4 style="color: #0ea5e9; margin-bottom: 1rem; font-weight: 600; font-size: 1.4rem;">
                ❤️ HEART DISEASE PREVENTION STRATEGIES
            </h4>
            
            <h5 style="color: #1e40af; margin-top: 1.5rem; margin-bottom: 0.8rem; font-weight: 600;">
                🍽️ Heart-Protective Nutrition:
            </h5>
            <ul style="margin-bottom: 1rem;">
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Mediterranean diet pattern:</strong> Emphasize olive oil, fish, whole grains, fruits, vegetables
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Limit saturated fats:</strong> Choose lean meats, low-fat dairy products
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Increase antioxidants:</strong> Berries, dark leafy greens, colorful vegetables
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Moderate sodium:</strong> Use herbs and spices instead of salt for flavor
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Stay hydrated:</strong> Adequate water intake supports cardiovascular function
                </li>
            </ul>
            
            <h5 style="color: #1e40af; margin-top: 1.5rem; margin-bottom: 0.8rem; font-weight: 600;">
                🏃‍♀️ Cardiovascular Fitness:
            </h5>
            <ul style="margin-bottom: 1rem;">
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Aerobic exercise:</strong> 150 minutes moderate or 75 minutes vigorous weekly
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Strength training:</strong> 2+ days per week targeting major muscle groups
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Daily activity:</strong> Take stairs, walk meetings, active hobbies
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Flexibility:</strong> Include stretching or yoga for overall wellness
                </li>
            </ul>
            
            <h5 style="color: #1e40af; margin-top: 1.5rem; margin-bottom: 0.8rem; font-weight: 600;">
                🔍 Preventive Health Monitoring:
            </h5>
            <ul style="margin-bottom: 1rem;">
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Regular checkups:</strong> Annual physical exams with cardiovascular assessment
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Know your numbers:</strong> Blood pressure, cholesterol, BMI, blood sugar
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Screening schedule:</strong> Follow age-appropriate guidelines for cardiac screening
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Family history:</strong> Discuss genetic risk factors with healthcare provider
                </li>
            </ul>
            
            <h5 style="color: #1e40af; margin-top: 1.5rem; margin-bottom: 0.8rem; font-weight: 600;">
                🌟 Lifestyle Optimization:
            </h5>
            <ul style="margin-bottom: 1rem;">
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Stress management:</strong> Practice meditation, deep breathing, or mindfulness
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Quality sleep:</strong> 7-9 hours nightly with good sleep hygiene
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Don't smoke:</strong> If you smoke, seek help to quit; avoid secondhand smoke
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Limit alcohol:</strong> No more than 1 drink/day for women, 2 for men
                </li>
                <li style="color: #000000; margin-bottom: 0.5rem; line-height: 1.5;">
                    <strong>Maintain healthy weight:</strong> BMI 18.5-24.9 range
                </li>
            </ul>
            
            <p style="color: #000000; line-height: 1.6; margin-bottom: 1rem;">
                <strong>🎯 Prevention Goal:</strong> Your current risk is low - maintain these healthy habits! Continue regular health screenings and be aware of any changes in cardiovascular symptoms.
            </p>
        </div>
        """)

# Main title - Blue
st.markdown('<div class="main-title">🏥 AI Health Prediction System</div>', unsafe_allow_html=True)

# Sidebar navigation - UPDATED WITH NEW PAGE
with st.sidebar:
    st.markdown("### 🔍 Navigation")
    selected = option_menu(
        'Health Predictions',
        ['Diabetes Prediction', 'Heart Disease Prediction', 'Data Analytics'],  # NEW PAGE ADDED
        icons=['droplet-fill', 'heart-fill', 'bar-chart-fill'],  # NEW ICON ADDED
        menu_icon='hospital-fill',
        default_index=0,
        styles={
            "container": {"padding": "10px", "background-color": "#f8f9fa"},
            "icon": {"color": "#1e40af", "font-size": "20px"}, 
            "nav-link": {
                "font-size": "16px", 
                "text-align": "left", 
                "margin": "5px", 
                "padding": "10px",
                "border-radius": "8px",
                "background-color": "transparent",
                "--hover-color": "#f0f4ff",
                "color": "#000000"
            },
            "nav-link-selected": {
                "background-color": "#1e40af",
                "color": "#ffffff"
            },
        }
    )

# Helper function for input fields
def create_input_field(label, help_text=None, key=None):
    return st.text_input(label, help=help_text, key=key)

# NEW DATA ANALYTICS PAGE - FIXED VERSION
if selected == 'Data Analytics':
    st.markdown('<div class="section-header">📊 Healthcare Data Analytics & Insights</div>', unsafe_allow_html=True)
    
    # Load datasets
    diabetes_df, heart_df = load_datasets()
    
    if diabetes_df is not None and heart_df is not None:
        # Information section
        st.markdown("""
        <div class="info-box">
            <h4>📈 About Data Analytics</h4>
            <p>Explore comprehensive insights from healthcare datasets. These visualizations help understand disease patterns, risk factors, and demographic trends to support better health predictions.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create tabs for different analysis types
        tab1, tab2, tab3, tab4 = st.tabs(["🥧 Disease Distribution", "📊 Risk Factors", "🔥 Correlations", "👥 Demographics"])
        
        with tab1:
            st.markdown('<div class="subsection-header">📈 Disease Distribution Analysis</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Diabetes Distribution Pie Chart
                diabetes_counts = diabetes_df['Outcome'].value_counts()
                fig1 = px.pie(
                    values=diabetes_counts.values,
                    names=['No Diabetes (500)', 'Has Diabetes (268)'],
                    title="<b>Diabetes Dataset Distribution</b><br><sub>Total: 768 patients</sub>",
                    color_discrete_sequence=['#16a34a', '#dc2626'],
                    hole=0.4
                )
                fig1.update_traces(textposition='inside', textinfo='percent+label', textfont_size=12)
                fig1.update_layout(
                    font=dict(family="Poppins, sans-serif", size=14),
                    title_x=0.5,
                    showlegend=True,
                    height=400,
                    margin=dict(t=80, b=20, l=20, r=20)
                )
                # FIXED: Remove all interactions
                st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False, 'staticPlot': True})
            
            with col2:
                # Heart Disease Distribution Pie Chart
                heart_counts = heart_df['target'].value_counts().sort_index()
                fig2 = px.pie(
                    values=heart_counts.values,
                    names=['No Disease (138)', 'Has Disease (165)'],
                    title="<b>Heart Disease Dataset Distribution</b><br><sub>Total: 303 patients</sub>",
                    color_discrete_sequence=['#16a34a', '#dc2626'],
                    hole=0.4
                )
                fig2.update_traces(textposition='inside', textinfo='percent+label', textfont_size=12)
                fig2.update_layout(
                    font=dict(family="Poppins, sans-serif", size=14),
                    title_x=0.5,
                    showlegend=True,
                    height=400,
                    margin=dict(t=80, b=20, l=20, r=20)
                )
                # FIXED: Remove all interactions
                st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False, 'staticPlot': True})
            
            # Combined Dataset Overview
            st.markdown('<div class="subsection-header">📋 Dataset Overview</div>', unsafe_allow_html=True)
            
            # Create summary metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label="🩺 Diabetes Cases",
                    value=f"{len(diabetes_df)}",
                    delta=f"{diabetes_counts[1]} positive"
                )
            
            with col2:
                st.metric(
                    label="❤️ Heart Disease Cases", 
                    value=f"{len(heart_df)}",
                    delta=f"{heart_counts[1]} positive"
                )
            
            with col3:
                diabetes_risk_rate = (diabetes_counts[1] / len(diabetes_df)) * 100
                st.metric(
                    label="🩺 Diabetes Risk Rate",
                    value=f"{diabetes_risk_rate:.1f}%",
                    delta="34.9% of patients"
                )
            
            with col4:
                heart_risk_rate = (heart_counts[1] / len(heart_df)) * 100
                st.metric(
                    label="❤️ Heart Disease Risk Rate",
                    value=f"{heart_risk_rate:.1f}%", 
                    delta="54.5% of patients"
                )
        
        with tab2:
            st.markdown('<div class="subsection-header">📊 Age Distribution & Risk Analysis</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Age distribution for diabetes
                fig3 = px.histogram(
                    diabetes_df, 
                    x='Age', 
                    color='Outcome',
                    title="<b>Age Distribution - Diabetes Dataset</b>",
                    nbins=15,
                    color_discrete_sequence=['#16a34a', '#dc2626'],
                    labels={'Outcome': 'Diabetes Status', 'count': 'Number of Patients'}
                )
                fig3.update_traces(opacity=0.8)
                fig3.update_layout(
                    font=dict(family="Poppins, sans-serif", size=12),
                    title_x=0.5,
                    xaxis_title="Age (years)",
                    yaxis_title="Number of Patients",
                    legend=dict(title="Status"),
                    height=400,
                    bargap=0.1,
                    xaxis=dict(range=[15, 85])  # FIXED: Correct syntax
                )
                # FIXED: Remove all interactions
                st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False, 'staticPlot': True})
            
            with col2:
                # Age distribution for heart disease
                fig4 = px.histogram(
                    heart_df,
                    x='age',
                    color='target',
                    title="<b>Age Distribution - Heart Disease Dataset</b>", 
                    nbins=15,
                    color_discrete_sequence=['#16a34a', '#dc2626'],
                    labels={'target': 'Heart Disease Status', 'count': 'Number of Patients'}
                )
                fig4.update_traces(opacity=0.8)
                fig4.update_layout(
                    font=dict(family="Poppins, sans-serif", size=12),
                    title_x=0.5,
                    xaxis_title="Age (years)",
                    yaxis_title="Number of Patients",
                    legend=dict(title="Status"),
                    height=400,
                    bargap=0.1,
                    xaxis=dict(range=[25, 80])  # FIXED: Correct syntax
                )
                # FIXED: Remove all interactions
                st.plotly_chart(fig4, use_container_width=True, config={'displayModeBar': False, 'staticPlot': True})
            
            # BMI vs Glucose Analysis
            st.markdown('<div class="subsection-header">⚖️ BMI vs Glucose Level Analysis</div>', unsafe_allow_html=True)
            
            fig5 = px.scatter(
                diabetes_df,
                x='BMI',
                y='Glucose', 
                color='Outcome',
                title="<b>BMI vs Glucose Level Relationship</b>",
                color_discrete_sequence=['#16a34a', '#dc2626'],
                labels={'Outcome': 'Diabetes Status'},
                hover_data=['Age', 'BloodPressure']
            )
            fig5.update_traces(marker=dict(size=8, opacity=0.7))
            fig5.update_layout(
                font=dict(family="Poppins, sans-serif", size=12),
                title_x=0.5,
                xaxis_title="BMI (kg/m²)",
                yaxis_title="Glucose Level (mg/dL)",
                legend=dict(title="Diabetes Status"),
                height=450
            )
            # FIXED: Remove all interactions
            st.plotly_chart(fig5, use_container_width=True, config={'displayModeBar': False, 'staticPlot': True})
        
        with tab3:
            st.markdown('<div class="subsection-header">🔥 Feature Correlation Analysis</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Diabetes Correlation Heatmap
                corr_diabetes = diabetes_df.corr()
                fig6 = px.imshow(
                    corr_diabetes,
                    title="<b>Diabetes Features Correlation Matrix</b>",
                    color_continuous_scale='RdBu',
                    aspect='auto'
                )
                fig6.update_layout(
                    font=dict(family="Poppins, sans-serif", size=10),
                    title_x=0.5,
                    height=400,
                    margin=dict(t=60, b=20, l=20, r=20)
                )
                # FIXED: Remove all interactions
                st.plotly_chart(fig6, use_container_width=True, config={'displayModeBar': False, 'staticPlot': True})
            
            with col2:
                # Heart Disease Correlation Heatmap
                corr_heart = heart_df.corr()
                fig7 = px.imshow(
                    corr_heart,
                    title="<b>Heart Disease Features Correlation Matrix</b>",
                    color_continuous_scale='RdBu',
                    aspect='auto'
                )
                fig7.update_layout(
                    font=dict(family="Poppins, sans-serif", size=10),
                    title_x=0.5,
                    height=400,
                    margin=dict(t=60, b=20, l=20, r=20)
                )
                # FIXED: Remove all interactions
                st.plotly_chart(fig7, use_container_width=True, config={'displayModeBar': False, 'staticPlot': True})
            
            # Top Correlations Analysis
            st.markdown('<div class="subsection-header">🎯 Key Feature Correlations</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Diabetes correlations with outcome
                diabetes_corr_outcome = corr_diabetes['Outcome'].abs().sort_values(ascending=False)[1:6]  # Top 5 excluding self
                fig8 = px.bar(
                    x=diabetes_corr_outcome.values,
                    y=diabetes_corr_outcome.index,
                    orientation='h',
                    title="<b>Top Risk Factors - Diabetes</b>",
                    color=diabetes_corr_outcome.values,
                    color_continuous_scale='Reds',
                    labels={'x': 'Correlation with Diabetes', 'y': 'Features'}
                )
                fig8.update_layout(
                    font=dict(family="Poppins, sans-serif", size=12),
                    title_x=0.5,
                    height=300,
                    showlegend=False,
                    yaxis={'categoryorder': 'total ascending'}
                )
                # FIXED: Remove all interactions
                st.plotly_chart(fig8, use_container_width=True, config={'displayModeBar': False, 'staticPlot': True})
            
            with col2:
                # Heart disease correlations with target
                heart_corr_target = corr_heart['target'].abs().sort_values(ascending=False)[1:6]  # Top 5 excluding self
                fig9 = px.bar(
                    x=heart_corr_target.values,
                    y=heart_corr_target.index,
                    orientation='h',
                    title="<b>Top Risk Factors - Heart Disease</b>",
                    color=heart_corr_target.values,
                    color_continuous_scale='Reds',
                    labels={'x': 'Correlation with Heart Disease', 'y': 'Features'}
                )
                fig9.update_layout(
                    font=dict(family="Poppins, sans-serif", size=12),
                    title_x=0.5,
                    height=300,
                    showlegend=False,
                    yaxis={'categoryorder': 'total ascending'}
                )
                # FIXED: Remove all interactions
                st.plotly_chart(fig9, use_container_width=True, config={'displayModeBar': False, 'staticPlot': True})
        
        with tab4:
            st.markdown('<div class="subsection-header">👥 Demographic Analysis</div>', unsafe_allow_html=True)
            
            # Gender analysis for heart disease (diabetes dataset doesn't have sex column)
            col1, col2 = st.columns(2)
            
            with col1:
                # Gender distribution in heart disease dataset
                gender_dist = heart_df['sex'].value_counts()
                fig10 = px.pie(
                    values=gender_dist.values,
                    names=['Female (96)', 'Male (207)'],
                    title="<b>Gender Distribution<br>Heart Disease Dataset</b>",
                    color_discrete_sequence=['#ec4899', '#3b82f6']
                )
                fig10.update_traces(textposition='inside', textinfo='percent+label')
                fig10.update_layout(
                    font=dict(family="Poppins, sans-serif", size=12),
                    title_x=0.5,
                    height=350
                )
                # FIXED: Remove all interactions
                st.plotly_chart(fig10, use_container_width=True, config={'displayModeBar': False, 'staticPlot': True})
            
            with col2:
                # Gender vs Heart Disease
                gender_disease = pd.crosstab(heart_df['sex'], heart_df['target'])
                fig11 = px.bar(
                    gender_disease,
                    title="<b>Heart Disease by Gender</b>",
                    color_discrete_sequence=['#16a34a', '#dc2626'],
                    labels={'value': 'Number of Patients', 'index': 'Gender'}
                )
                fig11.update_layout(
                    font=dict(family="Poppins, sans-serif", size=12),
                    title_x=0.5,
                    xaxis_title="Gender (0=Female, 1=Male)",
                    yaxis_title="Number of Patients",
                    legend=dict(title="Heart Disease Status"),
                    height=350
                )
                # FIXED: Remove all interactions
                st.plotly_chart(fig11, use_container_width=True, config={'displayModeBar': False, 'staticPlot': True})
            
            # Age group analysis
            st.markdown('<div class="subsection-header">🎂 Age Group Risk Analysis</div>', unsafe_allow_html=True)
            
            # Create age groups
            diabetes_df['AgeGroup'] = pd.cut(diabetes_df['Age'], 
                                           bins=[0, 30, 45, 60, 100], 
                                           labels=['Under 30', '30-45', '45-60', 'Over 60'])
            heart_df['AgeGroup'] = pd.cut(heart_df['age'], 
                                        bins=[0, 40, 55, 70, 100], 
                                        labels=['Under 40', '40-55', '55-70', 'Over 70'])
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Diabetes by age group
                diabetes_age_group = pd.crosstab(diabetes_df['AgeGroup'], diabetes_df['Outcome'], normalize='index') * 100
                fig12 = px.bar(
                    diabetes_age_group,
                    title="<b>Diabetes Risk by Age Group (%)</b>",
                    color_discrete_sequence=['#16a34a', '#dc2626'],
                    labels={'value': 'Percentage (%)', 'index': 'Age Group'}
                )
                fig12.update_layout(
                    font=dict(family="Poppins, sans-serif", size=12),
                    title_x=0.5,
                    xaxis_title="Age Group",
                    yaxis_title="Percentage (%)",
                    legend=dict(title="Diabetes Status"),
                    height=350
                )
                # FIXED: Remove all interactions
                st.plotly_chart(fig12, use_container_width=True, config={'displayModeBar': False, 'staticPlot': True})
            
            with col2:
                # Heart disease by age group
                heart_age_group = pd.crosstab(heart_df['AgeGroup'], heart_df['target'], normalize='index') * 100
                fig13 = px.bar(
                    heart_age_group,
                    title="<b>Heart Disease Risk by Age Group (%)</b>",
                    color_discrete_sequence=['#16a34a', '#dc2626'],
                    labels={'value': 'Percentage (%)', 'index': 'Age Group'}
                )
                fig13.update_layout(
                    font=dict(family="Poppins, sans-serif", size=12),
                    title_x=0.5,
                    xaxis_title="Age Group",
                    yaxis_title="Percentage (%)",
                    legend=dict(title="Heart Disease Status"),
                    height=350
                )
                # FIXED: Remove all interactions
                st.plotly_chart(fig13, use_container_width=True, config={'displayModeBar': False, 'staticPlot': True})
            
    else:
        st.error("Unable to load datasets. Please make sure diabetes.csv and heart.csv files are in the 'dataset' folder.")

# Diabetes Prediction Page
if selected == 'Diabetes Prediction':
    st.markdown('<div class="section-header">🩺 Diabetes Prediction using Machine Learning</div>', unsafe_allow_html=True)
    
    # Information section
    st.markdown("""
    <div class="info-box">
        <h4>ℹ️ About Diabetes Prediction</h4>
        <p>This tool uses advanced machine learning algorithms to predict diabetes risk based on various health parameters. Please enter your health information accurately for the best prediction results.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Input section
    st.markdown('<div class="subsection-header">📝 Enter Your Health Information</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        pregnancies = create_input_field('Number of Pregnancies', 'Number of times pregnant', 'pregnancies')
        skin_thickness = create_input_field('Skin Thickness (mm)', 'Triceps skin fold thickness', 'skin')
        diabetes_pedigree = create_input_field('Diabetes Pedigree Function', 'Diabetes pedigree function value', 'pedigree')
    
    with col2:
        glucose = create_input_field('Glucose Level (mg/dL)', 'Plasma glucose concentration', 'glucose')
        insulin = create_input_field('Insulin Level (μU/mL)', '2-Hour serum insulin', 'insulin')
        age = create_input_field('Age (years)', 'Age in years', 'age')
    
    with col3:
        blood_pressure = create_input_field('Blood Pressure (mmHg)', 'Diastolic blood pressure', 'bp')
        bmi = create_input_field('BMI (kg/m²)', 'Body mass index', 'bmi')
    
    # Model selection
    st.markdown('<div class="model-section">', unsafe_allow_html=True)
    st.markdown("### 🤖 Select Prediction Model")
    model_choice = st.selectbox(
        "Choose the machine learning model:",
        ["Logistic Regression", "Random Forest", "SVM"],
        help="Different models may give slightly different predictions."
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Prediction section
    st.markdown('<div class="subsection-header">🔍 Get Prediction</div>', unsafe_allow_html=True)
    if st.button('🔬 ANALYZE DIABETES RISK'):
        try:
            user_input = [pregnancies, glucose, blood_pressure, skin_thickness, insulin,
                         bmi, diabetes_pedigree, age]
            user_input = [float(x) if x else 0.0 for x in user_input]
            
            if models and 'diabetes' in models:
                selected_model = models['diabetes'][model_choice]
                prediction = selected_model.predict([user_input])
                
                if prediction[0] == 1:
                    st.error("⚠️ **HIGH RISK**: The model indicates a high risk of diabetes. Please consult with a healthcare professional immediately.")
                    show_diabetes_suggestions(1)
                else:
                    st.success("✅ **LOW RISK**: The model indicates a low risk of diabetes. Keep maintaining a healthy lifestyle!")
                    show_diabetes_suggestions(0)
                    
                st.info(f"📊 **Model Used**: {model_choice}")
            else:
                st.error("Models not loaded properly. Please check the model files.")
        except ValueError:
            st.error("Please enter valid numeric values for all fields.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Heart Disease Prediction Page
if selected == 'Heart Disease Prediction':
    st.markdown('<div class="section-header">❤️ Heart Disease Prediction using Machine Learning</div>', unsafe_allow_html=True)
    
    # Information section
    st.markdown("""
    <div class="info-box">
        <h4>ℹ️ About Heart Disease Prediction</h4>
        <p>This tool analyzes various cardiovascular parameters to assess heart disease risk. Please provide accurate medical information for reliable predictions.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Input section
    st.markdown('<div class="subsection-header">📝 Enter Your Cardiovascular Information</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        age = create_input_field('Age (years)', key='heart_age')
        trestbps = create_input_field('Resting Blood Pressure (mmHg)', key='trestbps')
        restecg = create_input_field('Resting ECG Results (0-2)', key='restecg')
        oldpeak = create_input_field('ST Depression', key='oldpeak')
        thal = create_input_field('Thalassemia (0-2)', key='thal')
    
    with col2:
        sex = create_input_field('Sex (0=Female, 1=Male)', key='sex')
        chol = create_input_field('Cholesterol (mg/dL)', key='chol')
        thalach = create_input_field('Max Heart Rate Achieved', key='thalach')
        slope = create_input_field('ST Segment Slope (0-2)', key='slope')
    
    with col3:
        cp = create_input_field('Chest Pain Type (0-3)', key='cp')
        fbs = create_input_field('Fasting Blood Sugar > 120 mg/dl (0/1)', key='fbs')
        exang = create_input_field('Exercise Induced Angina (0/1)', key='exang')
        ca = create_input_field('Major Vessels (0-3)', key='ca')
    
    # Model selection
    st.markdown('<div class="model-section">', unsafe_allow_html=True)
    st.markdown("### 🤖 Select Prediction Model")
    model_choice = st.selectbox(
        "Choose the machine learning model:",
        ["Logistic Regression", "Random Forest", "SVM"],
        help="Different models may give slightly different predictions.",
        key='heart_model'
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Prediction section
    st.markdown('<div class="subsection-header">🔍 Get Prediction</div>', unsafe_allow_html=True)
    if st.button('💓 ANALYZE HEART DISEASE RISK'):
        try:
            user_input = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, 
                         exang, oldpeak, slope, ca, thal]
            user_input = [float(x) if x else 0.0 for x in user_input]
            
            if models and 'heart' in models:
                selected_model = models['heart'][model_choice]
                prediction = selected_model.predict([user_input])
                
                if prediction[0] == 1:
                    st.error("⚠️ **HIGH RISK**: The model indicates a high risk of heart disease. Please consult with a cardiologist immediately.")
                    show_heart_disease_suggestions(1)
                else:
                    st.success("✅ **LOW RISK**: The model indicates a low risk of heart disease. Keep maintaining a heart-healthy lifestyle!")
                    show_heart_disease_suggestions(0)
                    
                st.info(f"📊 **Model Used**: {model_choice}")
            else:
                st.error("Models not loaded properly. Please check the model files.")
        except ValueError:
            st.error("Please enter valid numeric values for all fields.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Footer with Social Media Links - FIXED VERSION
st.markdown("---")
st.html("""
<div style="
    text-align: center;
    padding: 2rem;
    color: #000000;
    border-top: 2px solid #1e40af;
    margin-top: 2rem;
    background-color: #f8f9fa;
    border-radius: 10px;
">
    <p><strong>🔬 AI Health Prediction System</strong> | Built with Streamlit & Machine Learning</p>
    <p><small>⚠️ <strong>Disclaimer:</strong> This tool is for educational purposes only. Always consult healthcare professionals for medical advice.</small></p>
    
    <!-- Social Media Section -->
    <div style="margin-top: 20px; padding-top: 15px; border-top: 1px solid #ddd;">
        <p style="font-weight: 600; margin-bottom: 10px;">📞 Connect With Developer:</p>
        <div style="display: flex; justify-content: center; gap: 15px; flex-wrap: wrap;">
            
            <!-- Instagram -->
            <a href="https://instagram.com/mann_2502" target="_blank" style="
                color: #E4405F;
                text-decoration: none;
                display: flex;
                align-items: center;
                gap: 5px;
                padding: 8px 12px;
                border-radius: 8px;
                background-color: #ffffff;
                transition: all 0.3s ease;
                border: 1px solid #E4405F;
                font-size: 14px;
            ">
                📷 Instagram
            </a>
            
            <!-- LinkedIn -->
            <a href="https://www.linkedin.com/in/prajapatimann2502" target="_blank" style="
                color: #0077B5;
                text-decoration: none;
                display: flex;
                align-items: center;
                gap: 5px;
                padding: 8px 12px;
                border-radius: 8px;
                background-color: #ffffff;
                transition: all 0.3s ease;
                border: 1px solid #0077B5;
                font-size: 14px;
            ">
                💼 LinkedIn
            </a>
            
            <!-- GitHub -->
            <a href="https://github.com/MannPrajapati-Git" target="_blank" style="
                color: #333;
                text-decoration: none;
                display: flex;
                align-items: center;
                gap: 5px;
                padding: 8px 12px;
                border-radius: 8px;
                background-color: #ffffff;
                transition: all 0.3s ease;
                border: 1px solid #333;
                font-size: 14px;
            ">
                💻 GitHub
            </a>
            
            <!-- WhatsApp -->
            <a href="https://wa.me/917383797894" target="_blank" style="
                color: #25D366;
                text-decoration: none;
                display: flex;
                align-items: center;
                gap: 5px;
                padding: 8px 12px;
                border-radius: 8px;
                background-color: #ffffff;
                transition: all 0.3s ease;
                border: 1px solid #25D366;
                font-size: 14px;
            ">
                💬 WhatsApp
            </a>
            
        </div>
        
        <!-- Developer Credit -->
        <div style="margin-top: 15px; padding-top: 10px; border-top: 1px solid #eee;">
            <p style="font-size: 14px; color: #666; margin: 0;">
                👨‍💻 Developed by <strong style="color: #1e40af;">Mann Prajapati</strong> | 
                💡 Full Stack Developer & ML Enthusiast
            </p>
        </div>
    </div>
</div>
""")



