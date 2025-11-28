import speech_recognition as sr
import logging
import datetime
import wikipedia
import webbrowser
import subprocess
from google import genai
import os
import json
import sounddevice as sd
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()

logging.basicConfig(
    format="[%(asctime)s] %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)

# Define predefined commands (no Gemini needed for these)
PREDEFINED_COMMANDS = {
    "websites": {
        "youtube": "https://youtube.com",
        "google": "https://google.com",
        "github": "https://github.com",
        "twitter": "https://twitter.com",
        "reddit": "https://reddit.com",
        "facebook": "https://facebook.com",
        "instagram": "https://instagram.com",
        "linkedin": "https://linkedin.com",
        "netflix": "https://netflix.com",
        "amazon": "https://amazon.com",
    },
    "apps": {
        "terminal": "Terminal",
        "vscode": "Visual Studio Code",
        "code": "Visual Studio Code",
        "notes": "Notes",
        "mail": "Mail",
        "calendar": "Calendar",
        "finder": "Finder",
    }
}

def speak(text):
    """Text-to-speech using macOS native voices"""
    subprocess.run(["say", text])

def takeCommand():
    """Listen to user's voice command"""
    r = sr.Recognizer()
    print("Listening...")
    try:
        duration = 3
        samplerate = 16000
        audio_array = sd.rec(int(duration * samplerate), samplerate=samplerate, 
                                channels=1, dtype='int16')
        sd.wait()
        
        audio_bytes = audio_array.tobytes()
        audio_data = sr.AudioData(audio_bytes, samplerate, 2)
        
        print("Recognizing...")
        query = r.recognize_google(audio_data)
        print(f"User said: {query}\n")
        return query.lower()
    except Exception as e:
        logging.error(str(e))
        print("Say that again please!")
        return None

def handle_predefined_command(query: str) -> bool:
    """
    Check if query matches predefined commands.
    Returns True if handled, False if needs Gemini.
    """
    
    # Exit commands
    if any(word in query for word in ['exit', 'quit', 'goodbye', 'stop']):
        speak("Goodbye sir! Have a nice day.")
        return "EXIT"
    
    # Time query
    if "time" in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"Sir, the time is {strTime}")
        return True
    
    # Your name
    if "your name" in query:
        speak("My name is Jarvis, sir.")
        return True
    
    # Wikipedia search
    if "wikipedia" in query:
        speak("Searching Wikipedia...")
        search_query = query.replace("wikipedia", "").strip()
        try:
            results = wikipedia.summary(search_query, sentences=2)
            speak("According to Wikipedia")
            speak(results)
        except Exception as e:
            speak("I couldn't find that on Wikipedia.")
        return True
    
    # Website opening
    for keyword, url in PREDEFINED_COMMANDS["websites"].items():
        if f"open {keyword}" in query or f"launch {keyword}" in query or f"start {keyword}" in query:
            speak(f"Opening {keyword}")
            webbrowser.open(url)
            return True
    
    # App opening
    for keyword, app_name in PREDEFINED_COMMANDS["apps"].items():
        if f"open {keyword}" in query or f"launch {keyword}" in query or f"start {keyword}" in query:
            speak(f"Opening {app_name}")
            subprocess.Popen(["/usr/bin/open", "-a", app_name])
            return True
    
    # Not a predefined command
    return False

def ask_gemini_intelligent(query: str):
    """
    Use Gemini for complex/unknown queries.
    Gemini will interpret and provide actionable response.
    """
    try:

        # Configure your API Key
        client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))
        
        JARVIS_INTELLIGENT_PROMPT = """
You are JARVIS, an intelligent voice assistant for macOS.

Your job: Interpret the user's query and provide a structured response.

Available actions you can suggest:
1. "open_website" - For websites not in predefined list
2. "open_app" - For macOS apps not in predefined list  
3. "search_web" - Search something on Google
4. "answer" - Answer general questions directly

Response format (JSON only, no markdown):
{
  "action": "action_type",
  "parameters": {
    "url": "https://...",
    "app_name": "AppName",
    "query": "search query"
  },
  "speak": "What to say to user",
  "answer": "Direct answer if applicable"
}

Examples:

User: "What's the capital of France?"
{
  "action": "answer",
  "speak": "The capital of France is Paris",
  "answer": "The capital of France is Paris"
}

User: "Open Stack Overflow"
{
  "action": "open_website",
  "parameters": {"url": "https://stackoverflow.com"},
  "speak": "Opening Stack Overflow"
}

User: "Launch Slack"
{
  "action": "open_app",
  "parameters": {"app_name": "Slack"},
  "speak": "Launching Slack"
}

User: "Search for Python tutorials"
{
  "action": "search_web",
  "parameters": {"query": "Python tutorials"},
  "speak": "Searching for Python tutorials"
}

Keep answers concise and helpful.
"""
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"{JARVIS_INTELLIGENT_PROMPT}\n\nUser query: \"{query}\""
        )
        
        # Clean and parse response
        response_text = response.text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        
        command = json.loads(response_text.strip())
        logging.info(f"Gemini response: {command}")
        
        # Execute based on Gemini's interpretation
        speak(command.get("speak", "Working on it"))
        
        action = command.get("action")
        params = command.get("parameters", {})
        
        if action == "open_website":
            url = params.get("url")
            if url:
                webbrowser.open(url)
                
        elif action == "open_app":
            app_name = params.get("app_name")
            if app_name:
                subprocess.Popen(["/usr/bin/open", "-a", app_name])
                
        elif action == "search_web":
            search_query = params.get("query")
            if search_query:
                webbrowser.open(f"https://www.google.com/search?q={search_query}")
                
        elif action == "answer":
            answer = command.get("answer")
            if answer and answer != command.get("speak"):
                speak(answer)
        
    except json.JSONDecodeError as e:
        logging.error(f"JSON parsing error: {str(e)}")
        speak("I understood your request, but couldn't process it correctly.")
    except Exception as e:
        logging.error(f"Gemini error: {str(e)}")
        speak("I'm having trouble with that request.")

def greeting():
    """Greet the user based on time of day"""
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        speak("Good Morning sir! ")
    elif hour >= 12 and hour < 18: 
        speak("Good Afternoon sir! ")
    else:
        speak("Good Evening sir! ")

def main():
    """Main loop with cost-efficient command handling"""
    greeting()
    
    while True:
        query = takeCommand()
        
        if query is None:
            continue
        
        # First, try predefined commands (FREE)
        result = handle_predefined_command(query)
        
        if result == "EXIT":
            break
        elif result:
            logging.info("✓ Handled by predefined commands")
            continue
        
        # If not predefined, use Gemini (COSTS MONEY)
        logging.info("⚠ No predefined match - calling Gemini")
        ask_gemini_intelligent(query)

if __name__ == "__main__":
    main()