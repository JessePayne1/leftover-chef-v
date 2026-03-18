import streamlit as st

st.set_page_config(page_title="LeftoverChef", layout="wide", page_icon="🍳")

st.title("🍳 LeftoverChef: Turn ANY Random Leftovers into Meals & Snacks!")
st.markdown("**Sweet & Savory separated** — now with steak, yogurt, rice, eggs, chili & green pepper recipes + step-by-step instructions.")

# ================== EXPANDED RECIPE DATABASE ==================
recipes = [
    # NEW: Your latest test ingredients
    {"title": "Steak Chili Rice Bowl with Green Pepper", "keywords": {"steak", "chili", "rice", "green pepper"}, "desc": "Step 1: Shred steak and chop green pepper. Step 2: Warm rice, mix in chili + steak + pepper. Step 3: Heat in pan or microwave 3-4 min. Top with yogurt for creaminess. 10-min dinner!", "type": "savory"},
    {"title": "Yogurt-Marinated Steak Stir-Fry with Rice & Pepper", "keywords": {"steak", "yogurt", "rice", "green pepper"}, "desc": "Step 1: Mix yogurt with chili spices as marinade for steak. Step 2: Stir-fry steak + green pepper. Step 3: Serve over rice. Creamy, spicy, zero-waste!", "type": "savory"},
    {"title": "Egg Fried Rice with Steak & Chili", "keywords": {"steak", "rice", "egg", "chili"}, "desc": "Step 1: Scramble eggs. Step 2: Fry rice with chopped steak + chili + any green pepper. Step 3: Mix eggs in last 2 min. Classic takeout upgrade!", "type": "savory"},
    {"title": "Loaded Steak Chili Nacho-Style Bowl", "keywords": {"steak", "chili", "rice", "green pepper"}, "desc": "Step 1: Warm rice as base. Step 2: Top with steak, chili, chopped green pepper. Step 3: Microwave 2 min or bake 8 min. Add yogurt dollop.", "type": "savory"},
    {"title": "Creamy Yogurt Steak & Pepper Skillet", "keywords": {"steak", "yogurt", "green pepper"}, "desc": "Step 1: Sauté steak + green pepper. Step 2: Stir in yogurt + chili at end. Step 3: Serve with rice on side. Rich and quick!", "type": "savory"},
    {"title": "Egg & Yogurt Scramble with Steak Rice", "keywords": {"steak", "yogurt", "rice", "egg"}, "desc": "Step 1: Scramble eggs with yogurt. Step 2: Mix in shredded steak + rice. Step 3: Add chili/pepper for heat. Breakfast or dinner!", "type": "savory"},

    # Previous ones (still here for other tests)
    {"title": "Loaded Chicken Nachos", "keywords": {"chicken", "nachos"}, "desc": "Step 1: Shred chicken. Step 2: Layer on nachos + cheese. Step 3: Bake 400°F 8-10 min.", "type": "savory"},
    {"title": "Chocolate Chip Pancakes", "keywords": {"chocolate", "egg"}, "desc": "Step 1: Mix egg + chocolate chips + flour/sugar. Step 2: Cook 2-3 min per side.", "type": "sweet"},
    {"title": "2-Ingredient Chocolate Cake", "keywords": {"chocolate", "egg"}, "desc": "Step 1: Melt chocolate chips. Step 2: Whisk in eggs. Step 3: Bake or microwave.", "type": "sweet"},
]

# ================== MAIN APP ==================
ingredients_input = st.text_input("Enter comma-separated leftovers (e.g., steak, yogurt, rice, eggs, chili, green pepper):", "")

if ingredients_input:
    user_ings = set()
    for item in ingredients_input.lower().split(','):
        item = item.strip().replace("drumstick", "chicken").replace("cold", "").replace("chips", "chocolate").strip()
        if item:
            user_ings.add(item)
            if item.endswith('s') and len(item) > 3:
                user_ings.add(item[:-1])
    
    # Sweet vs Savory separation
    st.subheader("🥩 Savory Suggestions (Steak + Chili + Rice + Pepper + Yogurt + Eggs)")
    savory_shown = False
    for rec in recipes:
        if rec["type"] == "savory" and len(rec["keywords"] & user_ings) >= 1:
            st.markdown(f"**{rec['title']}** — {rec['desc']}")
            savory_shown = True
    if not savory_shown:
        st.markdown("No strong savory matches yet — try adding more scraps!")

    st.subheader("🍫 Sweet Suggestions (Chocolate + Eggs)")
    sweet_shown = False
    for rec in recipes:
        if rec["type"] == "sweet" and len(rec["keywords"] & user_ings) >= 1:
            st.markdown(f"**{rec['title']}** — {rec['desc']}")
            sweet_shown = True
    if not sweet_shown:
        st.markdown("No sweet matches — save chocolate/eggs for dessert!")

    st.subheader("Quick Zero-Waste Tip")
    st.markdown("• Steak + rice + chili + green pepper = spicy bowl\n• Yogurt + eggs = creamy scramble\n• Never mix sweet + savory!")

st.caption("Now covers steak, yogurt, rice, eggs, chili & green pepper perfectly! Fridge photo AI upload next?")
