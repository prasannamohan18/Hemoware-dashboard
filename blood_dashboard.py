import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

# ---------------- DATABASE ----------------
conn = sqlite3.connect("bloodbank.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS donors (
    name TEXT,
    age INTEGER,
    blood_group TEXT
)
""")

# ---------------- LOGIN ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.title("🔐 Blood Bank Login")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == "admin" and pwd == "1234":
            st.session_state.logged_in = True
        else:
            st.error("Invalid Login")

if not st.session_state.logged_in:
    login()
    st.stop()

# ---------------- SIDEBAR ----------------
st.sidebar.title("🩸 Menu")
menu = st.sidebar.radio("Navigation", ["Dashboard", "Add Donor", "View Donors", "Prediction", "Map"])

# ---------------- DATA ----------------
data = {
    "Blood Group": ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"],
    "Available": [50, 20, 45, 15, 60, 25, 30, 10],
    "Requested": [40, 15, 35, 10, 55, 20, 25, 5]
}
df = pd.DataFrame(data)

# ---------------- DASHBOARD ----------------
if menu == "Dashboard":
    st.title("📊 Blood Bank Dashboard")

    col1, col2 = st.columns(2)
    col1.metric("Total Available", df["Available"].sum())
    col2.metric("Total Requested", df["Requested"].sum())

    st.subheader("Filter")
    group = st.selectbox("Blood Group", df["Blood Group"])
    st.dataframe(df[df["Blood Group"] == group])

    fig, ax = plt.subplots()
    ax.bar(df["Blood Group"], df["Available"])
    st.pyplot(fig)

# ---------------- ADD DONOR ----------------
elif menu == "Add Donor":
    st.title("📝 Add Donor")

    name = st.text_input("Name")
    age = st.number_input("Age", 18, 60)
    blood = st.selectbox("Blood Group", df["Blood Group"])

    if st.button("Save"):
        cursor.execute("INSERT INTO donors VALUES (?, ?, ?)", (name, age, blood))
        conn.commit()
        st.success("Donor Saved!")

# ---------------- VIEW DONORS ----------------
elif menu == "View Donors":
    st.title("📁 Donor Records")

    data = pd.read_sql_query("SELECT * FROM donors", conn)
    st.dataframe(data)

# ---------------- PREDICTION ----------------
elif menu == "Prediction":
    st.title("🤖 Demand Prediction")

    df["Predicted"] = df["Requested"] + 5
    st.dataframe(df)

    fig, ax = plt.subplots()
    ax.bar(df["Blood Group"], df["Predicted"])
    st.pyplot(fig)

# ---------------- MAP ----------------
elif menu == "Map":
    st.title("🌍 Blood Bank Locations")

    map_data = pd.DataFrame({
        "lat": [13.0827, 12.9716, 11.0168],
        "lon": [80.2707, 77.5946, 76.9558]
    })

    st.map(map_data)
