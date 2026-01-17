import streamlit as st
import os
import random
import time
import requests
from dotenv import load_dotenv

# 1. Load local .env only if it exists (for local development)
if os.path.exists(".env"):
    load_dotenv()

# 2. Secure Configuration Fetching
# Prioritizes Streamlit Secrets (Cloud) then Environment Variables (Local)
def get_secret(key, default=None):
    return st.secrets.get(key, os.getenv(key, default))

ELITE_USER = get_secret("ELITE_USER")
ELITE_PASS = get_secret("ELITE_PASS")
SEC_ANSWER = get_secret("SEC_ANSWER")
FORM_URL = get_secret("FORM_URL")

# Build Flag Pool dynamically from 10 possible environment variables
FLAGS = []
for i in range(1, 11):
    f = get_secret(f"FLAG_{i}")
    if f:
        FLAGS.append(f)

# --- UI SETUP ---
st.set_page_config(page_title="NASH_STTRIKE // ELITE", layout="centered")

# Custom CSS for the Cyber Division aesthetic
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ff00; font-family: 'Courier New', monospace; }
    .stTextInput>div>div>input { background-color: #000 !important; color: #00ff00 !important; border: 1px solid #00ff00 !important; }
    .stButton>button { width: 100%; background-color: #00ff00; color: #000; font-weight: bold; border: none; }
    .stButton>button:hover { background-color: #ffffff; color: #000; border: none; }
    /* Style for the terminal-like code output */
    code { color: #ffcc00 !important; }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if 'step' not in st.session_state:
    st.session_state.step = 1

# --- HEADER ---
st.title("NASH_STTRIKE")
st.write("CODING CLUB :: CYBER_DIVISION")
st.divider()

# --- STEP 1: INITIAL LOGIN ---
if st.session_state.step == 1:
    st.info("> AUTH_REQUIRED: NODE_01")
    u_input = st.text_input("IDENTIFIER", key="u_in", autocomplete="off")
    p_input = st.text_input("PASS_KEY", type="password", key="p_in")
    
    if st.button("INITIATE_BYPASS"):
        # Use .strip() to prevent whitespace errors from mobile keyboards or autofill
        if u_input.strip() == ELITE_USER and p_input.strip() == ELITE_PASS:
            st.success("[SUCCESS] Access Granted.")
            st.session_state.step = 2
            st.rerun()
        else:
            st.error("[ERROR] Access Denied. Hash Mismatch.")

# --- STEP 2: SECURITY CHALLENGE ---
elif st.session_state.step == 2:
    st.warning("> CHALLENGE_TYPE: IDENTITY_VERIFICATION")
    a_input = st.text_input("SEC_QUESTION: FAV_COLOR?", key="a_in").lower().strip()
    
    if st.button("VALIDATE_AUTH"):
        if a_input == SEC_ANSWER.lower().strip():
            st.success("[SUCCESS] Identity Confirmed.")
            st.session_state.step = 3
            st.rerun()
        else:
            st.error("[FAIL] Key Incorrect.")

# --- STEP 3: DATA EXTRACTION & FORM SUBMISSION ---
elif st.session_state.step == 3:
    st.info("> FINALIZING_REGISTRATION: DATA_TUNNEL_OPEN")
    team = st.text_input("TEAM_ID", key="t_in").strip()
    
    if st.button("COMPLETE_EXTRACTION"):
        if team and FLAGS:
            selected_flag = random.choice(FLAGS)
            st.session_state.flag = selected_flag
            
            # GOOGLE FORM SUBMISSION LOGIC
            # Browser-like headers help prevent Google from blocking the automated request
            headers = {
                "Referer": FORM_URL,
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            
            # Map your local variables to your Google Form entry IDs
            payload = {
                "entry.1988266406": team, 
                "entry.569318071": selected_flag
            }
            
            try:
                # POST data to Google Forms
                response = requests.post(FORM_URL, data=payload, headers=headers, allow_redirects=True, timeout=10)
                if response.status_code == 200 or response.status_code == 302:
                    st.success("[LOGGED] Data transmitted to Cyber Division database.")
            except Exception as e:
                # Silent failure locally so the UI doesn't crash during the event
                pass
                
            st.success("SESSION LOGGED. DECRYPTING ELITE FEED...")
            time.sleep(1.5)
            st.session_state.step = 4
            st.rerun()
        else:
            st.warning("Please enter a valid Team ID to proceed.")

# --- STEP 4: ELITE FEED ---
elif st.session_state.step == 4:
    st.balloons()
    st.header("🔱 ELITE_ACCESS_GRANTED")
    
    # Instagram-style card layout
    st.markdown(f"**User:** {ELITE_USER} | **Status:** ELITE_BYPASS_ACTIVE")
    st.image("https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&q=80&w=1000")
    
    st.markdown("### TERMINAL_OUTPUT")
    st.code(f"""
> Establish secure tunnel... [OK]
> Packet interception... [OK]
> [FLAG_CODE]: {st.session_state.get('flag')}
> [REGISTRATION]: {ELITE_USER} -> Node Breach Successful.
    """, language="bash")
    
    if st.button("TERMINATE_SESSION"):
        st.session_state.clear()
        st.rerun()