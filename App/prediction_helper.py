import joblib
import numpy as np
import pandas as pd

# ── Load artifacts ────────────────────────────────────────────────────────────
model_data    = joblib.load("Artifacts/model_data.joblib")
model         = model_data['model']
scaler        = model_data['scaler']
features      = list(model_data['features'])
cols_to_scale = list(model_data['cols_to_scale'])

# Precompute midpoints for filler-only columns.
# The scaler was fitted on 18 columns; only 7 of those survive into the final model.
# The remaining 11 are "filler" — we never surface them in the UI, but the scaler
# still expects them in transform().  Using the training midpoints keeps them at ~0.5
# after scaling and avoids corrupting the predictions.
_scaler_mid = {
    col: float((scaler.data_min_[i] + scaler.data_max_[i]) / 2)
    for i, col in enumerate(cols_to_scale)
}

def _clip(val, col):
    """Clip a value to the range the scaler was fitted on."""
    i = cols_to_scale.index(col)
    return float(np.clip(val, scaler.data_min_[i], scaler.data_max_[i]))


def prepare_input(age, income, loan_amount, loan_tenure_months,
                  avg_dpd_per_deliquency, deliquency_ratio,
                  credit_utilization_ratio, num_open_accounts,
                  residence_type, loan_purpose, loan_type):
    """
    Build a 1-row DataFrame that exactly replicates the training pipeline:

      1. Derive loan_to_income.
      2. Clip every numeric UI input to the scaler's fitted [min, max] so
         out-of-range values don't push the logit to ±∞.
      3. Fill the 11 filler columns (not shown in the UI) with their training
         midpoints so they scale to ≈ 0.5 — a neutral, non-distorting value.
      4. Apply MinMaxScaler.transform (same scaler object fitted during training).
      5. One-hot encode categoricals with drop_first=True (matches training).
      6. Reindex to the exact 13-column feature order the model was trained on.

    Notes on training-data ranges (from the fitted scaler):
      avg_dpd_per_deliquency  : 0 – 10    (not 0–100; clip prevents blow-up)
      deliquency_ratio        : 0.0 – 1.0 (fraction, not percentage)
      credit_utilization_ratio: 0 – 99
      loan_tenure_months      : 6 – 59
      number_of_open_accounts : 1 – 4
      age                     : 18 – 70
    """
    loan_to_income = round(loan_amount / income, 2) if income > 0 else 0.0

    input_data = {
        # ── Features that survive into the final model ──────────────────────
        'age':                      _clip(age,                      'age'),
        'loan_tenure_months':       _clip(loan_tenure_months,       'loan_tenure_months'),
        'number_of_open_accounts':  _clip(num_open_accounts,        'number_of_open_accounts'),
        'credit_utilization_ratio': _clip(credit_utilization_ratio, 'credit_utilization_ratio'),
        'loan_to_income':           _clip(loan_to_income,           'loan_to_income'),
        'deliquency_ratio':         _clip(deliquency_ratio,         'deliquency_ratio'),
        'avg_dpd_per_deliquency':   _clip(avg_dpd_per_deliquency,   'avg_dpd_per_deliquency'),
        # ── Categoricals (not scaled; handled by get_dummies) ───────────────
        'loan_purpose':             loan_purpose,
        'residence_type':           residence_type,
        'loan_type':                loan_type,
        # ── Filler numerics (required for scaler shape; dropped after OHE) ──
        'number_of_dependants':         _scaler_mid['number_of_dependants'],
        'years_at_current_address':     _scaler_mid['years_at_current_address'],
        'zipcode':                      _scaler_mid['zipcode'],
        'sanction_amount':              _scaler_mid['sanction_amount'],
        'processing_fee':               _scaler_mid['processing_fee'],
        'gst':                          _scaler_mid['gst'],
        'net_disbursement':             _scaler_mid['net_disbursement'],
        'principal_outstanding':        _scaler_mid['principal_outstanding'],
        'bank_balance_at_application':  _scaler_mid['bank_balance_at_application'],
        'number_of_closed_accounts':    _scaler_mid['number_of_closed_accounts'],
        'enquiry_count':                _scaler_mid['enquiry_count'],
    }

    df = pd.DataFrame([input_data])
    df[cols_to_scale] = scaler.transform(df[cols_to_scale])
    df = pd.get_dummies(df, drop_first=True)
    df = df.reindex(columns=features, fill_value=0)
    return df


def calculate_credit_score(input_df, base_score=300, scale_length=600):
    """
    Manually compute logit → probability → credit score.
    Returns: (default_probability: float, credit_score: int, rating: str)
    """
    x = np.dot(input_df.values, model.coef_.T) + model.intercept_

    default_probability     = float((1 / (1 + np.exp(-x)))[0][0])
    non_default_probability = 1 - default_probability
    credit_score            = int(base_score + non_default_probability * scale_length)

    if credit_score < 500:
        rating = 'Poor'
    elif credit_score < 650:
        rating = 'Average'
    elif credit_score < 750:
        rating = 'Good'
    else:
        rating = 'Excellent'

    return round(default_probability, 4), credit_score, rating


def predict(age, income, loan_amount, loan_tenure_months,
            avg_dpd_per_deliquency, deliquency_ratio,
            credit_utilization_ratio, num_open_accounts,
            residence_type, loan_purpose, loan_type):
    """
    Main entry point called by main.py.
    Returns: (default_probability: float, credit_score: int, rating: str)
    """
    input_df = prepare_input(
        age, income, loan_amount, loan_tenure_months,
        avg_dpd_per_deliquency, deliquency_ratio,
        credit_utilization_ratio, num_open_accounts,
        residence_type, loan_purpose, loan_type
    )
    return calculate_credit_score(input_df)