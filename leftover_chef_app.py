import streamlit as st
from st_supabase_connection import SupabaseConnection
import time

# ====================== CONFIG ======================
st.set_page_config(page_title="LeftoverChef", page_icon="🍽️", layout="centered")

# Dark blue theme
st.markdown("""
    <style>
    .stApp {
        background-color: #0a2540;
        color: white;
    }
    .stButton>button {
        background-color: #00d4ff;
        color: black;
        font-weight: bold;
        border-radius: 8px;
    }
    .stButton>button:hover {
        background-color: #00b8e0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Supabase
conn = st.connection("supabase", type=SupabaseConnection)

# ====================== SESSION STATE ======================
if "user" not in st.session_state:
    st.session_state.user = None
if "is_premium" not in st.session_state:
    st.session_state.is_premium = False

# ====================== AUTH & USER CHECK ======================
def check_premium_status(user_id):
    try:
        response = conn.table("profiles").select("is_premium").eq("id", user_id).execute()
        if response.data and len(response.data) > 0:
            return response.data[0].get("is_premium", False)
        return False
    except:
        return False

# ====================== MAIN APP ======================
st.title("🍽️ LeftoverChef")
st.markdown("**Turn leftovers into delicious meals** — Save your favorites for later with Premium")

if st.session_state.user is None:
    # ================== LANDING PAGE (Home) ==================
    st.markdown("### Welcome to LeftoverChef!")
    st.markdown("""
    Generate creative meals from what you have in the fridge.  
    **Premium members** can save their favorite meals and access them days or weeks later.
    """)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 Sign Up for Premium", type="primary", use_container_width=True):
            st.switch_page("pages/1_Signup.py")   # We'll create this simple page next if needed
            # Or keep inline signup if you prefer

    with col2:
        if st.button("🔑 Already have an account? Login"):
            st.session_state.show_login = True
            st.rerun()

    # Optional inline login
    if st.session_state.get("show_login", False):
        st.subheader("Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            try:
                res = conn.auth.sign_in_with_password({"email": email, "password": password})
                st.session_state.user = res.user
                st.session_state.is_premium = check_premium_status(res.user.id)
                st.success("Logged in successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Login failed: {e}")

else:
    # ================== LOGGED IN VIEW ==================
    user = st.session_state.user
    st.session_state.is_premium = check_premium_status(user.id)

    st.sidebar.success(f"👤 {user.email}")
    if st.sidebar.button("Logout"):
        conn.auth.sign_out()
        st.session_state.user = None
        st.session_state.is_premium = False
        st.rerun()

    # Premium status banner
    if st.session_state.is_premium:
        st.success("✅ Premium Member — You can save meals!")
    else:
        st.warning("🔒 Free Account — Upgrade to Premium to save your meals for later")

    # Meal Generation Area (your existing logic goes here)
    st.subheader("Generate a Meal")
    if st.button("Generate New Meal Idea"):
        st.info("Your meal generation code with OpenAI goes here...")

    # Saved Meals - Gated
    if st.session_state.is_premium:
        if st.button("❤️ Save this Meal"):
            # TODO: Add actual save logic here once we have current_meal
            st.success("Meal saved to your library!")

        if st.button("📚 My Saved Meals"):
            st.info("Your saved meals will appear here")
            # TODO: Query saved_meals table filtered by user
    else:
        st.markdown("---")
        st.markdown("**Want to save this meal for later?**")
        if st.button("Upgrade to Premium Now", type="primary"):
            # Your existing Stripe button code that worked before
            st.info("Stripe Checkout would open here (your previous code)")

# Footer
st.caption("LeftoverChef — Making leftovers exciting again")
