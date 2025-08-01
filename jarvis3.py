import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import smtplib
import pyautogui
import os
import pyjokes
import webbrowser as wb
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth 
import pyautogui
import psutil
import pyjokes
import subprocess
import time
import numpy as np
import cv2
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()
import threading
import queue
import mss
import logging
import randfacts
import pywhatkit
import requests
import pyowm
from tkcalendar import Calendar
import mss
import randfacts

logging.getLogger('comtypes').setLevel(logging.INFO)
logging.basicConfig(level=logging.ERROR)
# Set the logging level
def record_video(output_folder, duration=10):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    video_filename = os.path.join(output_folder, f"video_{timestamp}.avi")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    fps = 20.0
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    out = cv2.VideoWriter(video_filename, fourcc, fps, (frame_width, frame_height))

    print("Recording... Say 'close' to stop early.")
    start_time = datetime.datetime.now()
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        out.write(frame)
        cv2.imshow("Recording", frame)
        if (datetime.datetime.now() - start_time).seconds >= duration:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        speech = takeSpeech().lower()
        if 'close' in speech or 'exit' in speech:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"Video saved as: {video_filename}")
    speak("Done")
    todo_list = []

def listen_for_task():
    while True:
        speak('Tell me the task')
        task = takeSpeech()
        if task and task.lower() != "none":
            todo_list.append(task)
            speak("Task added.")
        else:
            speak("No task was added.")

        speak("Do you want to add another task? (yes/add/no)")
        answer = takeSpeech()  
        if answer and "no" in answer.lower():
            break

def show_todolist():
    if todo_list:
        speak("Here is your to-do list:")
        print("Here is your to-do list:")  
        for i, item in enumerate(todo_list, start=1):
            print(f"{i}. {item}")  
            speak(f"{i}. {item}")  
    else:
        speak("Your to-do list is empty.")
        print("Your to-do list is empty.") 
        
def screen_record():
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    fps = 15.0
    screen_size = (1920, 1080)  # Set to your desired resolution
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'screen_recording_{timestamp}.avi'
    output_path = os.path.join(os.getcwd(), filename)
    out = cv2.VideoWriter(output_path, fourcc, fps, screen_size)

    print(f"Recording... Press 'q' or Say 'close' to stop. Saving as '{output_path}'.")

    try:
        consecutive_black_frames = 0
        with mss.mss() as sct:
            while True:
                img = sct.grab(sct.monitors[1])  
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

                if is_black_frame(frame):
                    consecutive_black_frames += 1
                    print("Detected black frame...")
                else:
                    consecutive_black_frames = 0

                out.write(frame)
                cv2.imshow("Recording", frame)

                if consecutive_black_frames > 10:
                    print("Screen recording may be blocked. Stopping recording.")
                    break

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                if 'close' in takeSpeech().lower() or 'exit' in takeSpeech().lower():
                    break

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        out.release()
        cv2.destroyAllWindows()
        print(f"Recording stopped and saved as '{output_path}'.")
        speak("Done")


active_mode = False
message_queue = queue.Queue()  
try:
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Setting default speech rate
except Exception as e:
    print(f"Error initializing speech engine: {e}")
    exit(1)
def female_voice():
    engine=pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        if 'zira' in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    engine.setProperty('rate', 170) 
    engine.setProperty('volume', 0.9)  
    engine.say("Hello, I am a female voice.")
    engine.runAndWait()

def choose_voice():
    speak("Would you like a male or female voice?")
    voice_choice = takeSpeech().lower()
    if "female" in voice_choice:
        female_voice()
    elif "male" in voice_choice:
        male_voice() 
    else:
        speak("I didn't understand your choice. Defaulting to male voice.")
        male_voice()  

def male_voice():
    engine=pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        if 'male' in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    engine.setProperty('rate', 150)  
    engine.setProperty('volume', 1)  
    engine.say("Hello, I am a male voice.")
    engine.runAndWait()
def open_calc():
      speak("Opening calculator")
      os.system("calc.exe")
      while True:
          com=takeSpeech().lower()
          if "close" in com:
              speak("closing calculator")
              pyautogui.hotkey('alt','f4')
              os.system("taskkill /f /im calc.exe")
              break


def is_black_frame(frame):
# Define a threshold for detecting black frames
    threshold = 10  
    return np.mean(frame) < threshold
def cpu():
    usage = str(psutil.cpu_percent())
    speak("CPU is at " + usage)

def battery_percent():
    battery = psutil.sensors_battery()
    speak("Battery is at")
    speak(f"{battery.percent}%")

