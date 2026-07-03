import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------
st.set_page_config(
    page_title="LPG Supply Chain & Distribution Analytics",
    page_icon="📊",
    layout="wide"
)

# ---------------------------------------------------
# Load Dataset
# ---------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, "datasets", "cleaned_dataset.csv")

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

df = load_data()

# ---------------------------------------------------
# Sidebar Filters
# ---------------------------------------------------
st.sidebar.title("Dashboard Filters")

year = st.sidebar.multiselect(
    "Select Year",
    sorted(df["Year"].unique()),
    default=sorted(df["Year"].unique())
)

state = st.sidebar.multiselect(
    "Select State",
    sorted(df["State"].unique()),
    default=sorted(df["State"].unique())
)

customer = st.sidebar.multiselect(
    "Customer Type",
    sorted(df["Customer_Type"].unique()),
    default=sorted(df["Customer_Type"].unique())
)

filtered_df = df[
    (df["Year"].isin(year)) &
    (df["State"].isin(state)) &
    (df["Customer_Type"].isin(customer))
]

# ---------------------------------------------------
# Dashboard Title
# ---------------------------------------------------
st.title("📦 LPG Supply Chain & Distribution Analytics")

st.markdown(
"""
Business Dashboard for Monitoring LPG Demand, Supply,
Revenue, Delivery Performance and Geopolitical Risks.
"""
)

st.markdown("---")

# ---------------------------------------------------
# KPI Cards
# ---------------------------------------------------

delivery_rate = (
    filtered_df["Cylinders_Delivered"].sum()
    / filtered_df["Cylinders_Requested"].sum()
) * 100

avg_delay = filtered_df["Shipment_Delay_Days"].mean()

avg_price = filtered_df["Domestic_LPG_Price"].mean()

total_revenue = filtered_df["Revenue"].sum()

total_profit = filtered_df["Profit"].sum()

complaints = filtered_df["Consumer_Complaints"].sum()

col1,col2,col3,col4,col5,col6 = st.columns(6)

col1.metric(
    "Revenue",
    f"₹ {total_revenue:,.0f}"
)

col2.metric(
    "Profit",
    f"₹ {total_profit:,.0f}"
)

col3.metric(
    "Delivery Rate",
    f"{delivery_rate:.1f}%"
)

col4.metric(
    "Avg Delay",
    f"{avg_delay:.1f} Days"
)

col5.metric(
    "Complaints",
    f"{complaints:,}"
)

col6.metric(
    "Avg LPG Price",
    f"₹ {avg_price:.0f}"
)

st.markdown("---")

# =====================================================
# CHART ROW 1
# =====================================================

col1, col2 = st.columns(2)

with col1:

    demand = filtered_df.groupby("Month")[["Cylinders_Requested","Cylinders_Delivered"]].sum().reset_index()

    fig = px.bar(
        demand,
        x="Month",
        y=["Cylinders_Requested","Cylinders_Delivered"],
        barmode="group",
        title="Demand vs Cylinders Delivered",
        color_discrete_sequence=["#1f77b4","#2ca02c"]
    )

    fig.update_layout(height=450)

    st.plotly_chart(fig, use_container_width=True)


with col2:

    revenue = filtered_df.groupby("Month")["Revenue"].sum().reset_index()

    fig = px.line(
        revenue,
        x="Month",
        y="Revenue",
        markers=True,
        title="Monthly Revenue Trend"
    )

    fig.update_layout(height=450)

    st.plotly_chart(fig, use_container_width=True)


# =====================================================
# CHART ROW 2
# =====================================================

col3, col4 = st.columns(2)

with col3:

    profit = filtered_df.groupby("Month")["Profit"].sum().reset_index()

    fig = px.area(
        profit,
        x="Month",
        y="Profit",
        title="Monthly Profit Trend"
    )

    fig.update_layout(height=450)

    st.plotly_chart(fig, use_container_width=True)


with col4:

    delay = filtered_df.groupby("Month")["Shipment_Delay_Days"].mean().reset_index()

    fig = px.line(
        delay,
        x="Month",
        y="Shipment_Delay_Days",
        markers=True,
        title="Average Shipment Delay"
    )

    fig.update_layout(height=450)

    st.plotly_chart(fig, use_container_width=True)


# =====================================================
# CHART ROW 3
# =====================================================

