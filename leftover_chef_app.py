import streamlit as st

st.set_page_config(page_title="LeftoverChef", layout="wide", page_icon="🍳")

st.title("🍳 LeftoverChef: Turn ANY Random Leftovers into Meals & Snacks!")
st.markdown("**Sweet & Savory now separated** — no more chocolate + chicken nonsense. Detailed steps included!")

# ================== RECIPE DATABASE WITH DETAILED STEPS ==================
recipes = [
    # SWEET (chocolate + eggs)
    {"title": "Chocolate Chip Pancakes or Waffles", "keywords": {"chocolate", "egg"}, "desc": "Step 1: Mix 1 cup flour (or oatmeal if no flour), 1 egg, 2 tbsp sugar (or honey), handful chocolate chips. Step 2: Add milk/water to make batter. Step 3: Cook on hot pan 2-3 min per side. Top with extra chips. Ready in 10 min!", "type": "sweet"},
    {"title": "2-Ingredient Chocolate Cake (or Mug Cake)", "keywords": {"chocolate", "egg"}, "desc": "Step 1: Melt 1 cup chocolate chips (microwave 30 sec). Step 2: Whisk in 4 eggs until smooth. Step 3: Bake at 350°F for 20-25 min (or microwave 1-2 min for mug cake). Super rich and zero-waste!", "type": "sweet"},

    # SAVORY (chicken + nachos + eggs)
    {"title": "Loaded Chicken Nachos (Reheat Upgrade)", "keywords": {"chicken", "nachos"}, "desc": "Step 1: Shred chicken drumstick meat. Step 2: Spread cold nachos on baking sheet, top with chicken + any cheese. Step 3: Bake at 400°F for 8-10 min until crispy and melty. Add egg on top if you want. Game-day level!", "type": "savory"},
    {"title": "Chicken Nacho Migas (Egg Scramble)", "keywords": {"chicken", "nachos", "egg"}, "desc": "Step 1: Crush cold nachos into pieces. Step 2: Scramble 2-3 eggs with shredded chicken. Step 3: Stir in crushed nachos last 2 min. Top with avocado or salsa if available. Breakfast or quick dinner!", "type": "savory"},
    {"title": "Cheesy Chicken Drumstick Nacho Bake", "keywords": {"chicken", "nachos"}, "desc": "Step 1: Shred chicken off drumstick. Step 2: Layer nachos in dish, add chicken + any cheese/scraps. Step 3: Bake 10 min at 400°F. Crispy, melty, uses everything!", "type": "savory"},

    # Flexible catch-alls
    {"title": "Sweet Chocolate Egg Treat", "keywords": {"chocolate", "egg"}, "desc": "Step 1: Whisk eggs with chocolate chips + sugar. Step 2: Cook like scrambled eggs or bake into cookies. 5-min snack!", "type": "sweet"},
    {"title": "Savory Chicken Nacho Bowl", "keywords": {"chicken", "nachos"}, "desc": "Step 1: Warm chicken drumstick. Step 2: Pile on cold nachos. Step 3: Microwave 1-2 min + add egg if you have one.", "type": "savory"},
]

# ================== MAIN APP ==================
ingredients_input = st.text_input("Enter comma-separated leftovers (e.g., chocolate chips, eggs, chicken drumstick, cold nachos):", "")

if ingredients_input:
    user_ings = set()
    for item in ingredients_input.lower().split(','):
        item = item.strip().replace("drumstick", "chicken").replace("cold", "").replace("chips", "chocolate").strip()
        if item:
            user_ings.add(item)
            if item.endswith('s') and len(item) > 3:
                user_ings.add(item[:-1])
    
    # Separate sweet & savory
    sweet_ings = {"chocolate", "egg"}
    savory_ings = {"chicken", "nachos"}
    
    st.subheader("🍫 Sweet Suggestions")
    sweet_shown = False
    for rec in recipes:
        if rec["type"] == "sweet" and len(rec["keywords"] & user_ings) >= 1:
            st.markdown(f"**{rec['title']}** — {rec['desc']}")
            sweet_shown = True
    if not sweet_shown:
        st.markdown("No strong sweet matches — try adding sugar/flour next time!")

    st.subheader("🥩 Savory Suggestions")
    savory_shown = False
    for rec in recipes:
        if rec["type"] == "savory" and len(rec["keywords"] & user_ings) >= 1:
            st.markdown(f"**{rec['title']}** — {rec['desc']}")
            savory_shown = True
    if not savory_shown:
        st.markdown("No strong savory matches — try adding cheese or spices!")

    # Always-useful quick tips
    st.subheader("Quick Zero-Waste Tips")
    st.markdown("• Sweet items (chocolate + eggs) = dessert only\n• Savory items (chicken + nachos) = reheat & upgrade\n• Never mix sweet + savory in one dish!")

st.caption("Now with separate sweet/savory + full step-by-step instructions! Fridge photo AI next?")