def ram_usage(): 
    process = psutil.Process()
    memory_info = process.memory_info()
    #Print used memory in bytes
  #speak(f"Used RAM: {memory_info.rss} bytes")
    used_ram_mb = memory_info.rss / (1024 ** 2)  # Convert to MB
    speak(f"Used RAM: {used_ram_mb:.2f} MB")

def jokes():
    speak("Here's one")
    joke=pyjokes.get_joke()
    print(joke)
    speak(joke)


output_folder = "recorded_videos"
todo_list = []

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeSpeech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        
        audio = r.listen(source)
        
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(query)
    except Exception as e:
        print(e)
        speak("Say it again please.")
        return "None"
    return query 

def listen_for_activation():
    try:
        recognizer = sr.Recognizer()
        print("Initializing microphone...")
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            while True:
                print("Listening for 'Hey Jarvis'...")
                try:
                    audio = recognizer.listen(source)
                    try:
                        command = recognizer.recognize_google(audio, language='en-in')
                        if command is not None and "hey jarvis" in command.lower():
                            speak("How can I help you?")
                            main_command_loop()  # Enter the command loop after activation
                    except sr.UnknownValueError:
                        print("Sorry, I could not understand the audio.")
                    except sr.RequestError as e:
                        print(f"Could not request results; {e}")
                except Exception as e:
                    print(f"Error listening: {e}")
                    continue
    except Exception as e:
        print(f"Error initializing microphone: {e}")
        exit(1)
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login("219X1A3343@gprec.ac.in", "Jassu@2021")# sender's gmail account
    #recipient_email = input("Enter the recipient's email address: ")
    server.sendmail('219X1A3343@gprec.ac.in', to, content)
    print("Email sent successfully")
    server.close()
def open_notepad() :
    os.startfile('notepad.exe')
    time.sleep(1)
    speak("Notepad is now open.")
    while True:
        nq = takeSpeech().lower()
        if "paste" in nq:
                pyautogui.hotkey('ctrl','v')
                speak("done sir")
        elif "save this file" in nq:
                pyautogui.hotkey('ctrl','s')
                speak("Please specify a name for this file")
                nsq=takeSpeech()
                pyautogui.write(nsq)
                pyautogui.press('enter')
        elif "type" in nq:
            speak("what do you want to type?")
            while True:
                nw=takeSpeech()
                if nw=='exit':
                        speak("done")
                        break
                else:
                        pyautogui.write(nw)
        elif "close notepad" in nq:
            speak("Closing notepad")
            pyautogui.hotkey('ctrl','w')
            break
def open_youtube():
    speak("Opening YouTube")
    wb.open(f'https://www.youtube.com')
    while True:
        yq = takeSpeech().lower()
        if 'search' in yq:
            yq=yq.replace("search","").strip()
            pyautogui.hotkey('ctrl','l')
            pyautogui.write(f"www.youtube.com/results?search_query={yq}")
            pyautogui.press('enter')
        elif 'close youtube' in yq:
            pyautogui.hotkey('ctrl','w')
            os.system("taskkill /f /im chrome.exe")
            break
        elif 'increase volume' in yq or 'volume up' in yq:
            pyautogui.press('volumeup')
            pyautogui.press('volumeup')
        elif 'decrease volume' in yq or 'volume down' in yq:
            pyautogui.press('volumedown')
        elif 'mute' in yq:
            pyautogui.press('volumemute')
        elif 'increase brightness' in yq:
            pyautogui.press('brightnessup')
        elif 'decrease brightness' in yq:
            pyautogui.press('brightnessdown')
        elif 'open notepad' in yq:
            open_notepad()
    
