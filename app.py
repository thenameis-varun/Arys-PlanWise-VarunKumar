# app.py

import streamlit as st  # ✅ Must be first
st.set_page_config(
    page_title="PlanWise - Smart Event Planner",
    page_icon="🎪",
    layout="wide",
    initial_sidebar_state="expanded"
)

import requests
import random
from datetime import datetime
import pandas as pd
import numpy as np

# -------------------------------
# Hugging Face API setup
# -------------------------------
HF_API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-small"
HF_API_TOKEN = "<YOUR_HUGGING_FACE_API_TOKEN>"  # <-- Put your token here

headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}

def hf_generate(prompt, max_tokens=200):
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": max_tokens}}
    response = requests.post(HF_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        output = response.json()
        if isinstance(output, list) and "generated_text" in output[0]:
            return output[0]["generated_text"]
    return "AI could not generate structured response."

# -------------------------------
# Styling
# -------------------------------
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

# -------------------------------
# App UI
# -------------------------------
st.title("🎪 PlanWise - Smart Event Planner")
st.subheader("AI-powered interactive event management system")

# -------------------------------
# Step 1: User Inputs
# -------------------------------
st.markdown("### Step 1: Enter Event Details")

event_type = st.selectbox(
    "Event Type", 
    ["Conference", "Concert", "Festival", "Networking Event", "Exhibition", "Workshop"]
)
duration = st.number_input("Duration (hours)", min_value=1, max_value=24, step=1)
budget = st.number_input("Budget (₹)", min_value=1000, step=500)
catering = st.selectbox("Catering Required?", ["Yes", "No"])

# -------------------------------
# AI1 Response Function using HF API
# -------------------------------
def ai1_response(event_type, duration, budget, catering):
    prompt = f"""
You are an event planning assistant.

The user has shared:
- Event Type: {event_type}
- Duration: {duration} hours
- Budget: ₹{budget}
- Catering: {catering}

Your tasks:
1. Greet the user.
2. Summarize their input values.
3. Compliment their idea and wish them luck.
4. Predict:
   - Audience Type (choose one: Mixed, Families, Public, Professionals, Students)
   - Tech Requirement (choose one: Low, Medium, High)

Format response exactly like this:
---
Greeting: <your greeting>
Summary: <your summary>
Compliment: <your compliment>
Audience Type: <one of allowed values>
Tech Requirement: <one of allowed values>
---
"""
    output = hf_generate(prompt, max_tokens=200)

    # Extract structured block
    if output.count("---") >= 2:
        structured = output.split("---")[1].strip()
    else:
        structured = output.strip()

    audience = "Mixed"
    tech = "Medium"

    for line in structured.splitlines():
        if line.startswith("Audience Type:"):
            audience = line.split(":", 1)[1].strip()
        if line.startswith("Tech Requirement:"):
            tech = line.split(":", 1)[1].strip()

    return structured, audience, tech

# -------------------------------
# Step 2: Process Submission
# -------------------------------
if st.button("Submit Event"):
    message, pred_audience, pred_tech = ai1_response(event_type, duration, budget, catering)
    st.success(message)
    
    # Autofilled dropdowns
    st.markdown("### Step 2: Confirm AI Suggestions")
    audience_type = st.selectbox(
        "Audience Type", 
        ["Mixed", "Families", "Public", "Professionals", "Students"],
        index=["Mixed", "Families", "Public", "Professionals", "Students"].index(pred_audience)
    )
    tech_requirement = st.selectbox(
        "Tech Requirement", 
        ["Low", "Medium", "High"],
        index=["Low", "Medium", "High"].index(pred_tech)
    )
    
    # -------------------------------
    # Step 3: AI2 - Budget Prediction (placeholder)
    # -------------------------------
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
    # Step 4: Event Success Confidence
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
    
    # Optional: Visual bar with user budget
    st.markdown(f"Predicted Budget Range: ₹{int(0.95*predicted_budget)} - ₹{int(1.05*predicted_budget)}")
    st.markdown(f"Your Budget: ₹{budget}")

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.markdown("PlanWise © 2025 | Powered by AI and Streamlit | AI1: Hugging Face Flan-T5-Small API")
