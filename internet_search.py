import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import time


class InternetSearch:
    def __init__(self):
        # We'll add API keys later
        self.wolfram_app_id = None
        self.weather_api_key = None

        # User-Agent header to avoid blocking
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        print("🌐 Internet search module initialized")

    def get_time_date(self):
        """Get current time and date"""
        now = datetime.now()
        current_time = now.strftime("%I:%M %p").lstrip('0')
        current_date = now.strftime("%B %d, %Y")
        day_of_week = now.strftime("%A")
        return f"The current time is {current_time} on {day_of_week}, {current_date}"

    def search_web_simple(self, query):
        """Simple web search using DuckDuckGo"""
        try:
            print(f"🔍 Searching for: {query}")
            # Clean the query
            clean_query = requests.utils.quote(query)
            search_url = f"https://duckduckgo.com/html/?q={clean_query}"

            response = requests.get(search_url, headers=self.headers, timeout=8)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Try to find instant answer
            answer = soup.find('div', class_='result__snippet')
            if answer:
                text = answer.get_text()[:250]
                return f"According to web search: {text}"

            # Alternative: look for Wikipedia result
            wikipedia_result = soup.find('a', class_='result__url')
            if wikipedia_result and 'wikipedia' in wikipedia_result.text.lower():
                # Try to get Wikipedia summary directly
                try:
                    wiki_url = wikipedia_result['href']
                    wiki_response = requests.get(wiki_url, headers=self.headers, timeout=8)
                    wiki_soup = BeautifulSoup(wiki_response.text, 'html.parser')

                    # Find first paragraph
                    for paragraph in wiki_soup.find_all('p'):
                        if paragraph.text.strip() and len(paragraph.text) > 50:
                            summary = paragraph.text[:300]
                            return f"Wikipedia says: {summary}"
                except:
                    pass

            # Last resort: return simple answer
            return f"I found information about {query.split()[0]} but need more specific details. Could you rephrase your question?"

        except requests.exceptions.Timeout:
            return "Search is taking too long. Please try again."
        except Exception as e:
            print(f"Search error: {e}")
            return "I'm having trouble searching right now. Please try again later."

    def get_weather_basic(self, city="your location"):
        """Basic weather without API (we'll enhance with API later)"""
        try:
            if city == "your location":
                try:
                    # Try to get city from IP
                    response = requests.get('https://ipinfo.io/city', headers=self.headers, timeout=5)
                    if response.status_code == 200:
                        city = response.text.strip()
                    else:
                        city = "London"
                except:
                    city = "London"

            print(f"🌤️  Getting weather for: {city}")

            # Alternative weather source with shorter timeout
            url = f"https://wttr.in/{city}?format=3"
            response = requests.get(url, headers=self.headers, timeout=5)

            if response.status_code == 200:
                weather_data = response.text.strip()
                return f"Weather in {city}: {weather_data}"
            else:
                # Fallback to static message
                return f"I can check detailed weather for {city} once we add the weather API."

        except requests.exceptions.Timeout:
            return "Weather service is taking too long. Please try again in a moment."
        except Exception as e:
            print(f"Weather check error: {e}")
            return f"I'll have weather updates soon. For now, you can check any weather app for {city}."

    def get_news_basic(self):
        """Get basic news headlines"""
        try:
            print("📰 Fetching news headlines...")

            # Alternative news source: Reddit worldnews (no API needed)
            url = "https://www.reddit.com/r/worldnews/.json"
            response = requests.get(url, headers=self.headers, timeout=8)

            if response.status_code == 200:
                data = response.json()
                articles = data['data']['children'][:5]  # Top 5 articles

                headlines = []
                for article in articles:
                    title = article['data']['title'][:100]  # Limit title length
                    headlines.append(title)

                if headlines:
                    news_summary = " | ".join(headlines)
                    return f"Top world news: {news_summary}"

            # Fallback to static news
            return "Today's important updates: Technology is advancing rapidly. Check news websites for latest updates."

        except Exception as e:
            print(f"News error: {e}")
            return "For the latest news, please check your favorite news website or app."

    def calculate(self, expression):
        """Simple calculation"""
        try:
            # Clean the expression - only allow safe characters
            safe_chars = set('0123456789+-*/.()% ')
            clean_expr = ''.join(char for char in expression if char in safe_chars)

            if not clean_expr:
                return "Please provide a valid mathematical expression."

            # Additional safety check
            if len(clean_expr) > 50:
                return "Expression too long for calculation."

            result = eval(clean_expr)
            return f"The result is {result}"

        except ZeroDivisionError:
            return "Cannot divide by zero."
        except SyntaxError:
            return "Invalid mathematical expression. Please use numbers and basic operators (+, -, *, /)."
        except Exception as e:
            print(f"Calculation error: {e}")
            return "I couldn't calculate that. Please check the expression."

    def get_joke(self):
        """Get a random joke"""
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the computer go to the doctor? Because it had a virus!",
            "What do you call a fake noodle? An impasta!",
            "Why don't eggs tell jokes? They'd crack each other up!",
            "What do you call a bear with no teeth? A gummy bear!",
            "Why did the math book look so sad? Because it had too many problems!",
        ]
        import random
        return random.choice(jokes)


# Test function
def test_internet_search():
    """Test internet search capabilities"""
    print("\n" + "=" * 60)
    print("🌐 TESTING UPDATED INTERNET SEARCH MODULE")
    print("=" * 60)

    search = InternetSearch()

    # Test 1: Time and Date
    print("\n1. Testing time and date...")
    time_info = search.get_time_date()
    print(f" {time_info}")

    # Test 2: Weather
    print("\n2. Testing weather...")
    weather_info = search.get_weather_basic("London")
    print(f"{weather_info}")

    # Test 3: News
    print("\n3. Testing news...")
    news_info = search.get_news_basic()
    print(f"{news_info[:150]}...")  # Show first 150 chars

    # Test 4: Web Search
    print("\n4. Testing web search...")
    search_result = search.search_web_simple("Python programming")
    print(f"{search_result}")

    # Test 5: Calculation
    print("\n5. Testing calculation...")
    calc_result = search.calculate("15 * 3 + 7")
    print(f" {calc_result}")

    # Test 6: Joke
    print("\n6. Testing joke...")
    joke = search.get_joke()
    print(f" {joke}")

    print("\n" + "=" * 60)
    print(" Internet search module test complete!")
    print("=" * 60)


if __name__ == "__main__":
    test_internet_search()