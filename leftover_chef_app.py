import streamlit as st
from st_supabase_connection import SupabaseConnection

# Page config
st.set_page_config(page_title="LeftoverChef", page_icon="🍽️", layout="centered")

# Dark blue + turquoise theme (matches your original look)
st.markdown("""
    <style>
    .stApp { background-color: #0a2540; color: white; }
    .stButton>button { 
        background-color: #00d4ff; 
        color: black; 
        font-weight: bold; 
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
    }
    .stButton>button:hover { background-color: #00b8e0; }
    </style>
""", unsafe_allow_html=True)

# Initialize Supabase connection
conn = st.connection("supabase", type=SupabaseConnection)

# Session state
if "user" not in st.session_state:
    st.session_state.user = None
if "is_premium" not in st.session_state:
    st.session_state.is_premium = False

# Simple premium check (we'll improve this with a real table later)
def check_premium_status(user_id):
    try:
        # For now, fallback to False until we create the profiles table
        return False
    except:
        return False

# ====================== HEADER / IMAGES ======================
# Add your three images here (peach, eggs in pan, chef)
# Replace the URLs with your actual hosted links or GitHub paths (e.g. "images/peach.jpg")
col1, col2, col3 = st.columns(3, gap="small")
with col1:
    st.image("https://via.placeholder.com/200x150/FFCC99/000000?text=Peach", use_column_width=True, caption="Fresh Ingredients")
with col2:
    st.image("https://via.placeholder.com/200x150/FFCC99/000000?text=Eggs+in+Pan", use_column_width=True, caption="Cooking Leftovers")
with col3:
    st.image("https://via.placeholder.com/200x150/FFCC99/000000?text=Chef", use_column_width=True, caption="LeftoverChef")

st.title("🍽️ LeftoverChef")
st.markdown("**Turn your leftovers into delicious meals** — Save your favorites for days or weeks later with **Premium**")

# ====================== MAIN FLOW ======================
if st.session_state.user is None:
    # Home / Landing Page (what users see first)
    st.markdown("### Ready to save your favorite recipes?")
    st.markdown("Premium members get a personal library to access saved meals anytime.")

    # Big turquoise CTA button (as you advertised)
    if st.button("🚀 Sign Up for Premium – Unlock Saved Meals", type="primary", use_container_width=True):
        st.info("🔄 Your original Stripe checkout / premium signup flow goes here (it worked before)")

    # Smaller login option
    if st.button("🔑 Already have an account? Login"):
        st.session_state.show_login = True
        st.rerun()

    # Inline login (keeps it simple, no extra pages)
    if st.session_state.get("show_login", False):
        st.subheader("Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login", type="primary"):
            try:
                res = conn.auth.sign_in_with_password({"email": email, "password": password})
                st.session_state.user = res.user
                st.session_state.is_premium = check_premium_status(res.user.id)
                st.success("Welcome back!")
                st.rerun()
            except Exception as e:
                st.error(f"Login failed: {str(e)}")

else:
    # Logged-in view
    user = st.session_state.user
    st.session_state.is_premium = check_premium_status(user.id)

    # Sidebar (this brings back the chevron / menu icon in top-left)
    with st.sidebar:
        st.success(f"👤 {user.email.split('@')[0]}")
        if st.button("Logout"):
            try:
                conn.auth.sign_out()
            except:
                pass
            st.session_state.user = None
            st.session_state.is_premium = False
            st.rerun()

    if st.session_state.is_premium:
        st.success("✅ Premium Active — Save as many meals as you want!")
        if st.button("❤️ Save this Meal"):
            st.success("Meal saved to your library! (full save logic coming next)")
        if st.button("📚 View My Saved Meals"):
            st.info("Your saved meals library will appear here")
    else:
        st.warning("🔒 Free Account — Upgrade to save meals for days or weeks later")
        if st.button("Upgrade to Premium Now", type="primary"):
            st.info("🔄 Your original Stripe button / checkout flow goes here")

# Footer
st.caption("LeftoverChef — Making leftovers exciting again 🍽️")
