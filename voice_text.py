import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

# def test_microphone():
#     with sr.Microphone(device_index=mic_index) as source:
#         print("Testing microphone... Speak into the mic!")
#         recognizer.adjust_for_ambient_noise(source, duration=2)
#         audio = recognizer.listen(source, timeout=5)
#         print("Microphone test complete! If you see this, the mic is working.")


def listen_for_speech():
    recognizer = sr.Recognizer()
    mic_index = 0
    
    with sr.Microphone(device_index=mic_index) as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Say something!")
        
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=20)
            print("Processing...")
            
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            
            if "hello monster" in text.lower():
                print("Wake word detected!")
            return text
                
        except sr.WaitTimeoutError:
            print("No speech detected.")
        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError as e:
            print(f"API error: {e}")
    
    return None

# if __name__ == "__main__":
#     print("Available microphones:")
#     # for index, name in enumerate(sr.Microphone.list_microphone_names()):
#     #     print(f"{index}: {name}")
#     
#     while True:
#         listen_for_speech()
#         # if result:
#         #     # Add your custom logic here
#         #     if "stress" in result.lower():
#         #         print("I hear you're stressed! Let me help.")