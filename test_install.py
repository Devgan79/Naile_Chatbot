# Simple test to check installations
try:
    import speech_recognition as sr
    import pyttsx3
    import pyaudio

    print("All audio libraries installed!")

    # Test text-to-speech
    engine = pyttsx3.init()
    print("Pyttsx3 working!")

    # Test speech recognition
    r = sr.Recognizer()
    print("SpeechRecognition working!")

    print("\n All basic installations are successful!")

except Exception as e:
    print(f"❌ Error: {e}")
    print("\nPlease share the error message with me.")