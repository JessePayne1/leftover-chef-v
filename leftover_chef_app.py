import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="LeftoverChef", layout="wide", page_icon="🍳")

st.title("🍳 LeftoverChef")
st.markdown("**Turn any leftovers into real meals** — AI finds smart combos using almost everything.")

with st.sidebar:
    api_key = st.text_input("OpenAI API Key", type="password", value=st.session_state.get("api_key", ""))
    if api_key:
        st.session_state.api_key = api_key
    st.caption("Your credits are ready!")

premium = st.checkbox("🔓 Premium Mode (fridge photo + 5-min recipes)", value=False)

if not st.session_state.get("api_key"):
    st.warning("Please enter your OpenAI API key in the sidebar to generate recipes.")
    st.stop()

client = OpenAI(api_key=st.session_state.get("api_key"))

ingredients = st.text_input("Enter your ingredients:", placeholder="steak, yogurt, rice, eggs, chili, green pepper")

if st.button("Generate Recipes"):
    with st.spinner("AI is creating recipes..."):
        prompt = f"""Create 2-3 practical zero-waste recipes using as many of these ingredients as possible: {ingredients}.
        Add common staples (oil, salt, garlic, etc.) if needed. Separate sweet and savory.
        For each recipe give:
        - Title
        - Ingredients used
        - Step-by-step instructions"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        
        st.subheader("Your Recipes")
        st.write(response.choices[0].message.content)

st.caption("Free tool by Grok. Premium features coming soon.")
