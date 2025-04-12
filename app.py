from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv

# --- Load environment variables ---
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("MODEL_NAME", "models/gemini-1.5-pro-latest")

# --- Configure Gemini ---
genai.configure(api_key=api_key)

app = Flask(__name__)
CORS(app)

# --- Supported Modes with Instructions ---
support_modes = {
    "calming": "Please respond with a gentle, calming, and reassuring tone to help someone feel relaxed and safe.",
    "motivational": "Please respond with a highly motivational and uplifting tone to encourage and inspire the user.",
    "friendly": "Please respond in a warm, friendly, and conversational style like a close friend offering support.",
    "professional": "Please respond in a clear, respectful, and professional tone as a mental health assistant.",
    "casual": "Please respond in a chill, humorous, and relaxed style like a fun, supportive friend.",
    "sad": "Please respond with a compassionate and understanding tone. The user might be feeling down or emotional.",
    "lonely": "Please respond with warmth and empathy. Help the user feel heard and not alone.",
    "overwhelmed": "Please respond in a grounding and supportive tone, helping the user slow down and feel less burdened.",
    "angry": "Please respond calmly and respectfully. Help the user feel understood without escalating emotions.",
    "confused": "Please respond with clarity and reassurance, helping the user feel more certain and supported.",
    "tired": "Please respond gently, acknowledging the user's fatigue while offering calm encouragement.",
    "hopeful": "Please respond in a positive, forward-looking, and optimistic tone to foster hope.",
    "grateful": "Please respond in a warm, appreciative, and reflective tone that matches a grateful mindset.",
    "determined": "Please respond in an encouraging and empowering tone, fueling the user's motivation.",
    "burned_out": "Please respond with empathy and understanding, acknowledging exhaustion and offering rest-oriented support."
}

# --- Session Store ---
chat_sessions = {}

# --- Instruction Fetcher ---
def get_instruction(mode):
    return support_modes.get(mode, support_modes["friendly"])

# --- Routes ---
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    session_id = data.get('session_id')
    user_input = data.get('message')
    selected_mode = data.get('mode')

    if not session_id or not selected_mode:
        return jsonify({'error': 'Session ID and mode required'}), 400

    # Initialize chat if not exists
    if session_id not in chat_sessions:
        model = genai.GenerativeModel(model_name)
        chat = model.start_chat(history=[
            {"role": "user", "parts": [get_instruction(selected_mode)]},
            {"role": "model", "parts": ["Understood. I will respond accordingly."]}
        ])
        chat_sessions[session_id] = {"chat": chat, "mode": selected_mode}
    else:
        chat = chat_sessions[session_id]["chat"]

    # Update mode if changed
    if chat_sessions[session_id]["mode"] != selected_mode:
        chat_sessions[session_id]["mode"] = selected_mode
        chat.send_message(get_instruction(selected_mode))

    try:
        # Log the input
        print(f"[{session_id}] Mode: {selected_mode}")
        print(f"[{session_id}] User: {user_input}")

        response = chat.send_message(user_input)

        # Fallback if no valid response
        if not hasattr(response, 'text') or not response.text:
            fallback = "I'm here for you. Can you tell me a bit more about how you're feeling?"
            return jsonify({'reply': fallback})

        return jsonify({'reply': response.text})

    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'Error talking to Gemini API'}), 500

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.json
    session_id = data.get('session_id')

    if not session_id or session_id not in chat_sessions:
        return jsonify({'error': 'Session not found'}), 400

    chat = chat_sessions[session_id]["chat"]
    mode = chat_sessions[session_id]["mode"]
    instruction = get_instruction(mode)

    try:
        history = chat.history[2:]  # Skip instruction + acknowledgment
        history_text = "\n".join(
            f"User: {h.parts[0].text}\nAI: {history[i+1].parts[0].text}"
            for i, h in enumerate(history[:-1:2])
        )

        model = genai.GenerativeModel(model_name)
        summary_response = model.generate_content([
            instruction,
            "Summarize this conversation briefly:\n" + history_text
        ])
        return jsonify({'summary': summary_response.text})
    except Exception as e:
        print("Error during summarization:", e)
        return jsonify({'error': 'Error generating summary'}), 500

@app.route('/modes', methods=['GET'])
def get_modes():
    return jsonify({'modes': list(support_modes.keys())})

@app.route('/delete', methods=['POST'])
def delete_session():
    data = request.json
    session_id = data.get('session_id')
    if session_id in chat_sessions:
        del chat_sessions[session_id]
    return jsonify({'status': 'deleted'})

# --- Run the App ---
if __name__ == '__main__':
    app.run(debug=True)
