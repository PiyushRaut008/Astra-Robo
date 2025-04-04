import speech_recognition as sr

def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Listening for command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

def run_script(file_name):
    try:
        print("successful")
    except Exception as e:
        print(f"⚠️ Failed to run {file_name}: {e}")

def main():
    while True:
        command = listen_command()

        if "switch to agriculture mode" in command:
            run_script("script1.py")
        elif "switch to tourist guide" in command:
            run_script("script2.py")
        elif "script three" in command:
            run_script("script3.py")
        elif "exit" in command or "quit" in command:
            print("👋 Exiting...")
            break
        else:
            print("🤖 Unknown command. Try saying 'script one', 'script two', etc.")

if __name__ == "__main__":
    main()
