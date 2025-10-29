# 🏥 Hospital Analytics Project
# Author: Manasa G V
# Tools: Python, SQL, Excel, Statistics, Tableau, ML

import pandas as pd
import numpy as np
import random
import os
import sqlite3
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

# ==============================================
# STEP 1️⃣ : Generate Synthetic Hospital Dataset
# ==============================================
os.makedirs("data", exist_ok=True)
np.random.seed(42)

departments = ["Cardiology", "Orthopedics", "Neurology", "Pediatrics", "Oncology", "General Medicine"]
genders = ["Male", "Female"]
diagnoses = [
    "Heart Disease", "Fracture", "Migraine", "Flu", "Cancer", "Diabetes",
    "Asthma", "Arthritis", "Stroke", "Infection"
]
payment_methods = ["Cash", "Insurance", "Credit Card", "Online"]
doctors = ["Dr. Sharma", "Dr. Mehta", "Dr. Kapoor", "Dr. Singh", "Dr. Nair"]

num_records = 600
data = {
    "Patient_ID": range(1001, 1001 + num_records),
    "Name": [f"Patient_{i}" for i in range(1, num_records + 1)],
    "Age": np.random.randint(18, 85, num_records),
    "Gender": np.random.choice(genders, num_records),
    "Department": np.random.choice(departments, num_records),
    "Doctor": np.random.choice(doctors, num_records),
    "Diagnosis": np.random.choice(diagnoses, num_records),
    "Admission_Date": pd.to_datetime(np.random.choice(pd.date_range("2023-01-01", "2024-12-31"), num_records)),
    "Discharge_Date": pd.to_datetime(np.random.choice(pd.date_range("2023-01-02", "2025-01-05"), num_records)),
    "Payment_Method": np.random.choice(payment_methods, num_records),
    "Charges": np.random.randint(2000, 50000, num_records),
    "Readmission_Within_30Days": np.random.choice(["Yes", "No"], num_records, p=[0.2, 0.8])
}

df = pd.DataFrame(data)
df["Stay_Length"] = (df["Discharge_Date"] - df["Admission_Date"]).dt.days
df["Stay_Length"] = df["Stay_Length"].apply(lambda x: x if x > 0 else random.randint(1, 10))

dataset_path = "data/healthcare_dataset.csv"
df.to_csv(dataset_path, index=False)
print(f"✅ Dataset created and saved to: {dataset_path}")

# ==============================================
# STEP 2️⃣ : Load Dataset and Clean
# ==============================================
print("\n🔹 Data Overview:")
print(df.head())

print("\nMissing values:\n", df.isnull().sum())

df = df.dropna()  # drop any nulls (if generated)
df["Charges"] = df["Charges"].astype(int)

# ==============================================
# STEP 3️⃣ : SQL Analysis
# ==============================================
conn = sqlite3.connect(":memory:")
df.to_sql("hospital", conn, index=False, if_exists="replace")

query1 = """
SELECT Department, 
       AVG(Charges) AS Avg_Charges, 
       COUNT(Patient_ID) AS Total_Patients
FROM hospital
GROUP BY Department
ORDER BY Avg_Charges DESC;
"""
print("\n🏥 Average Charges by Department:\n", pd.read_sql_query(query1, conn))

query2 = """
SELECT Doctor, COUNT(*) AS Readmissions
FROM hospital
WHERE Readmission_Within_30Days = 'Yes'
GROUP BY Doctor
ORDER BY Readmissions DESC;
"""
print("\n🔁 Doctor Readmission Stats:\n", pd.read_sql_query(query2, conn))

# ==============================================
# STEP 4️⃣ : Statistical Insights
# ==============================================
print("\n📊 Statistical Summary:\n", df.describe())
print("\nAverage Charges:", df["Charges"].mean())
print("Average Stay Length:", df["Stay_Length"].mean())

# ==============================================
# STEP 5️⃣ : Data Visualization
# ==============================================
sns.set(style="whitegrid")

plt.figure(figsize=(8,5))
sns.countplot(data=df, x="Department", hue="Gender")
plt.title("Patient Count by Department & Gender")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("data/patient_by_dept.png")
plt.show()

plt.figure(figsize=(6,4))
sns.histplot(df["Charges"], bins=30, kde=True)
plt.title("Distribution of Charges")
plt.tight_layout()
plt.savefig("data/charges_distribution.png")
plt.show()

plt.figure(figsize=(6,4))
sns.scatterplot(data=df, x="Age", y="Charges", hue="Gender")
plt.title("Age vs Charges")
plt.tight_layout()
plt.savefig("data/age_vs_charges.png")
plt.show()

print("✅ Visualizations saved in /data folder")

# ==============================================
# STEP 6️⃣ : Basic Machine Learning Model
# ==============================================
print("\n🤖 Running Simple Linear Regression to Predict Charges...")

df_ml = df[["Age", "Stay_Length", "Charges"]]
X = df_ml[["Age", "Stay_Length"]]
y = df_ml["Charges"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print("🔹 Model Coefficients:", model.coef_)
print("🔹 Model Intercept:", model.intercept_)
print("🔹 R2 Score:", r2_score(y_test, y_pred))
print("🔹 MAE:", mean_absolute_error(y_test, y_pred))

# ==============================================
# STEP 7️⃣ : Export to Excel for Tableau
# ==============================================
excel_path = "data/hospital_final_analysis.xlsx"
df.to_excel(excel_path, index=False)
print(f"✅ Excel file saved to: {excel_path}")

