import asyncio
import edge_tts
import os
from emotion_recognition import show_webcam
from voice_text import listen_for_speech
from chatbot import chatbot
import pygame 
import serial
import time


port  = '/dev/cu.usbserial-110'
baud_rate = 9600
async def get_voices():
    voices = await edge_tts.list_voices()
    return {v['ShortName']: v['FriendlyName'] for v in voices}

async def speak_text(text, voice="en-US-GuyNeural", rate="+0%"):
    try:
        # Create temporary audio file
        temp_file = "temp_audio.mp3"
        
        communicate = edge_tts.Communicate(text, voice, rate=rate)
        await communicate.save(temp_file)
        
        # Play audio using pygame
        pygame.mixer.init()
        pygame.mixer.music.load(temp_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.1)
            
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

async def main():
    voices = await get_voices()
    # print(f"Available voices: {list(voices.values())}")
    
    #select voice properly using its ShortName
    selected_voice = "en-US-GuyNeural"  # Default voice
    while(True):
      print("Say Hello to Activate Chompy...")
      # servo code to activate
      spoken_result = listen_for_speech()
      if(spoken_result == "hello"):
        while True:
            print("Waiting for visual input...")
            face_result = show_webcam()
            print("Webcam result:", face_result)

            print("Waiting for audio input...")
            spoken_result = listen_for_speech()
            if(spoken_result == "thank you"):
                # servo code to deactivate 
                # delay for 10 seconds then chomp down on the paper
                break

            if spoken_result and face_result:
                print("Spoken result:", spoken_result)
                user_input = f"{spoken_result} and I look {face_result}"
                
                print("Processing chatbot response...")
                chatbot_response = chatbot(user_input)
                print("Chatbot response:", chatbot_response)

                await speak_text(chatbot_response, voice=selected_voice)
                # ser = serial.Serial(port,baud_rate,timeout=1)
                # time.sleep(2)
                # ser.write(b'1')
                # print("Trigger sent to NODEMCU")
                # ser.close()
                # print("Closed COnn")

            user_choice = input("Interaction complete. Press Enter to continue or type 'exit' to quit: ")
            if user_choice.lower() == 'exit':
                break

if __name__ == "__main__":
    asyncio.run(main())