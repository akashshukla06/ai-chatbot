import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ==========================================
# 1. LOAD ENRICHED DATASET
# ==========================================

file_path = "dataset/processed/university_faq_enriched.csv"

df = pd.read_csv(file_path)

print("Dataset loaded successfully!")
print("Total questions:", len(df))

# ==========================================
# 2. CREATE TF-IDF VECTORIZER
# ==========================================

vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english"
)

# Convert all FAQ questions into TF-IDF vectors
question_vectors = vectorizer.fit_transform(df["question"])


# ==========================================
# 3. CHATBOT FUNCTION
# ==========================================

def get_answer(user_question):

    # Convert user's question into TF-IDF vector
    user_vector = vectorizer.transform([user_question])

    # Calculate similarity with all dataset questions
    similarity_scores = cosine_similarity(
        user_vector,
        question_vectors
    )

    # Find the most similar question
    best_match_index = similarity_scores.argmax()

    # Get similarity score
    best_score = similarity_scores[0][best_match_index]

    # Get matching question
    matched_question = df.iloc[best_match_index]["question"]

    # Get answer
    answer = df.iloc[best_match_index]["answer"]

    # Minimum confidence
    if best_score < 0.20:
        return "Sorry, I couldn't find a reliable answer to your question."

    # Show matching information
    print("\nMatched Question:", matched_question)
    print("Similarity Score:", round(best_score, 3))

    return answer


# ==========================================
# 4. START CHATBOT
# ==========================================

print("\n====================================")
print("       UNIVERSITY AI CHATBOT")
print("====================================")
print("Type 'exit' to stop the chatbot.\n")


while True:

    user_question = input("You: ")

    # Exit
    if user_question.lower() == "exit":
        print("Bot: Goodbye! 👋")
        break

    # Empty question
    if not user_question.strip():
        print("Bot: Please enter a question.")
        continue

    # Get answer
    answer = get_answer(user_question)

    print("Bot:", answer)