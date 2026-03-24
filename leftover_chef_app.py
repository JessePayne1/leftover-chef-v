import streamlit as st
from openai import OpenAI
import base64
import json

st.set_page_config(page_title="LeftoverChef", layout="wide", page_icon="🍳")

# === STYLING ===
st.html("""
<style>
    .stButton>button { background-color: #48D1CC !important; color: white !important; font-size: 18px !important; padding: 14px 28px !important; border-radius: 10px !important; }
    .stButton>button:hover { background-color: #20B2AA !important; }
    body, .stApp { background-color: #0A1F3D !important; color: white !important; }
    .chef-hat { font-size: 42px; transform: rotate(15deg); margin-left: 6px; }
    .recipe-card { background-color: #112B4D; padding: 20px; border-radius: 12px; margin-bottom: 20px; border: 2px solid #FFCC99; }
</style>
""")

# === TITLE ===
st.html("""
<h1 style="font-size: 3.5rem; margin-bottom: 8px; text-align: center; position: relative;">
  <span style="position: absolute; left: -45px; font-size: 5.5rem; top: -12px; opacity: 0.95;">🍳</span>
  <span style="text-decoration: underline; text-decoration-color: #FFCC99; text-decoration-thickness: 3px; text-underline-offset: 12px; color: white;">LeftoverChef</span>
</h1>
""")

st.markdown("**Turn any leftovers into real meals** — AI finds smart combos using almost everything.")

# Sidebar
with st.sidebar:
    api_key = st.text_input("OpenAI API Key", type="password", value=st.session_state.get("api_key", ""))
    if api_key: st.session_state.api_key = api_key
    st.caption("Your credits are ready!")

premium = st.checkbox("🔓 Premium Mode — unlocks fridge photo + 5-min & microwave BONUS versions + Saveable Recipe Cards", value=False)

client = OpenAI(api_key=st.session_state.get("api_key", ""))

if "saved_recipes" not in st.session_state:
    st.session_state.saved_recipes = []

uploaded_file = None
if premium:
    uploaded_file = st.file_uploader("📸 Snap a photo of your fridge (Premium)", type=["jpg", "jpeg", "png"])

ingredients_input = st.text_input("Or type your ingredients:", 
                                 placeholder="steak, yogurt, rice, eggs, chili, green pepper")

# === GENERATE BUTTON + CHEF'S HAT ===
col1, col2 = st.columns([5, 0.6])
with col1:
    generate_clicked = st.button("Generate Recipes", type="primary")
with col2:
    st.markdown('<span class="chef-hat">👨‍🍳</span>', unsafe_allow_html=True)

if generate_clicked and (ingredients_input or uploaded_file):
    with st.spinner("AI is creating recipes..."):
        detected = ""
        if uploaded_file and premium:
            bytes_data = uploaded_file.getvalue()
            base64_image = base64.b64encode(bytes_data).decode()
            vision_response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": [{"type": "text", "text": "List every visible food item as a comma-separated list."}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}]}]
            )
            detected = vision_response.choices[0].message.content + ", "
        
        full_ingredients = detected + (ingredients_input or "")

        # Regular recipes
        prompt = f"""Create 2-3 practical zero-waste recipes using as many of these ingredients as possible: {full_ingredients}.
        Add common staples (oil, salt, garlic, etc.) if needed. Separate sweet and savory.
        Return ONLY a valid JSON array like this:
        [
          {{"title": "Recipe Title 1", "ingredients": "item1, item2, item3", "steps": "1. First step...\\n2. Second step...\\n3. etc."}},
          {{"title": "Recipe Title 2", "ingredients": "item1, item2", "steps": "1. First step...\\n2. Second step..."}},
          {{"title": "Recipe Title 3", "ingredients": "item1, item2", "steps": "1. First step...\\n2. Second step..."}}
        ]"""

        response = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
        try:
            recipes_list = json.loads(response.choices[0].message.content)
        except:
            recipes_list = []

        st.subheader("🥇 Your Regular Recipes")
        for i, rec in enumerate(recipes_list):
            with st.container():
                st.markdown(f'<div class="recipe-card"><h3 style="color: #FFCC99;">{rec.get("title", "Recipe")}</h3><strong style="font-size: 1.4rem;">Ingredients used:</strong><br>– {rec.get("ingredients", "").replace(", ", ", – ")}<br><br><strong style="font-size: 1.4rem;">Step-by-step instructions:</strong><br>{rec.get("steps", "")}</div>', unsafe_allow_html=True)
                if premium and st.button("💾 Save to Favorites", key=f"save_reg_{i}"):
                    st.session_state.saved_recipes.append(rec)
                    st.success("Saved to Favorites!")

        # Premium bonus - now identical format
        if premium:
            extra_prompt = f"""For the same ingredients ({full_ingredients}), create quick 5-minute or microwave-only versions. Return ONLY the same JSON array format."""
            quick_response = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": extra_prompt}])
            try:
                quick_list = json.loads(quick_response.choices[0].message.content)
            except:
                quick_list = []
            
            st.subheader("⚡ Premium Bonus: 5-Min & Microwave Versions")
            for i, rec in enumerate(quick_list):
                with st.container():
                    st.markdown(f'<div class="recipe-card"><h3 style="color: #FFCC99;">{rec.get("title", "Quick Version")}</h3><strong style="font-size: 1.4rem;">Ingredients used:</strong><br>– {rec.get("ingredients", "").replace(", ", ", – ")}<br><br><strong style="font-size: 1.4rem;">Step-by-step instructions:</strong><br>{rec.get("steps", "")}</div>', unsafe_allow_html=True)
                    if st.button("💾 Save to Favorites", key=f"save_quick_{i}"):
                        st.session_state.saved_recipes.append(rec)
                        st.success("Saved to Favorites!")

# === MY FAVORITES ===
if premium and st.session_state.saved_recipes:
    st.subheader("❤️ My Saved Recipe Cards")
    for rec in st.session_state.saved_recipes:
        st.markdown(f'<div class="recipe-card"><h3 style="color: #FFCC99;">{rec.get("title", "Saved Recipe")}</h3><strong style="font-size: 1.4rem;">Ingredients used:</strong><br>– {rec.get("ingredients", "").replace(", ", ", – ")}<br><br><strong style="font-size: 1.4rem;">Step-by-step instructions:</strong><br>{rec.get("steps", "")}</div>', unsafe_allow_html=True)

st.caption("Free tier = regular recipes. Premium = fridge photo + quick versions + saveable recipe cards. Ready for the $4.99/month subscription button?")
