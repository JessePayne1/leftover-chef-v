import streamlit as st

st.set_page_config(page_title="LeftoverChef", layout="wide", page_icon="🍳")

st.title("🍳 LeftoverChef")

st.markdown("**Turn any leftovers into real meals**")

st.write("This is a minimal test version to get the app loading again.")

ingredients = st.text_input("Enter your ingredients (test):", placeholder="steak, yogurt, rice")

if st.button("Generate Recipes"):
    st.write("Test successful! Recipes would appear here.")
    st.write(f"You entered: {ingredients}")

st.caption("If you see this, the app is loading.")
