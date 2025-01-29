async function sendMessage() {
    const userInput = document.getElementById("user-input").value;
    const language = document.getElementById("language-select").value;
    const responseBox = document.getElementById("response-box");
    const aiFace = document.getElementById("ai-face");
    const chatBubble = document.getElementById("chat-bubble");

    if (!userInput.trim()) return;

    // Show typing animation
    chatBubble.innerHTML = "<span class='typing'>...</span>";
    chatBubble.classList.remove("hidden");

    try {
        const response = await fetch("/process-input", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ input: userInput, language: language })
        });

        const data = await response.json();
        if (data.response) {
            responseBox.innerHTML = `<p>${data.response}</p>`;
            chatBubble.innerHTML = data.response;
            aiFace.style.backgroundImage = `url('/static/images/${data.expression}.png')`;

            // Change AI Face Based on Response
            applyFaceExpression(data.commandType);

            // Use text-to-speech for response
            responsiveVoice.speak(data.response, getVoice(language));
        }
    } catch (error) {
        console.error("Error:", error);
    }
}

// AI Face Reaction Based on Command
function applyFaceExpression(commandType) {
    const aiFace = document.getElementById("ai-face");

    aiFace.classList.remove("happy", "surprised", "thinking", "neutral");

    switch (commandType) {
        case "greeting":
            aiFace.classList.add("happy");
            break;
        case "question":
            aiFace.classList.add("thinking");
            break;
        case "surprise":
            aiFace.classList.add("surprised");
            break;
        default:
            aiFace.classList.add("neutral");
    }
}

// Voice Recognition
function toggleVoiceInput() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = document.getElementById("language-select").value;
    
    recognition.onresult = function(event) {
        document.getElementById("user-input").value = event.results[0][0].transcript;
        sendMessage();
    };

    recognition.start();
}

// Get voice for language
function getVoice(language) {
    const voices = {
        "en": "UK English Female",
        "fr": "French Female",
        "es": "Spanish Female",
        "de": "Deutsch Female"
    };
    return voices[language] || "UK English Female";
}

