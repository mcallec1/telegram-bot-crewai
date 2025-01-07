from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from telegram_bot_crewai.tools.weather_tool import WeatherTool
from telegram_bot_crewai.tools.web_search_tool import WebSearchTool
from telegram_bot_crewai.tools.appointment_tool import AppointmentTool
from langchain_openai import ChatOpenAI
import logging
from typing import Optional

logger = logging.getLogger(__name__)

@CrewBase
class TelegramBotCrew:
	"""Telegram Bot crew for handling queries and appointments"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def general_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['general_agent'],
			tools=[
				WeatherTool(),
				WebSearchTool()
			],
			allow_delegation=False,
			verbose=True
		)

	@agent
	def appointment_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['appointment_agent'],
			tools=[AppointmentTool()],
			allow_delegation=True,
			verbose=True
		)

	@task
	def handle_query(self) -> Task:
		return Task(
			config=self.tasks_config['handle_query'],
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Telegram Bot crew with manager-based delegation"""
	
		try:
			return Crew(
				agents=self.agents,
				tasks=self.tasks,
				manager_llm=ChatOpenAI(
					temperature=0,
					model="gpt-4o-mini",
					verbose=True
				),
				process=Process.hierarchical,
				verbose=True,
			)
		except Exception as e:
			logger.error(f"Error creating crew: {str(e)}")
			raise

	# def format_response(self, response: Optional[str]) -> str:
	# 	"""Format the crew's response for Telegram"""
	# 	if not response:
	# 		return "Sorry, I couldn't process your request."
		
	# 	# Clean up the response by removing any "Final Answer:" prefix
	# 	response = response.replace("Final Answer:", "").strip()
	# 	return response
