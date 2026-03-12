import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# --- UI Setup ---
st.set_page_config(page_title="Business Debt Tracker", layout="wide")
st.title("💸 Business Debt Tracker (Cloud Sync)")

# --- Database Connection (Google Sheets) ---
# Ensure you have your URL in the Streamlit Secrets!
conn = st.connection("gsheets", type=GSheetsConnection)

# Load data from the sheet
try:
    df = conn.read()
except Exception:
    # If the sheet is empty or can't be read, create an empty DataFrame
    df = pd.DataFrame(columns=["Date", "Name", "Amount", "Note"])

# --- Sidebar: Add New Entry ---
st.sidebar.header("➕ Add New Debt")
with st.sidebar.form("debt_form", clear_on_submit=True):
    name = st.text_input("Person/Business Name")
    amount = st.number_input("Amount Owed", min_value=0.0, step=0.01)
    note = st.text_area("Notes")
    submit = st.form_submit_button("Add Entry")

    if submit and name:
        today = datetime.today().strftime('%Y-%m-%d')
        new_row = pd.DataFrame({"Date": [today], "Name": [name], "Amount": [amount], "Note": [note]})
        updated_df = pd.concat([df, new_row], ignore_index=True)
        conn.update(data=updated_df)
        st.sidebar.success(f"Saved to Google Sheets!")
        st.rerun()

# --- Search Bar ---
search_query = st.text_input("🔍 Search names:", "")
filtered_df = df[df["Name"].str.contains(search_query, case=False, na=False)] if (not df.empty and search_query) else df

# --- Main Dashboard ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Current Debtors")
    if not filtered_df.empty:
        st.dataframe(filtered_df.sort_values(by="Date"), use_container_width=True, hide_index=True)
        st.metric(label="Total Outstanding", value=f"${filtered_df['Amount'].sum():,.2f}")
    else:
        st.info("No records found.")

with col2:
    if not df.empty:
        st.subheader("✅ Actions")
        person_to_action = st.selectbox("Select person:", df["Name"].unique())
        
        if st.button("Clear Debt (Paid)"):
            updated_df = df[df["Name"] != person_to_action]
            conn.update(data=updated_df)
            st.success(f"Cleared {person_to_action}!")
            st.rerun()
