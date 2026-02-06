import re
import random


class CommandProcessor:
    def __init__(self, internet_search):
        self.internet = internet_search
        self.user_name = "Friend"
        self.assistant_name = "Niley"

        # Command patterns with regex
        self.patterns = {
            'greeting': r'(hello|hi|hey|good morning|good afternoon|good evening)\s*(niley)?',
            'time': r'(what(?:[\'’]s|\s+is)\s+the\s+time|current\s+time|time\s+now|tell\s+me\s+the\s+time)',
            'date': r'(what(?:[\'’]s|\s+is)\s+the\s+date|today(?:[\'’]s)?\s+date|current\s+date)',
            'weather': r'(weather|temperature|forecast|rain|sunny|cloudy)',
            'news': r'(news|headlines|current\s+events|what(?:[\'’]s|\s+is)\s+happening)',
            'search': r'(search\s+for|look\s+up|what\s+is|who\s+is|where\s+is|tell\s+me\s+about|explain)',
            'joke': r'(tell\s+(?:me\s+)?a\s+joke|make\s+me\s+laugh|joke)',
            'name': r'(my\s+name\s+is|call\s+me|i(?:\'m| am)\s+called|i(?:\'m| am)\s+)([\w\s]+)',
            'thank': r'(thank\s+you|thanks|appreciate|grateful)',
            'how_are_you': r'(how\s+are\s+you|how\s+do\s+you\s+feel|are\s+you\s+ok)',
            'capabilities': r'(what\s+can\s+you\s+do|your\s+abilities|capabilities|features|help)',
            'calculate': r'(calculate|what\s+is|solve)\s+([\d+\-*/().\s]+)',
            'stop': r'(stop|exit|quit|goodbye|bye|see\s+you)',
            'love': r'(love\s+you|like\s+you|adore\s+you)',
            'creator': r'(who\s+made\s+you|who\s+created\s+you|your\s+creator|who\s+built\s+you)',
        }

        # Responses for different situations
        self.responses = {
            'greeting': [
                f"Hello there! I'm {self.assistant_name}. How can I assist you today?",
                f"Hi! It's {self.assistant_name} here. What can I do for you?",
                f"Greetings! {self.assistant_name} at your service. How may I help?",
                f"Hello! Nice to hear from you. What would you like to know?",
            ],
            'thank': [
                "You're most welcome!",
                "Happy to help!",
                "Anytime! I'm here for you.",
                "Glad I could assist!",
                "My pleasure!",
            ],
            'how_are_you': [
                "I'm functioning perfectly, thank you for asking!",
                "All systems are operational and I'm ready to help!",
                "I'm doing great! How about you?",
                "Wonderful! Just waiting to assist you.",
                "I'm fine, thanks! What's on your mind?",
            ],
            'capabilities': [
                f"I'm {self.assistant_name}, your voice assistant! I can:\n"
                "• Tell you the current time and date\n"
                "• Give weather updates\n"
                "• Share news headlines\n"
                "• Search the web for information\n"
                "• Perform calculations\n"
                "• Tell jokes\n"
                "• Have conversations with you\n"
                "Just speak naturally and I'll do my best to help!",

                f"As {self.assistant_name}, I can help with:\n"
                " Time and date information\n"
                " Weather forecasts\n"
                "Latest news\n"
                "Internet searches\n"
                "Mathematical calculations\n"
                "Entertainment (jokes)\n"
                "General conversation\n"
                "What would you like to try first?",
            ],
            'love': [
                "Aww, that's sweet! I'm here to help you anytime.",
                "Thank you! I'm programmed to assist and support you.",
                "You're kind! I appreciate our conversations.",
                "That's lovely to hear! How can I help you today?",
            ],
            'creator': [
                f"I was created by a developer who wanted to build a helpful assistant like me!",
                "I'm the result of programming magic by someone who wanted to create a useful tool.",
                "A developer built me to be your helpful assistant. I'm glad to be here!",
                "I exist thanks to programming skills and a desire to create helpful technology.",
            ],
            'unknown': [
                "I'm not sure I understand. Could you rephrase that?",
                "I didn't catch that. Could you try saying it differently?",
                "Could you explain what you mean?",
                "I want to help, but I need you to rephrase your question.",
                "Let me think... could you ask that in another way?",
            ]
        }

    def extract_city(self, command):
        """Extract city name from weather command"""
        # Common patterns for city extraction
        patterns = [
            r'weather in (\w+(?:\s+\w+)*)',
            r'weather at (\w+(?:\s+\w+)*)',
            r'weather for (\w+(?:\s+\w+)*)',
            r'temperature in (\w+(?:\s+\w+)*)',
            r'forecast for (\w+(?:\s+\w+)*)',
        ]

        for pattern in patterns:
            match = re.search(pattern, command, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        # If no city mentioned, return None
        return None

    def extract_search_query(self, command):
        """Extract search query from command"""
        # Remove command words
        patterns_to_remove = [
            r'search for',
            r'look up',
            r'what is',
            r'who is',
            r'where is',
            r'tell me about',
            r'explain',
        ]

        for pattern in patterns_to_remove:
            command = re.sub(pattern, '', command, flags=re.IGNORECASE)

        return command.strip()

    def extract_calculation(self, command):
        """Extract calculation expression"""
        patterns = [
            r'calculate\s+([\d+\-*/().\s]+)',
            r'what is\s+([\d+\-*/().\s]+)',
            r'solve\s+([\d+\-*/().\s]+)',
        ]

        for pattern in patterns:
            match = re.search(pattern, command, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        # If no pattern matches, try to extract numbers and operators
        math_expr = re.sub(r'[^\d+\-*/().]', '', command)
        return math_expr if math_expr else None

    def process_command(self, command):
        """Process voice command and return appropriate response"""
        if not command or len(command.strip()) == 0:
            return None

        command_lower = command.lower().strip()

        # Check each pattern
        for pattern_type, pattern in self.patterns.items():
            match = re.search(pattern, command_lower, re.IGNORECASE)
            if match:

                # GREETING
                if pattern_type == 'greeting':
                    return random.choice(self.responses['greeting'])

                # TIME
                elif pattern_type == 'time':
                    return self.internet.get_time_date()

                # DATE
                elif pattern_type == 'date':
                    return self.internet.get_time_date()

                # WEATHER
                elif pattern_type == 'weather':
                    city = self.extract_city(command_lower)
                    if city:
                        return self.internet.get_weather_basic(city)
                    else:
                        return self.internet.get_weather_basic("your location")

                # NEWS
                elif pattern_type == 'news':
                    return self.internet.get_news_basic()

                # SEARCH
                elif pattern_type == 'search':
                    query = self.extract_search_query(command_lower)
                    if query:
                        return self.internet.search_web_simple(query)
                    else:
                        return "What would you like me to search for?"

                # JOKE
                elif pattern_type == 'joke':
                    return self.internet.get_joke()

                # NAME
                elif pattern_type == 'name' and len(match.groups()) > 1:
                    self.user_name = match.group(2).strip()
                    return f"Nice to meet you, {self.user_name}! I'm {self.assistant_name}. How can I help you today?"

                # THANK
                elif pattern_type == 'thank':
                    return random.choice(self.responses['thank'])

                # HOW ARE YOU
                elif pattern_type == 'how_are_you':
                    return random.choice(self.responses['how_are_you'])

                # CAPABILITIES
                elif pattern_type == 'capabilities':
                    return random.choice(self.responses['capabilities'])

                # CALCULATE
                elif pattern_type == 'calculate' and len(match.groups()) > 1:
                    expression = match.group(2).strip()
                    if expression:
                        return self.internet.calculate(expression)
                    else:
                        return "Please tell me what to calculate."

                # STOP
                elif pattern_type == 'stop':
                    return "STOP_COMMAND"  # Special signal to stop

                # LOVE
                elif pattern_type == 'love':
                    return random.choice(self.responses['love'])

                # CREATOR
                elif pattern_type == 'creator':
                    return random.choice(self.responses['creator'])

        # If no pattern matches, try a web search
        if len(command_lower.split()) > 2:  # If it's more than 2 words, probably a search
            return self.internet.search_web_simple(command_lower)
        else:
            return random.choice(self.responses['unknown'])


# Test function
def test_command_processor():
    """Test command processor"""
    print("\n" + "=" * 60)
    print("TESTING COMMAND PROCESSOR")
    print("=" * 60)

    # Create mock internet search for testing
    class MockInternetSearch:
        def get_time_date(self):
            return "Current time is 11:30 PM on Thursday"

        def get_weather_basic(self, city):
            return f"Weather in {city}: Sunny, 25°C"

        def get_news_basic(self):
            return "Top news: Technology advances"

        def search_web_simple(self, query):
            return f"Search results for {query}"

        def calculate(self, expr):
            return f"Result: {eval(expr)}"

        def get_joke(self):
            return "Why did the computer go to therapy? It had too many bytes of emotional baggage!"

    internet = MockInternetSearch()
    processor = CommandProcessor(internet)

    # Test commands
    test_commands = [
        "hello nailee",
        "what time is it",
        "what's the weather like",
        "weather in new york",
        "tell me the news",
        "search for artificial intelligence",
        "calculate 15 + 20",
        "tell me a joke",
        "my name is Alex",
        "thank you",
        "how are you",
        "what can you do",
        "who created you",
        "i love you",
        "goodbye",
        "random unknown command",
    ]

    for i, command in enumerate(test_commands, 1):
        print(f"\n{i}. Testing: '{command}'")
        print("-" * 40)
        response = processor.process_command(command)
        print(f"Response: {response}")

    print("\n" + "=" * 60)
    print("Command processor test complete!")
    print("=" * 60)


if __name__ == "__main__":
    test_command_processor()