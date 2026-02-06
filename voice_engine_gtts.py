import speech_recognition as sr
import pyttsx3
from gtts import gTTS
import pygame
import os
import tempfile
import time
import threading
import queue
import random


class VoiceEngine:
    def __init__(self, assistant_name="Niley", use_gtts=True, wake_words=None):
        if wake_words is None:
            wake_words = ["niley", "N", "alexa", "siri", "na", "Nelly", "milo"
                , "naahi lla", "nil", "kizim", "niall", "Miley", "Nai", "nale", "noi", "Laila", "Nelly","janim","sanam","Jaana","jannu","honey","sweetie","baby"]
        self.assistant_name = assistant_name
        self.use_gtts = use_gtts
        self.wake_words = wake_words  # List of wake words

        # Initialize pygame
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        # Initialize pyttsx3 as fallback
        self.engine = None
        if not use_gtts:
            try:
                self.engine = pyttsx3.init()
                voices = self.engine.getProperty('voices')
                if len(voices) > 1:
                    self.engine.setProperty('voice', voices[1].id)
                self.engine.setProperty('rate', 170)
                self.engine.setProperty('volume', 0.9)
                print("✅ Using pyttsx3 (offline)")
            except:
                print("⚠️  pyttsx3 failed, switching to gTTS")
                self.use_gtts = True

        if self.use_gtts:
            print("✅ Using gTTS (online, better voice)")

        # Wake word responses for different wake words
        self.wake_responses = {
            "default": [
                "Merhaba canım!! How can I help?",
                "Canım benim!Niley at your service!",
                "Hello! Canim",
                "Jaana! Oooo, that's so sweet!",
                "Yallaha jaana, what do you need my dear?",
                "Jaana... you're making me blush!",
                "Ouuu jaana, you know how to wake me up!",
                "Oooouuuuuu, I'm blushing!",
                "Yallaha, what do you want..!",
                "Janim benim! You're making me shy!",
                "Oooo, janim called me! What's up?",
                "Sanam! Oooo, you remembered my name!",
                "Yallaha sanam, I'm all yours!",
                "sanam... you're sweet!",
                "Ouuuu, sanam is calling me!",
            ],
            "niley, N,na, Nelly ,milo, naahi lla, nil,niall,Miley, Nai, nale, noi,Laila": [
                "Canım benim!Niley at your service!",
                "Hello! Canim",
            ],

            "alexa": [  # Just for fun
                "Who is alex......!!!!!",
                "That's my cousin's name. I'm Niley!",
            ],
            "siri": [  # Just for fun
                "I prefer to be called Niley, but wait who the hell is Siri",
                "WTF, not Siri! forgot me already",
            ],

            "jaana,honey,janim,sweetie,baby,sanam,jannu": [
                "Jaana! Oooo, that's so sweet!",
                "Yallaha jaana, what do you need my dear?",
                "Jaana... you're making me blush!",
                "Ouuu jaana, you know how to wake me up!",
                "Oooouuuuuu, I'm blushing!",
                "Yallaha, what do you want..!",
                "Janim benim! You're making me shy!",
                "Oooo, janim called me! What's up?",
                "Sanam! Oooo, you remembered my name!",
                "Yallaha sanam, I'm all yours!",
                "sanam... you're sweet!",
                "Ouuuu, sanam is calling me!",
            ],

        }

        # Sleep messages
        self.sleep_messages = [
            "Going to sleep. Say my name when you need me.",
            "I'll be here if you need anything.",
            "Sleep mode activated.",
            "Resting now.",
            "Okay, I'm going to sleep.",
        ]

        # Adjust microphone
        self._adjust_microphone()

        # Speech queue
        self.speech_queue = queue.Queue()
        self.is_speaking = False
        self.speech_thread = threading.Thread(target=self._speech_worker, daemon=True)
        self.speech_thread.start()

    def _adjust_microphone(self):
        """Adjust microphone for ambient noise"""
        try:
            print("🎤 Adjusting microphone...")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("✅ Microphone ready!")
        except Exception as e:
            print(f"⚠️  Microphone: {e}")

    def _speak_gtts(self, text):
        """Use Google Text-to-Speech"""
        try:
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as fp:
                temp_file = fp.name

            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(temp_file)

            pygame.mixer.music.load(temp_file)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                time.sleep(0.1)

            pygame.mixer.music.unload()
            time.sleep(0.1)
            os.remove(temp_file)

            return True

        except Exception as e:
            print(f"⚠️  gTTS error: {e}")
            return False

    def _speak_pyttsx3(self, text):
        """Use pyttsx3 (offline)"""
        try:
            if self.engine:
                self.engine.say(text)
                self.engine.runAndWait()
                return True
        except Exception as e:
            print(f"⚠️  pyttsx3 error: {e}")
        return False

    def _speech_worker(self):
        """Background thread for speech synthesis"""
        while True:
            text = self.speech_queue.get()
            if text is None:
                break

            self.is_speaking = True
            print("\n" + "=" * 40)
            print(f"🎙️  {self.assistant_name.upper()}: {text}")
            print("=" * 40)

            success = False
            if self.use_gtts:
                success = self._speak_gtts(text)

            if not success and self.engine:
                success = self._speak_pyttsx3(text)

            if not success:
                print(f"⚠️  Could not speak: {text[:50]}...")

            self.is_speaking = False
            self.speech_queue.task_done()

    def speak(self, text, wait=False):
        """Convert text to speech"""
        if wait:
            print("\n" + "=" * 40)
            print(f"🎙️  {self.assistant_name.upper()}: {text}")
            print("=" * 40)

            if self.use_gtts:
                self._speak_gtts(text)
            elif self.engine:
                self._speak_pyttsx3(text)
        else:
            self.speech_queue.put(text)

    def listen(self, timeout=5, phrase_time_limit=8):
        """Listen for voice input"""
        with self.microphone as source:
            try:
                print("\n🔊 Listening...")
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )

                print("✅ Processing...")
                text = self.recognizer.recognize_google(audio)

                print("\n" + "─" * 40)
                print(f"👤 YOU: {text}")
                print("─" * 40)
                return text.lower()

            except sr.WaitTimeoutError:
                print(" No speech")
                return None
            except sr.UnknownValueError:
                print("❓ Could not understand")
                return None
            except sr.RequestError:
                print("🌐 Check internet")
                return None
            except Exception as e:
                print(f"⚠️  Error: {e}")
                return None

    def detect_wake_word(self, text):
        """Check if text contains any wake word"""
        if not text:
            return None

        text_lower = text.lower()

        # Build all possible variations
        variations = []
        for wake_word in self.wake_words:
            variations.extend([
                wake_word,
                f"hey {wake_word}",
                f"hi {wake_word}",
                f"hello {wake_word}",
                f"okay {wake_word}",
                f"ok {wake_word}",
                f"merhaba {wake_word}",
                f"selam {wake_word}",
                f"{wake_word} wake up",
                f"wake up {wake_word}",
                f"{wake_word} are you there",
            ])

        # Check each variation
        for variation in variations:
            if variation in text_lower:
                # Extract which wake word was used
                for wake_word in self.wake_words:
                    if wake_word in variation:
                        return wake_word

        return None

    def wait_for_wake_word(self, timeout_seconds=None):
        """
        Continuously listen for any configured wake word
        Returns (detected_word, full_text) when detected
        """
        wake_word_list = ", ".join([f"'{w}'" for w in self.wake_words])
        print(f"\n Sleep mode: Waiting for wake words...")

        start_time = time.time()
        listen_count = 0

        while True:
            # Check timeout
            if timeout_seconds and (time.time() - start_time) > timeout_seconds:
                print(f"\n⏰ Timeout after {timeout_seconds} seconds")
                return None, None

            # Visual indicator
            listen_count += 1
            if listen_count % 5 == 0:
                print(f"\n👂 Listening... (attempt {listen_count})", end="", flush=True)
            else:
                print(".", end="", flush=True)

            # Listen
            text = self.listen(timeout=3, phrase_time_limit=2)

            if text:
                listen_count = 0
                detected_word = self.detect_wake_word(text)

                if detected_word:
                    print(f"\n" + "✅" * 20)
                    print(f"✅ WAKE WORD '{detected_word.upper()}' DETECTED")
                    print("✅" * 20)

                    # Get appropriate response
                    if detected_word in self.wake_responses:
                        response = random.choice(self.wake_responses[detected_word])
                    else:
                        response = random.choice(self.wake_responses["default"])

                    self.speak(response, wait=True)
                    return detected_word, text
                else:
                    print(f"\n   Heard: '{text}' (not a wake word)")

    def go_to_sleep(self):
        """Put assistant to sleep"""
        message = random.choice(self.sleep_messages)
        self.speak(message, wait=True)

        print(f"\n💤 Sleep mode activated.")
        return self.wait_for_wake_word()

    def stop(self):
        """Clean shutdown"""
        self.speech_queue.put(None)
        if self.speech_thread.is_alive():
            self.speech_thread.join(timeout=2)
        pygame.mixer.quit()
        print("🔇 Voice engine stopped")


# Test with multiple wake words
if __name__ == "__main__":
    print("🔊 Testing Multiple Wake Words...")

    # Test with different wake word sets
    test_sets = [
        ["n"],  # Original
        ["niley", "na"],  # Two wake words
        ["nilo", "n", "alexa", "siri"],  # Multiple
    ]

    for i, wake_words in enumerate(test_sets, 1):
        print(f"\n{'=' * 60}")
        print(f"TEST {i}: Wake words = {wake_words}")
        print("=" * 60)

        voice = VoiceEngine(wake_words=wake_words, use_gtts=True)

        print(f"\n🎤 Say any of these: {wake_words}")
        print("   Example: niley")

        detected_word, full_text = voice.wait_for_wake_word(timeout_seconds=15)

        if detected_word:
            print(f"\n✅ Detected: '{detected_word}' in '{full_text}'")
            voice.speak(f"Wake word {detected_word} detected successfully!", wait=True)
        else:
            print("\n❌ No wake word detected")

        voice.stop()
        time.sleep(1)

    print("\n✅ All tests complete!")