from crewai import Agent, Task, Crew, Process
from telegram_bot_crewai.tools.weather_tool import WeatherTool
from telegram_bot_crewai.tools.web_search_tool import WebSearchTool
from telegram_bot_crewai.tools.appointment_tool import AppointmentTool
import yaml
import logging

logger = logging.getLogger(__name__)

class TelegramBotCrewai:
	"""TelegramBotCrewai crew"""

	def __init__(self):
		self.load_config()
		self.create_agents()
		self.create_tasks()

	def load_config(self):
		"""Load agent and task configurations from YAML files."""
		with open('src/telegram_bot_crewai/config/agents.yaml', 'r') as f:
			self.agents_config = yaml.safe_load(f)
		with open('src/telegram_bot_crewai/config/tasks.yaml', 'r') as f:
			self.tasks_config = yaml.safe_load(f)

	def create_agents(self):
		"""Create the agents with their respective tools."""
		self.router_agent = Agent(
			role=self.agents_config['router']['role'],
			goal=self.agents_config['router']['goal'],
			backstory=self.agents_config['router']['backstory'],
			allow_delegation=False
		)

		self.general_agent = Agent(
			role=self.agents_config['general_agent']['role'],
			goal=self.agents_config['general_agent']['goal'],
			backstory=self.agents_config['general_agent']['backstory'],
			tools=[WeatherTool(), WebSearchTool()],
			allow_delegation=False
		)

		self.appointment_agent = Agent(
			role=self.agents_config['appointment_agent']['role'],
			goal=self.agents_config['appointment_agent']['goal'],
			backstory=self.agents_config['appointment_agent']['backstory'],
			tools=[AppointmentTool()],
			allow_delegation=False
		)

	def create_tasks(self):
		"""Create the tasks for each agent."""
		logger.info("Creating route query task")
		self.route_task = Task(
			description=self.tasks_config['route_query']['description'],
			agent=self.router_agent,
			expected_output=self.tasks_config['route_query']['expected_output']
		)

		logger.info("Creating general query task")
		self.general_task = Task(
			description=self.tasks_config['handle_general_query']['description'],
			agent=self.general_agent,
			expected_output=self.tasks_config['handle_general_query']['expected_output']
		)

		logger.info("Creating appointment task")
		self.appointment_task = Task(
			description=self.tasks_config['handle_appointment']['description'],
			agent=self.appointment_agent,
			expected_output=self.tasks_config['handle_appointment']['expected_output']
		)

	def crew(self, inputs=None):
		"""Create and return the crew with all agents and tasks."""
		logger.info("Creating crew with all agents and tasks")
		
		self.inputs = inputs or {}
		
		# First, get the routing decision
		routing_crew = Crew(
			agents=[self.router_agent],
			tasks=[self.route_task],
			process=Process.sequential
		)
		logger.info("Starting routing crew...")
		route_result = routing_crew.kickoff(inputs=self.inputs)
		route_decision = str(route_result).lower()
		logger.info(f"Routing decision: {route_decision}")
		
		# Based on the routing decision, create a crew with the appropriate agent and task
		selected_crew = None
		if "general" in route_decision:
			logger.info("Routing to general agent")
			selected_crew = Crew(
				agents=[self.general_agent],
				tasks=[self.general_task],
				process=Process.sequential
			)
		
		elif "appointment" in route_decision:
			logger.info("Routing to appointment agent")
			selected_crew = Crew(
				agents=[self.appointment_agent],
				tasks=[self.appointment_task],
				process=Process.sequential
			)
		
		else:
			# Default to general agent if routing is unclear
			logger.info("No clear routing decision, defaulting to general agent")
			selected_crew = Crew(
				agents=[self.general_agent],
				tasks=[self.general_task],
				process=Process.sequential
			)
		
		return selected_crew
