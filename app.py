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
Analyze ATM deployment, POS infrastructure, card issuance,
and transaction trends across Indian banks from 2022 onwards.
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
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Overview",
    "Infrastructure",
    "Cards",
    "Transactions",
    "Categories",
    "Insights",
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

# ==================================================
# DATA EXPLORER
# ==================================================
with tab7:

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