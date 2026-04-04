import streamlit as st
from st_supabase_connection import SupabaseConnection

st.set_page_config(page_title="LeftoverChef", page_icon="🍳", layout="centered")

# Dark blue background + peach title + turquoise buttons with red outline
st.markdown("""
    <style>
    .stApp { background-color: #0a2540; color: white; }
    h1 { color: #ffcc99 !important; }           /* Peach for title */
    .highlight { color: #ffcc99; font-weight: bold; }
    
    /* Turquoise button with nice red outline */
    .stLinkButton > a {
        background-color: #00d4ff !important;
        color: black !important;
        font-weight: bold !important;
        border: 3px solid #ff4d4d !important;   /* Red outline */
        border-radius: 10px !important;
        padding: 0.9rem 1.6rem !important;
        font-size: 1.15rem !important;
        box-shadow: 0 4px 8px rgba(255, 77, 77, 0.3) !important;
    }
    .stLinkButton > a:hover {
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

# ====================== IMAGES ======================
# Big frying pan with eggs at the top
st.image("https://via.placeholder.com/800x300/FFCC99/000000?text=🍳+Frying+Pan+with+Eggs", use_column_width=True)

# Three small images
col1, col2, col3 = st.columns(3, gap="small")
with col1:
    st.image("https://via.placeholder.com/200x150/FFCC99/000000?text=🍑+Peach", use_column_width=True)
with col2:
    st.image("https://via.placeholder.com/200x150/FFCC99/000000?text=🍳+Eggs", use_column_width=True)
with col3:
    st.image("https://via.placeholder.com/200x150/FFCC99/000000?text=👨‍🍳+Chef", use_column_width=True)

st.title("🍽️ LeftoverChef")
st.markdown('<p class="highlight">Turn your leftovers into delicious meals</p>', unsafe_allow_html=True)

if st.session_state.user is None:
    # ================== HOME PAGE ==================
    st.markdown("### Save your favorite meals for days or weeks later?")

    # Turquoise button with red outline → Stripe
    stripe_url = "https://buy.stripe.com/YOUR_REAL_STRIPE_CHECKOUT_LINK_HERE"  # ← Replace with your real Stripe link
    st.link_button("🚀 Sign Up for Premium – Unlock Saved Meals", stripe_url, use_container_width=True)

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

    # Little chef icon clearly under the buttons
    st.image("https://via.placeholder.com/180x180/FFCC99/000000?text=👨‍🍳+Chef", use_column_width=False)

    # Centered caption
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
        st.success("✅ Premium Active – Save as many meals as you want!")
        if st.button("❤️ Save this Meal"):
            st.success("Meal saved!")
        if st.button("📚 My Saved Meals"):
            st.info("Your saved meals library coming soon")
    else:
        st.warning("🔒 Free Account")
        stripe_url = "https://buy.stripe.com/YOUR_REAL_STRIPE_CHECKOUT_LINK_HERE"  # ← Same real Stripe link
        st.link_button("Upgrade to Premium Now", stripe_url, use_container_width=True)
