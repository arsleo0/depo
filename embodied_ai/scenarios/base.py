"""
Base Scenario Class

Defines the structure for scenario definitions.
Users can create custom scenarios by subclassing this.
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional
from datetime import datetime


class Scenario(ABC):
    """
    Base class for all scenarios.

    A scenario represents a specific activity or context during which
    EEG data is collected (e.g., "walking in park", "problem solving", etc.)
    """

    def __init__(
        self,
        scenario_id: str,
        scenario_type: str,
        duration_seconds: Optional[int] = None
    ):
        """
        Initialize scenario.

        Args:
            scenario_id: Unique identifier
            scenario_type: Type category
            duration_seconds: Optional fixed duration (None for manual stop)
        """
        self.scenario_id = scenario_id
        self.scenario_type = scenario_type
        self.duration_seconds = duration_seconds

        self.start_time = None
        self.end_time = None
        self.is_running = False

    @abstractmethod
    def get_instructions(self) -> str:
        """
        Return instructions to display to the user.

        Returns:
            String with scenario instructions
        """
        pass

    def on_start(self):
        """
        Called when scenario starts.
        Override to add custom initialization logic.
        """
        self.start_time = datetime.now()
        self.is_running = True
        print(f"\n[Scenario] Started: {self.scenario_type}")
        print(f"  ID: {self.scenario_id}")
        if self.duration_seconds:
            print(f"  Duration: {self.duration_seconds} seconds")
        print()

    def on_stop(self):
        """
        Called when scenario stops.
        Override to add custom cleanup logic.
        """
        self.end_time = datetime.now()
        self.is_running = False

        if self.start_time:
            duration = (self.end_time - self.start_time).total_seconds()
            print(f"\n[Scenario] Stopped: {self.scenario_type}")
            print(f"  Duration: {duration:.1f} seconds")
        print()

    def get_metadata(self) -> Dict:
        """
        Return scenario metadata for logging.

        Returns:
            Dictionary with scenario information
        """
        return {
            "scenario_id": self.scenario_id,
            "scenario_type": self.scenario_type,
            "duration_seconds": self.duration_seconds,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None
        }


class SimpleScenario(Scenario):
    """
    Simple scenario with just instructions and duration.
    Good for most use cases.
    """

    def __init__(
        self,
        scenario_id: str,
        scenario_type: str,
        instructions: str,
        duration_seconds: Optional[int] = None
    ):
        """
        Initialize simple scenario.

        Args:
            scenario_id: Unique identifier
            scenario_type: Type category
            instructions: Instructions to display
            duration_seconds: Optional fixed duration
        """
        super().__init__(scenario_id, scenario_type, duration_seconds)
        self.instructions = instructions

    def get_instructions(self) -> str:
        """Return the instructions."""
        return self.instructions
