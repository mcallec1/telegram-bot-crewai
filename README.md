# 🤖 Telegram Bot with CrewAI and OpenAI 🚀

This project is a Telegram bot powered by OpenAI's GPT models and CrewAI's agent framework. Designed as a boilerplate, the structure is highly customisable, with detailed comments and configuration files for easy future development. The bot demonstrates advanced capabilities in handling general queries, performing web searches, and managing appointments through a multi-agent system.

## 🌟 Features

- **💬 General Queries**: Answer user questions using AI agents
- **🌐 Web Search**: Search the web for the latest information
- **📅 Appointment Management**: Schedule, reschedule, and cancel appointments with persistent storage in a local JSON file
- **🌦️ Current Weather**: Provide real-time weather updates

## 🛠️ Architecture Overview

### 🔍 Router Agent

Analyzes user queries to determine which specialized agent should handle the task.

### 🤖 Specialized Agents

- **General Agent**: Handles general-purpose queries and information retrieval
- **Appointment Agent**: Manages all appointment-related operations

The system uses CrewAI's agent framework for task delegation and execution, with YAML-based configuration for easy customization.

## ⚙️ Setup Instructions

### 🔖 Creating a Telegram Bot

1. Open Telegram and search for **@BotFather**
2. Send `/newbot` and follow the prompts
3. Save the API token you receive

### Backend Setup

1. **Clone the repository**:

```bash
git clone https://github.com/mcallec1/telegram_bot_crewai.git
cd telegram-bot-crewai
```

2. **Install the package**:

```bash
pip install .
```

3. **Configure environment variables**:
   Create a `.env` file with:

```env
OPENAI_API_KEY=your_openai_api_key
SERPAPI_KEY=your_serpapi_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
OPENWEATHER_API_KEY=your_openweather_key
```

## 🚀 Running the Bot

Start the bot using:

```bash
crewai run
```

## 💡 Usage

### Basic Commands

- **/start**: Initialize the bot
- **/help**: View available commands

### Example Queries

#### General Knowledge

```
What is the capital of Japan?
Tell me about the history of pizza
Who invented the telephone?
```

#### Weather Information

```
What's the weather like in New York?
Tell me the temperature in Paris
Is it raining in Tokyo?
```

#### Appointment Management

```
Schedule a meeting tomorrow at 2 PM
Can you help me book an appointment for next week?
Reschedule my appointment from Monday to Tuesday
What appointments do I have scheduled?
```

#### Complex Multi-Task Queries

```
I need to schedule a meeting, but first tell me the weather forecast
Can you find information about restaurants in London and help me book a table?
What's the best time to schedule a meeting in Tokyo considering the weather?
```

These examples demonstrate the bot's capabilities in:

- Routing between general and appointment agents
- Weather information retrieval
- Web search functionality
- Appointment management with local storage
- Handling complex, multi-step requests

## 📊 Project Structure

```
telegram_bot_crewai/
├── src/
│   └── telegram_bot_crewai/
│       ├── config/
│       │   ├── agents.yaml    # Agent definitions
│       │   └── tasks.yaml     # Task configurations
│       ├── tools/
│       │   ├── appointment_tool.py
│       │   ├── weather_tool.py
│       │   └── web_search_tool.py
│       ├── bot.py            # Telegram interface
│       ├── crew.py          # CrewAI setup
│       └── main.py          # Entry point
└── appointments.json        # Appointment storage
```

## 🔗 Key Dependencies

- [CrewAI](https://github.com/joaomdmoura/crewAI)
- [python-telegram-bot](https://python-telegram-bot.org/)
- [OpenAI API](https://beta.openai.com/docs/)
- [SerpAPI](https://serpapi.com/)
- [OpenWeather API](https://openweathermap.org/api)

## 📝 Development

The project uses:

- CrewAI for agent-based task management
- YAML configuration for easy customization
- Pydantic for data validation
- Local JSON file for persistent appointment storage

## 📜 License

This project is licensed under the MIT License.

---

_Note: This is a CrewAI adaptation of the original LangChain implementation, optimized for better agent coordination and task management._

## 🙏 Acknowledgments

This project is based on the original [Telegram-Bot](https://github.com/osamatech786/Telegram-Bot) by [@osamatech786](https://github.com/osamatech786), which was implemented using LangChain.
