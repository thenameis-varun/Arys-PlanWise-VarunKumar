# app.py
import streamlit as st
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# -------------------------------
# Page config
# -------------------------------
st.set_page_config(
    page_title="PlanWise - Smart Event Planner",
    page_icon="🎪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# Load LLM for AI1
# -------------------------------
@st.cache_resource
def load_llm():
    tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
    model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")
    return tokenizer, model

tokenizer, model = load_llm()

# -------------------------------
# AI1 Function (Greeting + Summary + Audience & Tech prediction)
# -------------------------------
@st.cache_data
def ai1_generate(event_type, duration, budget, catering):
    # Hardcoded Greeting, Summary, Compliment
    greeting = f"Hello! You are planning a {event_type}."
    summary = f"This event will last {duration} hours with a budget of {budget}. Catering: {catering}."
    compliment = f"Great choice! Your {event_type} sounds exciting and well thought out."

    # LLM prompt for Audience Type & Tech Requirement
    prompt = f"""
You are an expert event planner. Based on these event details:
- Type: {event_type}
- Duration: {duration} hours
- Budget: {budget}
- Catering: {catering}

Choose the most suitable Audience Type (Mixed/Families/Public/Professionals/Students)
and Tech Requirement (Low/Medium/High). Respond ONLY in this EXACT format:
Audience Type: <choice>
Tech Requirement: <choice>
"""
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        **inputs,
        max_new_tokens=60,
        do_sample=True,
        temperature=0.7
    )
    output_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Defaults
    audience = "Mixed"
    tech = "Medium"

    for line in output_text.splitlines():
        if line.lower().startswith("audience type:"):
            audience = line.split(":", 1)[1].strip()
        if line.lower().startswith("tech requirement:"):
            tech = line.split(":", 1)[1].strip()

    return greeting, summary, compliment, audience, tech

# -------------------------------
# AI2 Function 
# -------------------------------
def ai2_predict_budget(user_budget):
    return int(user_budget * 0.1)

# -------------------------------
# UI - Step 1: Event Inputs
# -------------------------------
st.title("🎪 PlanWise - Smart Event Planner")
st.markdown("#### Step 1: Provide basic event details")

with st.form("event_inputs"):
    col1, col2 = st.columns(2)
    with col1:
        event_type = st.selectbox("Event Type", ["Conference", "Concert", "Festival", "Networking Event", "Exhibition", "Workshop"])
        duration = st.number_input("Duration (hours)", min_value=1, max_value=24, step=1)
    with col2:
        budget = st.number_input("Budget", min_value=1000, step=500)
        catering = st.selectbox("Catering Required?", ["Yes", "No"])
    submitted = st.form_submit_button("Generate AI Plan")

if submitted:
    # -------------------------------
    # AI1 Output
    # -------------------------------
    greeting, summary, compliment, pred_audience, pred_tech = ai1_generate(event_type, duration, budget, catering)

    st.markdown("### AI Plan (Step 2)")
    st.info(f"**{greeting}**\n\n{summary}\n\n{compliment}")

    # Autofill dropdowns for Audience Type & Tech Requirement
    st.markdown("#### Confirm AI Suggestions")
    audience_type = st.selectbox(
        "Audience Type",
        ["Mixed", "Families", "Public", "Professionals", "Students"],
        index=["Mixed", "Families", "Public", "Professionals", "Students"].index(pred_audience)
    )
    tech_requirements = st.selectbox(
        "Tech Requirement",
        ["Low", "Medium", "High"],
        index=["Low", "Medium", "High"].index(pred_tech)
    )

    # -------------------------------
    # AI2 Budget Prediction
    # -------------------------------
    predicted_budget = ai2_predict_budget(budget)
    st.markdown(f"#### AI Predicted Budget: **{predicted_budget}**")

    # -------------------------------
    # Event Success Confidence Bar
    # -------------------------------
    st.markdown("#### Event Success Confidence")
    min_budget = predicted_budget * 0.95
    max_budget = predicted_budget * 1.05
    user_budget = budget

    if user_budget <= min_budget:
        confidence = 0
    elif user_budget >= max_budget:
        confidence = 100
    else:
        confidence = int(((user_budget - min_budget) / (max_budget - min_budget)) * 100)

    st.progress(confidence)
    st.markdown(f"**User Budget: {user_budget} → Event Success Confidence: {confidence}%**")

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.markdown("PlanWise © 2025 | Powered by Local AI and Streamlit")

