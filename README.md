
---

# 🩺 Disease Prediction using ML (Mini Hackathon)

## 📌 Overview

This project is part of a **mini-hackathon challenge** where the goal is to build a machine learning model that can predict the presence of various diseases based on patient symptoms.

We trained and compared three state-of-the-art models:

* ⚡ **XGBoost**
* 🌿 **LightGBM**
* 🐱 **CatBoost**

The pipeline includes preprocessing, training, saving models, and evaluating them on a held-out test dataset.

---

## 📂 Project Structure

```
├── Data/
│   ├── cleaned_data.csv      # Training dataset
│   ├── Testing.csv           # Testing dataset
│
├── saved_models/
│   ├── xgb_disease_model.pkl # Trained XGBoost model
│   ├── lgb_disease_model.pkl # Trained LightGBM model
│   ├── cat_disease_model.pkl # Trained CatBoost model
│   ├── label_encoder.pkl     # Fitted label encoder for diseases
│
├── scripts/
│   ├── train_models.py       # Train and save XGB, LGBM, CatBoost
│   ├── test_single_model.py  # Load one model + evaluate
│   ├── compare_models.py     # Load all models + compare accuracy
│
├── README.md                 # Project documentation
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone repo & install dependencies

```bash
git clone <repo_url>
cd <repo_name>
pip install -r requirements.txt
```

Typical requirements:

```txt
pandas
scikit-learn
xgboost
lightgbm
catboost
matplotlib
joblib
```

---

### 2️⃣ Train Models

Run training script to build and save all three models:

```bash
python scripts/train_models.py
```

This will:

* Train **XGBoost, LightGBM, and CatBoost** on `cleaned_data.csv`
* Save trained models into `saved_models/`

---

### 3️⃣ Test a Single Model

To test an individual model (example: XGBoost):

```bash
python scripts/test_single_model.py
```

It will:

* Load model from `saved_models/`
* Evaluate on `Testing.csv`
* Print accuracy + classification report

---

### 4️⃣ Compare All Models

To compare **XGBoost, LightGBM, and CatBoost** side by side:

```bash
python scripts/compare_models.py
```

It will:

* Print accuracy + classification report for each model
* Show a **bar chart** comparing accuracy

---

## 📊 Example Results

| Model    | Accuracy |
| -------- | -------- |
| XGBoost  | 0.95     |
| LightGBM | 0.96     |
| CatBoost | 0.97     |

*(Values will vary depending on dataset & random seed)*

---

## 📌 Key Notes

* The target variable is **`prognosis`** (disease label).
* Labels are encoded using `LabelEncoder` before training.
* All models are saved with **joblib** for easy loading.

---

## 🚀 Future Improvements

* Add **confusion matrices** for better error analysis
* Hyperparameter tuning using **Optuna**
* Deploy model via **FastAPI/Streamlit** for interactive predictions

---
