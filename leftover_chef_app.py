import streamlit as st

st.set_page_config(page_title="LeftoverChef", layout="wide", page_icon="🍳")

st.title("🍳 LeftoverChef: Turn Leftovers into Meals!")
st.markdown("**Now smarter!** Enter ingredients — it finds *combined* dishes using as many as possible (no more random smoothies for steak).")

# ================== SMART RECIPE DATABASE ==================
recipes = [
    # Combined savory (meat + veggies)
    {"title": "Leftover Steak Stir-Fry or Fried Rice", "keywords": {"steak", "carrot", "vegetables", "broccoli", "onion"}, "desc": "Slice steak thin, stir-fry with your veggies and any rice or bread crumbs. Ready in 15 min. Uses 3–5 items!", "type": "savory"},
    {"title": "Beef & Veggie Stew or Pot Pie", "keywords": {"steak", "carrot", "vegetables", "potato peels", "onion"}, "desc": "Simmer steak + veggies in broth (use peels for stock). Top with mashed potato peels or bread crust for a quick pie. Classic zero-waste dinner.", "type": "savory"},
    {"title": "Veggie & Meat Hash or Frittata", "keywords": {"steak", "carrot", "potato peels", "vegetables"}, "desc": "Chop everything, pan-fry with egg or just oil. Breakfast-for-dinner that uses every scrap.", "type": "savory"},
    
    # Sweet / fruit combos
    {"title": "Banana-Carrot Bread or Muffins", "keywords": {"banana", "carrot", "bread"}, "desc": "Mash banana + grated carrot into bread batter. Moist, sweet, and hides both scraps perfectly.", "type": "sweet"},
    {"title": "Bread Pudding or French Toast Bake", "keywords": {"bread", "banana"}, "desc": "Soak stale bread in banana-milk mix, bake. Add any fruit scraps.", "type": "sweet"},
    {"title": "Fruit & Yogurt Smoothie Bowl", "keywords": {"banana"}, "desc": "Only for fruit/dairy — blend with yogurt or milk. (Meat skipped automatically!)", "type": "sweet"},
    
    # Pure veggie / scrap combos
    {"title": "Kitchen-Sink Vegetable Stir-Fry or Soup", "keywords": {"carrot", "vegetables", "potato peels", "broccoli"}, "desc": "Chop peels & scraps, stir-fry or simmer into soup. Add any bread for thickening.", "type": "savory"},
    {"title": "Root Veggie Hash Browns or Frittata", "keywords": {"potato peels", "carrot", "vegetables"}, "desc": "Shred and pan-fry — crispy side dish or main.", "type": "savory"},
    {"title": "Veggie Scrap Stock + Anything Soup", "keywords": {"carrot", "potato peels", "onion"}, "desc": "Simmer peels 1 hour for free broth, then add other leftovers.", "type": "savory"},
    
    # More flexible catch-alls
    {"title": "One-Pot Leftover Casserole", "keywords": {"steak", "bread", "vegetables", "carrot"}, "desc": "Layer everything in a dish, top with bread crumbs, bake. Uses whatever you have!", "type": "savory"},
]

def categorize_ingredients(ings):
    meat = any(w in ings for w in ["steak", "chicken", "beef", "meat"])
    fruit = any(w in ings for w in ["banana", "apple", "berry"])
    return meat, fruit

# ================== MAIN APP ==================
ingredients_input = st.text_input("Enter comma-separated leftovers (e.g., steak, carrot peels, banana, bread, leftover vegetables):", "")

if ingredients_input:
    user_ings = {i.strip().lower() for i in ingredients_input.split(',') if i.strip()}
    meat_present, fruit_present = categorize_ingredients(user_ings)
    
    # Score recipes by how many keywords match
    scored = []
    for rec in recipes:
        if meat_present and rec["type"] == "sweet":  # Block bad combos
            continue
        matches = len(rec["keywords"] & user_ings)
        if matches >= 1:
            score = matches / len(rec["keywords"])
            scored.append((score, matches, rec))
    
    scored.sort(reverse=True)
    
    st.subheader("🥇 Best Combined Dishes (using most of your items)")
    shown = 0
    for score, matches, rec in scored[:3]:
        if matches >= 2 or score > 0.5:
            st.markdown(f"**{rec['title']}** — Uses {matches} of your ingredients\n{rec['desc']}")
            shown += 1
    
    if shown == 0:
        st.info("Not enough matches for a big combo yet — try adding more common scraps!")
    
    # Separate simple ideas
    st.subheader("Separate Quick Ideas")
    for ing in user_ings:
        if ing in ["banana", "bread"]:
            st.markdown(f"• {ing.capitalize()}: Banana bread or bread pudding")
        elif "peel" in ing or "carrot" in ing:
            st.markdown(f"• {ing.capitalize()}: Roast into chips or add to soup")

st.caption("Free zero-waste tool — now with smart matching! Fridge photo upload + AI detection coming next.")
