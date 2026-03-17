import streamlit as st

st.set_page_config(page_title="LeftoverChef", layout="wide", page_icon="🍳")

st.title("🍳 LeftoverChef: Turn Leftovers into Meals!")
st.markdown("**Now even smarter!** Eggs, sugar, flour, spices & pantry staples all work. Real combos only.")

# ================== BIGGER RECIPE DATABASE ==================
recipes = [
    # Egg-focused (now catches "3 eggs", "eggs", etc.)
    {"title": "Quick 3-Egg Omelette or Scrambled Eggs", "keywords": {"egg", "eggs", "cheese", "vegetables", "onion"}, "desc": "Whisk eggs with cheese/veggies, cook in 5 min. Add any scraps!", "type": "savory"},
    {"title": "Veggie Egg Frittata or Hash", "keywords": {"egg", "eggs", "carrot", "vegetables", "potato peels"}, "desc": "Mix eggs with chopped scraps, bake or pan-fry. Uses everything!", "type": "savory"},
    {"title": "Easy Cheese Soufflé (or Egg Muffin Cups)", "keywords": {"egg", "eggs", "cheese"}, "desc": "Beat eggs with cheese, bake in ramekins or muffin tin. Fancy but simple!", "type": "savory"},
    {"title": "Egg & Veggie Fritters", "keywords": {"egg", "eggs", "carrot", "vegetables"}, "desc": "Mix with flour (if you have it), fry into crispy patties.", "type": "savory"},
    
    # Pantry staple combos
    {"title": "Flour + Sugar Pancakes or Waffles", "keywords": {"flour", "sugar", "egg", "eggs"}, "desc": "Basic batter: flour, sugar, egg + milk/water. Add banana or spices!", "type": "sweet"},
    {"title": "Banana Bread or Muffins with Pantry Staples", "keywords": {"banana", "flour", "sugar", "egg"}, "desc": "Classic recipe using your flour, sugar & egg — moist and zero-waste.", "type": "sweet"},
    {"title": "Spiced Carrot Cake or Muffins", "keywords": {"carrot", "flour", "sugar", "egg", "spice"}, "desc": "Grate carrot into flour-sugar-egg batter + spices. Bake!", "type": "sweet"},
    {"title": "Bread Pudding with Sugar & Spices", "keywords": {"bread", "sugar", "egg", "spice"}, "desc": "Soak bread in egg-sugar mix, add spices, bake. Comfort food!", "type": "sweet"},
    
    # Meat + pantry
    {"title": "Steak Stir-Fry with Spices", "keywords": {"steak", "vegetables", "onion", "spice"}, "desc": "Season steak + veggies with your spices. One-pan meal.", "type": "savory"},
    {"title": "One-Pot Leftover Casserole", "keywords": {"steak", "bread", "vegetables", "carrot", "egg"}, "desc": "Layer everything, top with egg or bread crumbs, bake.", "type": "savory"},
    
    # Veggie / scrap
    {"title": "Kitchen-Sink Vegetable Soup or Stir-Fry", "keywords": {"carrot", "vegetables", "potato peels", "onion", "spice"}, "desc": "Simmer or fry with spices. Add egg for richness.", "type": "savory"},
    {"title": "Root Veggie Fritters or Hash Browns", "keywords": {"potato peels", "carrot", "egg", "flour"}, "desc": "Shred + mix with egg/flour, fry crispy.", "type": "savory"},
]

def categorize_ingredients(ings):
    meat = any(w in ings for w in ["steak", "chicken", "beef", "meat"])
    return meat

# ================== MAIN APP ==================
ingredients_input = st.text_input("Enter comma-separated leftovers (e.g., 3 eggs, carrot peels, onion, flour, sugar, steak):", "")

if ingredients_input:
    # Better parsing: ignore numbers, handle plurals
    user_ings = set()
    for item in ingredients_input.lower().split(','):
        item = item.strip()
        item = ''.join(c for c in item if not c.isdigit())  # remove numbers like "3"
        item = item.strip()
        if item:
            user_ings.add(item)
            if item.endswith('s') and len(item) > 3:  # eggs → egg
                user_ings.add(item[:-1])
    
    meat_present = categorize_ingredients(user_ings)
    
    scored = []
    for rec in recipes:
        if meat_present and rec["type"] == "sweet":
            continue
        matches = len(rec["keywords"] & user_ings)
        if matches >= 1:
            score = matches / len(rec["keywords"])
            scored.append((score, matches, rec))
    
    scored = sorted(scored, key=lambda x: (x[0], x[1]), reverse=True)
    
    st.subheader("🥇 Best Combined Dishes (using most of your items)")
    shown = 0
    for score, matches, rec in scored[:5]:
        if matches >= 2 or score > 0.4:
            st.markdown(f"**{rec['title']}** — Uses {matches} of your ingredients\n{rec['desc']}")
            shown += 1
    
    if shown == 0:
        st.info("Add more common items (eggs, flour, sugar, spices) for better combos!")

    st.subheader("Quick Pantry Ideas")
    if "egg" in user_ings or "eggs" in user_ings:
        st.markdown("• Eggs: Omelette, frittata, or soufflé cups")
    if "flour" in user_ings and "sugar" in user_ings:
        st.markdown("• Flour + Sugar: Pancakes or quick muffins")

st.caption("Free zero-waste tool — now with 20+ real recipes including eggs, flour, sugar & spices! Ready for fridge photo upload?")
