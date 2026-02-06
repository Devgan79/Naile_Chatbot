import speech_recognition as sr
import time


def test_microphone():
    """Test which microphone is working"""
    print("\n" + "=" * 50)
    print("🎤 MICROPHONE TEST UTILITY")
    print("=" * 50)

    # List all microphones
    print("\n🔍 Available microphones:")
    mic_list = sr.Microphone.list_microphone_names()

    for i, mic_name in enumerate(mic_list):
        print(f"  [{i}] {mic_name}")

    print("\n" + "=" * 50)
    print("Testing microphones one by one...")
    print("=" * 50)

    # Test each microphone
    for i, mic_name in enumerate(mic_list):
        print(f"\n.. Testing microphone {i}: {mic_name}")

        try:
            with sr.Microphone(device_index=i) as source:
                r = sr.Recognizer()

                # Adjust for noise
                print("   Adjusting for ambient noise...")
                r.adjust_for_ambient_noise(source, duration=1)

                print("     SAY 'TESTING' NOW (3 seconds)...")
                audio = r.listen(source, timeout=3, phrase_time_limit=3)

                try:
                    text = r.recognize_google(audio)
                    print(f"    SUCCESS! Heard: '{text}'")
                    print(f"    RECOMMENDED MICROPHONE: Index {i}")
                    return i  # Return working microphone index
                except sr.UnknownValueError:
                    print("     Could not understand audio")
                except sr.RequestError:
                    print("   ❌ Speech service error")

        except Exception as e:
            print(f"   ❌ Error with microphone {i}: {e}")

    print("\n" + "=" * 50)
    print("❌ No working microphones found automatically.")
    print("\n TROUBLESHOOTING:")
    print("1. Check if microphone is plugged in")
    print("2. Check Windows Sound Settings")
    print("3. Make sure microphone is not muted")
    print("4. Try a different microphone")
    print("=" * 50)

    # Let user choose manually
    try:
        choice = int(input("\nEnter microphone index to use (or -1 to exit): "))
        if choice >= 0 and choice < len(mic_list):
            return choice
    except:
        pass

    return None


def quick_listening_test(mic_index=None):
    """Quick test of listening"""
    print("\n" + "=" * 50)
    print(" QUICK LISTENING TEST")
    print("=" * 50)

    r = sr.Recognizer()

    if mic_index is not None:
        print(f"Using microphone index: {mic_index}")
        mic = sr.Microphone(device_index=mic_index)
    else:
        print("Using default microphone")
        mic = sr.Microphone()

    with mic as source:
        r.adjust_for_ambient_noise(source, duration=1)

        for attempt in range(3):
            print(f"\nAttempt {attempt + 1}/3")
            print("Say something (3 seconds)...")

            try:
                audio = r.listen(source, timeout=3, phrase_time_limit=3)
                text = r.recognize_google(audio)
                print(f"Heard: '{text}'")
                return True
            except sr.WaitTimeoutError:
                print("Timeout - no speech detected")
            except sr.UnknownValueError:
                print("Could not understand audio")
            except Exception as e:
                print(f" Error: {e}")

    return False


if __name__ == "__main__":
    # Test microphones
    working_mic = test_microphone()

    if working_mic is not None:
        print(f"\n Working microphone found: Index {working_mic}")

        # Save to file for Niley to use
        with open("microphone_config.txt", "w") as f:
            f.write(str(working_mic))

        # Test listening
        success = quick_listening_test(working_mic)

        if success:
            print("\n✅ Microphone setup complete! Niley can hear you.")
        else:
            print("\n⚠️  Microphone works but speech recognition needs adjustment.")
    else:
        print("\n❌ Please fix microphone issues before continuing.")