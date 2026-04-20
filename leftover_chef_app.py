import streamlit as st
import openai

st.set_page_config(page_title="LeftoverChef", page_icon="🍳", layout="centered")

st.title("🍽️ LeftoverChef - Test Mode")

ingredients = st.text_area(
    "What do you have in the fridge?",
    placeholder="e.g. chicken, rice, broccoli, leftover pizza...",
    height=120
)

if st.button("🍳 Generate Meal Idea", type="primary"):
    if not ingredients or not ingredients.strip():
        st.warning("Please type some ingredients first!")
    else:
        with st.spinner("Creating a tasty idea from your leftovers..."):
            try:
                # Temporary: key is hardcoded for testing
                client = openai.OpenAI(
                    api_key="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"
                )
                
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a friendly home chef who creates quick, creative recipes from leftovers."},
                        {"role": "user", "content": f"Create one simple, delicious recipe using these ingredients: {ingredients}. Give it a fun title, list the ingredients, and provide short step-by-step instructions."}
                    ]
                )
                meal = response.choices[0].message.content
                st.success("Here's a meal idea for you:")
                st.markdown(meal)
            except Exception as e:
                st.error(f"Error: {str(e)}")

st.caption("Test version - OpenAI key is in code for debugging")
