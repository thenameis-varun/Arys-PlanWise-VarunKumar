# app.py
import streamlit as st
import random
from datetime import datetime
import pandas as pd
import numpy as np

# -------------------------------
# Page config and style
# -------------------------------
st.set_page_config(page_title="PlanWise - Smart Event Planner",
                   page_icon="🎪",
                   layout="wide",
                   initial_sidebar_state="expanded")

st.markdown("""
<style>
    .stButton>button {
        background-color: #4CAF50;
        color:white;
        font-size:16px;
        padding:10px 24px;
        border-radius:8px;
    }
    .stProgress>div>div>div>div {
        background-color:#4CAF50;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎪 PlanWise - Smart Event Planner")
st.subheader("AI-powered interactive event management system")

st.markdown("### Step 1: Enter Event Details")

event_type = st.selectbox("Event Type", ["Conference", "Concert", "Festival", "Networking Event", "Exhibition", "Workshop"])

duration = st.number_input("Duration (hours)", min_value=1, max_value=24, step=1)

budget = st.number_input("Budget (₹)", min_value=1000, step=500)

catering = st.selectbox("Catering Required?", ["Yes", "No"])


# -------------------------------
# Step 2: AI1 - LLM Summary & Suggestions
# -------------------------------
def ai1_response(event_type, duration, budget, catering):
    audience_options = ["Mixed", "Families", "Public", "Professionals", "Students"]
    tech_options = ["Low", "Medium", "High"]
    
    # Random prediction (placeholder for real LLM call)
    predicted_audience = random.choice(audience_options)
    predicted_tech = random.choice(tech_options)
    
    # Build summary message
    message = f"""
    👋 Hello! Thank you for sharing your event idea.  

    You are planning a **{event_type}** lasting **{duration} hours**,  
    with a budget of **₹{budget}**, and catering = **{catering}**.  

    💡 Your idea sounds amazing! Wishing you great success!  

    Based on your event, I suggest:
    - **Audience Type**: {predicted_audience}  
    - **Tech Requirement**: {predicted_tech}
    """
    
    return message, predicted_audience, predicted_tech

if st.button("Submit Event"):
    message, pred_audience, pred_tech = ai1_response(event_type, duration, budget, catering)
    st.success(message)
    
    # Autofilled dropdowns (editable)
    st.markdown("### Step 2: Confirm AI Suggestions")
    audience_type = st.selectbox("Audience Type", ["Mixed", "Families", "Public", "Professionals", "Students"],
                                 index=["Mixed", "Families", "Public", "Professionals", "Students"].index(pred_audience))
    tech_requirement = st.selectbox("Tech Requirement", ["Low", "Medium", "High"],
                                    index=["Low", "Medium", "High"].index(pred_tech))
    
    # -------------------------------
    # Step 3: AI2 - Budget Prediction
    # -------------------------------
    # Placeholder regression (replace with real ML model trained on your 170-row dataset)
    def ai2_predict_budget(event_type, duration, catering):
        base_budget = {
            "Conference": 100000,
            "Concert": 200000,
            "Festival": 300000,
            "Networking Event": 50000,
            "Exhibition": 150000,
            "Workshop": 40000,
        }
        b = base_budget.get(event_type, 50000)
        if catering == "Yes":
            b += 20000
        b += duration * 1000
        return b
    
    predicted_budget = ai2_predict_budget(event_type, duration, catering)
    st.info(f"💡 Predicted Budget: ₹{predicted_budget}")
    
    # -------------------------------
    # Step 4: Event Success Confidence Bar
    # -------------------------------
    def calculate_confidence(user_budget, predicted_budget):
        lower = 0.95 * predicted_budget
        upper = 1.05 * predicted_budget
        if user_budget <= lower:
            return 0
        elif user_budget >= upper:
            return 100
        else:
            return int(((user_budget - lower) / (upper - lower)) * 100)
    
    confidence = calculate_confidence(budget, predicted_budget)
    
    st.markdown("### Step 3: Event Success Confidence")
    st.progress(confidence / 100)
    st.write(f"**Confidence Score:** {confidence}%")
    
    # Optional: Visual bar with user budget marked
    st.markdown(f"Predicted Budget Range: ₹{int(0.95*predicted_budget)} - ₹{int(1.05*predicted_budget)}")
    st.markdown(f"Your Budget: ₹{budget}")

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.markdown("PlanWise © 2025 | Powered by AI and Streamlit")
