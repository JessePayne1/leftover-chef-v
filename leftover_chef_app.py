import streamlit as st
from openai import OpenAI
import base64

st.set_page_config(page_title="LeftoverChef", layout="wide", page_icon="🍳")

st.title("🍳 LeftoverChef: ANY Combo → Real Meals!")
st.markdown("**Premium unlocks fridge photo + 5-min & microwave recipes** — free tier still works great!")

# Sidebar
with st.sidebar:
    api_key = st.text_input("OpenAI API Key", type="password", value=st.session_state.get("api_key", ""))
    if api_key:
        st.session_state.api_key = api_key
    st.caption("Your $10 credits are ready — premium features coming soon!")

premium = st.checkbox("🔓 Premium Mode (unlocks fridge photo + 5-min & microwave recipes)", value=False)

client = OpenAI(api_key=st.session_state.get("api_key", ""))

# Photo upload (Premium only for full power, but free tier can still try)
uploaded_file = None
if premium:
    uploaded_file = st.file_uploader("📸 Snap a fridge photo (Premium feature)", type=["jpg", "jpeg", "png"])

ingredients_input = st.text_input("Or type ingredients (works in free tier too):", 
                                 placeholder="steak, yogurt, rice, eggs, chili, green pepper")

if st.button("Generate Recipes") and (ingredients_input or uploaded_file):
    with st.spinner("AI is cooking recipes that use almost everything..."):
        # Handle photo → detect ingredients
        detected = ""
        if uploaded_file and premium:
            bytes_data = uploaded_file.getvalue()
            base64_image = base64.b64encode(bytes_data).decode()
            vision_response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "List every visible food item in this fridge photo as a comma-separated list. Be specific (e.g., chicken drumstick, leftover rice, yogurt cup, green pepper)."},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ]
                }]
            )
            detected = vision_response.choices[0].message.content + ", "
        
        full_ingredients = detected + (ingredients_input or "")
        
        # Smart prompt with 5-min/microwave for premium
        extra = "Prioritize 5-minute meals and microwave-only versions when possible." if premium else ""
        prompt = f"""Create 2-3 practical zero-waste recipes using as many of these ingredients as possible: {full_ingredients}.
        You may add common staples (oil, salt, garlic, onion, flour, sugar, milk, spices).
        {extra}
        Separate sweet and savory clearly.
        For each recipe include:
        - Title
        - Ingredients it uses
        - Simple step-by-step (10-20 min or less)
        - Microwave version if possible"""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        
        st.subheader("🥇 Your AI Recipes (using most/all ingredients)")
        st.markdown(response.choices[0].message.content)

        if premium:
            st.success("✅ Premium features active! Photo detected + 5-min/microwave prioritized.")

st.caption("Free tier: text only. Premium: fridge photo + quick meals. Ready for real Stripe subscription?")
