import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# --------------------------------------------------------
# 1. PAGE CONFIGURATION & STYLING
# --------------------------------------------------------
st.set_page_config(
    page_title="LPG Demand, Supply & Service Quality Dashboard",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main-title { font-size:36px; font-weight:bold; color:#1E3A8A; margin-bottom:5px; }
    .sub-title { font-size:16px; color:#555555; margin-bottom:25px; }
    .metric-box { background-color:#F8FAFC; padding:15px; border-radius:10px; border: 1px solid #E2E8F0; }
    .alert-box { background-color:#FEF2F2; padding:15px; border-radius:10px; border: 1px solid #FEE2E2; color:#991B1B; }
    </style>
""", unsafe_allow_html=True)

# --------------------------------------------------------
# 2. DATA LOADING & PREPROCESSING (Path-Safe Version)
# --------------------------------------------------------
@st.cache_data
def load_and_clean_data():
    # Automatically finds the CSV file whether you run from parent or source directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Try looking in the same folder as app.py first, then look one folder up
    path_options = [
        os.path.join(current_dir, "cleaned_dataset.csv"),
        os.path.join(current_dir, "..", "cleaned_dataset.csv")
    ]
    
    df_loaded = None
    for path in path_options:
        if os.path.exists(path):
            df_loaded = pd.read_csv(path)
            break
            
    if df_loaded is None:
        raise FileNotFoundError("Could not find cleaned_dataset.csv in app directory or parent directory.")

    # Fill missing values identically to notebook
    if "Iran_Israel_Conflict_Level" in df_loaded.columns:
        df_loaded["Iran_Israel_Conflict_Level"] = df_loaded["Iran_Israel_Conflict_Level"].fillna("No Conflict")
    if "Festival" in df_loaded.columns:
        df_loaded["Festival"] = df_loaded["Festival"].fillna("No Festival")
        
    return df_loaded

# Global Initialization Guard
try:
    df = load_and_clean_data()
except Exception as e:
    st.error("❌ **Dataset Location Error:** Could not find 'cleaned_dataset.csv'.")
    st.info("💡 **Quick Fix:** Please make sure your `cleaned_dataset.csv` file is placed in the folder along with your `app.py` script.")
    st.stop()

# --------------------------------------------------------
# 3. SIDEBAR CONTROLS & FILTERS
# --------------------------------------------------------
st.sidebar.header("Dashboard Filters")

available_years = sorted(df["Year"].unique().tolist())
selected_years = st.sidebar.multiselect("Select Year(s)", options=available_years, default=available_years)

available_states = sorted(df["State"].unique().tolist())
selected_states = st.sidebar.multiselect("Select State(s)", options=available_states, default=available_states)

customer_types = sorted(df["Customer_Type"].unique().tolist())
selected_cust_types = st.sidebar.multiselect("Customer Type", options=customer_types, default=customer_types)

# Securely apply filter cuts
filtered_df = df[
    (df["Year"].isin(selected_years if selected_years else available_years)) &
    (df["State"].isin(selected_states if selected_states else available_states)) &
    (df["Customer_Type"].isin(selected_cust_types if selected_cust_types else customer_types))
]

# --------------------------------------------------------
# 4. HEADER SECTION & RISK ALERTS
# --------------------------------------------------------
st.markdown('<p class="main-title">LPG Demand & Operational Supply Chain Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Strategic performance insight report tailored for executive stakeholders</p>', unsafe_allow_html=True)

delayed_shipments = filtered_df[filtered_df["Shipment_Delay_Days"] > 3]
pct_delayed = (len(delayed_shipments) / len(filtered_df) * 100) if len(filtered_df) > 0 else 0

if pct_delayed > 15:
    st.markdown(
        f'<div class="alert-box">⚠️ <b>Logistical Bottleneck Warning:</b> {pct_delayed:.1f}% of shipments '
        f'are experiencing delays over 3 days. Review the Geopolitical Strain breakdown below to adjust buffer stock.</div>', 
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)

st.markdown("---")

# --------------------------------------------------------
# 5. KPI SUMMARY METRICS
# --------------------------------------------------------
total_requested = filtered_df["Cylinders_Requested"].sum()
total_delivered = filtered_df["Cylinders_Delivered"].sum()
fulfillment_rate = (total_delivered / total_requested * 100) if total_requested > 0 else 0
total_complaints = filtered_df["Consumer_Complaints"].sum()
total_profit = filtered_df["Profit"].sum()

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    st.markdown('<div class="metric-box">', unsafe_allow_html=True)
    st.metric(label="Total Demand (Cylinders)", value=f"{total_requested:,}")
    st.markdown('</div>', unsafe_allow_html=True)
with kpi2:
    st.markdown('<div class="metric-box">', unsafe_allow_html=True)
    st.metric(label="Total Delivered", value=f"{total_delivered:,}")
    st.markdown('</div>', unsafe_allow_html=True)
with kpi3:
    st.markdown('<div class="metric-box">', unsafe_allow_html=True)
    st.metric(label="Fulfillment Rate", value=f"{fulfillment_rate:.2f}%")
    st.markdown('</div>', unsafe_allow_html=True)
with kpi4:
    st.markdown('<div class="metric-box">', unsafe_allow_html=True)
    st.metric(label="Consumer Complaints", value=f"{total_complaints:,}")
    st.markdown('</div>', unsafe_allow_html=True)
with kpi5:
    st.markdown('<div class="metric-box">', unsafe_allow_html=True)
    st.metric(label="Net Profit Margin", value=f"₹{total_profit:,.2f}")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --------------------------------------------------------
# 6. STAKEHOLDER GRAPH VISUALIZATIONS
# --------------------------------------------------------
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("📍 Demand Intensity & Resource Prioritization by State")
    state_demand = filtered_df.groupby("State")["Cylinders_Requested"].sum().reset_index()
    
    fig_demand = px.bar(
        state_demand,
        x="Cylinders_Requested",
        y="State",
        orientation='h',
        title="Total LPG Cylinder Demand by State",
        labels={"Cylinders_Requested": "Requested Volumes", "State": "State / Region"},
        color="Cylinders_Requested",
        color_continuous_scale="Blugrn"
    )
    fig_demand.update_layout(yaxis={'categoryorder': 'total ascending'}, template="plotly_white", height=400)
    # Updated parameter here for compatibility
    st.plotly_chart(fig_demand, width='stretch')

with col_right:
    st.subheader("👥 Service Quality & Customer Dissatisfaction Analysis")
    fig_complaints = px.scatter(
        filtered_df,
        x="Shipment_Delay_Days",
        y="Consumer_Complaints",
        size="Cylinders_Requested",
        color="State",
        title="Complaints vs. Shipment Delay Days (Size = Order Volume)",
        labels={"Shipment_Delay_Days": "Delay (Days)", "Consumer_Complaints": "Registered Complaints"},
        template="plotly_white"
    )
    fig_complaints.update_layout(height=400)
    # Updated parameter here for compatibility
    st.plotly_chart(fig_complaints, width='stretch')

st.markdown("---")

col_macro1, col_macro2 = st.columns(2)

with col_macro1:
    fig_oil = px.scatter(
        filtered_df,
        x="Oil_Price_USD",
        y="Domestic_LPG_Price",
        color="Customer_Type",
        trendline="ols",
        title="Domestic LPG Cylinder Price vs. Global Crude Oil Price",
        labels={"Oil_Price_USD": "Crude Oil Price ($/Barrel)", "Domestic_LPG_Price": "Domestic Cylinder Price (INR)"},
        template="plotly_white"
    )
    # Updated parameter here for compatibility
    st.plotly_chart(fig_oil, width='stretch')

with col_macro2:
    state_subsidy = filtered_df.groupby("State")["Subsidy_Amount"].mean().reset_index()
    fig_subsidy = px.bar(
        state_subsidy,
        x="State",
        y="Subsidy_Amount",
        title="Average Government Subsidy Cushion Provided per State",
        labels={"Subsidy_Amount": "Avg Subsidy Amount (INR)"},
        template="plotly_white",
        color="Subsidy_Amount",
        color_continuous_scale="YlOrRd"
    )
    # Updated parameter here for compatibility
    st.plotly_chart(fig_subsidy, width='stretch')

st.markdown("---")
st.subheader("⛓️ Supply Chain Disruption & Chokepoint Tracking")
fig_delay = px.box(
    filtered_df,
    x="Strait_of_Hormuz_Status",
    y="Shipment_Delay_Days",
    color="Iran_Israel_Conflict_Level",
    title="Impact of Maritime Chokepoint Conditions on Delay Windows",
    labels={"Strait_of_Hormuz_Status": "Strait of Hormuz Status", "Shipment_Delay_Days": "Transit Delays (Days)"},
    template="plotly_white"
)
# Updated parameter here for compatibility
st.plotly_chart(fig_delay, width='stretch')

# --------------------------------------------------------
# 7. ROOT CAUSE LAYMAN INSIGHTS & STRATEGIC RECOMMENDATIONS
# --------------------------------------------------------
st.markdown("---")
st.header("🎯 Root Cause Analysis & Action Plan")

insight_col, rec_col = st.columns(2)

with insight_col:
    st.subheader("💡 What the Data is Telling Us (Layman Insights)")
    st.markdown("""
    * **Where the System Breaks:** Regional logistics hubs in **Rajasthan, Andhra Pradesh, and Odisha** are under-resourced. They experience the highest volumes of orders left unfulfilled.
    * **The Root Cause Trigger:** Local distribution delays are tightly tied to global market stress. When maritime chokepoints close up, our inbound shipping windows instantly degrade from **3 days up to 12 days**.
    * **The Customer Fallout:** Customer anger tracks these delivery lags directly. The moment a shipment takes longer than 5 days, customer complaints double as families and commercial users face cooking gas shortages.
    """)

with rec_col:
    st.subheader("🛠️ Strategic Recommendations for Leadership")
    st.markdown("""
    1. **Build a Geopolitical 'Buffer Stock':** When conflict levels move to *Medium*, regional distribution hubs in **Karnataka** and **Andhra Pradesh** must proactively build a 10-day safety stock cushion of physical cylinders to absorb shipping delays.
    2. **Re-route Logistics Assets to Bottleneck States:** Shift excess distribution trucks and fleet capacity dynamically into **Rajasthan** and **Odisha** to clear out their unfulfilled backlog metrics.
    3. **Implement Automated Delay Warnings:** Since complaints track delays almost perfectly, send automated SMS alerts to consumers when a global supply disruption occurs. Proactive communication manages expectations before complaints are filed.
    """)

# --------------------------------------------------------
# 8. RAW DATA ACCESS TABLE
# --------------------------------------------------------
st.markdown("---")
st.subheader("🗂️ Granular Data Explorer")
with st.expander("Click to expand and inspect filtered row records"):
    # Updated parameter here for compatibility
    st.dataframe(filtered_df, width='stretch')