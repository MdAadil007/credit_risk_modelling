import joblib
import numpy as np
import pandas as pd

# ── Load artifacts ────────────────────────────────────────────────────────────
model_data    = joblib.load("Artifacts/model_data.joblib")
model         = model_data['model']          # LogisticRegression
scaler        = model_data['scaler']         # MinMaxScaler
features      = list(model_data['features']) # 13 final feature columns (exact order)
cols_to_scale = model_data['cols_to_scale']  # 18 numeric cols scaler was fitted on


def prepare_input(age, income, loan_amount, loan_tenure_months,
                  avg_dpd_per_deliquency, deliquency_ratio,
                  credit_utilization_ratio, num_open_accounts,
                  residence_type, loan_purpose, loan_type):
    """
    Replicates notebook pipeline exactly:
      1. Compute loan_to_income from raw inputs
      2. Build full DataFrame with ALL cols_to_scale columns present
         (dummy values for cols dropped later — needed only for scaler.transform)
      3. Scale numeric cols with saved MinMaxScaler
      4. One-hot encode categorical columns (drop_first=True)
      5. Select & reorder to match training feature order
    """

    loan_to_income = round(loan_amount / income, 2) if income > 0 else 0

    # Build row with all columns that were present when scaler was fitted
    # Dummy values for columns not used in final model (needed for scaler shape)
    input_data = {
        # ── Columns used in final model ──────────────────────────────────────
        'age'                      : age,
        'loan_tenure_months'       : loan_tenure_months,
        'number_of_open_accounts'  : num_open_accounts,
        'credit_utilization_ratio' : credit_utilization_ratio,
        'loan_to_income'           : loan_to_income,
        'deliquency_ratio'         : deliquency_ratio,   # note: typo from notebook preserved
        'avg_dpd_per_deliquency'   : avg_dpd_per_deliquency,
        # ── Categorical (not scaled — handled by get_dummies) ─────────────
        'loan_purpose'             : loan_purpose,
        'residence_type'           : residence_type,
        'loan_type'                : loan_type,
        # ── Dummy numeric cols required by scaler (dropped after scaling) ──
        'number_of_dependants'          : 0,
        'years_at_current_address'      : 0,
        'zipcode'                       : 0,
        'sanction_amount'               : 0,
        'processing_fee'                : 0,
        'gst'                           : 0,
        'net_disbursement'              : 0,
        'principal_outstanding'         : 0,
        'bank_balance_at_application'   : 0,
        'number_of_closed_accounts'     : 0,
        'enquiry_count'                 : 0,
    }

    df = pd.DataFrame([input_data])

    # Scale only the numeric columns (same set scaler was fitted on)
    df[cols_to_scale] = scaler.transform(df[cols_to_scale])

    # One-hot encode categorical columns — drop_first=True matches training
    df = pd.get_dummies(df, drop_first=True)

    # Align to exact training column order; fill any missing OHE cols with 0
    df = df.reindex(columns=features, fill_value=0)

    return df


def calculate_credit_score(input_df, base_score=300, scale_length=600):
    """
    Manually computes logit → sigmoid (matches reference code exactly).
    Returns: (default_probability float, credit_score int, rating str)
    """
    x = np.dot(input_df.values, model.coef_.T) + model.intercept_

    default_probability     = 1 / (1 + np.exp(-x))
    non_default_probability = 1 - default_probability

    credit_score = base_score + non_default_probability.flatten()[0] * scale_length

    def get_rating(score):
        if 300 <= score < 500:
            return 'Poor'
        elif 500 <= score < 650:
            return 'Average'
        elif 650 <= score < 750:
            return 'Good'
        elif 750 <= score <= 900:
            return 'Excellent'
        else:
            return 'Undefined'

    return (
        round(float(default_probability.flatten()[0]), 4),
        int(credit_score),
        get_rating(credit_score)
    )


def predict(age, income, loan_amount, loan_tenure_months,
            avg_dpd_per_deliquency, deliquency_ratio,
            credit_utilization_ratio, num_open_accounts,
            residence_type, loan_purpose, loan_type):
    """
    Main entry point called by main.py.
    Returns: (default_probability, credit_score, rating)
    """
    input_df = prepare_input(
        age, income, loan_amount, loan_tenure_months,
        avg_dpd_per_deliquency, deliquency_ratio,
        credit_utilization_ratio, num_open_accounts,
        residence_type, loan_purpose, loan_type
    )
    return calculate_credit_score(input_df)
