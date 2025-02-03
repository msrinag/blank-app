import streamlit as st
import speech_recognition as sr
import google.generativeai as genai
import os

# Set up API key for Google Gemini (GenAI)
genai.configure(api_key=os.getenv("API_KEY"))  # Or replace with your actual API key
model = genai.GenerativeModel("gemini-1.5-flash-8b")  # Use the Gemini model you have access to

# Function to capture speech and convert it to text
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.listen(source)
    try:
        speech_text = recognizer.recognize_google(audio)
        st.write(f"You said: {speech_text}")
        return speech_text
    except sr.UnknownValueError:
        st.write("Sorry, I couldn't understand that.")
        return None
    except sr.RequestError:
        st.write("Sorry, there was an issue with the speech recognition service.")
        return None

# Function to get a response from Google Gemini (GenAI)
def get_gemini_response(text):
    try:
        # Create a prompt for Gemini based on the user's speech
        prompt = f"User said: {text}\nGemini, please respond in a conversational and helpful manner."
        response = model.generate(prompt)
        return response.text.strip()
    except Exception as e:
        st.write(f"Error: {e}")
        return "Sorry, I couldn't get a response from Gemini."

# Streamlit UI
st.title("Speech-to-Text & Gemini Chat")

# Button to start speech recognition
if st.button("Start Speaking"):
    speech_text = recognize_speech()
    if speech_text:
        gemini_response = get_gemini_response(speech_text)
        st.write(f"Gemini Response: {gemini_response}")
