import streamlit as st
import openai
import os

st.set_page_config(page_title="LeftoverChef", page_icon="🍳", layout="centered")

st.title("🍽️ LeftoverChef - Debug Mode")

st.write("**Testing OpenAI Key**")

# Show what secrets Streamlit actually sees
st.write("Available secrets keys:", list(st.secrets.keys()) if st.secrets else "No secrets found")

if "OPENAI_API_KEY" in st.secrets:
    st.success("✅ OPENAI_API_KEY found in secrets!")
    api_key = st.secrets["OPENAI_API_KEY"]
    st.write("Key starts with:", api_key[:20] + "...")
else:
    st.error("❌ OPENAI_API_KEY is MISSING from secrets")

ingredients = st.text_area("What do you have in the fridge?", placeholder="chicken rice broccoli", height=100)

if st.button("🍳 Generate Meal Idea"):
    if not ingredients.strip():
        st.warning("Type ingredients first")
    else:
        with st.spinner("Trying to generate..."):
            try:
                api_key = st.secrets["OPENAI_API_KEY"]
                os.environ["OPENAI_API_KEY"] = api_key
                client = openai.OpenAI(api_key=api_key)
                
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful chef."},
                        {"role": "user", "content": f"Create a simple recipe with: {ingredients}"}
                    ]
                )
                st.success("Success!")
                st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"Error: {str(e)}")

st.caption("Debug version - tell me what you see above")
