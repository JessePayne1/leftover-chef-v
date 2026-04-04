import streamlit as st
from st_supabase_connection import SupabaseConnection

st.set_page_config(page_title="LeftoverChef", page_icon="🍽️", layout="centered")

# Dark blue + turquoise theme
st.markdown("""
    <style>
    .stApp { background-color: #0a2540; color: white; }
    .stButton>button { 
        background-color: #00d4ff; 
        color: black; 
        font-weight: bold; 
        border-radius: 8px;
        padding: 0.8rem 1.5rem;
        font-size: 1.1rem;
    }
    .stButton>button:hover { background-color: #00b8e0; }
    </style>
""", unsafe_allow_html=True)

# Connections
conn = st.connection("supabase", type=SupabaseConnection)

# Session state
if "user" not in st.session_state:
    st.session_state.user = None
if "is_premium" not in st.session_state:
    st.session_state.is_premium = False

# ====================== IMAGES ======================
# Replace these placeholder URLs with your real peach, eggs-in-pan, and chef images
col1, col2, col3 = st.columns(3, gap="small")
with col1:
    st.image("https://via.placeholder.com/250x180/FFCC99/000000?text=🍑+Peach", use_column_width=True)
with col2:
    st.image("https://via.placeholder.com/250x180/FFCC99/000000?text=🍳+Eggs+in+Pan", use_column_width=True)
with col3:
    st.image("https://via.placeholder.com/250x180/FFCC99/000000?text=👨‍🍳+Chef", use_column_width=True)

st.title("🍽️ LeftoverChef")
st.markdown("**Turn your leftovers into delicious meals**")

if st.session_state.user is None:
    # ================== LANDING PAGE ==================
    st.markdown("### Save your favorite meals for days or weeks later?")
    st.markdown("**Premium** unlocks your personal saved meals library.")

    # Big turquoise button → directly opens Stripe Checkout
    if st.button("🚀 Sign Up for Premium – Unlock Saved Meals", type="primary", use_container_width=True):
        stripe_publishable_key = st.secrets["stripe"]["PUBLISHABLE_KEY"]
        
        # Simple redirect to your Stripe Checkout link (easiest method)
        # Replace this URL with your actual Stripe Payment Link or Checkout Session URL
        checkout_url = "https://buy.stripe.com/https://buy.stripe.com/6oU7sM9Pa9oIdIrfPz4sE00"   # ← CHANGE THIS
        
        # Optional: Use st.markdown with unsafe_allow_html for a cleaner redirect
        st.markdown(f"""
            <meta http-equiv="refresh" content="0; url={checkout_url}">
        """, unsafe_allow_html=True)
        
        st.success("Redirecting to secure Stripe checkout...")

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
                st.success("Logged in!")
                st.rerun()
            except Exception as e:
                st.error(f"Login failed: {str(e)}")

else:
    # ================== LOGGED-IN VIEW ==================
    with st.sidebar:
        st.success(f"👤 {st.session_state.user.email}")
        if st.button("Logout"):
            conn.auth.sign_out()
            st.session_state.user = None
            st.rerun()

    if st.session_state.is_premium:
        st.success("✅ Premium Active – You can now save meals!")
        if st.button("❤️ Save this Meal"):
            st.success("Meal saved to your library!")
        if st.button("📚 My Saved Meals"):
            st.info("Your saved meals will appear here (coming next)")
    else:
        st.warning("🔒 Free Account")
        if st.button("Upgrade to Premium Now", type="primary"):
            # Reuse the same Stripe redirect logic
            checkout_url = "https://buy.stripe.com/https://buy.stripe.com/6oU7sM9Pa9oIdIrfPz4sE00"   # ← CHANGE THIS
            st.markdown(f'<meta http-equiv="refresh" content="0; url={checkout_url}">', unsafe_allow_html=True)
            st.success("Redirecting to Stripe...")

st.caption("LeftoverChef — Leftovers never tasted so good 🍽️")
