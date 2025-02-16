import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util
from fuzzywuzzy import process

# Load Pre-trained SBERT Model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load the Dataset
df = pd.read_csv("data/college_data.csv", encoding="ISO-8859-1")

# Convert Questions to Embeddings (for SBERT)
df["question"] = df["question"].str.strip().str.lower()  # Normalize dataset questions
df["question_embedding"] = df["question"].apply(lambda q: model.encode(q, convert_to_tensor=True))

# Function to Get the Best Matching Answer
def get_answer(user_query):
    # ✅ **Preprocess user input**
    user_query = user_query.strip().lower()

    # 1️⃣ **Keyword-Based Matching**
    keywords = {
        "location": "where is college located?",
        "address": "where is college located?",
        "chairman": "who is the chairman?",
        "courses": "what are the courses offered?",
    }
    
    for key, value in keywords.items():
        if key in user_query:
            match = df[df["question"] == value]
            if not match.empty:
                return match.iloc[0]["answer"]

    # 2️⃣ **Fuzzy Matching - Get Best Match**
    fuzzy_result = process.extractOne(user_query, df["question"], scorer=process.fuzz.partial_ratio)
    
    if fuzzy_result:
        fuzzy_match, fuzzy_score = fuzzy_result[0], fuzzy_result[1]
    else:
        fuzzy_match, fuzzy_score = None, 0  

    if fuzzy_score > 70:
        match = df[df["question"] == fuzzy_match]
        if not match.empty:
            return match.iloc[0]["answer"]

    # 3️⃣ **SBERT Similarity Matching**
    user_embedding = model.encode(user_query, convert_to_tensor=True)
    similarities = [util.pytorch_cos_sim(user_embedding, q_emb)[0].item() for q_emb in df["question_embedding"]]
    
    best_match_idx = np.argmax(similarities)

    if similarities[best_match_idx] > 0.3:
        return df.iloc[best_match_idx]["answer"]

    return "I'm sorry, I don't have an answer for that."