col5, col6 = st.columns(2)

with col5:

    fig = px.scatter(
        filtered_df,
        x="Oil_Price_USD",
        y="Domestic_LPG_Price",
        color="Iran_Israel_Conflict_Level",
        size="Shipment_Delay_Days",
        hover_name="State",
        title="Oil Price vs Domestic LPG Price"
    )

    fig.update_layout(height=450)

    st.plotly_chart(fig, use_container_width=True)


with col6:

    fig = px.box(
        filtered_df,
        x="Iran_Israel_Conflict_Level",
        y="Shipment_Delay_Days",
        color="Iran_Israel_Conflict_Level",
        title="Conflict Level vs Shipment Delay"
    )

    fig.update_layout(height=450)

    st.plotly_chart(fig, use_container_width=True)


# =====================================================
# CHART ROW 4
# =====================================================

col7, col8 = st.columns(2)

with col7:

    state_rev = filtered_df.groupby("State")["Revenue"].sum().reset_index()

    state_rev = state_rev.sort_values(
        by="Revenue",
        ascending=False
    )

    fig = px.bar(
        state_rev,
        x="Revenue",
        y="State",
        orientation="h",
        title="Revenue by State"
    )

    fig.update_layout(height=500)

    st.plotly_chart(fig, use_container_width=True)


with col8:

    complaints = filtered_df.groupby("State")["Consumer_Complaints"].sum().reset_index()

    complaints = complaints.sort_values(
        by="Consumer_Complaints",
        ascending=False
    )

    fig = px.bar(
        complaints,
        x="Consumer_Complaints",
        y="State",
        orientation="h",
        title="Consumer Complaints by State",
        color="Consumer_Complaints"
    )

    fig.update_layout(height=500)

    st.plotly_chart(fig, use_container_width=True)

    # =====================================================
# EXECUTIVE INSIGHTS
# =====================================================

st.markdown("---")
st.header("📋 Executive Business Insights")

highest_revenue_state = (
    filtered_df.groupby("State")["Revenue"]
    .sum()
    .idxmax()
)

highest_profit_state = (
    filtered_df.groupby("State")["Profit"]
    .sum()
    .idxmax()
)

highest_delay_state = (
    filtered_df.groupby("State")["Shipment_Delay_Days"]
    .mean()
    .idxmax()
)

highest_complaints_state = (
    filtered_df.groupby("State")["Consumer_Complaints"]
    .sum()
    .idxmax()
)

delivery_rate = (
    filtered_df["Cylinders_Delivered"].sum()
    / filtered_df["Cylinders_Requested"].sum()
) * 100

st.success(f"""
### Key Business Insights

✅ Highest Revenue State : **{highest_revenue_state}**

💰 Highest Profit State : **{highest_profit_state}**

🚚 Highest Shipment Delay : **{highest_delay_state}**

☎ Highest Consumer Complaints : **{highest_complaints_state}**

📦 Overall Delivery Rate : **{delivery_rate:.2f}%**

""")

# =====================================================
# TOP 5 STATES
# =====================================================

st.markdown("---")
st.subheader("🏆 Top 5 Revenue Generating States")

top5 = (
    filtered_df.groupby("State")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)

fig = px.bar(
    top5,
    x="State",
    y="Revenue",
    color="Revenue",
    text_auto=".2s",
    title="Top 5 States by Revenue"
)

st.plotly_chart(fig, use_container_width=True)

# =====================================================
# FESTIVAL ANALYSIS
# =====================================================

st.markdown("---")
st.subheader("🎉 Festival vs LPG Demand")

festival = (
    filtered_df.groupby("Festival")["Cylinders_Requested"]
    .sum()
    .reset_index()
)

fig = px.pie(
    festival,
    names="Festival",
    values="Cylinders_Requested",
    hole=0.5,
    title="Festival-wise LPG Demand"
)

st.plotly_chart(fig, use_container_width=True)

# =====================================================
# DOWNLOAD DATA
# =====================================================

st.markdown("---")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Dataset",
    data=csv,
    file_name="LPG_Dashboard_Report.csv",
    mime="text/csv"
)

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.markdown(
"""
<center>

### LPG Supply Chain & Distribution Analytics

Developed using Streamlit • Plotly • Python

Educational Project

</center>
""",
unsafe_allow_html=True
)