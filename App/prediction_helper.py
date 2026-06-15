import joblib
import numpy as np
import pandas as pd

# ── Load artifacts ────────────────────────────────────────────────────────────
model_data    = joblib.load("Artifacts/model_data.joblib")
model         = model_data['model']          # LogisticRegression
scaler        = model_data['scaler']         # MinMaxScaler
features      = list(model_data['features']) # 13 final columns (exact order from joblib)
cols_to_scale = list(model_data['cols_to_scale'])  # 18 numeric cols scaler was fitted on


def prepare_input(age, income, loan_amount, loan_tenure_months,
                  avg_dpd_per_deliquency, deliquency_ratio,
                  credit_utilization_ratio, num_open_accounts,
                  residence_type, loan_purpose, loan_type):

    loan_to_income = round(loan_amount / income, 2) if income > 0 else 0

    # ── Step 1: Build the EXACT 18-column numeric DataFrame the scaler expects ──
    # Order and names must match cols_to_scale exactly as fitted:
    # age, number_of_dependants, years_at_current_address, zipcode,
    # sanction_amount, processing_fee, gst, net_disbursement,
    # loan_tenure_months, principal_outstanding, bank_balance_at_application,
    # number_of_open_accounts, number_of_closed_accounts, enquiry_count,
    # credit_utilization_ratio, loan_to_income, deliquency_ratio, avg_dpd_per_deliquency
    scale_df = pd.DataFrame([{
        'age'                        : age,
        'number_of_dependants'       : 0,
        'years_at_current_address'   : 0,
        'zipcode'                    : 0,
        'sanction_amount'            : 0,
        'processing_fee'             : 0,
        'gst'                        : 0,
        'net_disbursement'           : 0,
        'loan_tenure_months'         : loan_tenure_months,
        'principal_outstanding'      : 0,
        'bank_balance_at_application': 0,
        'number_of_open_accounts'    : num_open_accounts,
        'number_of_closed_accounts'  : 0,
        'enquiry_count'              : 0,
        'credit_utilization_ratio'   : credit_utilization_ratio,
        'loan_to_income'             : loan_to_income,
        'deliquency_ratio'           : deliquency_ratio,
        'avg_dpd_per_deliquency'     : avg_dpd_per_deliquency,
    }])[cols_to_scale]   # enforce exact column order scaler was fitted on

    # ── Step 2: Scale ──────────────────────────────────────────────────────────
    scaled_array = scaler.transform(scale_df)
    scaled_df    = pd.DataFrame(scaled_array, columns=cols_to_scale)

    # ── Step 3: Build final row with scaled numerics + raw categoricals ────────
    final_row = {
        # scaled numeric values (only the 7 that survive to final features)
        'age'                      : scaled_df['age'].iloc[0],
        'loan_tenure_months'       : scaled_df['loan_tenure_months'].iloc[0],
        'number_of_open_accounts'  : scaled_df['number_of_open_accounts'].iloc[0],
        'credit_utilization_ratio' : scaled_df['credit_utilization_ratio'].iloc[0],
        'loan_to_income'           : scaled_df['loan_to_income'].iloc[0],
        'deliquency_ratio'         : scaled_df['deliquency_ratio'].iloc[0],
        'avg_dpd_per_deliquency'   : scaled_df['avg_dpd_per_deliquency'].iloc[0],
        # raw categoricals for get_dummies
        'loan_purpose'             : loan_purpose,
        'residence_type'           : residence_type,
        'loan_type'                : loan_type,
    }

    df = pd.DataFrame([final_row])

    # ── Step 4: One-hot encode (drop_first=True matches training) ─────────────
    df = pd.get_dummies(df, drop_first=True)

    # ── Step 5: Reindex to exact 13-column training order, fill missing with 0 ─
    df = df.reindex(columns=features, fill_value=0)

    return df, loan_to_income


def calculate_credit_score(input_df, base_score=300, scale_length=600):
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

    input_df, _ = prepare_input(
        age, income, loan_amount, loan_tenure_months,
        avg_dpd_per_deliquency, deliquency_ratio,
        credit_utilization_ratio, num_open_accounts,
        residence_type, loan_purpose, loan_type
    )
    return calculate_credit_score(input_df)