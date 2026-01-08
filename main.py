# develop API's --- get, post, put, delete
from fastapi import FastAPI
# connect to frontend (ex. React, Angular, VueJS, CoffeeScript, ...)
from fastapi.middleware.cors import CORSMiddleware
# detect request format
from pydantic import BaseModel

# NLP module
import nltk
# load pkl files
import joblib
# use json format
import json
# convert human english ---> dictionary english
from nltk.stem import WordNetLemmatizer

#punkit - sentence splitter
#download
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('wordnet')

# create app
app = FastAPI(title="NLP Chatbot Appln",
                description= "we want to build e2e appln including frontend, fastapi, NLP, AWS, MongoDB",
                version="1.0")

# app object used to build rest api calls

#Jenkins defaults to port 8080 for its web interface (HTTP)
#Docker Port 80 for standard HTTP web servers (e.g., Nginx, Apache).
#The default port for a React development server (when using tools like Create React App or Vite) is 3000

app.add_middleware(CORSMiddleware,
                   #allow on all ports 
                   allow_origins=["*"],
                   #allow on all crendentials, password, etc
                   allow_credentials=True,
                   allow_methods=["*"],
                   #allow tokens
                   allow_headers=["*"])

#load pkl files using joblib
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

#read json file in read mode
with open("intents.json", "r") as file:
    intents = json.load(file)
    lemmatizer = WordNetLemmatizer()

class ChatRequest(BaseModel):
    message : str

#text coming from react, text convert to nltk for cleaning, words converted to dictionary english
def clean_text(text: str):
    words = nltk.word_tokenize(text)
    words = [lemmatizer.lemmatize(word.lower()) for word in words]
    return " ".join(words)

def get_bot_response(user_message:str):
    cleaned_message = clean_text(user_message)
    vector = vectorizer.transform([cleaned_message])
    predicted_tag = model.predict(vector)[0]
    
    for intent in intents["intents"]:
        if intent["tag"] == predicted_tag:
            return intent["responses"][0]
    
    return "Sorry, I didn't understand your message"
    
@app.get("/")
def home():
    return {
        "status" : "success",
        "message" : "ChatBot API is running successfully"
    }
        
@app.post("/chat")
def chat(request : ChatRequest):
    response = get_bot_response(request.message)
    return {
        "user_message" : request.message,
        "bot_response" : response
    }