def get_chrome_path():
    common_paths = [
        "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
        r"//usr//bin//google-chrome",  # For Linux
        r"//Applications//Google Chrome.app//Contents//MacOS//Google Chrome"  # For macOS
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            return path
    return None

# chrome_path = get_chrome_path()               


def is_app_installed(app_name):
    common_paths = [
        r"C:\Program Files",
        r"C:\Program Files (x86)",
        r"C:\Users\<YourUsername>\AppData\Local",
        r"C:\Users\<YourUsername>\AppData\Roaming"
    ]
    for path in common_paths:
        if os.path.exists(os.path.join(path, app_name)):
            return True
    return False
def open_calendar():
    def show_selected_date():
        selected_date = cal.get_date()
        print(f"Selected date: {selected_date}")

    def close_calendar(event=None):
        root.quit()
        

    root = tk.Tk()
    root.title("Calendar")
    root.geometry("300x300")
    current_date = datetime.datetime.now()
    cal = Calendar(root, selectmode='day', year=current_date.year, month=current_date.month, day=current_date.day)
    cal.pack(pady=20)

    btn = tk.Button(root, text="Get Selected Date", command=show_selected_date)
    btn.pack(pady=10)

    root.bind('<q>', close_calendar)
    root.protocol("WM_DELETE_WINDOW", close_calendar)
    root.mainloop()# Ensure the window is visible
    
    
      

def screenshot():
    screenshots_dir = os.path.join(os.path.expanduser('~'), 'Pictures', 'Screenshots')
    os.makedirs(screenshots_dir, exist_ok=True)
    img = pyautogui.screenshot()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(screenshots_dir, f"screenshot_{timestamp}.jpg")
    img.save(filename)
    print(f"Screenshot saved to: {filename}")

def main_command_loop():
    output_folder="videos"
    global active_mode
    wishme()
    choose_voice()
    
    while True:
        if is_spotify_running():
                print("Spotify is running. Waiting for it to close...")
                continue  # Skip to the next iteration if Spotify is running
        if active_mode:
                time.sleep(1)
                continue
        query = takeSpeech().lower()
        
        if 'time' in query:
            get_time()  # Call the renamed function
            
        elif 'date' in query:
            get_date()
        
        elif 'wikipedia' in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            res = wikipedia.summary(query, sentences=2)
            print(res)
            speak(res)
        
        elif 'send email' in query:
            try:
                recipient_email = input("Enter the recipient's email address: ")
                speak("What should I say?")
                content = takeSpeech()
                to = recipient_email
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Unable to send the email")
        
        elif 'search' in query:
            speak("What do you want to search for?")
            search = takeSpeech().lower()
            if search != 'none':
                search_url = f"https://www.google.com/search?q={search}"
                browser_path = get_chrome_path() 
                subprocess.Popen([browser_path, search_url])  # Open the browser with the search URL
                wait_for_browser_to_close(browser_path)  # Wait until the browser is closed
            else:
                speak("Please say the search query again")
        elif 'open on browser' in query:
                speak("What do you want to open for?")
                search = takeSpeech().lower()
                if search != 'none':
                    search_url = f"https://www.google.com/search?q={search}.com"
                    # browser_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" 
                    browser_path = get_chrome_path() 
                    subprocess.Popen([browser_path, search_url])  # Open the browser with the search URL
                    wait_for_browser_to_close(browser_path)  # Wait until the browser is closed
                else:
                    speak("Please say the search query again")
        
        elif 'logout' in query:
            os.system("shutdown -l")
        
        elif 'shutdown' in query:
            os.system("shutdown /s /t 1")
        
        elif 'restart' in query:
            os.system("shutdown /r /t 1")
                        
        elif 'remember' in query:
            speak("What do you want me to remember?")
            data = takeSpeech()
            speak("You said me to remember that " + data)
            remember = open('data.txt', 'w')
            remember.write(data)
            remember.close()
            
        elif 'reminder' in query:
            remember = open('data.txt', 'r')
            speak("You said me to remember that " + remember.read())
        elif 'make a to do list' in query:
                listen_for_task()
                
        elif 'show me the to do list' in query:
                show_todolist()
            
        elif 'screenshot' in query:
            speak("Taking screenshot...")
            screenshot()
            speak("done")
        elif 'youtube' in query:
            open_youtube()
        elif 'battery percent' in query or 'battery percentage' in query:
                battery_percent()
                
        elif 'cpu' in query:
                cpu()
                
        elif 'ram used' in query:
                ram_usage()
                
        elif 'joke' in query or 'jokes' in query:
                jokes()
            
      
            
        elif 'play songs' in query or 'play song' in query:
            speak("Asking spotify to play songs...")
            play_spotify()
                        
        elif 'sketch me' in query:
            handle_sketching()
            
        elif 'how is the weather' in query:
            handle_weather()
            
        elif 'calendar' in query:
            speak("Opening calendar...")
            open_calendar() 
            
        elif 'latest news' in query:
            speak("Here are the latest news")
            newsapi_key = os.getenv('newsapi_key')
            if not newsapi_key:
                speak("News API key is not set. Please set the newsapi_key environment variable.")
                print("Error: News API key is not set. Please set the newsapi_key environment variable.")
            else:
                get_latest_news(newsapi_key)

        elif "let's chat" in query or 'chat with me' in query:
            speak("Okay, as you wish.")
            chat_thread = threading.Thread(target=chat_with_user)
            chat_thread.start() 
            
        elif "fact" in query or "facts" in query:
            x = randfacts.get_fact()
            print(x)
            speak("Did you know that, " + x)
        
        elif 'notepad' in query:
            speak("Opening Notepad...")
            open_notepad()
        elif 'start recording' in query:
            speak("Recording started. Please speak now.")
            record_video(output_folder, duration=10)
        elif 'activate screen recorder' in query:
            speak('Recording started')
            screen_record()

        
        elif 'open command prompt' in query:
            speak("Opening Command Prompt...")
            os.system("start cmd")
        
        elif 'close command prompt' in query:
            speak("Closing Command Prompt...")
            os.system("taskkill /f /im cmd.exe")
        
        elif 'play' and 'video' in query:
            query = query.replace("play video", '').strip()
            speak("Playing " + query)
            pywhatkit.playonyt(query)
        elif 'calculator' in query:
            open_calc()
        
        elif 'maximize' in query:
            speak("Maximizing.")
            pyautogui.hotkey('win', 'up', 'up')
        
        elif 'minimise' in query:
            speak("Minimizing.")
            pyautogui.hotkey('win', 'down', 'down')
        elif 'close' in query:
            query=query.replace('close','').strip()
            close_application('query')
        elif 'condition of pc' in query:
            speak("Checking the condition of your PC...")
            condition()
        elif 'increase volume' in query or 'volume up' in query:
            pyautogui.press('volumeup')
            pyautogui.press('volumeup')
            pyautogui.press('volumeup')
        elif 'decrease volume' in query or 'volume down' in query:
            pyautogui.press('volumedown')
        elif 'mute' in query:
            pyautogui.press('volumemute')
        elif 'increase brightness' in query:
            pyautogui.press('brightnessup')
            pyautogui.press('brightnessup')
        elif 'decrease brightness' in query:
            pyautogui.press('brightnessdown')
        elif 'offline' in query:
            quit()

def get_time():  
    Time = datetime.datetime.now().strftime("%I:%M:%S")
    speak("The current time is")
    speak(Time)
def condition():
    usage = str(psutil.cpu_percent())
    speak(f"CPU is at {usage} percentage")
    battery = psutil.sensors_battery()
    percentage = battery.percent
    speak(f"Boss our system have {percentage} percentage battery")

    if percentage>=80:
        speak("Boss we could have enough charging to continue our recording")
    elif percentage>=40 and percentage<=75:
        speak("Boss we should connect our system to charging point to charge our battery")
    else:
        speak("Boss we have very low power, please connect to charging otherwise recording should be off...")

def get_date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    day = int(datetime.datetime.now().day)
    
    speak("Today's date is")
    speak(f'{day} {month} {year}')

def get_latest_news(api_key):
    url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            news_data = response.json()
            for article in news_data['articles'][:3]:
                speak(f"Title: {article['title']}")
                print(f"Title: {article['title']}")
                speak(f"Description: {article['description']}")
                print(f"Description: {article['description']}")
                print(f"URL: {article['url']}\n")
        else:
            print("Failed to fetch news")
            speak("Failed to fetch news. Please check your API key and internet connection.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching news: {e}")
        speak("An error occurred while fetching news. Please check your internet connection.")
def wishme():
    speak("Welcome back Sir!")
    #get_time()
    #get_date()    
    hour = datetime.datetime.now().hour
    if hour >= 6 and hour < 12:
        speak("Good morning sir!")
    elif hour >= 12 and hour < 18:
        speak("Good afternoon sir!")
    elif hour >= 18 and hour < 24:
        speak("Good evening sir!")
    else:
        speak("Good night sir!")
    
    speak("Please tell me how can I help you?")

def get_weather(city, wapi_key):
    try:
        owm = pyowm.OWM(wapi_key)
        mgr = owm.weather_manager()

        observation = mgr.weather_at_place(city)
        weather = observation.weather

        print(f"Weather in {city}:")
        speak(f"Description: {weather.detailed_status}")
        print(f"Description: {weather.detailed_status}")
        speak(f"Temperature: {weather.temperature('celsius')['temp']}°C")
        print(f"Temperature: {weather.temperature('celsius')['temp']}°C")
        print(f"Humidity: {weather.humidity}%")
        print(f"Wind Speed: {weather.wind()['speed']} m/s")

    except pyowm.exceptions.NotFoundError:
        print(f"City '{city}' not found. Please check the name and try again.")
        speak(f"Sorry, I couldn't find the weather for {city}. Please check the city name.")
    
    except pyowm.exceptions.UnauthorizedError:
        print("Invalid API key. Please check your API key and try again.")
        speak("I encountered an issue with the API key. Please check your settings.")

    except Exception as e:
        print(f"An error occurred: {e}")
        speak("Sorry, I encountered an error while fetching the weather information.")

def play_spotify():
    path = "C:\\Users\\Jaswanth Kumar Reddy\\AppData\\Roaming\\Spotify\\spotify.exe"  

    if is_spotify_running():
        speak("Spotify is already running. Playing a song...")
    else:
        if os.path.exists(path):
            os.startfile(path)  
            #os.system("start Spotify")
            speak("Spotify is now open.")
            time.sleep(2)
        else:
            try:
                sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv("client_id"),
                                                                client_secret=os.getenv("client_secret"),
                                                                redirect_uri='http://localhost:8888/callback',
                                                                scope='user-modify-playback-state,user-read-playback-state'))

                results = sp.current_user_saved_tracks(limit=1)  
                if results['items']:
                    track_id = results['items'][0]['id']
                    track_uri = f'spotify:track:{track_id}'
                    sp.start_playback(uris=[track_uri])
                    speak("Playing a song now.")
                else:
                    speak("No songs found in your library.")
            except Exception as e:
                print(e)
                speak("There was an error trying to play a song.")
