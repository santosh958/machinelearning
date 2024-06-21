#!/usr/bin/env python
# coding: utf-8

# In[3]:


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

    # Update button states
    update_buttons()

    # Listen to microphone with a short chunk duration for responsiveness
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        transcription_label.config(text="Listening...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            transcription_label.config(text="No speech detected. Please try again.")
            recording = False
            update_buttons()
            return

    # Stop recording and transcribe audio in a separate thread
    stop_recording_thread = threading.Thread(target=stop_recording_and_transcribe, args=(audio,))
    stop_recording_thread.start()

def stop_recording_and_transcribe(audio):
    global recording
    recording = False
    update_buttons()

    try:
        # Use Google Speech Recognition for transcription (requires internet connection)
        text = recognizer.recognize_google(audio)
        transcription_label.after(0, lambda: transcription_label.config(text=f"You said: {text}"))
    except sr.UnknownValueError:
        transcription_label.after(0, lambda: transcription_label.config(text="Could not understand audio. Please try again."))
    except sr.RequestError as e:
        transcription_label.after(0, lambda: transcription_label.config(text=f"Request error from Google Speech Recognition service: {e}"))
    except Exception as e:
        transcription_label.after(0, lambda: transcription_label.config(text=f"An error occurred: {e}"))

def stop_recording():
    global recording
    recording = False
    update_buttons()

# Create the main window
root = tk.Tk()
root.title("Audio Transcription")

# Create buttons for record and stop
record_button = tk.Button(root, text="Start Recording", command=start_recording)
record_button.pack(pady=10)
stop_button = tk.Button(root, text="Stop Recording", command=stop_recording, state="disabled")
stop_button.pack(pady=10)

# Label to display transcribed text
transcription_label = tk.Label(root, text="Click 'Start Recording' to begin.")
transcription_label.pack(pady=20)

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




