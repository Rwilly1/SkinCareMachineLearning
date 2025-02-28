import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from datetime import datetime
import os
import random

# Set page configuration
st.set_page_config(
    page_title="Skincare Ingredient Compatibility",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS to hide Streamlit elements and style the app
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Remove horizontal scrollbar */
        body {
            overflow-x: hidden !important;
            width: 100% !important;
            max-width: 100% !important;
        }
        
        [data-testid="stAppViewContainer"] {
            overflow-x: hidden !important;
            width: 100% !important;
            max-width: 100% !important;
        }
        
        section[data-testid="stSidebar"] {
            overflow-x: hidden !important;
        }
        
        .element-container, .stMarkdown {
            overflow-x: hidden !important;
            width: 100% !important;
            max-width: 100% !important;
        }
        
        /* Center disclaimer */
        [data-testid="stExpander"] {
            width: 100%;
        }
        
        [data-testid="stExpanderContent"] {
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        /* Reset Streamlit defaults */
        .stApp {
            background: #FFFFFF !important;
            overflow-x: hidden !important;
        }
        
        div[data-testid="stToolbar"] {
            display: none;
        }
        
        /* Layout */
        .main .block-container {
            padding: 0 !important;
            max-width: 414px !important;
            margin-left: calc(2rem + 2.0in) !important;
            margin-right: auto !important;
            padding-left: 1rem;
            padding-right: 1rem;
            max-width: 100%;
            overflow-x: hidden;
        }
        
        /* Phone container */
        div[data-testid="stAppViewContainer"] > .main {
            background: transparent;
            padding: 2rem 2rem 2rem 0;
            position: relative;
        }
        
        div[data-testid="stAppViewContainer"] > .main > .block-container {
            background: #132A13;
            border-radius: 40px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            height: 812px;
            position: relative;
            overflow: hidden;
            border: 12px solid #1f1f1f;
            z-index: 1;
        }
        
        /* Content area with white background */
        div[data-testid="stAppViewContainer"] > .main > .block-container > div {
            background: #132A13;
            height: calc(100% - 44px);
            overflow-y: auto;
            margin-top: 44px;
            padding: 20px;
            position: relative;
            z-index: 2;
            color: #ECF39E;
        }
        
        /* Status bar */
        div[data-testid="stAppViewContainer"] > .main > .block-container::after {
            content: '16:17';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 44px;
            background: #132A13;
            z-index: 999;
            color: white;
            display: flex;
            align-items: center;
            padding: 0 20px;
            font-weight: 600;
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        /* Status bar icons */
        div[data-testid="stAppViewContainer"] > .main > .block-container::before {
            content: '';
            position: absolute;
            top: 12px;
            right: 20px;
            width: 90px;
            height: 20px;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 90 16'%3E%3Cpath fill='white' d='M82,0H59v16h23V0z M81,2v12H60V2H81z M74,4v8H62V4H74z M35,6h3v6h-3V6z M30,8h3v4h-3V8z M25,10h3v2h-3V10z'/%3E%3Cpath fill='white' d='M40,4h3v8h-3V4z M35,6h3v6h-3V6z M30,8h3v4h-3V8z M25,10h3v2h-3V10z'/%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-size: contain;
            z-index: 1000;
        }
        
        /* Info box */
        .info-box {
            position: fixed;
            top: 0;
            left: calc(414px + 2.5in);
            right: 0;
            width: auto;
            height: 100vh;
            background: #FFFFF;
            border-radius: 0;
            padding: 0;
            color: #ECF39E;
            overflow: hidden;
            box-shadow: none;
            display: flex;
            justify-content: flex-start;
            align-items: center;
            z-index: -1;
            pointer-events: none;
        }
        
        .info-box img {
            height: 100%;
            width: auto;
            object-fit: contain;
            position: sticky;
            top: 0;
            left: 0;
        }
        
        /* Text styling */
        .stMarkdown p, .stTextInput label {
            color: #ECF39E !important;
        }
        
        h1, h2, h3 {
            color: #ECF39E !important;
        }
        
        /* Input field styling */
        .stTextArea > div > div > textarea {
            background-color: #31572C !important;
            color: #ECF39E !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 15px !important;
            font-size: 16px !important;
            min-height: 150px !important;
        }
        
        /* Hide empty/unused elements */
        [data-testid="stVerticalBlock"] > div:empty {
            display: none !important;
        }
        
        /* Button styling */
        .stButton > button {
            background-color: #31572C !important;
            color: #ECF39E !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 10px 20px !important;
            width: 100% !important;
            font-size: 16px !important;
            margin-top: 10px !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton > button:hover {
            background-color: #4F772D !important;
            transform: translateY(-2px) !important;
        }
        
        /* Card styling */
        .card {
            background: #31572C;
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border: 1px solid #4F772D;
            color: #ECF39E;
        }
        
        /* Custom scrollbar */
        div[data-testid="stAppViewContainer"] > .main > .block-container > div::-webkit-scrollbar {
            width: 6px;
        }
        
        div[data-testid="stAppViewContainer"] > .main > .block-container > div::-webkit-scrollbar-track {
            background: #31572C;
        }
        
        div[data-testid="stAppViewContainer"] > .main > .block-container > div::-webkit-scrollbar-thumb {
            background: #4F772D;
            border-radius: 3px;
        }
        
        /* Pro Tips section */
        .stMarkdown div[data-testid="stMarkdownContainer"] ul {
            list-style: none;
            padding-left: 0;
        }
        
        .stMarkdown div[data-testid="stMarkdownContainer"] ul li {
            color: #31572C !important;
            margin-bottom: 10px;
            font-weight: 500;
        }
        
        /* Content styling */
        .stTitle h1 {
            color: #ECF39E !important;
            font-size: 24px !important;
            margin-bottom: 20px !important;
            padding-top: 20px !important;
        }
        
        .stMetricValue {
            color: #ECF39E !important;
        }
        
        .stMetricDelta {
            color: #4F772D !important;
        }
        
        .stMetricLabel {
            color: #ECF39E !important;
        }
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: #4F772D !important;
            color: #ECF39E !important;
            border-radius: 8px !important;
            padding: 8px 16px !important;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #31572C !important;
        }
        
        /* Warning styling */
        .stAlert {
            background-color: #4F772D !important;
            color: #ECF39E !important;
            border: none !important;
            border-radius: 12px !important;
        }
        
        /* Upload box styling */
        .upload-box {
            background-color: #31572C;
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
        }
        
        .stButton>button {
            width: 100%;
        }
        
        [data-testid="stFileUploader"] {
            background-color: #1f1f1f;
            border-radius: 10px;
            padding: 10px;
        }
        [data-testid="stFileUploader"] > div {
            padding: 0 !important;
        }
        [data-testid="stFileUploader"] [data-testid="stButton"] {
            width: 100% !important;
            margin: 0;
        }
        [data-testid="stFileUploader"] [data-testid="stButton"] button {
            width: 100%;
            height: auto;
            padding: 1rem;
            display: flex;
            flex-direction: column;
            align-items: center;
            background-color: #1f1f1f;
            border: 1px solid #31572C;
        }
        [data-testid="stFileUploader"] [data-testid="stMarkdownContainer"] {
            display: none;
        }
        .custom-upload-text {
            color: #ECF39E;
            text-align: center;
            margin: 5px 0;
        }
        .file-limit-text {
            color: #90A955;
            font-size: 0.8em;
            margin-top: 5px;
        }
        
        [data-testid="stAppViewContainer"] {
            overflow-x: hidden;
        }
        .upload-text {
            color: #ECF39E;
            font-size: 0.9em;
            margin-bottom: 10px;
            white-space: nowrap;
        }
        .browse-button {
            background-color: #31572C;
            color: #ECF39E;
            padding: 6px 12px;
            border-radius: 5px;
            display: inline-block;
            margin-bottom: 10px;
            font-size: 0.9em;
        }
        .file-limit {
            color: #90A955;
            font-size: 0.75em;
        }
        
        .streamlit-expanderContent {
            display: flex;
            justify-content: center;
            text-align: center;
        }
        
        /* File uploader styling */
        .stFileUploader {
            padding: 0 !important;
            margin: 0 !important;
            overflow: hidden !important;
            height: 140px !important;
            max-height: 140px !important;
        }

        .stFileUploader > div {
            padding: 0 !important;
            margin: 0 !important;
            height: 140px !important;
            max-height: 140px !important;
            overflow: hidden !important;
        }

        .stFileUploader [data-testid="stFileUploadDropzone"] {
            height: 140px !important;
            max-height: 140px !important;
            padding: 0 !important;
            margin: 0 !important;
            overflow: hidden !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
            align-items: center !important;
            gap: 10px !important;
            background-color: rgba(0, 0, 0, 0.2) !important;
            border-radius: 10px !important;
            border: none !important;
        }

        /* Cloud icon */
        [data-testid="stFileUploadDropzone"] img {
            width: 36px !important;
            height: 36px !important;
            margin: 0 !important;
            padding: 0 !important;
            opacity: 0.8 !important;
        }

        /* Text styling */
        [data-testid="stFileUploadDropzone"] > div > div {
            font-size: 0.9em !important;
            color: #90A955 !important;
            margin: 0 !important;
            padding: 0 !important;
            text-align: center !important;
        }

        /* Browse button */
        .browse-button {
            background-color: #31572C !important;
            color: #ECF39E !important;
            padding: 6px 12px !important;
            border-radius: 6px !important;
            font-size: 0.9em !important;
            margin: 0 !important;
            border: none !important;
            cursor: pointer !important;
        }

        /* File size limit text */
        .upload-text {
            color: #90A955 !important;
            font-size: 0.8em !important;
            margin: 0 !important;
            padding: 0 !important;
            opacity: 0.8 !important;
        }

        /* Remove any possible scroll containers */
        [data-testid="stFileUploadDropzone"] div {
            overflow: visible !important;
        }
        
        /* Custom file upload styling with camera icon */
        [data-testid="stFileUploadDropzone"] {
            width: 50px !important;
            height: 50px !important;
            padding: 0 !important;
            margin: 0 auto !important;
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
        }
        
        [data-testid="stFileUploadDropzone"] > div {
            width: 100% !important;
            height: 100% !important;
            padding: 0 !important;
            margin: 0 !important;
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
        }
        
        [data-testid="stFileUploadDropzone"] button {
            width: 50px !important;
            height: 50px !important;
            padding: 0 !important;
            margin: 0 !important;
            background-color: #31572C !important;
            border: none !important;
            border-radius: 10px !important;
            position: relative !important;
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            cursor: pointer !important;
        }
        
        [data-testid="stFileUploadDropzone"] button::before {
            content: '' !important;
            width: 30px !important;
            height: 30px !important;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 512 512'%3E%3Cpath fill='%23ECF39E' d='M149.1 64.8L138.7 96H64C28.7 96 0 124.7 0 160V416c0 35.3 28.7 64 64 64H448c35.3 0 64-28.7 64-64V160c0-35.3-28.7-64-64-64H373.3L362.9 64.8C356.4 45.2 338.1 32 317.4 32H194.6c-20.7 0-39 13.2-45.5 32.8zM256 192a96 96 0 1 1 0 192 96 96 0 1 1 0-192z'/%3E%3C/svg%3E");
            background-repeat: no-repeat !important;
            background-position: center !important;
            background-size: contain !important;
            display: block !important;
        }
        
        [data-testid="stFileUploadDropzone"] button:hover {
            background-color: #4a7c47 !important;
            transform: translateY(-1px) !important;
        }
        
        /* Hide the text and other elements */
        [data-testid="stFileUploadDropzone"] span,
        [data-testid="stFileUploadDropzone"] p,
        [data-testid="stFileUploadDropzone"] small {
            display: none !important;
        }
        
        /* General text container styling */
        .text-container {
            padding: 20px;
            margin: 10px 0;
            min-height: fit-content;
            height: auto;
            overflow: visible;
            word-wrap: break-word;
        }
        
        /* Benefits and Concerns sections */
        .benefits-section, .concerns-section {
            background-color: #1a472a;
            padding: 20px;
            border-radius: 10px;
            margin: 15px 0;
            min-height: 200px;
            height: auto;
        }
        
        /* Section headings */
        .section-heading {
            color: #ECF39E;
            font-size: 24px;
            margin-bottom: 15px;
            padding: 5px 0;
        }
        
        /* List items */
        .benefit-item, .concern-item {
            color: #ECF39E;
            font-size: 18px;
            margin: 10px 0;
            padding: 5px 0;
            line-height: 1.5;
        }
        
        /* Ensure text doesn't overflow */
        * {
            overflow-wrap: break-word;
            word-wrap: break-word;
            -ms-word-break: break-all;
            word-break: break-word;
        }
        
    </style>
""", unsafe_allow_html=True)


# Main content
st.markdown("<h1 style='color: #ECF39E;'> Mobile Prototype</h1>", unsafe_allow_html=True)

st.markdown("<p style='color: #ECF39E; margin-bottom: 20px; text-align: center;'>Upload photos of the two skincare products you plan to layer to check for interactions:</p>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div style='text-align: center; overflow: hidden;'>
            <div style='
                width: 60px;
                height: 60px;
                margin: 0 auto 8px;
                background-color: #31572C;
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 12px;
                overflow: hidden;
            '>
                <svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 512 512' style='width: 36px; height: 36px;'>
                    <path fill='#ECF39E' d='M149.1 64.8L138.7 96H64C28.7 96 0 124.7 0 160V416c0 35.3 28.7 64 64 64H448c35.3 0 64-28.7 64-64V160c0-35.3-28.7-64-64-64H373.3L362.9 64.8C356.4 45.2 338.1 32 317.4 32H194.6c-20.7 0-39 13.2-45.5 32.8zM256 192a96 96 0 1 1 0 192 96 96 0 1 1 0-192z'/>
                </svg>
            </div>
            <div style='color: #ECF39E; font-size: 1em; margin-bottom: 4px; overflow: hidden;'>Browse files</div>
            <div style='color: #90A955; font-size: 0.7em; overflow: hidden;'>This Button Is Fake!</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div style='text-align: center; overflow: hidden;'>
            <div style='
                width: 60px;
                height: 60px;
                margin: 0 auto 8px;
                background-color: #31572C;
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 12px;
                overflow: hidden;
            '>
                <svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 512 512' style='width: 36px; height: 36px;'>
                    <path fill='#ECF39E' d='M149.1 64.8L138.7 96H64C28.7 96 0 124.7 0 160V416c0 35.3 28.7 64 64 64H448c35.3 0 64-28.7 64-64V160c0-35.3-28.7-64-64-64H373.3L362.9 64.8C356.4 45.2 338.1 32 317.4 32H194.6c-20.7 0-39 13.2-45.5 32.8zM256 192a96 96 0 1 1 0 192 96 96 0 1 1 0-192z'/>
                </svg>
            </div>
            <div style='color: #ECF39E; font-size: 1em; margin-bottom: 4px; overflow: hidden;'>Browse files</div>
            <div style='color: #90A955; font-size: 0.7em; overflow: hidden;'>This Button is Fake!</div>
        </div>
    """, unsafe_allow_html=True)

# Add the demo text below both buttons
st.markdown("""
    <div style='
        text-align: center;
        color: #3172C;
        font-size: 0.9em;
        margin-top: 20px;
        margin-bottom: 20px;
    '>
        Click Analyze to Test the Demo
    </div>
""", unsafe_allow_html=True)

def generate_random_analysis():
    compatibility_levels = ["High", "Medium", "Low"]
    concerns = [
        "May increase skin sensitivity when layered",
        "Products may neutralize each other's effects",
        "Could cause irritation when used together",
        "pH levels may interfere with absorption",
        "Active ingredients may be too strong in combination",
        "May disrupt skin barrier when layered",
        "Potential for oxidation when mixed",
        "Risk of pilling when applied together"
    ]
    benefits = [
        "Complementary ingredients enhance absorption",
        "pH levels work well together",
        "Ingredients boost each other's effectiveness",
        "Good layering compatibility",
        "Synergistic hydration benefits",
        "Enhanced skin barrier support",
        "Active ingredients work well together",
        "Optimal absorption sequence"
    ]
    
    compatibility = random.choice(compatibility_levels)
    
    if compatibility == "High":
        num_concerns = random.randint(0, 1)
        num_benefits = random.randint(2, 3)
    elif compatibility == "Medium":
        num_concerns = random.randint(1, 2)
        num_benefits = random.randint(1, 2)
    else:  # Low
        num_concerns = random.randint(2, 3)
        num_benefits = random.randint(0, 1)
    
    result = {
        "compatibility": compatibility,
        "concerns": random.sample(concerns, k=num_concerns),
        "benefits": random.sample(benefits, k=num_benefits),
        "recommendation": get_layering_recommendation(compatibility)
    }
    return result

def get_layering_recommendation(compatibility):
    if compatibility == "High":
        return "✓ Safe to layer together. Apply thinnest product first."
    elif compatibility == "Medium":
        return "⚠️ Can be layered, but wait 5-10 minutes between applications."
    else:
        return "❌ Not recommended to use these products in the same routine."

def display_benefits_and_concerns(analysis):
    benefits = analysis["benefits"]
    concerns = analysis["concerns"] if analysis["concerns"] else ["No risks found"]
    
    benefits_html = """
        <div class="benefits-section text-container" style="flex: 1; background-color: #31572C; border-radius: 10px; padding: 15px;">
            <div class="section-heading" style="color: #ECF39E; font-size: 22px; text-align: center; margin-bottom: 10px;">Benefits</div>
            {}
        </div>
    """.format(''.join([f'<div class="benefit-item" style="color: #ECF39E; font-size: 16px; margin: 8px 0;">✓ {benefit}</div>' for benefit in benefits]))
    
    concerns_html = """
        <div class="concerns-section text-container" style="flex: 1; background-color: #31572C; border-radius: 10px; padding: 15px;">
            <div class="section-heading" style="color: #ECF39E; font-size: 22px; text-align: center; margin-bottom: 10px;">Risks</div>
            {}
        </div>
    """.format(''.join([f'<div class="concern-item" style="color: #ECF39E; font-size: 16px; margin: 8px 0; line-height: 1.3;">{("⚠️ " if concerns[0] != "No risks found" else "✓ ")}{concern}</div>' for concern in concerns]))
    
    return st.markdown(f"""
        <div style="display: flex; gap: 15px; justify-content: space-between; margin: 15px 0; background-color: #132A13; padding: 15px; border-radius: 15px;">
            {benefits_html}
            {concerns_html}
        </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='border: 1px solid #31572C; margin: 30px 0;'>", unsafe_allow_html=True)

if st.button("Analyze", type="primary"):
    analysis = generate_random_analysis()
    
    # Display compatibility level with color coding
    color_map = {
        "High": "#4CAF50",
        "Medium": "#FFA726",
        "Low": "#EF5350"
    }
    st.markdown(f"""
        <div style='text-align: center; margin: 20px 0;'>
            <h2 style='color: #ECF39E;'>Compatibility Analysis</h2>
            <div style='
                color: {color_map[analysis["compatibility"]]};
                font-size: 1.5em;
                margin: 10px 0;
                font-weight: bold;
            '>
                {analysis["compatibility"]} Compatibility
            </div>
            <div style='
                color: #ECF39E;
                margin: 15px 0;
                padding: 10px;
                background-color: #31572C;
                border-radius: 5px;
                font-size: 0.95em;
            '>
                {analysis["recommendation"]}
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Display benefits and concerns in columns
    display_benefits_and_concerns(analysis)
    
    # Add Save and Share buttons
    st.markdown("<div style='text-align: center; margin-top: 20px;'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.button("💾 Save Analysis")
    with col2:
        st.button("📤 Share Results")
    st.markdown("</div>", unsafe_allow_html=True)

# Add disclaimer as an expander
with st.expander("⚠️ Demo Disclaimer"):
    st.markdown("""
        <div style='
            width: 100%;
            max-width: 600px;
            margin: 0 auto;
            text-align: center;
            padding: 20px;
            font-size: 0.9em;
            color: #ECF39E;
        '>
            This is a prototype to demonstrate potential functionality. The compatibility analysis shown here is randomly generated 
            and does not reflect actual product interactions. A real implementation would require comprehensive dermatological data, 
            clinical research, and expert validation from dermatologists to provide accurate recommendations.
        </div>
    """, unsafe_allow_html=True)

# Info box
try:
    image_path = 'Image/OnePager.jpeg'
    if not os.path.exists(image_path):
        st.error(f"Image file not found at: {image_path}")
    else:
        import base64
        
        def get_image_base64(image_path):
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
                
        img_base64 = get_image_base64(image_path)
        st.markdown(f"""
            <div class='info-box'>
                <img src="data:image/jpeg;base64,{img_base64}" 
                     style="max-width: 100%; max-height: 100%; object-fit: contain;">
            </div>
        """, unsafe_allow_html=True)
except Exception as e:
    st.error(f"Error loading image: {e}")

# Simulated ingredient extraction
def extract_ingredients(product_name):
    fake_ingredients = {
        'cerave_moisturizer': ['ceramides', 'hyaluronic acid', 'glycerin'],
        'ordinary_retinol': ['retinol', 'squalane', 'jojoba oil'],
        'neutrogena_cleanser': ['salicylic acid', 'benzoyl peroxide', 'glycerin'],
        'la_roche_posay': ['niacinamide', 'glycerin', 'zinc'],
    }
    return fake_ingredients.get(product_name, ['ingredient1', 'ingredient2', 'ingredient3'])

def analyze_ingredients(ingredients_list):
    # Simulate ingredient analysis
    common_interactions = {
        'retinol': {
            'compatibility': {
                'hyaluronic acid': 'Safe',
                'vitamin c': 'Caution',
                'benzoyl peroxide': 'Avoid',
                'dapsone': 'Caution'
            },
            'description': 'A powerful anti-aging ingredient that can increase skin sensitivity.',
            'cautions': 'Use at night, avoid combining with acids and oxidizing agents.'
        },
        'dapsone': {
            'compatibility': {
                'benzoyl peroxide': 'Avoid',
                'retinol': 'Caution',
                'niacinamide': 'Safe'
            },
            'description': 'Topical antibiotic used for acne treatment.',
            'cautions': 'May cause temporary orange discoloration when combined with benzoyl peroxide.'
        }
    }
    
    results = []
    warnings = []
    
    for i, ingredient1 in enumerate(ingredients_list):
        ingredient1 = ingredient1.lower().strip()
        if ingredient1 in common_interactions:
            # Add ingredient info
            results.append({
                'ingredient': ingredient1,
                'description': common_interactions[ingredient1]['description'],
                'cautions': common_interactions[ingredient1]['cautions']
            })
            
            # Check interactions
            for ingredient2 in ingredients_list[i+1:]:
                ingredient2 = ingredient2.lower().strip()
                if ingredient2 in common_interactions[ingredient1].get('compatibility', {}):
                    compatibility = common_interactions[ingredient1]['compatibility'][ingredient2]
                    if compatibility != 'Safe':
                        warnings.append(f"⚠️ {ingredient1.title()} + {ingredient2.title()}: {compatibility}")
    
    return results, warnings