def take_photo():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        messagebox.showerror("Error", "Cannot open camera")
        return None
    ret, frame = cap.read()
    if not ret:
        messagebox.showerror("Error", "Can't receive frame")
        return None
    cap.release()
    cv2.imwrite("captured_photo.jpg", frame)
    return frame
def load_image_from_file():
    file_path = filedialog.askopenfilename(title="Select an Image", 
                                            filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp")])
    if file_path:
        image = cv2.imread(file_path)
        return image
    return None
def display_images(original, sketch):
    cv2.imshow("Original Photo", original)
    cv2.imshow("Sketch", sketch)
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):  # Press 'q' to quit
            break

    cv2.destroyAllWindows()
def close_application(application_name):
    speak(f"Closing {application_name}...")
    if application_name=='calculator':
        application_name='calc'
    os.system(f"taskkill /f /im {application_name}.exe")

def wait_for_browser_to_close(browser_path):
    """Wait for the specific browser instance to close or close it via voice command."""
    speak("Please close the browser when you are done.")
    process = subprocess.Popen([browser_path]) 
    pid = process.pid  

    while True:
        time.sleep(1)  
        if psutil.pid_exists(pid):
            # Check for the voice command to exit the browser
            command = takeSpeech()
            if "exit browser" or "close browser" in command:
                pyautogui.hotkey('ctrl', 'w')  # Close the current tab (works for most browsers)
                speak("Closing the browser.")
                break
        else:
            speak("Browser closed. You can give me another command.")
            break
