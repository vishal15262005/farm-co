import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# Load dataset
df = pd.read_csv('chatbot_data.csv')

# Fit TF-IDF vectorizer
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['question'])

# Save vectorizer and answers
with open('model/chatbot_vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)
df['answer'].to_csv('model/chatbot_answers.txt', index=False, header=False)
df['question'].to_csv('model/chatbot_questions.txt', index=False, header=False)