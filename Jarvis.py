import pyttsx3
import speech_recognition as sr
import random
import re
import webbrowser
import datetime
from plyer import notification
import pyautogui
import wikipedia
import pywhatkit as pwk
import user  # Assuming user.py contains the password for email
import smtplib
from spotify_control import SpotifyController
from camera import capture_photo, record_video
from weather import get_weather
from system_control import set_brightness, set_volume
from internet_speed import get_speed
from sys_utils import battery_status, system_info
from screenshot import take_screenshot



engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice (usually)
engine.setProperty('rate', 200)
spotify = SpotifyController()
now =datetime.datetime.now()
send_time = now + datetime.timedelta(minutes=2)  
hour = send_time.hour
minute = send_time.minute

def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def command():
    r = sr.Recognizer()
    retries = 3  # Retry 3 times for listening
    for attempt in range(retries):
        try:
            with sr.Microphone() as source:
                print("Listening... Please speak.")
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
            content = r.recognize_google(audio, language="en-IN")
            print("You Said: " + content)
            return content.lower()
        except sr.WaitTimeoutError:
            print("Listening timed out, please try again.")
        except sr.UnknownValueError:
            print("Sorry, I did not catch that.")
            speak("Sorry, I didn't catch that. Please say again.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            speak("Sorry, I am unable to connect to the speech service.")
            break  # No point retrying if service is down
        except Exception as e:
            print(f"Unexpected error: {e}")
            speak("Sorry, something went wrong. Please try again.")
    return ""  # Return empty string if all retries fail


def main_process():
    while True:
        try:
            request = command()
            if not request:
                continue  # If no command, listen again

            if "hello" in request:
                speak("Hello, I am Jarvis, your personal assistant.")

            # Spotify controls
            elif "play spotify" in request:
                song = request.replace("play spotify", "").strip()
                if song:
                    response = spotify.play_song(song)
                    speak(response)
                else:
                    speak("Please tell me which song to play on Spotify.")

            elif "pause spotify" in request or "stop spotify" in request:
                speak(spotify.pause())
            elif "resume spotify" in request:
                speak(spotify.resume())
            elif "next song" in request:
                speak(spotify.next_track())
            elif "previous song" in request:
                speak(spotify.previous_track())
            elif "shuffle on" in request:
                speak(spotify.shuffle(True))
            elif "shuffle off" in request:
                speak(spotify.shuffle(False))
            elif "repeat song" in request:
                speak(spotify.repeat("track"))
            elif "repeat playlist" in request:
                speak(spotify.repeat("context"))
            elif "repeat off" in request:
                speak(spotify.repeat("off"))
            elif "spotify status" in request:
                speak(spotify.current_playing())

            # Play random music from preset YouTube links
            elif "play music" in request:
                speak("Playing music")
                song = random.randint(1, 3)
                if song == 1:
                    webbrowser.open("https://www.youtube.com/watch?v=c7POv4qiZLM")
                elif song == 2:
                    webbrowser.open("https://www.youtube.com/watch?v=fXRvluHnjxE")
                elif song == 3:
                    webbrowser.open("https://www.youtube.com/watch?v=KUpwupYj_tY")

            # Play YouTube video by query
            elif "play" in request:
                query = request.replace("play", "").strip()
                if query:
                    pwk.playonyt(query)

            # Camera functions
            elif "take picture" in request or "take a photo" in request:
                response = capture_photo()
                speak(response)

            elif "record video" in request:
                speak("Recording video for 5 seconds")
                response = record_video(duration=5)
                speak(response)

            elif "take screenshot" in request or "screenshot" in request:
                response = take_screenshot()
                speak(response)


            
            #internet and system utilities
                        # Internet Speed & System Utilities
            elif "internet speed" in request or "network speed" in request or "check internet" in request:
                speak("Checking internet speed, please wait...")
                speed = get_speed()
                print(speed)
                speak(speed)

            elif "battery status" in request or "battery level" in request or "check battery" in request:
                status = battery_status()
                print(status)
                speak(status)

            elif "system info" in request or "system status" in request or "check system" in request:
                info = system_info()
                print(info)
                speak(info)




            # Weather
            elif any(phrase in request for phrase in ["weather", "temperature", "forecast"]):
                city = None
    # Try to extract city from the sentence
                match = re.search(r"weather in ([a-zA-Z\s]+)", request)
                if not match:
                    match = re.search(r"temperature in ([a-zA-Z\s]+)", request)
                if not match:
                    match = re.search(r"forecast in ([a-zA-Z\s]+)", request)

                if match:
                    city = match.group(1).strip()
                else:
                    speak("Which city's weather would you like to know?")
                    city = command()
                if city:
                    weather_info = get_weather(city)
                    print(weather_info)
                    speak(weather_info)
                else:
                    speak("I didn't get the city name.")


            # Brightness control
            elif "set brightness" in request:
                speak("What level do you want the brightness set to? Please give a number from 0 to 100.")
                try:
                    level = int(command())
                    result = set_brightness(level)
                    speak(result)
                except Exception:
                    speak("Please provide a valid number for brightness.")

            # Volume control
            elif "set volume" in request:
                speak("What level do you want the volume set to? Please give a number from 0 to 100.")
                try:
                    level = int(command())
                    result = set_volume(level)
                    speak(result)
                except Exception:
                    speak("Please provide a valid number for volume.")

            # Time and date
            elif "say time" in request:
                now_time = datetime.datetime.now().strftime("%H:%M")
                speak("The time is " + now_time)
            elif "say date" in request:
                now_date = datetime.datetime.now().strftime("%Y-%m-%d")
                speak("Date is " + now_date)

            # To-do list management
            elif "new task" in request:
                task = request.replace("new task", "").strip()
                if task:
                    speak("Adding task: " + task)
                    with open("todo.txt", "a") as file:
                        file.write(task + "\n")

            elif "delete task" in request:
                task = request.replace("delete task", "").strip()
                if task:
                    speak("Deleting task: " + task)
                    with open("todo.txt", "r") as file:
                        lines = file.readlines()
                    with open("todo.txt", "w") as file:
                        for line in lines:
                            if line.strip("\n") != task:
                                file.write(line)

            elif "speak task" in request:
                with open("todo.txt", "r") as file:
                    tasks = file.read()
                if tasks.strip() == "":
                    speak("You have no tasks for today.")
                else:
                    speak("Work we have to do today is: " + tasks)

            elif "show work" in request:
                with open("todo.txt", "r") as file:
                    tasks = file.read()
                if tasks.strip() == "":
                    tasks = "No tasks for today."
                notification.notify(
                    title="Work to do",
                    message=tasks,
                    timeout=10
                )

            # Open apps or files using keyboard shortcuts
            elif "open" in request:
                query = request.replace("open", "").strip()
                if query:
                    pyautogui.press("super")
                    pyautogui.typewrite(query)
                    pyautogui.press("enter")

            # Wikipedia search
            elif "wikipedia" in request:
                query = request.replace("jarvis", "").replace("search wikipedia", "").strip()
                if query:
                    try:
                        result = wikipedia.summary(query, sentences=3)
                        speak(result)
                    except Exception:
                        speak("Sorry, I couldn't find any results on Wikipedia.")

            # Google search
            elif "search google" in request:
                query = request.replace("jarvis", "").replace("search google", "").strip()
                if query:
                    webbrowser.open("https://www.google.com/search?q=" + query)

            # YouTube search
            elif "search youtube" in request:
                query = request.replace("jarvis", "").replace("search youtube", "").strip()
                if query:
                    webbrowser.open("https://www.youtube.com/results?search_query=" + query)

            # WhatsApp message sending (customize as needed)
            elif "send whatsapp" in request:
                # Note: update number/time dynamically if needed
                pwk.sendwhatmsg("+917326907026", "Hi", hour, minute, 30)
                speak("WhatsApp message scheduled.")

            # Email sending
            elif "send email" in request:
                try:
                    s = smtplib.SMTP('smtp.gmail.com', 587)
                    s.starttls()
                    s.login("binayaknaudiagenaisj@gmail.com", user.password)
                    message = "Hello, this is a test email from Jarvis."
                    s.sendmail("binayaknaudiagenaisj@gmail.com", "binayaknaudiavk18@gmail.com", message)
                    s.quit()
                    speak("Email sent successfully")
                except Exception as e:
                    print(e)
                    speak("Sorry, I was unable to send the email.")

            # Exit the assistant
            elif "exit" in request or "quit" in request:
                speak("Goodbye! See you later.")
                break

            else:
                speak("I didn't understand that. Please try again.")

        except Exception as e:
            print(f"An error occurred: {e}")
            speak("Sorry, something went wrong. Please try again.")


if __name__ == "__main__":
    main_process()
