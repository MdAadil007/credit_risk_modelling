import streamlit as st
from prediction_helper import predict

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Lauki Finance | Credit Risk",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

/* ── Reset & Base ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #0A0F1E;
}

/* ── Hero ── */
.hero {
    background: linear-gradient(135deg, #0D1B3E 0%, #1A1040 50%, #0D2137 100%);
    border: 1px solid rgba(99, 179, 237, 0.15);
    border-radius: 20px;
    padding: 48px 48px 40px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -80px; right: -80px;
    width: 320px; height: 320px;
    background: radial-gradient(circle, rgba(99,179,237,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -60px; left: 30%;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(167,139,250,0.08) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-badge {
    display: inline-block;
    background: rgba(99,179,237,0.12);
    border: 1px solid rgba(99,179,237,0.3);
    color: #63B3ED;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 5px 14px;
    border-radius: 20px;
    margin-bottom: 16px;
}
.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 38px;
    font-weight: 700;
    color: #F0F4FF;
    line-height: 1.2;
    margin: 0 0 10px;
}
.hero-title span {
    background: linear-gradient(90deg, #63B3ED, #A78BFA);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sub {
    color: #7A8BAD;
    font-size: 15px;
    font-weight: 400;
    max-width: 560px;
    line-height: 1.6;
    margin: 0;
}
.hero-stats {
    display: flex;
    gap: 32px;
    margin-top: 28px;
    padding-top: 24px;
    border-top: 1px solid rgba(255,255,255,0.06);
}
.hero-stat-val {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: #F0F4FF;
}
.hero-stat-lbl {
    font-size: 11px;
    color: #7A8BAD;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 2px;
}

/* ── Persona Cards ── */
.persona-row {
    display: flex;
    gap: 12px;
    margin-bottom: 28px;
}
.persona-card {
    flex: 1;
    background: #111827;
    border: 2px solid #1E293B;
    border-radius: 14px;
    padding: 16px 14px;
    cursor: pointer;
    transition: all 0.2s ease;
    text-align: center;
}
.persona-card:hover {
    border-color: #63B3ED;
    background: #0D1B3E;
}
.persona-card.active {
    border-color: #63B3ED;
    background: linear-gradient(135deg, #0D1B3E, #111827);
    box-shadow: 0 0 20px rgba(99,179,237,0.15);
}
.persona-icon { font-size: 28px; margin-bottom: 6px; }
.persona-name {
    font-size: 12px;
    font-weight: 600;
    color: #CBD5E1;
    margin-bottom: 2px;
}
.persona-desc {
    font-size: 10px;
    color: #475569;
}

/* ── Section headers ── */
.section-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #4B6CB7;
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(75,108,183,0.25);
}

/* ── Input card ── */
.input-card {
    background: #111827;
    border: 1px solid #1E293B;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 16px;
}

/* ── Streamlit widget overrides ── */
[data-testid="stNumberInput"] label,
[data-testid="stSelectbox"] label {
    color: #94A3B8 !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    letter-spacing: 0.5px !important;
    text-transform: uppercase !important;
}

[data-testid="stNumberInput"] input {
    background: #0D1422 !important;
    border: 1px solid #1E293B !important;
    border-radius: 10px !important;
    color: #F0F4FF !important;
    font-size: 15px !important;
    font-weight: 500 !important;
}
[data-testid="stNumberInput"] input:focus {
    border-color: #63B3ED !important;
    box-shadow: 0 0 0 3px rgba(99,179,237,0.1) !important;
}

[data-testid="stSelectbox"] > div > div {
    background: #0D1422 !important;
    border: 1px solid #1E293B !important;
    border-radius: 10px !important;
    color: #F0F4FF !important;
}

/* ── Derived field display ── */
.derived-field {
    background: #0D1422;
    border: 1px solid #1E293B;
    border-radius: 10px;
    padding: 10px 14px;
    margin-top: 24px;
}
.derived-label {
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    color: #94A3B8;
    margin-bottom: 4px;
}
.derived-value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 20px;
    font-weight: 600;
    color: #63B3ED;
}

/* ── CTA Button ── */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #2563EB, #7C3AED) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    padding: 14px 32px !important;
    letter-spacing: 0.5px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 24px rgba(37,99,235,0.3) !important;
}
[data-testid="stButton"] > button:hover {
    box-shadow: 0 6px 32px rgba(37,99,235,0.5) !important;
    transform: translateY(-1px) !important;
}

/* ── Result cards ── */
.result-grid {
    display: flex;
    gap: 16px;
    margin: 24px 0;
}
.result-card {
    flex: 1;
    background: #111827;
    border: 1px solid #1E293B;
    border-radius: 16px;
    padding: 24px 20px;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.result-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
}
.result-card.prob::before  { background: linear-gradient(90deg, #EF4444, #F97316); }
.result-card.score::before { background: linear-gradient(90deg, #2563EB, #7C3AED); }
.result-card.rating::before { background: linear-gradient(90deg, #10B981, #3B82F6); }

.result-icon { font-size: 28px; margin-bottom: 8px; }
.result-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #4B6CB7;
    margin-bottom: 8px;
}
.result-value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 32px;
    font-weight: 700;
    color: #F0F4FF;
    line-height: 1;
}
.result-sub {
    font-size: 12px;
    color: #475569;
    margin-top: 6px;
}

/* ── Verdict banner ── */
.verdict {
    border-radius: 14px;
    padding: 18px 24px;
    display: flex;
    align-items: center;
    gap: 16px;
    margin-top: 8px;
}
.verdict.excellent { background: rgba(16,185,129,0.08); border: 1px solid rgba(16,185,129,0.25); }
.verdict.good      { background: rgba(59,130,246,0.08); border: 1px solid rgba(59,130,246,0.25); }
.verdict.average   { background: rgba(245,158,11,0.08); border: 1px solid rgba(245,158,11,0.25); }
.verdict.poor      { background: rgba(239,68,68,0.08);  border: 1px solid rgba(239,68,68,0.25);  }

.verdict-icon { font-size: 32px; }
.verdict-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 17px;
    font-weight: 700;
    margin-bottom: 3px;
}
.verdict.excellent .verdict-title { color: #10B981; }
.verdict.good      .verdict-title { color: #3B82F6; }
.verdict.average   .verdict-title { color: #F59E0B; }
.verdict.poor      .verdict-title { color: #EF4444; }
.verdict-body { font-size: 13px; color: #7A8BAD; }

/* ── Score bar ── */
.score-track {
    background: #1E293B;
    border-radius: 8px;
    height: 8px;
    margin: 20px 0 8px;
    position: relative;
}
.score-fill {
    height: 100%;
    border-radius: 8px;
    background: linear-gradient(90deg, #EF4444 0%, #F59E0B 33%, #3B82F6 66%, #10B981 100%);
}
.score-bar-labels {
    display: flex;
    justify-content: space-between;
    font-size: 10px;
    color: #475569;
}

/* ── Divider ── */
.my-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #1E293B, transparent);
    margin: 28px 0;
}

/* hide streamlit default elements */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }
</style>
""", unsafe_allow_html=True)


# ── HERO SECTION ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">🏦 Lauki Finance · Credit Intelligence</div>
    <div class="hero-title">Credit Risk <span>Assessment</span> Engine</div>
    <p class="hero-sub">
        Enter applicant details below to compute default probability,
        generate a credit score, and receive an instant risk verdict.
    </p>
    <div class="hero-stats">
        <div>
            <div class="hero-stat-val">98.7%</div>
            <div class="hero-stat-lbl">Model AUC</div>
        </div>
        <div>
            <div class="hero-stat-val">50,000+</div>
            <div class="hero-stat-lbl">Training Records</div>
        </div>
        <div>
            <div class="hero-stat-val">13</div>
            <div class="hero-stat-lbl">Risk Features</div>
        </div>
        <div>
            <div class="hero-stat-val">LR · Optuna</div>
            <div class="hero-stat-lbl">Model Type</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ── CUSTOMER PERSONA QUICK-FILL ───────────────────────────────────────────────
st.markdown('<div class="section-label">Quick-fill by persona</div>', unsafe_allow_html=True)
st.markdown("""
<div class="persona-row">
    <div class="persona-card">
        <div class="persona-icon">👨‍💼</div>
        <div class="persona-name">Salaried Professional</div>
        <div class="persona-desc">Stable income · Low risk</div>
    </div>
    <div class="persona-card">
        <div class="persona-icon">👩‍💻</div>
        <div class="persona-name">Young IT Employee</div>
        <div class="persona-desc">High income · Short history</div>
    </div>
    <div class="persona-card">
        <div class="persona-icon">🏪</div>
        <div class="persona-name">Small Business Owner</div>
        <div class="persona-desc">Variable income · Medium risk</div>
    </div>
    <div class="persona-card">
        <div class="persona-icon">👴</div>
        <div class="persona-name">Retired Applicant</div>
        <div class="persona-desc">Fixed income · Long history</div>
    </div>
    <div class="persona-card">
        <div class="persona-icon">⚠️</div>
        <div class="persona-name">High-Risk Profile</div>
        <div class="persona-desc">Delinquent history · Low score</div>
    </div>
</div>
<p style="font-size:11px; color:#374151; margin-top:-14px; margin-bottom:24px;">
    ↑ Persona cards are illustrative — fill the form below manually.
</p>
""", unsafe_allow_html=True)


# ── FORM ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Applicant details</div>', unsafe_allow_html=True)

with st.container():
    c1, c2, c3 = st.columns(3)
    with c1:
        age = st.number_input("🧑 Age", min_value=18, max_value=100, step=1, value=28)
    with c2:
        income = st.number_input("💰 Income (₹)", min_value=1, value=1200000, step=10000)
    with c3:
        loan_amount = st.number_input("🏦 Loan Amount (₹)", min_value=1, value=2560000, step=10000)

# Derived metric shown live
loan_to_income_ratio = round(loan_amount / income, 2) if income > 0 else 0
lti_color = "#10B981" if loan_to_income_ratio < 3 else "#F59E0B" if loan_to_income_ratio < 5 else "#EF4444"
st.markdown(f"""
<div style="background:#0D1422; border:1px solid #1E293B; border-radius:12px;
            padding:14px 20px; margin:4px 0 20px; display:inline-block; min-width:200px;">
    <div style="font-size:11px; font-weight:600; letter-spacing:1.5px; text-transform:uppercase;
                color:#64748B; margin-bottom:4px;">📊 Loan-to-Income Ratio</div>
    <div style="font-family:'Space Grotesk',sans-serif; font-size:26px; font-weight:700;
                color:{lti_color};">{loan_to_income_ratio:.2f}
        <span style="font-size:12px; font-weight:400; color:#475569; margin-left:6px;">
            {"✅ Healthy" if loan_to_income_ratio < 3 else "⚠️ Moderate" if loan_to_income_ratio < 5 else "🔴 High"}
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-label">Loan details</div>', unsafe_allow_html=True)
c4, c5, c6 = st.columns(3)
with c4:
    loan_tenure_months = st.number_input("📅 Loan Tenure (months)", min_value=1, max_value=360, step=1, value=36)
with c5:
    avg_dpd_per_deliquency = st.number_input("📉 Avg DPD per Delinquency", min_value=0, value=20, step=1)
with c6:
    num_open_accounts = st.number_input("🗂️ Open Loan Accounts", min_value=0, max_value=20, step=1, value=2)

st.markdown('<div class="section-label">Risk indicators</div>', unsafe_allow_html=True)
c7, c8 = st.columns(2)
with c7:
    deliquency_ratio = st.number_input("⚠️ Delinquency Ratio", min_value=0, max_value=100, step=1, value=30)
with c8:
    credit_utilization_ratio = st.number_input("💳 Credit Utilization Ratio", min_value=0, max_value=100, step=1, value=30)

st.markdown('<div class="section-label">Classification</div>', unsafe_allow_html=True)
c9, c10, c11 = st.columns(3)
with c9:
    residence_type = st.selectbox("🏠 Residence Type", ["Owned", "Rented", "Mortgage"])
with c10:
    loan_purpose = st.selectbox("🎯 Loan Purpose", ["Education", "Home", "Auto", "Personal"])
with c11:
    loan_type = st.selectbox("🔐 Loan Type", ["Unsecured", "Secured"])

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

# ── CTA ───────────────────────────────────────────────────────────────────────
col_btn, col_pad = st.columns([1, 2])
with col_btn:
    run = st.button("⚡ Run Risk Assessment", use_container_width=True)


# ── RESULTS ──────────────────────────────────────────────────────────────────
if run:
    probability, credit_score, rating = predict(
        age, income, loan_amount, loan_tenure_months,
        avg_dpd_per_deliquency, deliquency_ratio,
        credit_utilization_ratio, num_open_accounts,
        residence_type, loan_purpose, loan_type
    )

    st.markdown('<div class="my-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Risk assessment results</div>', unsafe_allow_html=True)

    # ── Three metric cards ──
    score_pct = int((credit_score - 300) / 600 * 100)
    st.markdown(f"""
    <div class="result-grid">
        <div class="result-card prob">
            <div class="result-icon">🎯</div>
            <div class="result-label">Default Probability</div>
            <div class="result-value">{probability:.2%}</div>
            <div class="result-sub">Likelihood of non-repayment</div>
        </div>
        <div class="result-card score">
            <div class="result-icon">📊</div>
            <div class="result-label">Credit Score</div>
            <div class="result-value">{credit_score}</div>
            <div class="result-sub">Out of 900 points</div>
        </div>
        <div class="result-card rating">
            <div class="result-icon">🏷️</div>
            <div class="result-label">Rating</div>
            <div class="result-value">{rating}</div>
            <div class="result-sub">Risk classification</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Score bar ──
    st.markdown(f"""
    <div style="background:#111827; border:1px solid #1E293B; border-radius:16px; padding:20px 24px; margin-bottom:16px;">
        <div style="font-size:11px; font-weight:700; letter-spacing:2px; text-transform:uppercase;
                    color:#4B6CB7; margin-bottom:14px;">Credit Score Position</div>
        <div class="score-track">
            <div class="score-fill" style="width:{score_pct}%;"></div>
        </div>
        <div class="score-bar-labels">
            <span>300 · Poor</span>
            <span>500 · Average</span>
            <span>650 · Good</span>
            <span>750 · Excellent · 900</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Verdict banner ──
    verdicts = {
        "Excellent": ("excellent", "✅", "Excellent — Strongly Recommend Approval",
                      "Very low probability of default. This applicant has a strong credit profile and poses minimal risk to the lender."),
        "Good":      ("good",      "🟢", "Good — Recommend Approval with Standard Terms",
                      "Low-moderate risk. Applicant shows healthy repayment indicators. Proceed with standard loan terms."),
        "Average":   ("average",   "⚠️", "Average — Manual Review Recommended",
                      "Elevated risk detected. A credit officer should review this application before approval."),
        "Poor":      ("poor",      "🔴", "Poor — Recommend Rejection",
                      "High default probability. This applicant does not meet the minimum credit threshold for approval."),
    }
    cls, icon, title, body = verdicts.get(rating, verdicts["Poor"])
    st.markdown(f"""
    <div class="verdict {cls}">
        <div class="verdict-icon">{icon}</div>
        <div>
            <div class="verdict-title">{title}</div>
            <div class="verdict-body">{body}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)