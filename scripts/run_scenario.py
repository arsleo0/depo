#!/usr/bin/env python3
"""
Scenario Runner CLI

Command-line interface for executing data collection scenarios.
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from embodied_ai.utils.config import load_config, ensure_data_directories
from embodied_ai.devices import SimulatorDevice
from embodied_ai.devices.muse import Muse2Device
from embodied_ai.scenarios import SimpleScenario, ScenarioRunner


def create_predefined_scenario(scenario_type: str, duration: int = None) -> SimpleScenario:
    """
    Create a predefined scenario.

    Args:
        scenario_type: Type of scenario
        duration: Duration in seconds (None for manual)

    Returns:
        SimpleScenario instance
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    scenario_id = f"{scenario_type}_{timestamp}"

    scenarios = {
        "baseline_rest": {
            "instructions": """
BASELINE RESTING STATE

Instructions:
1. Sit comfortably in a quiet place
2. Close your eyes
3. Relax and breathe naturally
4. Try to clear your mind
5. Stay still for the duration

This establishes your baseline brain activity.
            """,
            "default_duration": 300  # 5 minutes
        },

        "focused_task": {
            "instructions": """
FOCUSED COGNITIVE TASK

Instructions:
1. Work on a challenging problem or task
2. Maintain concentration
3. Think actively and engage your mind
4. Examples: math problems, coding, writing

This measures brain activity during focused work.
            """,
            "default_duration": 600  # 10 minutes
        },

        "meditation": {
            "instructions": """
MEDITATION SESSION

Instructions:
1. Sit comfortably
2. Close your eyes
3. Focus on your breath
4. When mind wanders, gently return to breath
5. Maintain calm awareness

This measures meditative brain states.
            """,
            "default_duration": 600  # 10 minutes
        },

        "physical_activity": {
            "instructions": """
PHYSICAL ACTIVITY

Instructions:
1. Perform light to moderate exercise
2. Examples: walking, stretching, light cardio
3. Maintain steady activity
4. Be mindful of your body and surroundings

This measures brain activity during movement.
            """,
            "default_duration": 900  # 15 minutes
        },

        "creative_work": {
            "instructions": """
CREATIVE WORK

Instructions:
1. Engage in creative activity
2. Examples: drawing, writing, brainstorming
3. Let ideas flow freely
4. Don't judge or edit

This measures creative cognitive states.
            """,
            "default_duration": 900  # 15 minutes
        }
    }

    if scenario_type not in scenarios:
        raise ValueError(f"Unknown scenario type: {scenario_type}")

    scenario_def = scenarios[scenario_type]

    # Use provided duration or default
    if duration is None:
        duration = scenario_def.get("default_duration")

    return SimpleScenario(
        scenario_id=scenario_id,
        scenario_type=scenario_type,
        instructions=scenario_def["instructions"],
        duration_seconds=duration
    )


def list_scenario_types():
    """Print available scenario types."""
    print("\nAvailable Scenario Types:")
    print("-" * 60)
    print("  baseline_rest      - Resting state baseline (5 min)")
    print("  focused_task       - Focused cognitive work (10 min)")
    print("  meditation         - Meditation session (10 min)")
    print("  physical_activity  - Physical movement (15 min)")
    print("  creative_work      - Creative activities (15 min)")
    print()
    print("Use --duration to override default durations (in seconds)")
    print("Use --manual to record until manually stopped (Ctrl+C)")
    print()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Run an EEG data collection scenario",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_scenario.py baseline_rest
  python run_scenario.py focused_task --duration 300
  python run_scenario.py meditation --manual
  python run_scenario.py --list
        """
    )

    parser.add_argument(
        "scenario_type",
        nargs="?",
        help="Type of scenario to run"
    )

    parser.add_argument(
        "--duration",
        type=int,
        help="Duration in seconds (overrides default)"
    )

    parser.add_argument(
        "--manual",
        action="store_true",
        help="Manual stop (ignores duration)"
    )

    parser.add_argument(
        "--list",
        action="store_true",
        help="List available scenario types"
    )

    parser.add_argument(
        "--config",
        default="config.yaml",
        help="Path to configuration file (default: config.yaml)"
    )

    parser.add_argument(
        "--no-auto-start",
        action="store_true",
        help="Wait for user input before starting recording"
    )

    args = parser.parse_args()

    # List scenarios
    if args.list:
        list_scenario_types()
        return

    # Validate scenario type
    if not args.scenario_type:
        parser.error("scenario_type is required (or use --list)")

    try:
        # Load configuration
        config = load_config(args.config)

        # Ensure data directories exist
        ensure_data_directories(config)

        # Create device
        device_type = config["eeg_device"]["type"]
        print(f"[Setup] Using device: {device_type}")

        if device_type == "simulator":
            device = SimulatorDevice(config["eeg_device"])
        elif device_type == "muse2":
            device = Muse2Device(config["eeg_device"])
        else:
            print(f"ERROR: Unknown device type: {device_type}")
            sys.exit(1)

        # Connect to device
        print("[Setup] Connecting to device...")
        if not device.connect():
            print("ERROR: Failed to connect to device")
            sys.exit(1)

        # Start streaming
        print("[Setup] Starting data stream...")
        if not device.start_streaming():
            print("ERROR: Failed to start streaming")
            device.disconnect()
            sys.exit(1)

        print("[Setup] Device ready")
        print()

        # Create scenario
        duration = None if args.manual else args.duration
        scenario = create_predefined_scenario(args.scenario_type, duration)

        # Create runner
        runner = ScenarioRunner(
            device=device,
            data_path=config["data_storage"]["base_path"],
            config=config
        )

        # Run scenario
        success = runner.run(scenario, auto_start=not args.no_auto_start)

        # Cleanup
        device.stop_streaming()
        device.disconnect()

        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
