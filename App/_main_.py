import streamlit as st
from prediction_helper import predict

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Credit Risk Modelling",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 Credit Risk Modelling")
st.markdown("Fill in the applicant details to predict default probability and credit score.")
st.divider()

# ── Input Grid ────────────────────────────────────────────────────────────────
row1 = st.columns(3)
row2 = st.columns(3)
row3 = st.columns(3)
row4 = st.columns(3)

with row1[0]:
    age = st.number_input("Age", min_value=18, max_value=100, step=1, value=28)
with row1[1]:
    income = st.number_input("Income (₹)", min_value=1, value=1200000, step=10000)
with row1[2]:
    loan_amount = st.number_input("Loan Amount (₹)", min_value=1, value=2560000, step=10000)

# Derived field shown live
loan_to_income_ratio = round(loan_amount / income, 2) if income > 0 else 0
with row2[0]:
    st.markdown("**Loan to Income Ratio**")
    st.markdown(f"### {loan_to_income_ratio}")

with row2[1]:
    loan_tenure_months = st.number_input("Loan Tenure (months)", min_value=1, max_value=360, step=1, value=36)
with row2[2]:
    avg_dpd_per_deliquency = st.number_input("Avg DPD per Delinquency", min_value=0, value=20, step=1)

with row3[0]:
    deliquency_ratio = st.number_input("Delinquency Ratio", min_value=0, max_value=100, step=1, value=30)
with row3[1]:
    credit_utilization_ratio = st.number_input("Credit Utilization Ratio", min_value=0, max_value=100, step=1, value=30)
with row3[2]:
    num_open_accounts = st.number_input("Open Loan Accounts", min_value=0, max_value=20, step=1, value=2)

with row4[0]:
    residence_type = st.selectbox("Residence Type", ["Owned", "Rented", "Mortgage"])
with row4[1]:
    loan_purpose = st.selectbox("Loan Purpose", ["Education", "Home", "Auto", "Personal"])
with row4[2]:
    loan_type = st.selectbox("Loan Type", ["Unsecured", "Secured"])

st.divider()

# ── Predict Button ────────────────────────────────────────────────────────────
if st.button("🔍 Calculate Risk", use_container_width=True):
    probability, credit_score, rating = predict(
        age, income, loan_amount, loan_tenure_months,
        avg_dpd_per_deliquency, deliquency_ratio,
        credit_utilization_ratio, num_open_accounts,
        residence_type, loan_purpose, loan_type
    )

    st.subheader("📊 Results")
    r1, r2, r3 = st.columns(3)

    with r1:
        st.metric("Default Probability", f"{probability:.2%}")
    with r2:
        st.metric("Credit Score", f"{credit_score} / 900")
    with r3:
        st.metric("Rating", rating)

    # Colour-coded verdict
    if rating == "Excellent":
        st.success(f"✅ Excellent ({credit_score}) — Very low risk. Recommend approval.")
    elif rating == "Good":
        st.info(f"🟢 Good ({credit_score}) — Low-moderate risk. Likely approve.")
    elif rating == "Average":
        st.warning(f"⚠️ Average ({credit_score}) — Elevated risk. Review carefully.")
    else:
        st.error(f"🔴 Poor ({credit_score}) — High default risk. Recommend rejection.")
        