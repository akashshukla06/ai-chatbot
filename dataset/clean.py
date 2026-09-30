import pandas as pd

# Load raw dataset
input_file = "dataset/raw/university_faq.csv"

df = pd.read_csv(input_file)

print("Original dataset shape:", df.shape)

# Remove completely empty rows
df = df.dropna(how="all")

# Remove rows where important fields are missing
df = df.dropna(subset=["question", "answer", "category", "intent"])

# Convert text columns to string
text_columns = ["question", "answer", "category", "intent"]

for column in text_columns:
    df[column] = df[column].astype(str).str.strip()

# Remove duplicate questions
df = df.drop_duplicates(subset=["question"])

# Save cleaned dataset
output_file = "dataset/processed/university_faq_clean.csv"

df.to_csv(output_file, index=False)

print("Cleaned dataset shape:", df.shape)
print("Cleaned dataset saved successfully!")
print("File:", output_file)