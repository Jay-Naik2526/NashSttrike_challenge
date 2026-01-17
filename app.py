import streamlit as st
import os
import random
import time
from dotenv import load_dotenv

load_dotenv()

# --- CONFIG ---
ELITE_USER = os.getenv("ELITE_USER")
ELITE_PASS = os.getenv("ELITE_PASS")
SEC_ANSWER = os.getenv("SEC_ANSWER")
FORM_URL = os.getenv("FORM_URL")
FLAGS = [os.getenv(f"FLAG_{i}") for i in range(1, 11)]

st.set_page_config(page_title="NASH_STTRIKE // ELITE", layout="centered")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp { background-color: black; color: #0f0; font-family: monospace; }
    input { background-color: #000 !important; color: #0f0 !important; border: 1px solid #0f0 !important; }
    .stButton>button { width: 100%; background-color: #0f0; color: black; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- APP LOGIC ---
if 'step' not in st.session_state:
    st.session_state.step = 1

st.title("NASH_STTRIKE")
st.subheader("CODING CLUB :: CYBER_DIVISION")

# STEP 1: LOGIN
if st.session_state.step == 1:
    u = st.text_input("IDENTIFIER")
    p = st.text_input("PASS_KEY", type="password")
    if st.button("INITIATE_BYPASS"):
        if u == ELITE_USER and p == ELITE_PASS:
            st.session_state.step = 2
            st.rerun()
        else:
            st.error("ACCESS DENIED")

# STEP 2: SECURITY
elif st.session_state.step == 2:
    a = st.text_input("CHALLENGE: FAVORITE COLOR?").lower().strip()
    if st.button("VALIDATE_AUTH"):
        if a == SEC_ANSWER:
            st.session_state.step = 3
            st.rerun()
        else:
            st.error("KEY MISMATCH")

# STEP 3: FINALIZE
elif st.session_state.step == 3:
    team = st.text_input("TEAM_ID")
    if st.button("COMPLETE_EXTRACTION"):
        flag = random.choice(FLAGS)
        st.session_state.flag = flag
        # You can use a library like 'requests' here to send data to Google Forms silently
        st.success("SESSION FINALIZED. REDIRECTING...")
        time.sleep(1.5)
        st.session_state.step = 4
        st.rerun()

# FINAL STEP: ELITE FEED
elif st.session_state.step == 4:
    st.balloons()
    st.header("ELITE_ACCESS_GRANTED")
    st.write(f"WELCOME {ELITE_USER}")
    st.info(f"EXTRACTION_KEY: {st.session_state.get('flag')}")