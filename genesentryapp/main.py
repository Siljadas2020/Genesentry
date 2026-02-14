# import pandas as pd
# import joblib

# # =========================
# # Load model and encoders
# # =========================
# model = joblib.load(r'F:\Gensentry_main\Genesentry\genesentryapp\model.pkl')
# le_dict = joblib.load(r'F:\Gensentry_main\Genesentry\genesentryapp\label_encoders.pkl')

# # =========================
# # Model feature names
# # =========================
# feature_names = [
#     'Patient Age',
#     "Genes in mother's side",
#     'Inherited from father',
#     'Maternal gene',
#     'Paternal gene',
#     'Blood cell count mcL',
#     "Mother's age",
#     "Father's age",
#     'Respiratory Rate breathsmin',
#     'Heart Rate ratesmin',
#     'Gender',
#     'HO radiation exposure xray',
#     'White Blood cell count thousand per microliter'
# ]

# # =========================
# # Categorical columns
# # =========================
# categorical_cols = [
#     "Genes in mother's side",
#     'Inherited from father',
#     'Maternal gene',
#     'Paternal gene',
#     'Respiratory Rate breathsmin',
#     'Heart Rate ratesmin',
#     'Gender',
#     'HO radiation exposure xray'
# ]

# # =========================
# # API FIELD → MODEL FIELD MAP
# # =========================
# FIELD_MAP = {
#     "patient_age": "Patient Age",
#     "genes_mother_side": "Genes in mother's side",
#     "inherited_father": "Inherited from father",
#     "maternal_gene": "Maternal gene",
#     "paternal_gene": "Paternal gene",
#     "blood_cell_count": "Blood cell count mcL",
#     "Mother_age": "Mother's age",
#     "father_age": "Father's age",
#     "respiratory_rate": "Respiratory Rate breathsmin",
#     "heart_rate": "Heart Rate ratesmin",
#     "gender": "Gender",
#     "HO radiation exposure xray": "HO radiation exposure xray",
#     "white_blood_cell_count": "White Blood cell count thousand per microliter"
# }

# # =========================
# # Prediction function
# # =========================
# def predict_disease(data):
#     print("++++++++++++Predicting disease with data:", data)

#     input_dict = {}

#     for api_field, model_field in FIELD_MAP.items():
#         value = data.get(api_field)

#         # Handle missing / empty values
#         if value in [None, "", "null"]:
#             if model_field in categorical_cols:
#                 value = "No"   # safe default
#             else:
#                 raise ValueError(f"Missing numeric field: {api_field}")

#         # Convert types
#         if model_field in categorical_cols:
#             input_dict[model_field] = str(value)
#         else:
#             input_dict[model_field] = float(value)

#     # Create DataFrame in correct format
#     print("++++++++++++Input dict for model:", input_dict)
#     input_df = pd.DataFrame([input_dict])
#     print("++++++++++++Input DataFrame for model:\n", input_df)
    
#     # Encode categorical columns
#     for col in categorical_cols:
#         if col in le_dict:
#             input_df[col] = le_dict[col].transform(input_df[col])

#     # Predict

#     prediction = model.predict(input_df)[0]

#     return {
#         "Predicted Disorder Subclass": prediction
#     }




# //////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////


import pandas as pd
import joblib

# =========================
# Load model and encoders
# =========================
model = joblib.load(
    r'F:\Gensentry_main\Genesentry\genesentryapp\model.pkl'
)

le_dict = joblib.load(
    r'F:\Gensentry_main\Genesentry\genesentryapp\label_encoders.pkl'
)

# =========================
# Model feature names
# =========================
feature_names = [
    'Patient Age',
    "Genes in mother's side",
    'Inherited from father',
    'Maternal gene',
    'Paternal gene',
    'Blood cell count mcL',
    "Mother's age",
    "Father's age",
    'Respiratory Rate breathsmin',
    'Heart Rate ratesmin',
    'Gender',
    'HO radiation exposure xray',
    'White Blood cell count thousand per microliter'
]

# =========================
# Categorical columns
# =========================
categorical_cols = [
    "Genes in mother's side",
    'Inherited from father',
    'Maternal gene',
    'Paternal gene',
    'Respiratory Rate breathsmin',
    'Heart Rate ratesmin',
    'Gender',
    'HO radiation exposure xray'
]

# =========================
# API FIELD → MODEL FIELD MAP
# =========================
FIELD_MAP = {
    "patient_age": "Patient Age",
    "genes_mother_side": "Genes in mother's side",
    "inherited_father": "Inherited from father",
    "maternal_gene": "Maternal gene",
    "paternal_gene": "Paternal gene",
    "blood_cell_count": "Blood cell count mcL",
    "Mother_age": "Mother's age",
    "father_age": "Father's age",
    "respiratory_rate": "Respiratory Rate breathsmin",
    "heart_rate": "Heart Rate ratesmin",
    "gender": "Gender",
    "HO radiation exposure xray": "HO radiation exposure xray",
    "white_blood_cell_count": "White Blood cell count thousand per microliter"
}

# =========================
# Prediction function
# =========================
def predict_disease(data):
    print("++++++++++++Predicting disease with data:", data)

    input_dict = {}

    # -------------------------
    # Build input dictionary
    # -------------------------
    for api_field, model_field in FIELD_MAP.items():
        value = data.get(api_field)

        # Handle missing values
        if value in [None, "", "null"]:
            if model_field in categorical_cols:
                value = "No"  # safe categorical default
            else:
                raise ValueError(f"Missing numeric field: {api_field}")

        # Convert types
        if model_field in categorical_cols:
            input_dict[model_field] = str(value)
        else:
            input_dict[model_field] = float(value)

    print("++++++++++++Input dict for model:", input_dict)

    input_df = pd.DataFrame([input_dict])
    print("++++++++++++Input DataFrame for model:\n", input_df)

    # -------------------------
    # SAFE LABEL ENCODING
    # -------------------------
    for col in categorical_cols:
        if col in le_dict:
            le = le_dict[col]

            def safe_encode(val):
                if val in le.classes_:
                    return le.transform([val])[0]
                else:
                    fallback = le.classes_[0]
                    print(
                        f"⚠️ Unseen label '{val}' for column '{col}'. "
                        f"Using fallback '{fallback}'"
                    )
                    return le.transform([fallback])[0]

            input_df[col] = input_df[col].apply(safe_encode)

    # -------------------------
    # Predict
    # -------------------------
    prediction = model.predict(input_df)[0]

    return {
        "Predicted Disorder Subclass": prediction
    }
