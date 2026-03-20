import streamlit as st
from openai import OpenAI
import base64

st.set_page_config(page_title="LeftoverChef", layout="wide", page_icon="🍳")

# === CLEAN CUSTOM STYLING (no more raw code showing) ===
st.html("""
<style>
    .stButton>button {
        background-color: #4CAF50 !important;
        color: white !important;
        font-size: 18px !important;
        padding: 12px 24px !important;
        border-radius: 8px !important;
    }
    .stButton>button:hover {
        background-color: #388E3C !important;
    }
    h1 { font-size: 2.8rem !important; font-weight: 700 !important; }
    h2 { font-size: 2.2rem !important; font-weight: 600 !important; }
    .stMarkdown h3 { font-size: 1.8rem !important; }
</style>
""")

st.title("🍳 LeftoverChef: ANY Combo → Real Meals!")
st.markdown("**AI-powered + Premium unlocks fridge photo + 5-min & microwave recipes**")

# Sidebar
with st.sidebar:
    api_key = st.text_input("OpenAI API Key", type="password", value=st.session_state.get("api_key", ""))
    if api_key:
        st.session_state.api_key = api_key
    st.caption("Your $10 credits are ready!")

premium = st.checkbox("🔓 Premium Mode (fridge photo + 5-min & microwave recipes)", value=False)

client = OpenAI(api_key=st.session_state.get("api_key", ""))

uploaded_file = None
if premium:
    uploaded_file = st.file_uploader("📸 Snap a fridge photo (Premium)", type=["jpg", "jpeg", "png"])

ingredients_input = st.text_input("Or type ingredients:", 
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
        prompt = f"""Create 2-3 zero-waste recipes using as many of these as possible: {full_ingredients}.
        Add common staples if needed. {extra}
        Separate sweet/savory. For each: Title, ingredients used, step-by-step."""

        response = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
        recipes_text = response.choices[0].message.content
        
        st.subheader("🥇 Your AI Recipes")
        st.markdown(recipes_text)

        st.subheader("📸 Recipe Inspiration Photos")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.image("https://picsum.photos/id/1015/400/300", use_column_width=True, caption="Fresh & ready")
        with col2:
            st.image("https://picsum.photos/id/292/400/300", use_column_width=True, caption="Quick microwave style")
        with col3:
            st.image("https://picsum.photos/id/431/400/300", use_column_width=True, caption="Zero-waste bowl")

        if premium:
            st.success("✅ Premium active — photo detected + 5-min/microwave prioritized!")

st.caption("Free tier works great. Premium = fridge photo + quick meals. Ready for Stripe subscription button?")
