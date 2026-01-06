import streamlit as st
import pandas as pd
import pyodbc
import plotly.express as px

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Ola Ride Insights - Streamlit",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 Ola Ride Insights Dashboard")
st.markdown("Interactive SQL-powered analytics dashboard built using Streamlit")

# -------------------- DB CONNECTION --------------------
@st.cache_resource
def get_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=YOUR_SERVER_NAME;"
        "DATABASE=YOUR_DATABASE_NAME;"
        "Trusted_Connection=yes;"
    )

conn = get_connection()

# -------------------- SIDEBAR FILTERS --------------------
st.sidebar.header("🔍 Filters")

# Date filter
date_df = pd.read_sql(
    "SELECT DISTINCT Date FROM ola_rides_clean ORDER BY Date",
    conn
)

start_date, end_date = st.sidebar.date_input(
    "Select Date Range",
    [date_df["Date"].min(), date_df["Date"].max()]
)

# Vehicle type filter
vehicle_df = pd.read_sql(
    "SELECT DISTINCT Vehicle_Type FROM ola_rides_clean",
    conn
)

vehicle_filter = st.sidebar.multiselect(
    "Vehicle Type",
    vehicle_df["Vehicle_Type"],
    default=list(vehicle_df["Vehicle_Type"])
)

# -------------------- VIEW SELECTION --------------------
view = st.sidebar.radio(
    "Select Dashboard View",
    ["Overall", "Vehicle Type", "Revenue", "Cancellation", "Ratings"]
)

# -------------------- BASE FILTER --------------------
base_filter = f"""
WHERE Date BETWEEN '{start_date}' AND '{end_date}'
AND Vehicle_Type IN ({','.join("'" + v + "'" for v in vehicle_filter)})
"""

# ======================================================
# 1️⃣ OVERALL VIEW
# ======================================================
if view == "Overall":
    st.header("📊 Overall Ride Analysis")

    # Ride Volume Over Time
    q1 = f"""
    SELECT Date, COUNT(Booking_ID) AS Total_Rides
    FROM ola_rides_clean
    {base_filter}
    GROUP BY Date
    ORDER BY Date
    """
    df1 = pd.read_sql(q1, conn)

    st.subheader("Ride Volume Over Time")
    st.code(q1, language="sql")
    st.dataframe(df1)

    fig1 = px.line(df1, x="Date", y="Total_Rides", markers=True)
    st.plotly_chart(fig1, use_container_width=True)

    # Booking Status Breakdown
    q2 = f"""
    SELECT Booking_Status, COUNT(*) AS Count
    FROM ola_rides_clean
    {base_filter}
    GROUP BY Booking_Status
    """
    df2 = pd.read_sql(q2, conn)

    st.subheader("Booking Status Breakdown")
    st.code(q2, language="sql")
    st.dataframe(df2)

    fig2 = px.pie(df2, names="Booking_Status", values="Count")
    st.plotly_chart(fig2, use_container_width=True)

