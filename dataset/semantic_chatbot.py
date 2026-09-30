import pandas as pd
import numpy as np

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# ==========================================
# 1. LOAD DATASET
# ==========================================

file_path = "dataset/processed/university_faq_enriched.csv"

df = pd.read_csv(file_path)

print("Dataset loaded successfully!")
print("Total questions:", len(df))


# ==========================================
# 2. LOAD EMBEDDING MODEL
# ==========================================

print("\nLoading AI embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model loaded successfully!")


# ==========================================
# 3. LOAD SAVED EMBEDDINGS
# ==========================================

embedding_file = "dataset/processed/question_embeddings.npy"

question_embeddings = np.load(embedding_file)

print("Question embeddings loaded successfully!")
print("Embedding shape:", question_embeddings.shape)


# ==========================================
# 4. CHECK DATASET AND EMBEDDING SIZE
# ==========================================

if len(df) != len(question_embeddings):

    raise ValueError(
        "Dataset rows and embedding rows do not match!"
    )


# ==========================================
# 5. CHATBOT FUNCTION
# ==========================================

def get_answer(user_question):

    # Create embedding for user's question
    user_embedding = model.encode([user_question])

    # Calculate cosine similarity
    similarity_scores = cosine_similarity(
        user_embedding,
        question_embeddings
    )[0]

    # Find best match
    best_match_index = similarity_scores.argmax()

    # Get similarity score
    best_score = similarity_scores[best_match_index]

    # Get matched question
    matched_question = df.iloc[best_match_index]["question"]

    # Get answer
    answer = df.iloc[best_match_index]["answer"]

    print("\nMatched Question:", matched_question)
    print("Similarity Score:", round(float(best_score), 3))

    # Confidence threshold
    if best_score < 0.40:

        return (
            "Sorry, I couldn't find a reliable answer "
            "to your question."
        )

    return answer


# ==========================================
# 6. START CHATBOT
# ==========================================

print("\n====================================")
print("     SEMANTIC UNIVERSITY CHATBOT")
print("====================================")

print("Type 'exit' to stop the chatbot.\n")


while True:

    user_question = input("You: ")

    # Exit
    if user_question.lower().strip() == "exit":

        print("Bot: Goodbye! 👋")
        break

    # Empty input
    if not user_question.strip():

        print("Bot: Please enter a question.")
        continue

    # Get answer
    answer = get_answer(user_question)

    print("Bot:", answer)