import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="LeftoverChef", layout="wide", page_icon="🍳")

st.title("🍳 LeftoverChef: Truly ANY Combo → Real Meals!")
st.markdown("**AI-powered now** — type any ingredients. It uses as many as possible + common staples (oil, salt, garlic, etc.).")

# Sidebar for your free OpenAI key (get one at platform.openai.com — $5–18 free credits)
with st.sidebar:
    api_key = st.text_input("OpenAI API Key (free tier works)", type="password")
    st.caption("Sign up at platform.openai.com → API keys → Create new key")

if not api_key:
    st.warning("Enter your OpenAI API key in the sidebar to unlock unlimited random combos!")
    st.stop()

client = OpenAI(api_key=api_key)

ingredients_input = st.text_input("Enter comma-separated leftovers (ANY combo!):", 
                                 placeholder="steak, yogurt, rice, eggs, chili, green pepper, chocolate chips")

if ingredients_input:
    with st.spinner("AI is creating recipes that use almost everything..."):
        prompt = f"""You are a zero-waste chef. Create 2-3 practical recipes using as many of these ingredients as possible: {ingredients_input}.
        You may add common household staples (oil, salt, garlic, onion, flour, sugar, milk, spices, bread crumbs, cheese, etc.).
        Separate sweet and savory clearly.
        For each recipe give:
        - Title
        - Which ingredients it uses (list them)
        - Step-by-step instructions (simple, 10-20 min)
        - How it clears the fridge

        Never suggest mixing sweet and savory in one dish."""

        response = client.chat.completions.create(
            model="gpt-4o-mini",  # cheap & fast (pennies per use)
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        recipes = response.choices[0].message.content
        
        st.subheader("🥇 AI-Generated Recipes (using most/all your items)")
        st.markdown(recipes)

    st.caption("Every combo now works! Test wild lists — the AI always finds a way.")

st.caption("Fridge photo upload + AI detection is the next (and final) upgrade — just say the word!")
