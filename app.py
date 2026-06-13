import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Banking Statistics Dashboard",
    page_icon="🏦",
    layout="wide"
)
st.markdown("""
<style>

/* =========================
   FINTECH BACKGROUND IMAGE
========================= */
.stApp {
    background: url("/mnt/data/a_clean_modern_fintech_banking_themed_backgroun.png");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* =========================
   GLASS OVERLAY LAYER
========================= */
.stApp::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(255, 255, 255, 0.55);
    backdrop-filter: blur(10px);
    z-index: 0;
}

/* Keep content above overlay */
.block-container {
    position: relative;
    z-index: 1;
}

/* =========================
   SIDEBAR GLASS EFFECT
========================= */
[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.6);
    backdrop-filter: blur(12px);
    border-right: 1px solid rgba(255, 255, 255, 0.3);
}

/* =========================
   GLASS KPI CARDS
========================= */
[data-testid="metric-container"] {
    background: rgba(255, 255, 255, 0.35);
    backdrop-filter: blur(15px);
    border-radius: 16px;
    padding: 18px;
    border: 1px solid rgba(255, 255, 255, 0.4);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
}

/* =========================
   CHART / CONTAINER GLASS
========================= */
div[data-testid="stVerticalBlock"] > div {
    background: rgba(255, 255, 255, 0.25);
    backdrop-filter: blur(12px);
    border-radius: 14px;
    padding: 10px;
    border: 1px solid rgba(255, 255, 255, 0.3);
}

/* =========================
   HEADINGS (clean fintech look)
========================= */
h1, h2, h3, h4, h5, h6 {
    color: #0f172a !important;
    font-weight: 600;
    letter-spacing: 0.2px;
}

/* =========================
   REMOVE DEFAULT SPACING CLUTTER
========================= */
.css-1d391kg {
    padding-top: 1rem;
}
/* Make all text black */
html, body, [class*="css"] {
    color: black !important;
}

/* Streamlit text elements */
p, span, div, label, li, td, th {
    color: black !important;
}

/* Sidebar text */
[data-testid="stSidebar"] * {
    color: black !important;
}

/* Metric values and labels */
[data-testid="metric-container"] * {
    color: black !important;
}

/* Info, Success, Warning boxes */
[data-testid="stAlert"] * {
    color: black !important;
}

/* Tabs */
button[data-baseweb="tab"] {
    color: black !important;
}

/* Dataframe text */
[data-testid="stDataFrame"] * {
    color: black !important;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# LOAD DATA
# ==================================================
@st.cache_data
def load_data():
    df = pd.read_csv("bankwise-atm-pos-card-statistics-2022-onwards.csv")

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce",
        dayfirst=True
    )

    df = df.dropna(subset=["date"])

    return df

df = load_data()

# ==================================================
# HEADER
# ==================================================
st.title("🏦 Bank-wise ATM, POS & Card Statistics Dashboard")

st.markdown("""
<div style='
background: linear-gradient(90deg,#1e3a8a,#2563eb);
padding:25px;
border-radius:15px;
text-align:center;
margin-bottom:20px;
'>

<h1 style='color:white;'>
🏦 Banking Statistics Dashboard
</h1>

<p style='color:white;font-size:18px;'>
Comprehensive analysis of ATM Networks, POS Infrastructure,
Card Issuance and Digital Payment Trends across Indian Banks.
</p>

</div>
""", unsafe_allow_html=True)

st.info("""
### 📖 About Banking Statistics

This dashboard provides insights into India's banking ecosystem.

Key Focus Areas:

• ATM & CRM Infrastructure

• POS Deployment

• Credit & Debit Card Adoption

• QR Payment Growth

• Digital Transaction Trends

• Bank Category Performance

The dashboard helps identify growth opportunities,
digital adoption patterns, and infrastructure expansion.
""")

# ==================================================
# SIDEBAR FILTERS
# ==================================================
st.sidebar.header("🔍 Dashboard Filters")

# Bank Category
selected_category = st.sidebar.multiselect(
    "Bank Category",
    options=sorted(df["bank_category"].dropna().unique()),
    default=sorted(df["bank_category"].dropna().unique())
)

filtered_df = df[
    df["bank_category"].isin(selected_category)
]

# Bank Name
selected_bank = st.sidebar.multiselect(
    "Bank Name",
    options=sorted(filtered_df["bank_name"].dropna().unique()),
    default=sorted(filtered_df["bank_name"].dropna().unique())
)

filtered_df = filtered_df[
    filtered_df["bank_name"].isin(selected_bank)
]

# Date Range
if not filtered_df.empty:

    min_date = filtered_df["date"].min().date()
    max_date = filtered_df["date"].max().date()

    date_range = st.sidebar.date_input(
        "Date Range",
        value=(min_date, max_date)
    )

    if len(date_range) == 2:
        filtered_df = filtered_df[
            (filtered_df["date"] >= pd.Timestamp(date_range[0]))
            & (filtered_df["date"] <= pd.Timestamp(date_range[1]))
        ]

# Top N Selector
top_n = st.sidebar.slider(
    "Top Banks",
    min_value=5,
    max_value=20,
    value=10
)

# ==================================================
# KPI SECTION
# ==================================================
total_banks = filtered_df["bank_name"].nunique()

total_atm = (
    filtered_df["atms_crms_onsite"].sum()
    + filtered_df["atms_crms_offsite"].sum()
)

total_pos = filtered_df["pos"].sum()

total_credit = filtered_df["credit_cards"].sum()

total_debit = filtered_df["debit_cards"].sum()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("🏦 Banks", f"{total_banks:,}")

col2.metric(
    "🏧 Total ATMs",
    f"{total_atm:,.0f}"
)

col3.metric(
    "💳 POS",
    f"{total_pos:,.0f}"
)

col4.metric(
    "💳 Credit Cards",
    f"{total_credit:,.0f}"
)

col5.metric(
    "🏦 Debit Cards",
    f"{total_debit:,.0f}"
)

st.divider()

# ==================================================
# TABS
# ==================================================
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "Overview",
    "Infrastructure",
    "Cards",
    "Transactions",
    "Categories",
    "Insights",
    "Heatmap",
    "Data"
])

# ==================================================
# OVERVIEW
# ==================================================
with tab1:

    st.subheader("🏆 Top Banks by POS")

    top_pos = (
        filtered_df.groupby("bank_name")["pos"]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )

    fig = px.bar(
        top_pos,
        x="pos",
        y="bank_name",
        orientation="h",
        color="pos",
        title="Top Banks by POS Deployment"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🏧 Top Banks by ATM Network")

    atm_df = filtered_df.copy()

    atm_df["total_atm"] = (
        atm_df["atms_crms_onsite"]
        + atm_df["atms_crms_offsite"]
    )

    top_atm = (
        atm_df.groupby("bank_name")["total_atm"]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )

    fig = px.bar(
        top_atm,
        x="total_atm",
        y="bank_name",
        orientation="h",
        color="total_atm",
        title="Top Banks by ATM Network"
    )

    st.plotly_chart(fig, use_container_width=True)

# ==================================================
# INFRASTRUCTURE
# ==================================================
with tab2:

    st.subheader("🏧 Infrastructure Analytics")

    infra_df = pd.DataFrame({
        "Metric": [
            "Onsite ATM",
            "Offsite ATM",
            "POS",
            "Micro ATM",
            "Bharat QR",
            "UPI QR"
        ],
        "Count": [
            filtered_df["atms_crms_onsite"].sum(),
            filtered_df["atms_crms_offsite"].sum(),
            filtered_df["pos"].sum(),
            filtered_df["micro_atms"].sum(),
            filtered_df["bharat_qr"].sum(),
            filtered_df["upi_qr"].sum()
        ]
    })

    fig = px.bar(
        infra_df,
        x="Metric",
        y="Count",
        color="Metric",
        title="Infrastructure Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

# ==================================================
# CARD ANALYTICS
# ==================================================
with tab3:

    st.subheader("💳 Credit vs Debit Cards")

    card_df = pd.DataFrame({
        "Card Type": ["Credit Cards", "Debit Cards"],
        "Count": [total_credit, total_debit]
    })

    fig = px.pie(
        card_df,
        names="Card Type",
        values="Count",
        hole=0.4
    )

    st.plotly_chart(fig, use_container_width=True)

# ==================================================
# TRANSACTION ANALYTICS
# ==================================================
with tab4:
    

    st.subheader("📈 Online Transaction Trends")

    trend = (
        filtered_df.groupby("date")[
            [
                "cc_pay_trns_online_val",
                "dc_pay_trns_online_val"
            ]
        ]
        .sum()
        .reset_index()
    )

    fig = px.line(
        trend,
        x="date",
        y=[
            "cc_pay_trns_online_val",
            "dc_pay_trns_online_val"
        ],
        markers=True,
        title="Credit vs Debit Online Transactions"
    )

    st.plotly_chart(fig, use_container_width=True)

monthly = (
    filtered_df
    .groupby(pd.Grouper(key="date", freq="ME"))
    ["pos"]
    .sum()
    .reset_index()
)

fig_month = px.line(
    monthly,
    x="date",
    y="pos",
    markers=True,
    title="Monthly POS Growth Trend"
)

st.plotly_chart(fig_month, use_container_width=True)
# ==================================================
# BANK CATEGORY ANALYSIS
# ==================================================
with tab5:

    st.subheader("🏦 Bank Category Analysis")

    category_df = (
        filtered_df.groupby("bank_category")
        [["pos", "credit_cards", "debit_cards"]]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        category_df,
        x="bank_category",
        y="pos",
        color="bank_category",
        title="POS Distribution by Bank Category"
    )

    st.plotly_chart(fig, use_container_width=True)

# ==================================================
# INSIGHTS & RECOMMENDATIONS
# ==================================================
with tab6:

    st.subheader("📈 Key Insights")

    atm_leader = (
        filtered_df.groupby("bank_name")
        ["atms_crms_onsite"]
        .sum()
        .idxmax()
    )

    pos_leader = (
        filtered_df.groupby("bank_name")
        ["pos"]
        .sum()
        .idxmax()
    )

    credit_leader = (
        filtered_df.groupby("bank_name")
        ["credit_cards"]
        .sum()
        .idxmax()
    )

    debit_leader = (
        filtered_df.groupby("bank_name")
        ["debit_cards"]
        .sum()
        .idxmax()
    )

    st.success(f"🏧 Highest ATM Network: {atm_leader}")
    st.success(f"💳 Highest POS Deployment: {pos_leader}")
    st.success(f"💳 Highest Credit Card Issuer: {credit_leader}")
    st.success(f"🏦 Highest Debit Card Issuer: {debit_leader}")

    ratio = total_debit / total_credit if total_credit > 0 else 0

    st.info(
        f"Debit cards are approximately {ratio:.1f} times more common than credit cards."
    )

    st.subheader("📌 Recommendations")

    st.markdown("""
### 1️⃣ Expand POS Infrastructure
Increase POS deployment in under-served areas to improve digital payment accessibility.

### 2️⃣ Promote Credit Card Adoption
Introduce rewards, cashback, and loyalty programs.

### 3️⃣ Strengthen Digital Payments
Invest in QR-based payment infrastructure and UPI ecosystem growth.

### 4️⃣ Improve Security
Enhance fraud detection systems and transaction monitoring.

### 5️⃣ Rural Financial Inclusion
Expand ATM and Micro-ATM networks in rural regions.

### 6️⃣ Customer Awareness
Conduct digital banking literacy programs to improve adoption.
""")
    
with tab7:

    st.subheader("📊 Correlation Heatmap")

    cols = [
        "atms_crms_onsite",
        "atms_crms_offsite",
        "pos",
        "micro_atms",
        "credit_cards",
        "debit_cards"
    ]

    corr = filtered_df[cols].corr()

    fig = px.imshow(
        corr,
        text_auto=True,
        title="Correlation Between Banking Metrics"
    )

    st.plotly_chart(fig, use_container_width=True)

# ==================================================
# DATA EXPLORER
# ==================================================
with tab8:

    st.subheader("📋 Data Explorer")

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

    csv = filtered_df.to_csv(index=False)

    st.download_button(
        label="📥 Download Filtered Data",
        data=csv,
        file_name="filtered_banking_data.csv",
        mime="text/csv"
    )

st.markdown("""
---
## 📑 Executive Summary

### Key Findings

✅ Growth in ATM and POS infrastructure continues.

✅ Debit cards significantly outnumber credit cards.

✅ QR-based payments are rapidly expanding.

✅ Online transaction values continue to increase.

✅ Major public and private sector banks dominate infrastructure deployment.

### Strategic Recommendations

1. Expand ATM and POS coverage in underserved areas.

2. Encourage credit card adoption through incentives.

3. Continue investing in UPI and QR ecosystems.

4. Strengthen fraud monitoring and cybersecurity.

5. Improve financial inclusion through Micro ATM expansion.

---
""")
# ==================================================
# FOOTER
# ==================================================
st.markdown("---")

st.markdown("""
### 📌 Dashboard Summary

This dashboard provides insights into:

- ATM Deployment
- POS Infrastructure
- Debit & Credit Card Analytics
- Digital Transaction Trends
- Bank Category Performance
- Banking Infrastructure Growth

**Built using Streamlit, Pandas, and Plotly**
""")
