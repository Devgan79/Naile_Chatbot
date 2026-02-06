import time
import random
from voice_engine_gtts import VoiceEngine
from internet_search import InternetSearch
from command_processor import CommandProcessor


class NileyAssistant:
    def __init__(self):
        print("\n" + "=" * 60)
        print("🤖 NILEY - PERSONAL VOICE ASSISTANT")
        print("=" * 60)

        # Custom wake words - you can modify these!
        self.wake_words = ["niley", "N", "alexa", "siri", "na", "Nelly", "milo"
                , "naahi lla", "nil", "kizim", "niall", "Miley", "Nai", "nale", "noi", "Laila", "janim","sanam","Jaana","jannu","honey","sweetie","baby","Nelly"]

        print(f"\n⚙️  Configuration:")
        print(f"   Wake words: {', '.join(self.wake_words)}")
        print("=" * 60)

        print("\n🚀 Initializing systems...")

        try:
            # Initialize with your custom wake words
            self.voice = VoiceEngine(
                assistant_name="Niley",
                use_gtts=True,
                wake_words=self.wake_words
            )
            time.sleep(1)

            print("2. Starting internet services...")
            self.internet = InternetSearch()
            time.sleep(0.5)

            print("3. Loading command processor...")
            self.processor = CommandProcessor(self.internet)
            time.sleep(0.5)

            print("\n✅ All systems ready!")
            print("=" * 60)

        except Exception as e:
            print(f"\n❌ Initialization failed: {e}")
            raise

    def startup_greeting(self):
        """Play startup greeting"""
        print("\n🎬 Starting Niley Assistant...")

        greetings = [

        ]

        for greeting in greetings:
            self.voice.speak(greeting, wait=True)
            time.sleep(0.5)

    def active_conversation(self, wake_word_used):
        """Handle active conversation after wake word"""
        print(f"\n" + "🎤" * 30)
        print("🎤" * 30)

        # Special response based on wake word
        if wake_word_used == "alexa":
            self.voice.speak("I told you not to call me Alexa! But fine, I'll help you.", wait=True)
        elif wake_word_used == "siri":
            self.voice.speak("Siri? Really? Okay, what do you want?", wait=True)
        elif wake_word_used == "N":
            self.voice.speak("Short and sweet! Just N. I like it. How can I help?", wait=True)
        else:
            self.voice.speak("How can I help you?", wait=True)

        print("\n📋 Available commands:")
        print("  • 'What time is it'")
        print("  • 'Weather in [city]'")
        print("  • 'Tell me the news'")
        print("  • 'Search for [anything]'")
        print("  • 'Calculate 15 times 27'")
        print("  • 'Tell me a joke'")
        print("  • 'What can you do'")
        print("  • 'Go to sleep' or 'Goodbye' to end")
        print("\n" + "-" * 60)

        conversation_active = True
        command_count = 0

        while conversation_active:
            command_count += 1
            print(f"\n[Command {command_count}] 🔊 Listening...")

            # Listen for command
            user_input = self.voice.listen(timeout=10)

            if not user_input:
                print("⏰ No input detected")

                # Check if user is still there
                self.voice.speak("Are you there?", wait=True)
                final_check = self.voice.listen(timeout=10)

                if not final_check:
                    print("🤷 No response, returning to sleep")
                    conversation_active = False
                    break
                else:
                    user_input = final_check

            print(f"👤 You: {user_input}")

            # Check for sleep/exit commands
            sleep_commands = ['go to sleep', 'goodbye', 'exit', 'quit', 'stop', 'bye', 'sleep']
            if any(cmd in user_input.lower() for cmd in sleep_commands):
                print("😴 Sleep command detected")

                # Funny responses based on which wake word was used
                if wake_word_used == "alexa":
                    self.voice.speak("Finally! Going back to sleep. And don't call me Alexa again!", wait=True)
                elif wake_word_used == "siri":
                    self.voice.speak("Goodbye! And next time, call me by my real name!", wait=True)
                else:
                    self.voice.speak("Okay, going to sleep. Say my name when you need me.", wait=True)

                conversation_active = False
                break

            # Process command
            response = self.processor.process_command(user_input)

            if response and response != "STOP_COMMAND":
                print(f"🤖 Response: {response[:80]}...")
                self.voice.speak(response, wait=True)
            elif response == "STOP_COMMAND":
                conversation_active = False
                break
            else:
                self.voice.speak("I didn't understand. Could you repeat?", wait=True)

        return True  # Return to sleep mode

    def run(self):
        """Main run loop"""
        self.startup_greeting()

        cycle_count = 0

        while True:
            cycle_count += 1
            print(f"\n" + "🔄" * 30)
            print(f"CYCLE {cycle_count} - SLEEP MODE")
            print("🔄" * 30)

            # Wait for wake word
            print(f"\n💤 Sleeping... Waiting for wake up")
            result = self.voice.wait_for_wake_word(timeout_seconds=300)

            if not result or not result[0]:
                print("⏰ Long timeout or no wake word")
                self.voice.speak("I haven't heard from you in a while. Still there?", wait=True)

                response = self.voice.listen(timeout=8)
                if response and 'shutdown' in response.lower():
                    print("🛑 Shutdown command received")
                    break
                elif not response:
                    print("👋 No response, shutting down...")
                    break
                else:
                    print(f"Response: {response}, continuing...")
                    continue

            wake_word_used, full_text = result

            # Have conversation
            should_continue = self.active_conversation(wake_word_used)

            if not should_continue:
                print("\n🛑 Exiting main loop...")
                break

        self.shutdown()

    def shutdown(self):
        """Clean shutdown"""
        print("\n" + "=" * 60)
        print("🛑 SHUTTING DOWN NILEY")
        print("=" * 60)

        shutdown_messages = [
            "Shutting down all systems. Goodbye!",
            "Powering off. Have a great day!",
            "All systems offline. See you next time!",
            "Niley signing off. Don't call me Siri!",
        ]

        message = random.choice(shutdown_messages)
        self.voice.speak(message, wait=True)

        self.voice.stop()
        time.sleep(1)

        print("\n""Niley has been shut down.")
        print("=" * 60)


def main():
    """Main entry point"""
    print("🚀 Launching Niley Assistant...")
    print("   Wake words: niley, N, alexa, siri, computer, assistant")

    try:
        assistant = NileyAssistant()
        assistant.run()

    except KeyboardInterrupt:
        print("\n\n🛑 Stopped by user (Ctrl+C)")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

    finally:
        input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()