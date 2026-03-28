import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="LeftoverChef", layout="wide", page_icon="🍳")

st.title("🍳 LeftoverChef")

st.markdown("**Turn any leftovers into real meals**")

with st.sidebar:
    api_key = st.text_input("OpenAI API Key", type="password")
    premium = st.checkbox("Premium Mode (fridge photo + 5-min recipes)", value=False)

if not api_key:
    st.warning("Please enter your OpenAI API key in the sidebar.")
    st.stop()

client = OpenAI(api_key=api_key)

ingredients = st.text_input("Enter your ingredients:", placeholder="steak, yogurt, rice, eggs, chili, green pepper")

if st.button("Generate Recipes"):
    with st.spinner("Creating recipes..."):
        prompt = f"""Create 2-3 practical zero-waste recipes using as many of these ingredients as possible: {ingredients}.
        Add common staples like oil, salt, garlic if needed.
        Separate sweet and savory.
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
