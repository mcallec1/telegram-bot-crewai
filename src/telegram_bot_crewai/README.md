# Telegram Bot with CrewAI

A Telegram bot built using CrewAI that can handle general queries and manage appointments.

## Features

- **General Information**

  - Weather information for any location
  - Web search capabilities
  - General knowledge queries

- **Appointment Management**
  - Schedule new appointments
  - List all current appointments
  - Reschedule existing appointments
  - Cancel appointments
  - Persistent storage in JSON format

## Setup

1. Create a Telegram bot by talking to [@BotFather](https://t.me/botfather) and get your bot token
2. Create a `.env` file based on `.env.example` and add your:

   - `TELEGRAM_BOT_TOKEN`
   - `OPENAI_API_KEY`

3. Install dependencies:

```bash
crewai install
```

4. Run the bot:

```bash
crewai run
```

## Usage Examples

### General Queries

```
What's the weather in London?
Tell me about the history of pizza
```

### Appointment Management

The bot manages appointments with natural language commands:

1. View Appointments:

```
What appointments do I have scheduled?
Show my appointments
```

2. Schedule Appointments:

```
Schedule a team meeting for tomorrow at 2 PM
Schedule a doctor's appointment for next Monday at 10 AM
```

3. Reschedule Appointments:

```
Reschedule my 2 PM meeting to 3 PM
```

4. Cancel Appointments:

```
Cancel my meeting at 2 PM tomorrow
```

## Appointment Storage

Appointments are stored in a `appointments.json` file in the following format:

```json
[
  {
    "appointment_time": "YYYY-MM-DD HH:MM",
    "description": "Appointment description"
  }
]
```

The appointment times are stored in 24-hour format (e.g., "2024-01-07 14:00").
The JSON file is automatically created and managed by the bot, providing persistent storage between bot restarts.

## Commands

- `/start` - Start the bot and get a welcome message
- `/help` - Show available commands and usage information
