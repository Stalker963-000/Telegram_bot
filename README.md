# Telegram_bot

Features:

- User Registration: Collects and securely stores user details (passwords are hashed with SHA-256).

- Weather Updates: Provides real-time weather forecasts for user-specified cities with temperature and weather conditions.

- Interactive Responses: Handles commands (/start, /help, /weather), specific text inputs, and multimedia like photos.

- Inline Keyboards: Offers buttons for actions like deleting or editing messages, or linking to websites.

- Help Menu: Shares a help file with users for guidance.



Setup:

- Clone the repository and navigate to the project folder:
    git clone https://github.com/your-username/telegram-bot.git
    cd telegram-bot

- Install dependencies:
    pip install pyTelegramBotAPI requests

- Replace placeholder values in the script:
    BOT_TOKEN with your Telegram Bot Token.
    API_KEY with your OpenWeather API Key.

- Run the bot:
    python bot.py



Usage:

/start or /hello: Begins user registration.

/weather: Prompts for a city name and provides weather details.

/help: Sends a help file to the user.



Notes:

- Password Security: User passwords are stored as hashed values for protection.

- Token Safety: Keep your bot token and API key private to prevent unauthorized access.
