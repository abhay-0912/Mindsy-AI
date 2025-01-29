import random
import json
from transformers import pipeline
import spacy
from langdetect import detect

# Load Hugging Face's NER pipeline (you can change to a multilingual model if needed)
nlp_ner = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")

# Load SpaCy for other NLP tasks (optional)
nlp = spacy.load("en_core_web_sm")  # You can add other languages based on need

# Custom intents and responses
INTENTS = {
    "greeting": {
        "patterns": ["hello", "hi", "hey", "good morning", "good evening"],
        "responses": ["Hello! 😊", "Hi there! 👋", "Hey! How can I help you?", "Greetings!"],
        "expression": "happy"
    },
    "farewell": {
        "patterns": ["bye", "goodbye", "see you", "later"],
        "responses": ["Goodbye! 👋", "See you soon! 😊", "Take care!"],
        "expression": "neutral"
    },
    "thanks": {
        "patterns": ["thank you", "thanks", "appreciate it"],
        "responses": ["You're welcome! 😊", "No problem! Happy to help!", "Anytime!"],
        "expression": "happy"
    },
    "question": {
        "patterns": ["what", "how", "why", "when", "where"],
        "responses": ["That's a great question! 🤔", "Hmm, let me think..."],
        "expression": "thinking"
    },
    "surprise": {
        "patterns": ["wow", "amazing", "awesome", "incredible"],
        "responses": ["Wow indeed! 😲", "That's amazing! 🎉", "Glad you liked it!"],
        "expression": "surprised"
    },
    "fallback": {
        "responses": ["I'm not sure I understand. 🤔", "Could you rephrase that?", "I need more details."],
        "expression": "neutral"
    }
}

def detect_language(text):
    """Detects the language of the user input."""
    try:
        return detect(text)
    except:
        return "en"

def classify_intent(user_input):
    """Simple intent classification (can be enhanced with more advanced models)."""
    user_input = user_input.lower()
    
    for intent, data in INTENTS.items():
        if any(pattern in user_input for pattern in data["patterns"]):
            return intent
    
    return "fallback"

def generate_response(user_input):
    """Generates an appropriate response and AI expression."""
    detected_language = detect_language(user_input)
    intent = classify_intent(user_input)

    # Get entity recognition results using Hugging Face's model
    entities = nlp_ner(user_input)
    
    # If entities are detected, add them to the response context
    entity_text = ""
    if entities:
        entity_text = " I noticed some interesting entities: " + ", ".join([e['word'] for e in entities])

    response = random.choice(INTENTS[intent]["responses"])
    expression = INTENTS[intent]["expression"]

    # Include detected entities in the response
    response += entity_text

    return {
        "response": response,
        "expression": expression,
        "commandType": intent,
        "language": detected_language,
        "entities": entities
    }

if __name__ == "__main__":
    # Test the chatbot with some input
    user_input = input("You: ")
    result = generate_response(user_input)
    
    print(f"Bot ({result['expression']}): {result['response']}")
    print(f"Detected Entities: {result['entities']}")

