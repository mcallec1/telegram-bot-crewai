from crewai.tools import BaseTool
from typing import Type, Optional, List
from pydantic import BaseModel, Field
import json
import logging
from datetime import datetime
import os

logger = logging.getLogger(__name__)

class Appointment(BaseModel):
    """Model for an appointment."""
    appointment_time: str
    description: str

class AppointmentToolInput(BaseModel):
    """Input schema for AppointmentTool."""
    action: str = Field(
        ..., 
        description="The action to perform (schedule, reschedule, list, cancel)"
    )
    details: Optional[str] = Field(
        None,
        description="""JSON string containing appointment details.
        For schedule: {"appointment_time": "YYYY-MM-DD HH:MM", "description": "..."}
        For reschedule: {"old_time": "...", "new_time": "...", "description": "..."}
        For cancel: {"appointment_time": "..."}
        For list: no details needed"""
    )

class AppointmentTool(BaseTool):
    """Tool for managing appointments."""
    
    name: str = "Appointment Manager"
    description: str = """Manage appointments including scheduling, rescheduling, and listing appointments.
    Use this tool to:
    - Schedule new appointments
    - List all current appointments
    - Reschedule existing appointments
    - Cancel appointments
    """
    args_schema: Type[BaseModel] = AppointmentToolInput
    appointments_file: str = Field(default="appointments.json")
    appointments: List[Appointment] = Field(default_factory=list)
    
    def __init__(self, **data):
        super().__init__(**data)
        self._load_appointments()
    
    def _load_appointments(self):
        """Load appointments from file."""
        if os.path.exists(self.appointments_file):
            with open(self.appointments_file, 'r') as f:
                appointments_data = json.load(f)
                self.appointments = [Appointment(**apt) for apt in appointments_data]
        else:
            self.appointments = []
            self._save_appointments()
    
    def _save_appointments(self):
        """Save appointments to file."""
        with open(self.appointments_file, 'w') as f:
            json.dump([apt.dict() for apt in self.appointments], f, indent=2)
    
    def _run(self, action: str, details: Optional[str] = None) -> str:
        """
        Manage appointments based on the action requested.
        """
        # Clean up the action string by removing quotes and whitespace
        action = action.strip().strip('"\'').lower()
        logger.info(f"Managing appointment - Action: {action}, Details: {details}")
        
        try:
            if action == "list":
                logger.info(f"Current appointments: {self.appointments}")
                if not self.appointments:
                    return "No appointments scheduled"
                appointments_list = ["Current appointments:"]
                for apt in sorted(self.appointments, key=lambda x: x.appointment_time):
                    appointments_list.append(f"- {apt.appointment_time}: {apt.description}")
                return "\n".join(appointments_list)
            
            elif action == "schedule":
                if not details:
                    return "Please provide appointment details (time and description)"
                appointment_data = json.loads(details)
                appointment = Appointment(**appointment_data)
                self.appointments.append(appointment)
                self._save_appointments()
                logger.info(f"Scheduled new appointment: {appointment}")
                return f"Appointment scheduled for {appointment.appointment_time}: {appointment.description}"
            
            elif action == "reschedule":
                if not details:
                    return "Please provide old and new appointment details"
                reschedule_info = json.loads(details)
                for apt in self.appointments:
                    if apt.appointment_time == reschedule_info["old_time"]:
                        old_time = apt.appointment_time
                        apt.appointment_time = reschedule_info["new_time"]
                        self._save_appointments()
                        logger.info(f"Rescheduled appointment from {old_time} to {apt.appointment_time}")
                        return f"Appointment rescheduled to {reschedule_info['new_time']}"
                return "Original appointment not found"
            
            elif action == "cancel":
                if not details:
                    return "Please provide appointment time to cancel"
                cancel_info = json.loads(details)
                original_length = len(self.appointments)
                cancelled_appointments = [apt for apt in self.appointments 
                                       if apt.appointment_time == cancel_info["appointment_time"]]
                self.appointments = [apt for apt in self.appointments 
                                   if apt.appointment_time != cancel_info["appointment_time"]]
                if len(self.appointments) < original_length:
                    self._save_appointments()
                    logger.info(f"Cancelled appointments: {cancelled_appointments}")
                    return f"Appointment at {cancel_info['appointment_time']} cancelled"
                return "No appointment found at the specified time"
            
            else:
                logger.warning(f"Unknown action requested: {action}")
                return f"Unknown action: {action}"
                
        except Exception as e:
            logger.error(f"Error managing appointment: {e}", exc_info=True)
            return f"Error managing appointment: {str(e)}" 