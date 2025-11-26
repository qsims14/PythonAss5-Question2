import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Daily Sales Trend Dashboard")

# --- File uploader ---
uploaded_file = st.file_uploader("Upload your dataset (CSV or XLSX)", type=["csv", "xlsx"])

if uploaded_file:
    # Load file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Clean column names (remove spaces only)
    df.columns = df.columns.str.strip()

    # Show columns for debugging
    st.write("Detected columns:", df.columns.tolist())

    # Check required columns
    if {"Date Ordered", "Sales"}.issubset(df.columns):

        # Convert Date Ordered to datetime
        df["Date Ordered"] = pd.to_datetime(df["Date Ordered"], errors="coerce")

        # Convert Sales to numeric
        df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")

        # Clean dataset
        df_clean = df.dropna(subset=["Date Ordered", "Sales"])

        # Group by date
        daily_sales = df_clean.groupby("Date Ordered")["Sales"].sum().sort_index()

        st.write("### Daily Sales Trend")
        st.line_chart(daily_sales)

        # Matplotlib chart
        fig, ax = plt.subplots()
        ax.plot(daily_sales.index, daily_sales.values, marker="o")
        ax.set_title("Daily Sales Trend")
        ax.set_xlabel("Date Ordered")
        ax.set_ylabel("Total Sales ($)")
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # Interpretation
        st.write("### Interpretation")
        st.write(
            "This line chart shows how total sales change over time. "
            "Higher points represent strong sales days, while lower points indicate slower performance. "
            "This helps identify patterns and peak sales periods."
        )

    else:
        st.error("Your file must include the columns: 'Date Ordered' and 'Sales'.")
else:
    st.info("Upload a CSV or Excel file to generate the daily sales trend chart.")