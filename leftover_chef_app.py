import streamlit as st
from openai import OpenAI
import base64

st.set_page_config(page_title="LeftoverChef", layout="wide", page_icon="🍳")

# === CLEAN STYLING (turquoise-gray button + peach titles) ===
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
    h1 { font-size: 2.8rem !important; font-weight: 700 !important; }
    h2 { font-size: 2.2rem !important; font-weight: 600 !important; }
</style>
""")

st.title("🍳 LeftoverChef")
st.markdown("**Turn any leftovers into real meals** — AI finds smart combos using almost everything.")

# Sidebar
with st.sidebar:
    api_key = st.text_input("OpenAI API Key", type="password", value=st.session_state.get("api_key", ""))
    if api_key:
        st.session_state.api_key = api_key
    st.caption("Your credits are ready!")

premium = st.checkbox("🔓 Premium Mode — unlocks fridge photo + 5-min & microwave recipes", value=False)

client = OpenAI(api_key=st.session_state.get("api_key", ""))

uploaded_file = None
if premium:
    uploaded_file = st.file_uploader("📸 Snap a photo of your fridge (Premium)", type=["jpg", "jpeg", "png"])

ingredients_input = st.text_input("Or type your ingredients:", 
                                 placeholder="steak, yogurt, rice, eggs, chili, green pepper")

if st.button("Generate Recipes", type="primary") and (ingredients_input or uploaded_file):
    with st.spinner("AI is creating recipes that use almost everything..."):
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
        
        extra = "Prioritize 5-minute meals and microwave-only versions." if premium else ""
        prompt = f"""Create 2-3 practical zero-waste recipes using as many of these ingredients as possible: {full_ingredients}.
        Add common staples (oil, salt, garlic, etc.) if needed. {extra}
        Separate sweet and savory clearly.
        Format EXACTLY like this (use HTML for styling):

        <h3 style="color: #FFCC99;">Recipe Title Here</h3>
        <strong style="font-size: 1.4rem;">Ingredients used:</strong>
        - list them here

        <strong style="font-size: 1.4rem;">Step-by-step instructions:</strong>
        1. First step...
        2. Second step...
        3. etc."""

        response = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
        recipes_text = response.choices[0].message.content
        
        st.subheader("🥇 Your AI Recipes")
        st.markdown(recipes_text, unsafe_allow_html=True)

        if premium:
            st.success("✅ Premium active — fridge photo detected + quick versions prioritized!")

st.caption("Free tier works great. Premium = fridge photo + 5-min/microwave recipes. Ready for the $4.99/month subscription button?")
