# import required libraries
import nltk
import joblib
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import json

#punkit - sentence splitter
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('wordnet')

with open("intents.json", "r") as file:
    intents = json.load(file)

lemmatizer = WordNetLemmatizer()
texts = []
labels = []

for intent in intents["intents"]:
    for pattern in intent["patterns"]:
        words = nltk.word_tokenize(pattern)
        words = [lemmatizer.lemmatize(word.lower()) for word in words]
        texts.append(" ".join(words))
        labels.append(intent["tag"])

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)

model = LogisticRegression(max_iter=1000)
model.fit(X, labels)

joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("Training completed and ready for Fast API")