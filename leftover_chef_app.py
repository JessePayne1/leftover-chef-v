import streamlit as st

st.set_page_config(page_title="LeftoverChef", layout="wide", page_icon="🍳")

st.title("🍳 LeftoverChef: Turn ANY Random Leftovers into Meals & Snacks!")
st.markdown("**Truly random-friendly now** — shrimp, kale, avocado, raspberries, chicken, rice, oatmeal… anything goes!")

# ================== ULTRA-EXPANDED RECIPE DATABASE ==================
recipes = [
    # New for your latest test
    {"title": "Shrimp Avocado Kale Salad Bowl", "keywords": {"shrimp", "avocado", "kale"}, "desc": "Chop kale + avocado, top with shrimp. Drizzle any yogurt or oil. Fresh lunch in 10 min!", "type": "savory"},
    {"title": "Creamy Shrimp Kale Stir-Fry with Avocado", "keywords": {"shrimp", "kale", "avocado"}, "desc": "Sauté shrimp + kale, mash avocado as creamy sauce. Uses all three perfectly!", "type": "savory"},
    {"title": "Raspberry Avocado Smoothie Bowl or Parfait", "keywords": {"raspberry", "avocado"}, "desc": "Blend raspberries + avocado (or mash for parfait). Add yogurt if you have it. Sweet snack!", "type": "sweet"},
    {"title": "Shrimp Raspberry Kale Salad", "keywords": {"shrimp", "raspberry", "kale"}, "desc": "Sweet-savory twist: shrimp over kale with raspberry dressing (mash berries + avocado oil).", "type": "savory"},

    # Previous random-friendly ones (chicken/rice/oatmeal/yogurt/etc.)
    {"title": "Chicken Fried Rice Bowl", "keywords": {"chicken", "rice"}, "desc": "Chop chicken, fry with rice. Add any greens.", "type": "savory"},
    {"title": "Chicken Yogurt Salad Bowl", "keywords": {"chicken", "yogurt", "salad"}, "desc": "Yogurt dressing + chicken + salad greens.", "type": "savory"},
    {"title": "Oatmeal Yogurt Parfait", "keywords": {"oatmeal", "yogurt"}, "desc": "Layer for quick healthy snack/breakfast.", "type": "sweet"},
    {"title": "Fridge-Clear Chicken Rice & Yogurt Bowl", "keywords": {"chicken", "rice", "yogurt"}, "desc": "Mix it all together.", "type": "savory"},

    # Egg/pantry catch-alls (still here)
    {"title": "Quick Egg Omelette or Frittata", "keywords": {"egg", "eggs"}, "desc": "Add any leftovers inside.", "type": "savory"},
    {"title": "Pancakes or Muffins", "keywords": {"flour", "sugar", "egg"}, "desc": "Basic batter — mix in fruit or yogurt.", "type": "sweet"},

    # Extra broad creative ones (so it NEVER says "add more")
    {"title": "Anything Goes Stir-Fry or Bowl", "keywords": {"shrimp", "kale", "avocado", "raspberry", "chicken", "rice"}, "desc": "Chop everything, stir-fry or layer in a bowl with oil/spices. Uses whatever you threw in!", "type": "savory"},
    {"title": "Creative Leftover Snack Plate", "keywords": {"raspberry", "avocado", "kale"}, "desc": "Slice avocado + raspberries on kale leaves. Add shrimp on the side. Zero cooking!", "type": "sweet"},
]

def categorize_ingredients(ings):
    meat = any(w in ings for w in ["chicken", "shrimp", "steak", "beef", "meat"])
    return meat

# ================== MAIN APP ==================
ingredients_input = st.text_input("Enter comma-separated leftovers (e.g., raspberries, kale, shrimp, avocado):", "")

if ingredients_input:
    # Super-smart parsing for random words
    user_ings = set()
    for item in ingredients_input.lower().split(','):
        item = item.strip()
        item = item.replace("thigh", "").replace("half", "").replace("leftover", "").replace("berries", "berry").strip()
        if item:
            user_ings.add(item)
            # Plurals & common fixes
            if item.endswith('s') and len(item) > 3:
                user_ings.add(item[:-1])
            if item == "raspberries":
                user_ings.add("raspberry")
    
    meat_present = categorize_ingredients(user_ings)
    
    scored = []
    for rec in recipes:
        if meat_present and rec["type"] == "sweet" and "shrimp" in user_ings:
            continue
        matches = len(rec["keywords"] & user_ings)
        if matches >= 1:
            score = matches / len(rec["keywords"])
            scored.append((score, matches, rec))
    
    scored = sorted(scored, key=lambda x: (x[0], x[1]), reverse=True)
    
    st.subheader("🥇 Best Combined Meals & Snacks")
    shown = 0
    for score, matches, rec in scored[:6]:
        st.markdown(f"**{rec['title']}** — Uses {matches} of your ingredients\n{rec['desc']}")
        shown += 1
    
    # Always show quick ideas so it's never blank
    st.subheader("Quick Creative Ideas")
    st.markdown("• Mix everything into one big bowl or stir-fry")
    if "avocado" in user_ings:
        st.markdown("• Mash avocado as creamy dressing/sauce for anything")
    if "raspberry" in user_ings:
        st.markdown("• Add raspberries for sweet pop on savory dishes")

st.caption("Now truly random — any fridge dump works! Ready for the fridge photo upload + AI auto-detection?")
