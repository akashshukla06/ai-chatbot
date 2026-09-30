import pandas as pd


# ==========================================
# 1. LOAD CLEAN DATASET
# ==========================================

input_file = "dataset/processed/university_faq_clean.csv"

df = pd.read_csv(input_file)

print("Original rows:", len(df))


# ==========================================
# 2. SPECIAL ANSWERS
# ==========================================

special_answers = {

    "exam_attendance_eligibility":
        "Exam eligibility may depend on the attendance requirement set by the university. "
        "Check the latest official attendance rules or contact your department for confirmation."
}


# ==========================================
# 3. QUESTION VARIATIONS
# ==========================================

variations = {

    # --------------------------------------
    # ATTENDANCE REQUIREMENT
    # --------------------------------------

    "attendance_requirement": [

        "What is the minimum attendance required?",
        "How much attendance do I need?",
        "What percentage of attendance is required?",
        "How much attendance is compulsory?",
        "What attendance percentage do I need?",
        "What percentage attendance is mandatory?",
        "How much attendance should I maintain?",
        "What is the required attendance percentage?"

    ],


    # --------------------------------------
    # ATTENDANCE CHECK
    # --------------------------------------

    "attendance_check": [

        "How can I check my attendance?",
        "Where can I see my attendance?",
        "How do I check my attendance?",
        "Where can I check my attendance percentage?",
        "How can I see my attendance record?",
        "Where is my attendance displayed?"

    ],


    # --------------------------------------
    # LOW ATTENDANCE
    # --------------------------------------

    "low_attendance": [

        "What happens if my attendance is low?",
        "What happens when attendance is below the requirement?",
        "What if my attendance percentage is low?",
        "What happens if I have low attendance?",
        "What can happen because of low attendance?",
        "What should I do if my attendance is low?"

    ],


    # --------------------------------------
    # ATTENDANCE CORRECTION
    # --------------------------------------

    "attendance_correction": [

        "Can attendance be corrected if it is wrong?",
        "What should I do if my attendance is incorrect?",
        "How can I correct an attendance mistake?",
        "My attendance is wrong, how can I fix it?",
        "Can an incorrect attendance record be changed?"

    ],


    # --------------------------------------
    # EXAM ATTENDANCE ELIGIBILITY
    # --------------------------------------

    "exam_attendance_eligibility": [

        "Can I appear for exams with low attendance?",
        "Can I sit for exams if my attendance is low?",
        "Will low attendance affect my exam eligibility?",
        "Can I give exams with low attendance?",
        "Am I eligible for exams if my attendance is below the requirement?",
        "Will I be allowed to take the exam with low attendance?",
        "What happens to exam eligibility because of low attendance?"

    ]

}


# ==========================================
# 4. CREATE NEW ROWS
# ==========================================

new_rows = []


for intent, questions in variations.items():

    # Find original row for this intent
    matching_rows = df[df["intent"] == intent]

    # Special intent may not exist in original dataset
    if matching_rows.empty:

        # Only continue if we have a special answer
        if intent not in special_answers:
            print(f"Warning: No original data found for {intent}")
            continue

        category = "Attendance"

        answer = special_answers[intent]

    else:

        original_row = matching_rows.iloc[0]

        category = original_row["category"]

        answer = special_answers.get(
            intent,
            original_row["answer"]
        )


    # Create rows for every question variation
    for question in questions:

        new_rows.append({

            "question": question,

            "answer": answer,

            "category": category,

            "intent": intent

        })


# ==========================================
# 5. CONVERT TO DATAFRAME
# ==========================================

new_df = pd.DataFrame(new_rows)


print("\nNew variation rows:", len(new_df))


# ==========================================
# 6. COMBINE ORIGINAL + NEW DATA
# ==========================================

df_combined = pd.concat(
    [df, new_df],
    ignore_index=True
)


# ==========================================
# 7. REMOVE DUPLICATE QUESTIONS
# ==========================================

df_combined = df_combined.drop_duplicates(
    subset=["question"]
)


# ==========================================
# 8. RESET INDEX
# ==========================================

df_combined = df_combined.reset_index(
    drop=True
)


# ==========================================
# 9. SAVE ENRICHED DATASET
# ==========================================

output_file = "dataset/processed/university_faq_enriched.csv"

df_combined.to_csv(
    output_file,
    index=False
)


# ==========================================
# 10. FINAL INFORMATION
# ==========================================

print("\n====================================")
print(" ENRICHED DATASET CREATED")
print("====================================")

print("Original rows:", len(df))

print("New variation rows:", len(new_df))

print("Final rows:", len(df_combined))

print("Output file:")
print(output_file)

print("\nColumns:")
print(df_combined.columns.tolist())

print("\nIntent counts:")
print(df_combined["intent"].value_counts())