
import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="SmartSpend", layout="wide")

st.title("📊 SmartSpend – Credit Card Analyzer")

uploaded_file = st.file_uploader("Upload a credit card statement (.xlsx or .csv)", type=["xlsx", "csv"])

if uploaded_file:
    file_type = uploaded_file.name.split('.')[-1]
    if file_type == 'csv':
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file, skiprows=3)

    df.columns = [
        "transaction_date", "merchant_name", "transaction_amount",
        "charge_amount", "transaction_type", "category", "notes"
    ]
    df.dropna(subset=["transaction_date", "merchant_name"], inplace=True)
    df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors='coerce')

    st.success("✅ File uploaded and parsed successfully.")
    
    # Show raw table
    st.subheader("📋 Transactions")
    st.dataframe(df, use_container_width=True)

    # Pie chart by category
    st.subheader("📈 Category Breakdown")
    if "category" in df.columns:
        category_summary = df.groupby("category")["charge_amount"].sum().sort_values(ascending=False)
        st.bar_chart(category_summary)

    # Duplicate detection
    st.subheader("⚠️ Potential Duplicate Charges")
    duplicates = df[df.duplicated(subset=["merchant_name", "charge_amount", "transaction_date"], keep=False)]
    st.dataframe(duplicates if not duplicates.empty else pd.DataFrame({"Message": ["No duplicates found."]}))

    # Spike detection (based on category)
    st.subheader("🚨 Category Spikes (Mock Logic)")
    category_avg = df.groupby("category")["charge_amount"].mean()
    category_latest = df.groupby("category")["charge_amount"].sum()
    spikes = category_latest[category_latest > category_avg * 1.3]
    st.write(spikes if not spikes.empty else "No category spikes detected.")
