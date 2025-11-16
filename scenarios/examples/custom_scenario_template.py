#!/usr/bin/env python3
"""
Custom Scenario Template

Example of how to create a custom scenario by extending the Scenario base class.
Copy this file and modify for your specific use case.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from embodied_ai.scenarios.base import Scenario


class CustomScenario(Scenario):
    """
    Example custom scenario.

    Override the methods below to customize behavior:
    - get_instructions(): Display instructions to user
    - on_start(): Called when recording starts
    - on_stop(): Called when recording stops
    """

    def __init__(self, scenario_id: str):
        """Initialize your custom scenario."""
        super().__init__(
            scenario_id=scenario_id,
            scenario_type="custom_example",
            duration_seconds=300  # 5 minutes, or None for manual stop
        )

        # Add any custom attributes here
        self.custom_data = {}

    def get_instructions(self) -> str:
        """
        Return instructions to show the user.

        This is displayed before the scenario starts.
        """
        return """
CUSTOM SCENARIO EXAMPLE

Instructions:
1. Do something specific
2. Follow these steps
3. Maintain focus
4. Complete the task

This is where you describe what the user should do.
        """

    def on_start(self):
        """
        Called when scenario starts.

        Use this to:
        - Initialize state
        - Print custom messages
        - Set up timers
        - etc.
        """
        # Call parent method first
        super().on_start()

        # Add your custom logic
        print("[CustomScenario] Starting custom logic...")

    def on_stop(self):
        """
        Called when scenario stops.

        Use this to:
        - Clean up resources
        - Print summary
        - Process collected data
        - etc.
        """
        # Add your custom logic
        print("[CustomScenario] Stopping custom logic...")

        # Call parent method
        super().on_stop()


# Example usage
if __name__ == "__main__":
    from datetime import datetime
    from embodied_ai.utils.config import load_config
    from embodied_ai.devices import SimulatorDevice
    from embodied_ai.scenarios import ScenarioRunner

    # Load config
    config = load_config("config.yaml")

    # Create device
    device = SimulatorDevice(config["eeg_device"])
    device.connect()
    device.start_streaming()

    # Create custom scenario
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    scenario = CustomScenario(f"custom_{timestamp}")

    # Run it
    runner = ScenarioRunner(
        device=device,
        data_path=config["data_storage"]["base_path"],
        config=config
    )

    runner.run(scenario)

    # Cleanup
    device.stop_streaming()
    device.disconnect()
