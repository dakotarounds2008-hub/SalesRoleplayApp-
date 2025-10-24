# sales_training_app.py
import streamlit as st
import pandas as pd
import random
from datetime import datetime

st.set_page_config(page_title="Sales Roleplay Simulator", layout="wide")

st.title("🔥 Sales Roleplay Simulator")

# ---------- User Login ----------
if 'username' not in st.session_state:
    st.session_state['username'] = ''

if not st.session_state['username']:
    username = st.text_input("Enter your name for leaderboard tracking:")
    if st.button("Start"):
        st.session_state['username'] = username
else:
    username = st.session_state['username']
    st.write(f"Welcome, **{username}**!")

# ---------- Define Industries and Objections ----------
industries = {
    "Fiber/Internet": {
        "objections": {
            "too expensive": [
                "I hear you. Many neighbors thought the same, but they end up saving over time with our plan.",
                "Understood. If I could show a way to get faster internet for cheaper, would you consider it?"
            ],
            "not interested": [
                "No problem. Can I quickly show why many people switch to our service?",
                "I understand. May I ask who you currently use?"
            ],
            "need to talk to spouse": [
                "Absolutely, would it help if I gave a clear comparison to share with them?",
                "Totally, can I explain the offer so you both see the benefits?"
            ]
        }
    },
    "Pest Control": {
        "objections": {
            "too expensive": [
                "I understand. Most customers find that avoiding infestations saves way more in the long run.",
                "I hear you. If I could offer a package that prevents issues efficiently, would that help?"
            ],
            "already using another company": [
                "I get that. Many switched after comparing effectiveness and pricing with us.",
                "Understood. Can I show you a plan that targets the pests better and costs less?"
            ],
            "don’t need it": [
                "I understand. May I ask if you’ve had issues in the past or just want preventive coverage?",
                "Many customers thought the same but were surprised by unseen infestations we prevent."
            ]
        }
    },
    "Alarms/Security": {
        "objections": {
            "too expensive": [
                "I hear you. Our packages are cost-effective for 24/7 protection.",
                "I understand. If I can show a way to protect your home for less than your daily coffee, would you consider it?"
            ],
            "already have a system": [
                "Got it. Many clients upgraded to our system for better monitoring and lower cost.",
                "I understand. Can I show why our system is more reliable?"
            ],
            "don’t need it": [
                "I understand. Would you mind if I quickly explained why most neighbors prefer proactive security?",
                "Many people think that, but after a break-in in the neighborhood, they wished they had coverage."
            ]
        }
    }
}

industry_choice = st.selectbox("Select Industry", list(industries.keys()))

# ---------- Roleplay Logic ----------
if st.button("Start Roleplay"):
    objections = industries[industry_choice]["objections"]
    customer_objection = random.choice(list(objections.keys()))
    st.session_state['current_objection'] = customer_objection
    st.session_state['responses'] = objections[customer_objection]
    st.session_state['start_time'] = datetime.now()

if 'current_objection' in st.session_state:
    st.write(f"**Customer objection:** {st.session_state['current_objection'].capitalize()}")
    response_choice = st.radio("Choose your response:", st.session_state['responses'])
    if st.button("Submit Response"):
        # Evaluate response
        success = random.choice([True, False])  # Can later be based on “best practice” mapping
        st.write(f"**You responded:** {response_choice}")
        if success:
            st.success("Customer seems interested! You handled it well.")
            st.session_state['last_result'] = 'Closed'
        else:
            st.warning("Customer walked away. Try to improve your pitch next time.")
            st.session_state['last_result'] = 'Lost'

        # Store results in CSV for leaderboard
        try:
            df = pd.read_csv("leaderboard.csv")
        except FileNotFoundError:
            df = pd.DataFrame(columns=['Username','Industry','Objection','Response','Result','Time'])
        new_row = {
            "Username": username,
            "Industry": industry_choice,
            "Objection": st.session_state['current_objection'],
            "Response": response_choice,
            "Result": st.session_state['last_result'],
            "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv("leaderboard.csv", index=False)
        st.session_state['current_objection'] = None

# ---------- Leaderboard ----------
st.header("🏆 Leaderboard")
try:
    df = pd.read_csv("leaderboard.csv")
    leaderboard = df.groupby('Username').apply(lambda x: (x['Result']=='Closed').sum()/len(x)*100).reset_index()
    leaderboard.columns = ['Username', 'Close %']
    leaderboard = leaderboard.sort_values(by='Close %', ascending=False)
    st.dataframe(leaderboard)
except FileNotFoundError:
    st.write("No leaderboard data yet. Be the first to play!")
