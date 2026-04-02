import streamlit as st
from st_supabase_connection import SupabaseConnection
import time

# Initialize Supabase connection (Streamlit caches it nicely)
conn = st.connection("supabase", type=SupabaseConnection)

st.title("🍽️ Meal Planner")
st.markdown("Save your favorite meals and access them anytime.")

# ====================== AUTHENTICATION ======================
if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:
    # Tabbed Login / Sign Up
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Sign Up"])

    with tab1:  # Login
        st.subheader("Login to your account")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", type="primary", use_container_width=True):
            if email and password:
                with st.spinner("Logging in..."):
                    try:
                        res = conn.auth.sign_in_with_password({
                            "email": email,
                            "password": password
                        })
                        st.session_state.user = res.user
                        st.success(f"Welcome back, {email}!")
                        time.sleep(1)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Login failed: {str(e)}")
            else:
                st.warning("Please enter email and password.")

    with tab2:  # Sign Up
        st.subheader("Create a new account")
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password (min 6 characters)", type="password", key="signup_password")
        
        if st.button("Sign Up", type="primary", use_container_width=True):
            if email and password and len(password) >= 6:
                with st.spinner("Creating account..."):
                    try:
                        res = conn.auth.sign_up({
                            "email": email,
                            "password": password,
                            # Optional: redirect URL after email confirmation
                            # "options": {"emailRedirectTo": "https://your-app.streamlit.app"}
                        })
                        st.success("Account created! Please check your email (including spam) and click the confirmation link.")
                        st.info("After confirming your email, come back and login.")
                    except Exception as e:
                        st.error(f"Sign up failed: {str(e)}")
            else:
                st.warning("Please enter a valid email and password (at least 6 characters).")

else:
    # ====================== Logged-in View ======================
    user = st.session_state.user
    st.sidebar.success(f"👤 Logged in as: {user.email}")
    
    if st.sidebar.button("Logout"):
        try:
            conn.auth.sign_out()
        except:
            pass
        st.session_state.user = None
        st.rerun()

    st.success(f"Welcome, {user.email.split('@')[0]}! 🎉")
    
    # === YOUR MEAL PLANNER CONTENT GOES HERE ===
    st.write("### Your meal generation and planner goes below")
    
    # Example placeholder for your existing meal logic
    if st.button("Generate a New Meal"):
        st.info("Meal generation logic will go here...")
    
    # We'll add the "Save Meal" button and "My Saved Meals" next
