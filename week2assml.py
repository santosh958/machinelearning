#!/usr/bin/env python
# coding: utf-8

# In[1]:


import speech_recognition as sr
import tkinter as tk
import threading

# Initialize recognizer and microphone
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Flag to track recording status
recording = False

def start_recording():
  global recording
  recording = True

  # Listen to microphone with a short chunk duration for responsiveness
  with microphone as source:
    recognizer.adjust_for_ambient_noise(source, duration=0.5)
    print("Speak...")
    audio = recognizer.listen(source)

  # Stop recording and transcribe audio in a separate thread
  stop_recording_thread = threading.Thread(target=stop_recording_and_transcribe, args=(audio,))
  stop_recording_thread.start()

def stop_recording_and_transcribe(audio):
  global recording
  recording = False

  try:
    # Use Google Speech Recognition for transcription (requires internet connection)
    text = recognizer.recognize_google(audio)
    print("You said:", text)
    # Update UI with transcribed text (example using label)
    transcription_label.config(text=text)
  except sr.UnknownValueError:
    print("Could not understand audio")
  except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))

def stop_recording():
  global recording
  recording = False

# Create the main window
root = tk.Tk()
root.title("Audio Transcription")

# Create buttons for record and stop
record_button = tk.Button(root, text="Start Recording", command=start_recording)
record_button.pack(pady=10)
stop_button = tk.Button(root, text="Stop Recording", command=stop_recording, state="disabled")
stop_button.pack(pady=10)

# Label to display transcribed text
transcription_label = tk.Label(root, text="")
transcription_label.pack()

# Disable stop button initially and enable it only while recording
def update_buttons():
  if recording:
    stop_button.config(state="normal")
    record_button.config(state="disabled")
  else:
    stop_button.config(state="disabled")
    record_button.config(state="normal")

root.after(100, update_buttons)  # Update button states every 100 milliseconds

root.mainloop()


# In[ ]:




