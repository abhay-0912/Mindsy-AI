from responsive_voice import ResponsiveVoice

voice_engine = ResponsiveVoice()

VOICE_OPTIONS = {
    "en": "UK English Female",
    "fr": "French Female",
    "es": "Spanish Female",
    "de": "Deutsch Female"
}

def get_voice(language_code):
    return VOICE_OPTIONS.get(language_code, "UK English Female")

def speak_text(text, language="en"):
    selected_voice = get_voice(language)
    voice_engine.speak(text, selected_voice)
