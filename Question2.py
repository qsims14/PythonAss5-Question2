import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Daily Sales Trend Dashboard")

# ----- File uploader -----
uploaded_file = st.file_uploader("Upload your dataset (CSV or XLSX)", type=["csv", "xlsx"])

if uploaded_file:
    try:
        # Load the file
        if uploaded_file.name.lower().endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # Normalize column names
        df.columns = [col.strip().capitalize() for col in df.columns]

        st.write("Columns found:", list(df.columns))

        # Check required columns
        if {"Date Ordered", "Sales"}.issubset(df.columns):
            # Convert Date Ordered to datetime
            df["Date Ordered"] = pd.to_datetime(df["Date Ordered"], errors="coerce")
            df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")

            # Drop rows with missing Date or Sales
            df_clean = df.dropna(subset=["Date Ordered", "Sales"])

            if not df_clean.empty:
                # Group by date and sum sales
                daily_sales = df_clean.groupby("Date Ordered")["Sales"].sum().sort_index()

                # ----- Streamlit line chart -----
                st.write("### Daily Sales Over Time")
                st.line_chart(daily_sales)

                # ----- Optional Matplotlib chart -----
                fig, ax = plt.subplots()
                ax.plot(daily_sales.index, daily_sales.values, marker='o', linestyle='-')
                ax.set_title("Daily Sales Trend")
                ax.set_xlabel("Date Ordered")
                ax.set_ylabel("Total Sales ($)")
                plt.xticks(rotation=45)
                st.pyplot(fig)
                plt.close(fig)

                # ----- Interpretation -----
                st.write("### Interpretation:")
                st.write(
                    "This line chart shows the trend of total sales over time. "
                    "Peaks indicate days with higher sales, while dips indicate slower days. "
                    "This helps identify patterns, seasonality, and sales performance over time."
                )
            else:
                st.warning("No valid data found to plot daily sales.")
        else:
            st.error("The dataset must include 'Date Ordered' and 'Sales' columns.")

    except Exception as e:
        st.error("An error occurred while processing the file.")
        st.text(str(e))
else:
    st.info("Upload a CSV or XLSX file with 'Date Ordered' and 'Sales' columns to view the daily sales trend.")