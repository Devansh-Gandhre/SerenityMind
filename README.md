# SerenityMind 🧘‍♂️

SerenityMind is an AI-powered mental health assistant designed to provide emotional support and mental well-being guidance. This project aims to offer personalized and mood-specific interactions to help users manage stress, anxiety, and other emotions through conversational AI.

## Project Features ✨

- **AI-Driven Conversations**: Chat with the AI, which adapts to different emotional states and moods.
- **Mood Selection**: Choose your mood before chatting (e.g., Calm, Motivational, Friendly, etc.).
- **Emotion-Specific Responses**: The AI adjusts its tone based on your selected mood.
- **Conversation Summary**: Get a summary of your chat for future reference.
- **Mini Activities**: Engage in small activities designed to help with relaxation and mental clarity.

## How It Works ⚙️

1. **Install Dependencies**:
   - Make sure Python and pip are installed.
   - Install the required packages using `pip install -r requirements.txt`.

2. **Set Up Your API Key 🔑**:
   - Create a `.env` file and add your **Google API Key** to it:
     ```plaintext
     GOOGLE_API_KEY=your_api_key_here
     ```

3. **Run the Flask App**:
   - Start the Flask app with:
     ```bash
     python app.py
     ```
   - The app will be available at `http://127.0.0.1:5000/`.

4. **Start Chatting**:
   - Select a mood and start chatting with the AI.
   - The AI will respond based on your selected mood and help with emotional support.

## Project Structure 🗂️

```plaintext
.
├── .env                     # Contains the API key for secure use.
├── .gitignore               # Git ignore file to exclude sensitive files.
├── app.py                   # Main backend script for the Flask app.
├── requirements.txt         # Dependencies required for the project.
└── templates/               # Folder containing HTML files for front-end.
    ├── index.html           # Home page of the app.
    ├── activities.html      # Page for mini activities.
    ├── chat.html            # Page for chatting with the AI.
    ├── mood-history.html    # Page to view past mood history.
    └── mood.html            # Page for selecting mood.


Technologies Used 💻

Flask: Web framework for creating the web application.

Google Gemini API: Powers the AI backend for dynamic conversations.

Python-dotenv: Manages environment variables for secure API key storage.

HTML/CSS/JS: Frontend structure and interactivity.


Contribution Guidelines 📝

Feel free to fork the repository, make changes, and create a pull request! Contributions are always welcome.


License 📄

This project is open-source and available under the MIT License.


Contact 💬

For any questions or feedback, reach out to me at:

Email: [devanshgandhre@gmail.com]

GitHub: Devansh-Gandhre


Let's create a peaceful and supportive environment together! 🌿