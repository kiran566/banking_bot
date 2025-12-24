import pickle
import json
import numpy as np
from  preprocessing import preprocess_text

# Load trained files
model = pickle.load(open("../models/model.pkl", "rb"))
vectorizer = pickle.load(open("../models/vectorizer.pkl", "rb"))
label_encoder = pickle.load(open("../models/label_encoder.pkl", "rb"))

with open("../data/intents.json", "r", encoding="utf-8") as f:
    intents = json.load(f)

print("Total intents:", len(intents["intents"]))
print("Intent tags:", [i["tag"] for i in intents["intents"]])
print("Contains 'hi':", "hi" in vectorizer.vocabulary_)
print("Contains 'hello':", "hello" in vectorizer.vocabulary_)
print("Vocabulary size:", len(vectorizer.vocabulary_))
GREETINGS = {"hi", "hello", "hey", "good morning", "good evening"}
GOODBYES = {"bye", "goodbye", "see you", "exit"}



def predict_intent(text, threshold=0.3):
    clean_text = preprocess_text(text)  
    if clean_text in GREETINGS:
        return "greeting"

    if clean_text in GOODBYES:
        return "goodbye"
 
    text_vec = vectorizer.transform([text])
    probs = model.predict_proba(text_vec)

    max_prob = np.max(probs)
    index = np.argmax(probs)

    if max_prob < threshold:
        return "fallback"

    return label_encoder.inverse_transform([index])[0]


# Get chatbot response
def get_response(intent):
    for item in intents["intents"]:
        if item["tag"] == intent:
            return np.random.choice(item["responses"])

    return "Sorry, I did not understand that."


# Chat loop

print("🤖 Chatbot started (type 'exit' to stop)")
while True:
    user = input("You: ")
    if user.lower() == "exit":
        break

    intent = predict_intent(user)
    response = get_response(intent)

    print("Bot:", response)
