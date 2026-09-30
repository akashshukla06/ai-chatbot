import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer


# ==========================================
# 1. LOAD ABES DATASET
# ==========================================

file_path = "dataset/processed/abes_knowledge.csv"

df = pd.read_csv(file_path)

print("ABES dataset loaded!")
print("Total records:", len(df))


# ==========================================
# 2. LOAD EMBEDDING MODEL
# ==========================================

print("\nLoading embedding model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Embedding model loaded!")


# ==========================================
# 3. CREATE TEXT FOR EMBEDDINGS
# ==========================================

questions = df["question"].astype(str).tolist()


# ==========================================
# 4. CREATE EMBEDDINGS
# ==========================================

print("\nCreating ABES embeddings...")

embeddings = model.encode(
    questions,
    show_progress_bar=True
)


# ==========================================
# 5. CONVERT TO NUMPY
# ==========================================

embeddings = np.array(embeddings)


# ==========================================
# 6. SAVE EMBEDDINGS
# ==========================================

output_file = (
    "dataset/processed/abes_question_embeddings.npy"
)

np.save(
    output_file,
    embeddings
)


# ==========================================
# 7. DISPLAY RESULT
# ==========================================

print("\nABES embeddings created successfully!")

print(
    "Embedding shape:",
    embeddings.shape
)

print(
    "Saved to:",
    output_file
)