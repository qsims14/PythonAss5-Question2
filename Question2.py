import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Juices & Smoothies Sales Dashboard")

# Placeholder charts before any upload
st.write("### Category Sales (placeholder)")
st.bar_chart(pd.DataFrame({"Category": ["Juices", "Smoothies"], "Sales": [0, 0]}))

st.write("### Daily Sales Trend (placeholder)")
st.line_chart(pd.DataFrame({"Date": pd.date_range(start="2025-01-01", periods=5),
                            "Sales": [0, 0, 0, 0, 0]}).set_index("Date"))

# File uploader
uploaded_file = st.file_uploader("Upload your dataset (CSV or XLSX)", type=["csv", "xlsx"])

if uploaded_file:
    try:
        # Load file
        if uploaded_file.name.lower().endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # Normalize column names
        df.columns = [col.strip().capitalize() for col in df.columns]

        st.write("Columns found:", list(df.columns))
        if df.empty:
            st.warning("The uploaded file is empty.")
        else:
            # ----- Category Sales Bar Chart -----
            required_bar = {"Category", "Sales"}
            if required_bar.issubset(df.columns):
                df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
                df_bar = df.dropna(subset=["Category", "Sales"])
                if not df_bar.empty:
                    category_sales = df_bar.groupby("Category")["Sales"].sum().sort_values(ascending=False)
                    st.write("### Total Sales by Category")
                    st.dataframe(category_sales)

                    # Plot bar chart
                    fig, ax = plt.subplots()
                    ax.bar(category_sales.index, category_sales.values, color=['#1f77b4', '#ff7f0e'])
                    ax.set_title("Total Sales: Juices vs Smoothies")
                    ax.set_xlabel("Category")
                    ax.set_ylabel("Total Sales ($)")
                    plt.xticks(rotation=45)
                    st.pyplot(fig)
                    plt.close(fig)
                else:
                    st.warning("No valid sales data to plot for categories.")
            else:
                st.error("Missing required columns for category sales: 'Category' and 'Sales'")

            # ----- Daily Sales Line Chart -----
            required_line = {"Date Ordered", "Sales"}
            if required_line.issubset(df.columns):
                df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
                df["Date Ordered"] = pd.to_datetime(df["Date Ordered"], errors="coerce")
                df_line = df.dropna(subset=["Date Ordered", "Sales"])
                if not df_line.empty:
                    daily_sales = df_line.groupby("Date Ordered")["Sales"].sum().sort_index()
                    st.write("### Daily Sales Over Time")
                    st.line_chart(daily_sales)

                    # Optional Matplotlib plot
                    fig, ax = plt.subplots()
                    ax.plot(daily_sales.index, daily_sales.values, marker='o', linestyle='-')
                    ax.set_title("Daily Sales Trend")
                    ax.set_xlabel("Date Ordered")
                    ax.set_ylabel("Total Sales ($)")
                    plt.xticks(rotation=45)
                    st.pyplot(fig)
                    plt.close(fig)

                    st.write("### Interpretation:")
                    st.write(
                        "This line chart shows the trend of total sales over time. "
                        "Peaks represent days with high sales, dips represent slower sales days. "
                        "Patterns and seasonality can be observed from this trend."
                    )
                else:
                    st.warning("No valid data to plot daily sales.")
            else:
                st.error("Missing required columns for daily sales: 'Date Ordered' and 'Sales'")

    except Exception as e:
        st.error("An unexpected error occurred while processing the file.")
        st.text(str(e))
else:
    st.info("Upload a CSV or XLSX file with columns for 'Category', 'Sales', and 'Date Ordered'.")