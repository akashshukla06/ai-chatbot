import pandas as pd

# Dataset path
file_path = "dataset/raw/university_faq.csv"

# Load dataset
df = pd.read_csv(file_path)

print("\n===== FIRST 5 ROWS =====")
print(df.head())

print("\n===== DATASET SHAPE =====")
print(df.shape)

print("\n===== COLUMN NAMES =====")
print(df.columns)

print("\n===== DATA TYPES =====")
print(df.dtypes)

print("\n===== DATASET INFORMATION =====")
df.info()

print("\n===== MISSING VALUES =====")
print(df.isnull().sum())

print("\n===== DUPLICATES =====")
print(df.duplicated().sum())
print("\n===== CATEGORY COUNTS =====")
print(df["category"].value_counts())

print("\n===== INTENT COUNTS =====")
print(df["intent"].value_counts())