# ======================================================
# 2️⃣ VEHICLE TYPE VIEW
# ======================================================
elif view == "Vehicle Type":
    st.header("🚕 Vehicle Type Insights")

    q = f"""
    SELECT TOP 5 Vehicle_Type,
           SUM(Ride_Distance) AS Total_Distance
    FROM ola_rides_clean
    {base_filter}
    GROUP BY Vehicle_Type
    ORDER BY Total_Distance DESC
    """
    df = pd.read_sql(q, conn)

    st.subheader("Top 5 Vehicle Types by Ride Distance")
    st.code(q, language="sql")
    st.dataframe(df)

    fig = px.bar(df, x="Vehicle_Type", y="Total_Distance", text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

# ======================================================
# 3️⃣ REVENUE VIEW
# ======================================================
elif view == "Revenue":
    st.header("💰 Revenue Analysis")

    # Revenue by Payment Method
    q1 = f"""
    SELECT 
        Payment_Method,
        SUM(Booking_Value) AS Total_Revenue
        FROM ola_rides_clean
        {base_filter}
        AND Payment_Method IS NOT NULL
        AND Payment_Method <> 'null'
        AND Payment_Method <> ''
        GROUP BY Payment_Method
        ORDER BY Total_Revenue DESC
        """
    df1 = pd.read_sql(q1, conn)

    st.subheader("Revenue by Payment Method")
    st.code(q1, language="sql")
    st.dataframe(df1, use_container_width=True)

    fig1 = px.bar(
        df1,
        x="Payment_Method",
        y="Total_Revenue",
        title="Revenue by Payment Method"
    )
    st.plotly_chart(fig1, use_container_width=True)


    # Top 5 Customers
    q2 = f"""
    SELECT TOP 5 Customer_ID,
           SUM(Booking_Value) AS Total_Booking_Value
    FROM ola_rides_clean
    {base_filter}
    GROUP BY Customer_ID
    ORDER BY Total_Booking_Value DESC
    """
    df2 = pd.read_sql(q2, conn)

    st.subheader("Top 5 Customers by Total Booking Value")
    st.code(q2, language="sql")
    st.dataframe(df2)

    fig2 = px.bar(df2, x="Customer_ID", y="Total_Booking_Value")
    st.plotly_chart(fig2, use_container_width=True)

    # Ride Distance Per Day
    q3 = f"""
    SELECT 
        Date,
        SUM(Ride_Distance) AS Total_Distance
        FROM ola_rides_clean
        {base_filter}
        AND Ride_Distance IS NOT NULL
        GROUP BY Date
        ORDER BY Date
        """
    df3 = pd.read_sql(q3, conn)

    st.subheader("Ride Distance Trend Per Day")
    st.code(q3, language="sql")
    st.dataframe(df3, use_container_width=True)

    fig3 = px.line(
        df3,
        x="Date",
        y="Total_Distance",
        markers=True,
        title="Daily Ride Distance Trend"
    )
    st.plotly_chart(fig3, use_container_width=True)


# ======================================================
# 4️⃣ CANCELLATION VIEW
# ======================================================
elif view == "Cancellation":
    st.header("❌ Cancellation Analysis")

    # ---------------- CUSTOMER CANCELLATION ----------------
    q1 = f"""
    SELECT 
        Canceled_Rides_by_Customer AS Reason,
        COUNT(*) AS Count
    FROM ola_rides_clean
    {base_filter}
    AND Canceled_Rides_by_Customer IS NOT NULL
    AND Canceled_Rides_by_Customer <> 'null'
    AND Canceled_Rides_by_Customer <> ''
    GROUP BY Canceled_Rides_by_Customer
    ORDER BY Count DESC
    """
    df1 = pd.read_sql(q1, conn)

    st.subheader("Cancelled Rides Reasons (Customer)")
    st.code(q1, language="sql")
    st.dataframe(df1, use_container_width=True)

    if not df1.empty:
        fig1 = px.pie(
            df1,
            names="Reason",
            values="Count",
            title="Customer Cancellation Reasons"
        )
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("No customer cancellation data available for selected filters.")

    # ---------------- DRIVER CANCELLATION ----------------
    q2 = f"""
    SELECT 
        Canceled_Rides_by_Driver AS Reason,
        COUNT(*) AS Count
    FROM ola_rides_clean
    {base_filter}
    AND Canceled_Rides_by_Driver IS NOT NULL
    AND Canceled_Rides_by_Driver <> 'null'
    AND Canceled_Rides_by_Driver <> ''
    GROUP BY Canceled_Rides_by_Driver
    ORDER BY Count DESC
    """
    df2 = pd.read_sql(q2, conn)

    st.subheader("Cancelled Rides Reasons (Driver)")
    st.code(q2, language="sql")
    st.dataframe(df2, use_container_width=True)

    if not df2.empty:
        fig2 = px.pie(
            df2,
            names="Reason",
            values="Count",
            title="Driver Cancellation Reasons"
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No driver cancellation data available for selected filters.")

# ======================================================
# 5️⃣ RATINGS VIEW
# ======================================================
elif view == "Ratings":
    st.header("⭐ Ratings Analysis")

    # Driver ratings
    q1 = f"""
    SELECT Driver_Ratings
    FROM ola_rides_clean
    {base_filter}
    AND Driver_Ratings IS NOT NULL
    """
    df1 = pd.read_sql(q1, conn)

    st.subheader("Driver Ratings Distribution")
    st.code(q1, language="sql")
    fig1 = px.histogram(df1, x="Driver_Ratings", nbins=10)
    st.plotly_chart(fig1, use_container_width=True)

    # Customer ratings
    q2 = f"""
    SELECT Customer_Rating
    FROM ola_rides_clean
    {base_filter}
    AND Customer_Rating IS NOT NULL
    """
    df2 = pd.read_sql(q2, conn)

    st.subheader("Customer Ratings Distribution")
    st.code(q2, language="sql")
    fig2 = px.histogram(df2, x="Customer_Rating", nbins=10)
    st.plotly_chart(fig2, use_container_width=True)
