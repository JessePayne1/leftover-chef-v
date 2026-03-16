import streamlit as st

st.set_page_config(page_title="LeftoverChef", layout="wide", page_icon="🍳")

st.title("🍳 LeftoverChef: Turn Leftovers into Meals!")
st.markdown("**Now smarter!** Enter ingredients — it finds *combined* dishes using as many as possible (no smoothies for steak, no 'no exact match' nonsense).")

# ================== SMART RECIPE DATABASE ==================
recipes = [
    # Savory combos (meat + veggies)
    {"title": "Leftover Steak Stir-Fry or Fried Rice", "keywords": {"steak", "carrot", "vegetables", "broccoli", "onion"}, "desc": "Slice steak thin, stir-fry with veggies + any rice/bread crumbs. Uses 3–5 items in one pan!", "type": "savory"},
    {"title": "Beef & Veggie Stew or Pot Pie", "keywords": {"steak", "carrot", "vegetables", "potato peels", "onion"}, "desc": "Simmer everything into broth (peels make free stock). Top with bread crust. One-pot dinner!", "type": "savory"},
    {"title": "Steak & Veggie Hash or Frittata", "keywords": {"steak", "carrot", "potato peels", "vegetables"}, "desc": "Chop & pan-fry everything together with egg or oil. Breakfast-for-dinner that clears your fridge!", "type": "savory"},
    {"title": "One-Pot Leftover Casserole", "keywords": {"steak", "bread", "vegetables", "carrot", "onion"}, "desc": "Layer it all, top with bread crumbs, bake. Uses almost everything you have!", "type": "savory"},
    
    # Sweet combos
    {"title": "Banana-Carrot Bread or Muffins", "keywords": {"banana", "carrot", "bread"}, "desc": "Mash banana + grate carrot into bread batter. Moist and delicious combo!", "type": "sweet"},
    {"title": "Bread Pudding or French Toast Bake", "keywords": {"bread", "banana"}, "desc": "Soak stale bread in banana-milk mix and bake. Add any fruit scraps.", "type": "sweet"},
    
    # Pure veggie combos
    {"title": "Kitchen-Sink Vegetable Stir-Fry or Soup", "keywords": {"carrot", "vegetables", "potato peels", "broccoli", "onion"}, "desc": "Chop peels & scraps, stir-fry or simmer. Add bread for thickening.", "type": "savory"},
    {"title": "Root Veggie Hash Browns", "keywords": {"potato peels", "carrot", "vegetables"}, "desc": "Shred and pan-fry into crispy hash. Uses every peel!", "type": "savory"},
    {"title": "Free Veggie Scrap Stock + Soup", "keywords": {"carrot", "potato peels", "onion"}, "desc": "Simmer peels 1 hour for broth, then dump in other leftovers.", "type": "savory"},
]

def categorize_ingredients(ings):
    meat = any(w in ings for w in ["steak", "chicken", "beef", "meat"])
    return meat

# ================== MAIN APP ==================
ingredients_input = st.text_input("Enter comma-separated leftovers (e.g., steak, carrot peels, onion, leftover vegetables):", "")

if ingredients_input:
    user_ings = {i.strip().lower() for i in ingredients_input.split(',') if i.strip()}
    meat_present = categorize_ingredients(user_ings)
    
    # Score recipes (fixed sorting!)
    scored = []
    for rec in recipes:
        if meat_present and rec["type"] == "sweet":  # Block bad combos
            continue
        matches = len(rec["keywords"] & user_ings)
        if matches >= 1:
            score = matches / len(rec["keywords"])
            scored.append((score, matches, rec))
    
    # FIXED: Safe sorting that never compares dictionaries
    scored = sorted(scored, key=lambda x: (x[0], x[1]), reverse=True)
    
    st.subheader("🥇 Best Combined Dishes (using most of your items)")
    shown = 0
    for score, matches, rec in scored[:4]:
        if matches >= 2 or score > 0.4:
            st.markdown(f"**{rec['title']}** — Uses {matches} of your ingredients\n{rec['desc']}")
            shown += 1
    
    if shown == 0:
        st.info("Try adding more scraps — the engine needs at least 2 matches for combos!")
    
    # Separate quick ideas only for true leftovers
    st.subheader("Separate Quick Ideas")
    for ing in user_ings:
        if "peel" in ing or "carrot" in ing:
            st.markdown(f"• {ing.capitalize()}: Roast into chips or add to soup")

st.caption("Free zero-waste tool — now bug-free and smarter! Fridge photo + AI detection coming in the next update.")
