import streamlit as st

# Your recipes dictionary (expand as needed – copy more from your original script)
recipes = {
    "banana": "Banana Bread: Mash overripe bananas with flour, sugar, egg, oil. Bake at 350°F.",
    "bread": "Bread Pudding: Soak stale bread in milk, eggs, sugar. Bake.",
    "carrot": "Carrot Top Pesto or add to soups/stir-fries.",
    "potato peels": "Potato Peel Chips: Toss peels with oil and salt, bake at 400°F until crispy.",
    "leftover vegetables": "Vegetable Stir-Fry: Chop and stir-fry with soy sauce. Serve over rice.",
    # Add as many as you want from your earlier version!
}

st.set_page_config(page_title="LeftoverChef", layout="wide", page_icon="🍳")

st.title("🍳 LeftoverChef: Turn Leftovers into Meals!")
st.markdown("Enter your leftover ingredients to get zero-waste recipe ideas. (Fridge photo upload coming soon!)")

# Text input for ingredients
ingredients = st.text_input("Comma-separated leftovers (e.g., banana, bread, carrot peels):", "")

if ingredients:
    suggestions = []
    for ing in [i.strip().lower() for i in ingredients.split(',')]:
        found = False
        for key in recipes:
            if key in ing:
                suggestions.append(recipes[key])
                found = True
                break
        if not found:
            suggestions.append(f"No exact match for '{ing}' – try soups, stir-fries, or smoothies!")
    
    if suggestions:
        st.subheader("Your Recipe Ideas")
        for i, sug in enumerate(suggestions, 1):
            st.markdown(f"**{i}.** {sug}")
    else:
        st.info("No ingredients entered yet!")

st.markdown("---")
st.caption("Free tool to reduce food waste – built with Grok help! Share your creations.")
