import streamlit as st
from openai import OpenAI
import base64

st.set_page_config(page_title="LeftoverChef", layout="wide", page_icon="🍳")

# === CLEAN STYLING (midnight blue + turquoise button + peach titles) ===
st.html("""
<style>
    .stButton>button {
        background-color: #48D1CC !important;
        color: white !important;
        font-size: 18px !important;
        padding: 14px 28px !important;
        border-radius: 10px !important;
    }
    .stButton>button:hover {
        background-color: #20B2AA !important;
    }
    body, .stApp {
        background-color: #0A1F3D !important;
        color: white !important;
    }
</style>
""")

# === BIGGER EMOJI + UNDERLINED TITLE (looks great on phone) ===
st.html("""
<h1 style="font-size: 3.8rem; margin-bottom: 10px; text-align: center;">
  🍳 <span style="text-decoration: underline; text-decoration-color: #FFCC99; text-decoration-thickness: 4px; color: white;">LeftoverChef</span>
</h1>
""")

st.markdown("**Turn any leftovers into real meals** — AI finds smart combos using almost everything.")

# Sidebar
with st.sidebar:
    api_key = st.text_input("OpenAI API Key", type="password", value=st.session_state.get("api_key", ""))
    if api_key:
        st.session_state.api_key = api_key
    st.caption("Your credits are ready!")

premium = st.checkbox("🔓 Premium Mode — unlocks fridge photo + 5-min & microwave BONUS versions", value=False)

client = OpenAI(api_key=st.session_state.get("api_key", ""))

uploaded_file = None
if premium:
    uploaded_file = st.file_uploader("📸 Snap a photo of your fridge (Premium)", type=["jpg", "jpeg", "png"])

ingredients_input = st.text_input("Or type your ingredients:", 
                                 placeholder="steak, yogurt, rice, eggs, chili, green pepper")

if st.button("Generate Recipes", type="primary") and (ingredients_input or uploaded_file):
    with st.spinner("AI is creating recipes..."):
        detected = ""
        if uploaded_file and premium:
            bytes_data = uploaded_file.getvalue()
            base64_image = base64.b64encode(bytes_data).decode()
            vision_response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "List every visible food item as a comma-separated list."},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ]
                }]
            )
            detected = vision_response.choices[0].message.content + ", "
        
        full_ingredients = detected + (ingredients_input or "")
        
        # Regular recipes
        prompt = f"""Create 2-3 practical zero-waste recipes using as many of these ingredients as possible: {full_ingredients}.
        Add common staples (oil, salt, garlic, etc.) if needed.
        Separate sweet and savory clearly.
        Format EXACTLY like this:

        <h3 style="color: #FFCC99;">Recipe Title Here</h3>
        <strong style="font-size: 1.4rem;">Ingredients used:</strong>
        - list them here

        <strong style="font-size: 1.4rem;">Step-by-step instructions:</strong>
        1. First step...
        2. Second step...
        3. etc."""

        response = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
        recipes_text = response.choices[0].message.content
        
        st.subheader("🥇 Your Regular Recipes")
        st.markdown(recipes_text, unsafe_allow_html=True)

        # Premium bonus (clean lists)
        if premium:
            extra_prompt = f"""For the same ingredients ({full_ingredients}), create quick 5-minute or microwave-only versions.
            Format EXACTLY like this (step-by-step on its own line):

            <h3 style="color: #FFCC99;">Quick 5-Min / Microwave Version: Recipe Title</h3>
            <strong style="font-size: 1.4rem;">Ingredients used:</strong>
            - list them here

            <strong style="font-size: 1.4rem;">Step-by-step instructions:</strong>
            1. First step...
            2. Second step...
            3. etc."""

            quick_response = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": extra_prompt}])
            quick_text = quick_response.choices[0].message.content
            
            st.subheader("⚡ Premium Bonus: 5-Min & Microwave Versions")
            st.markdown(quick_text, unsafe_allow_html=True)
            
            st.success("✅ Premium active — fridge photo + quick versions unlocked!")

st.caption("Free tier = regular recipes. Premium = fridge photo + 5-min/microwave bonus add-ons. Ready for the $4.99/month subscription button?")
