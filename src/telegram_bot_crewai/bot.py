import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv
from telegram_bot_crewai.crew import TelegramBotCrew

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    await update.message.reply_text('Hi! I am your AI assistant. How can I help you today?')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    help_text = """
    Available commands:
    /start - Start the bot
    /help - Show this help message
    Just send me any message, and I'll help you with your query!
    """
    await update.message.reply_text(help_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle user messages and respond using CrewAI."""
    user_message = update.message.text
    logger.info(f"Received message: {user_message}")
    
    try:
        # Create crew instance
        logger.info("Creating CrewAI instance...")
        crew_instance = TelegramBotCrew()
        
        # Get the crew
        crew = crew_instance.crew()
        
        # Prepare inputs
        inputs = {
            'message': user_message
        }
        logger.info(f"Starting crew execution with inputs: {inputs}")
        
        # Execute the crew with inputs
        result = crew.kickoff(inputs=inputs)
        logger.info(f"Crew execution completed. Raw result: {result}")
        
        # Extract the response from the result
        response_text = str(result)
        logger.info(f"Response after str conversion: {response_text}")
        
        # Clean up the response
        if "## Final Answer:" in response_text:
            response_text = response_text.split("## Final Answer:")[-1].strip()
            logger.info(f"Response after Final Answer extraction: {response_text}")
        else:
            logger.warning("No '## Final Answer:' found in response")
        
        # Remove any remaining markdown headers and clean up formatting
        cleaned_lines = []
        for line in response_text.splitlines():
            if not line.startswith('#'):
                # Remove asterisks and clean up appointment formatting
                line = line.replace('**', '')
                if line.strip().startswith('-'):
                    # Format appointment lines
                    line = line.strip()[1:].strip()  # Remove the leading dash
                cleaned_lines.append(line.strip())
        
        # Join lines and format the final message
        if "appointment" in user_message.lower():
            response_text = "Here are your scheduled appointments:\n\n"
            response_text += '\n'.join(cleaned_lines)
        else:
            response_text = '\n'.join(cleaned_lines)
        
        logger.info(f"Response after markdown cleanup: {response_text}")
        
        if not response_text or not response_text.strip():
            logger.warning("No valid response found in the result")
            response_text = "Sorry, I couldn't process your request."
        
        logger.info(f"Final response to be sent: {response_text}")
        await update.message.reply_text(response_text)
        logger.info("Response sent to Telegram successfully")
    except Exception as e:
        logger.error(f"Error processing message: {e}", exc_info=True)
        await update.message.reply_text("Sorry, I encountered an error. Please try again.")

def main():
    """Start the bot."""
    # Create the Application and pass it your bot's token
    application = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main() 