from flask import Flask, request, jsonify
from services.ai_engine import detect_intent, generate_response
from services.voice_manager import speak_text
from services.animations import get_expression

app = Flask(__name__)

@app.route("/process-input", methods=["POST"])
def process_input():
    data = request.json
    user_input = data.get("input", "")
    language = data.get("language", "en")

    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    intent = detect_intent(user_input)
    response = generate_response(intent)
    expression = get_expression(intent)

    speak_text(response, language)

    return jsonify({"response": response, "expression": expression})
