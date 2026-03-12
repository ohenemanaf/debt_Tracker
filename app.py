import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- Configuration & Data Loading ---
DATA_FILE = "debts.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["Date", "Name", "Amount", "Note"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# --- UI Setup ---
st.set_page_config(page_title="Business Debt Tracker", layout="wide")
st.title("💸 Business Debt Tracker")

df = load_data()

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
        df = pd.concat([df, new_row], ignore_index=True)
        save_data(df)
        st.sidebar.success(f"Added {name}!")
        st.rerun()

# --- Search Bar ---
search_query = st.text_input("🔍 Search for a person or business:", "")
filtered_df = df[df["Name"].str.contains(search_query, case=False, na=False)] if search_query else df

# --- Main Dashboard ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Current Debtors")
    if not filtered_df.empty:
        df_display = filtered_df.sort_values(by="Date")
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        current_total = filtered_df["Amount"].sum()
        st.metric(label="Total for Current View", value=f"${current_total:,.2f}")
    else:
        st.info("No records found.")

with col2:
    if not df.empty:
        # --- Edit / Partial Payment Section ---
        st.subheader("✏️ Edit Entry")
        person_to_edit = st.selectbox("Select to Edit/Update:", df["Name"].unique())
        
        # Get the current values for the selected person
        current_row = df[df["Name"] == person_to_edit].iloc[0]
        
        with st.form("edit_form"):
            new_amount = st.number_input("Update Amount", value=float(current_row["Amount"]), min_value=0.0)
            new_note = st.text_area("Update Notes", value=current_row["Note"])
            
            if st.form_submit_button("Save Changes"):
                # Update the value in the dataframe
                df.loc[df["Name"] == person_to_edit, "Amount"] = new_amount
                df.loc[df["Name"] == person_to_edit, "Note"] = new_note
                save_data(df)
                st.success("Record updated!")
                st.rerun()

        st.divider()
        
        # --- Mark as Paid Section ---
        st.subheader("✅ Quick Clear")
        if st.button(f"Mark {person_to_edit} as Paid"):
            df = df[df["Name"] != person_to_edit]
            save_data(df)
            st.rerun()
        
        st.divider()
        
        # --- Download Report Section ---
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(label="📥 Download CSV Report", data=csv_data, 
                           file_name=f"debt_report_{datetime.today().strftime('%Y-%m-%d')}.csv", 
                           mime='text/csv')
            
    if st.checkbox("Show Danger Zone"):
        if st.button("Clear All Data"):
            if os.path.exists(DATA_FILE):
                os.remove(DATA_FILE)
                st.rerun()import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- Configuration & Data Loading ---
DATA_FILE = "debts.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["Date", "Name", "Amount", "Note"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# --- UI Setup ---
st.set_page_config(page_title="Business Debt Tracker", layout="wide")
st.title("💸 Business Debt Tracker")

df = load_data()

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
        df = pd.concat([df, new_row], ignore_index=True)
        save_data(df)
        st.sidebar.success(f"Added {name}!")
        st.rerun()

# --- Search Bar ---
search_query = st.text_input("🔍 Search for a person or business:", "")
filtered_df = df[df["Name"].str.contains(search_query, case=False, na=False)] if search_query else df

# --- Main Dashboard ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Current Debtors")
    if not filtered_df.empty:
        df_display = filtered_df.sort_values(by="Date")
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        current_total = filtered_df["Amount"].sum()
        st.metric(label="Total for Current View", value=f"${current_total:,.2f}")
    else:
        st.info("No records found.")

with col2:
    if not df.empty:
        # --- Edit / Partial Payment Section ---
        st.subheader("✏️ Edit Entry")
        person_to_edit = st.selectbox("Select to Edit/Update:", df["Name"].unique())
        
        # Get the current values for the selected person
        current_row = df[df["Name"] == person_to_edit].iloc[0]
        
        with st.form("edit_form"):
            new_amount = st.number_input("Update Amount", value=float(current_row["Amount"]), min_value=0.0)
            new_note = st.text_area("Update Notes", value=current_row["Note"])
            
            if st.form_submit_button("Save Changes"):
                # Update the value in the dataframe
                df.loc[df["Name"] == person_to_edit, "Amount"] = new_amount
                df.loc[df["Name"] == person_to_edit, "Note"] = new_note
                save_data(df)
                st.success("Record updated!")
                st.rerun()

        st.divider()
        
        # --- Mark as Paid Section ---
        st.subheader("✅ Quick Clear")
        if st.button(f"Mark {person_to_edit} as Paid"):
            df = df[df["Name"] != person_to_edit]
            save_data(df)
            st.rerun()
        
        st.divider()
        
        # --- Download Report Section ---
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(label="📥 Download CSV Report", data=csv_data, 
                           file_name=f"debt_report_{datetime.today().strftime('%Y-%m-%d')}.csv", 
                           mime='text/csv')
            
    if st.checkbox("Show Danger Zone"):
        if st.button("Clear All Data"):
            if os.path.exists(DATA_FILE):
                os.remove(DATA_FILE)
                st.rerun()
