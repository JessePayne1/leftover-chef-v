import streamlit as st
from st_supabase_connection import SupabaseConnection
import openai

st.set_page_config(page_title="LeftoverChef", page_icon="🍳", layout="centered")

# Dark blue + peach title + turquoise premium button with thin red outline only
st.markdown("""
    <style>
    .stApp { background-color: #0a2540; color: white; }
    h1 { color: #ffcc99 !important; }
    .highlight { color: #ffcc99; font-weight: bold; }
    
    /* Thin red outline ONLY on premium button */
    .stLinkButton > a {
        background-color: #00d4ff !important;
        color: black !important;
        font-weight: bold !important;
        border: 2px solid #ff4d4d !important;
        border-radius: 10px !important;
        padding: 0.9rem 1.6rem !important;
        font-size: 1.15rem !important;
    }
    .stLinkButton > a:hover {
        background-color: #00b8e0 !important;
    }
    </style>
""", unsafe_allow_html=True)

conn = st.connection("supabase", type=SupabaseConnection)

if "user" not in st.session_state:
    st.session_state.user = None
if "is_premium" not in st.session_state:
    st.session_state.is_premium = False

# ====================== HEADER ======================
st.image("https://via.placeholder.com/800x250/FFCC99/000000?text=🍳+Frying+Pan+with+Eggs", use_column_width=True)

st.title("🍽️ LeftoverChef")

# Freemium Version label + input box
st.markdown("**Freemium Version**")
ingredients = st.text_area(
    "What do you have in the fridge?",
    placeholder="e.g. chicken, rice, broccoli, leftover pizza...",
    height=120
)

st.markdown('<p class="highlight">Turn your leftovers into delicious meals</p>', unsafe_allow_html=True)

# ====================== GENERATE MEAL BUTTON (Always visible in Freemium) ======================
if st.button("🍳 Generate Meal Idea", type="primary", use_container_width=True):
    if not ingredients.strip():
        st.warning("Please type some ingredients or leftovers first!")
    else:
        with st.spinner("Creating a tasty idea from your leftovers..."):
            try:
                client = openai.OpenAI()
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a friendly home chef who creates quick, creative recipes from leftovers."},
                        {"role": "user", "content": f"Create one simple, delicious recipe using these ingredients: {ingredients}. "
                                                  "Give it a fun title, list the ingredients, and provide short step-by-step instructions."}
                    ]
                )
                meal = response.choices[0].message.content
                st.success("Here's a meal idea for you:")
                st.markdown(meal)
            except Exception as e:
                st.error("Meal generation failed. Please make sure your OpenAI key is correctly added in Streamlit Secrets.")

if st.session_state.user is None:
    # ================== LANDING PAGE ==================
    st.markdown("### Take pictures of your open fridge and see what meals are built?!")

    # Premium button with thin red outline
    stripe_url = "https://buy.stripe.com/YOUR_REAL_STRIPE_CHECKOUT_LINK_HERE"  # ← Replace with your real Stripe link
    st.link_button("🚀 Sign Up for Premium $4.99 – Unlock Saving, 5-Min Meals & Microwave Versions", 
                   stripe_url, use_container_width=True)

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

    # Chef icon under the button area
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
        st.success("✅ Premium Active – You can save meals!")
        if st.button("❤️ Save this Meal"):
            st.success("Meal saved to your library!")
        if st.button("📚 My Saved Meals"):
            st.info("Your saved meals will appear here soon")
    else:
        st.warning("🔒 Free Account")
        stripe_url = "https://buy.stripe.com/YOUR_REAL_STRIPE_CHECKOUT_LINK_HERE"
        st.link_button("Upgrade to Premium $4.99 Now", stripe_url, use_container_width=True)
