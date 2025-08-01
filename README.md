# Jarvis AI Assistant

**Jarvis** is a Python-based desktop AI assistant that listens to your voice commands and performs a wide range of tasks like telling the time/date, searching the web, playing music, managing to-do lists, sending emails, taking screenshots, recording the screen, checking system stats, and much more.

## Features

- 🎤 Voice-activated interaction (`Hey Jarvis`)
- 🕓 Tells current time and date
- 🌐 Wikipedia and Google search
- 📧 Send emails via Gmail
- 📄 Notepad integration with speech typing
- 🧮 Calculator control
- 📷 Take screenshots and photos
- 🎥 Record screen and webcam
- 🗓️ Calendar UI
- 🎵 Play music via Spotify
- 🔋 System stats (CPU, RAM, Battery)
- 😂 Tells jokes and fun facts
- 🌦️ Weather updates
- 📰 Fetch latest news
- 🧠 Gemini chatbot integration
- 🎨 Sketch photo from webcam or file
- 📋 To-do list management
- 🔊 Volume and brightness control
- 🌐 Browser automation

## 🛠 Requirements

- Python 3.8+
- Microphone and speaker
- Installed apps: Chrome, Notepad, Calculator, Spotify

### Install Dependencies

Install required Python libraries using pip:

```bash
pip install -r requirements.txt

**🧪 Setup**

- Clone the repository.
- Create a .env file with the following keys:

client_id=YOUR_SPOTIFY_CLIENT_ID
client_secret=YOUR_SPOTIFY_CLIENT_SECRET
newsapi_key=YOUR_NEWS_API_KEY
wapi_key=YOUR_OPENWEATHERMAP_API_KEY
GEMINI_API_KEY=YOUR_GEMINI_API_KEY

- Make sure your microphone permissions are enabled.
- Run the assistant:
python jarvis3.py


**🗣 Activation**
Say "**Hey Jarvis**" to activate the assistant.

📸 Examples
"Take a screenshot"

"Play songs"

"What's the weather in London?"

"Tell me a joke"

"Make a to do list"

**📌 Note**
Some functions are Windows-specific (e.g., calc.exe, taskkill, Notepad).

Voice recognition uses Google’s speech API—ensure internet connection.

For email features, you may need to enable less secure apps in Gmail or use an app password.

**🧑‍💻 Author**
Created by Shaik Mohammed Riyaz
Email functionality uses shaikriyazsm@gmail.com
