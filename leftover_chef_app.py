import streamlit as st
from st_supabase_connection import SupabaseConnection

st.set_page_config(page_title="LeftoverChef", page_icon="🍳", layout="centered")

# Dark blue + peach title + turquoise with red outline
st.markdown("""
    <style>
    .stApp { background-color: #0a2540; color: white; }
    h1 { color: #ffcc99 !important; }
    .highlight { color: #ffcc99; font-weight: bold; }
    
    /* Turquoise button with nice red outline */
    .stLinkButton > a, .stButton > button {
        background-color: #00d4ff !important;
        color: black !important;
        font-weight: bold !important;
        border: 3px solid #ff4d4d !important;
        border-radius: 10px !important;
        padding: 0.9rem 1.6rem !important;
        font-size: 1.15rem !important;
    }
    .stLinkButton > a:hover, .stButton > button:hover {
        background-color: #00b8e0 !important;
        border-color: #ff6666 !important;
    }
    </style>
""", unsafe_allow_html=True)

conn = st.connection("supabase", type=SupabaseConnection)

if "user" not in st.session_state:
    st.session_state.user = None
if "is_premium" not in st.session_state:
    st.session_state.is_premium = False

# ====================== HEADER IMAGES & TITLE ======================
# Frying pan with eggs right before / next to title
st.image("https://via.placeholder.com/800x250/FFCC99/000000?text=🍳+Frying+Pan+with+Eggs", use_column_width=True)

st.title("🍽️ LeftoverChef")

# Input box for food/ingredients (visible to everyone)
ingredients = st.text_area(
    "What do you have in the fridge? (type ingredients or leftovers)",
    placeholder="e.g. chicken, rice, broccoli, leftover pizza...",
    height=100
)

if ingredients:
    st.info("Great! Generate a meal below (premium unlocks 5-min & microwave versions + fridge photo feature)")

st.markdown('<p class="highlight">Turn your leftovers into delicious meals</p>', unsafe_allow_html=True)

if st.session_state.user is None:
    # ================== HOME / LANDING ==================
    st.markdown("### Take pictures of your open fridge and see what meals are built?!")

    # Big turquoise button with red outline + price
    stripe_url = "https://buy.stripe.com/YOUR_REAL_STRIPE_CHECKOUT_LINK_HERE"  # ← Replace with your actual Stripe link
    st.link_button("🚀 Sign Up for Premium $4.99 – Unlock Saving, 5-Min Meals & Microwave Versions", 
                   stripe_url, use_container_width=True)

    # Login option
    if st.button("🔑 Already have an account? Login"):
        st.session_state.show_login = True
        st.rerun()

    if st.session_state.get("show_login", False):
        st.subheader("Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login", type="primary"):
            try:
                res = conn.auth.sign_in_with_password({"email": email, "password": password})
                st.session_state.user = res.user
                st.success("Welcome back!")
                st.rerun()
            except Exception as e:
                st.error(f"Login failed: {str(e)}")

    # Chef icon underneath and left of button area, before tagline
    st.image("https://via.placeholder.com/180x180/FFCC99/000000?text=👨‍🍳+Chef", use_column_width=False)

    # Centered tagline
    st.markdown('<p style="text-align: center; color: #ffcc99; font-size: 1.1rem;">Leftovers never tasted so good 🍽️</p>', unsafe_allow_html=True)

else:
    # ================== LOGGED-IN VIEW ==================
    with st.sidebar:
        st.success(f"👤 {st.session_state.user.email}")
        if st.button("Logout"):
            conn.auth.sign_out()
            st.session_state.user = None
            st.rerun()

    if st.session_state.is_premium:
        st.success("✅ Premium Active – Save meals, get 5-min & microwave versions!")
        if st.button("❤️ Save this Meal"):
            st.success("Meal saved to your library!")
        if st.button("📚 My Saved Meals"):
            st.info("Your saved meals will appear here")
        if st.button("📸 Take Fridge Photo (Premium)"):
            st.info("Camera upload coming soon")
    else:
        st.warning("🔒 Free Account – Upgrade for saving, 5-min meals, microwave versions & fridge photo feature")
        stripe_url = "https://buy.stripe.com/YOUR_REAL_STRIPE_CHECKOUT_LINK_HERE"
        st.link_button("Upgrade to Premium $4.99 Now", stripe_url, use_container_width=True)
