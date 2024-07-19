import openai
import pyttsx3
import speech_recognition as sr
import webbrowser
import os

openai.api_key = "Your secret key here"

text_speech = pyttsx3.init()
recognizer = sr.Recognizer()
microphone = sr.Microphone()

def chat_with_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()

def open_website(url):
    if not url.startswith("http"):
        url = "https://" + url
    if not url.endswith(".com"):
        url += ".com"
    webbrowser.open(url)

def open_app(app_name):
    # Dictionary to map user-friendly app names to executable names
    app_executables = {
        "whatsapp": "WhatsApp.exe",
        # Add more app names and their corresponding executables as needed
    }
    # Check if the app exists in the dictionary
    if app_name.lower() in app_executables:
        app_path = os.path.join("C:\\Program Files", app_executables[app_name.lower()])
        if os.path.exists(app_path):
            os.system(f"start {app_path}")
            return True
    return False

if __name__ == "__main__":
    while True:
        with microphone as source:
            print("Listening:")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        
        try:
            user_input = recognizer.recognize_google(audio)
            print("You said:", user_input)
        except sr.UnknownValueError:
            print("Could not understand audio")
            continue
        except sr.RequestError as e:
            print("Error; {0}".format(e))
            continue
        
        if user_input.lower() in ["quit", "exit", "bye"]:
            text_speech.say("Chatbot: I am going to shutdown")
            break
        elif "open app" in user_input.lower() and "in my device" in user_input.lower():
            app_name = user_input.split("open app ")[-1]
            if not open_app(app_name):
                text_speech.say("Chatbot: I'm sorry, I am not able to access or open apps on your device. If you need any information or assistance related to " + app_name + ", feel free to ask me!")
            continue
        elif "open website" in user_input.lower():
            website_name = "".join(user_input.split("open website ")[1:]).replace(" ", "")
            open_website(website_name)
            continue
        elif "open" in user_input.lower() or "website" in user_input.lower():
            website_name = "".join(user_input.split("open ")[1:]).replace(" ", "")
            open_website(website_name)
            continue
        elif "How are you" in user_input.lower():
            text_speech.say("I am fine thanks for asking, how can I assist you")
            continue

        
        response = chat_with_gpt(user_input)
        if "How are you" or "how r u" in user_input.lower():
            text_speech.say("I am fine thanks for asking, how can I assist you")
            continue
        else:
            text_speech.say(response)
            text_speech.runAndWait()
        print("Chatbot:", response)