def sketch_image(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    
    inverted_image = 255 - gray_image
    blurred_image = cv2.GaussianBlur(inverted_image, (21, 21), 0)
    inverted_blurred = 255 - blurred_image
    sketch = cv2.divide(gray_image, inverted_blurred, scale=256.0)
    return sketch

def handle_sketching():
    while True:   
        choice = messagebox.askquestion("Choose Option", "Would you like to take a photo with the camera?")

        if choice == 'yes':
            speak("Say cheese and smile...")
            photo = take_photo()
        else:
            photo = load_image_from_file()
        if photo is not None:                
            sketch = sketch_image(photo)
            display_images(photo, sketch)
            another = messagebox.askquestion("Continue", "Would you like to take another photo or select another image?")
            if another == 'no':
                break  
        else:
            messagebox.showinfo("Info", "No image selected.")

def handle_weather():
    speak("Tell me the city name: ")
    city = takeSpeech().lower()
    wapi_key = os.getenv("wapi_key") 
    if city is not None: 
        get_weather(city, wapi_key)
    else:
        speak("Tell me again.")
        while city is not None:
            city = takeSpeech().lower()
            if city is not None:
                break

def chat_with_user():
    global active_mode
    active_mode = True
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )
    history = []
    print("Bot: Hello, how can I help you?")
    while True:
        user_input = input("You: ")
        chat_session = model.start_chat(
            history=history
        )

        response = chat_session.send_message(user_input)

        model_response = response.text
        print(f'Bot: {model_response}')
        print()
        history.append({"role": "user", "parts": [user_input]})
        history.append({"role": "model", "parts": [model_response]})
        if user_input.lower() in ["exit", "quit"]:
            print("Bot: Goodbye!")
            break
    active_mode = False

def is_spotify_running():
    """Check if the Spotify application is running."""
    for process in psutil.process_iter(['name']):
        if process.info['name'] == 'Spotify.exe':
            return True
    return False

if __name__ == "__main__":
    listen_for_activation()
