"""
Scenario Runner

Orchestrates scenario execution with EEG recording and metadata collection.
"""

import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict

from .base import Scenario
from ..devices.base import EEGDevice
from ..data.logger import EEGLogger
from ..data.metadata import ScenarioMetadata


class ScenarioRunner:
    """
    Executes scenarios with coordinated EEG recording and metadata collection.

    Workflow:
    1. Prepare scenario (show instructions)
    2. Start EEG recording
    3. Execute scenario (timed or manual)
    4. Stop recording
    5. Collect metadata (notes, GPS, etc.)
    6. Save all data
    """

    def __init__(
        self,
        device: EEGDevice,
        data_path: Path,
        config: Dict
    ):
        """
        Initialize scenario runner.

        Args:
            device: EEG device instance
            data_path: Base path for data storage
            config: Configuration dictionary
        """
        self.device = device
        self.data_path = Path(data_path)
        self.config = config

        # Ensure data directories exist
        self.raw_path = self.data_path / "raw"
        self.scenarios_path = self.data_path / "scenarios"
        self.raw_path.mkdir(parents=True, exist_ok=True)
        self.scenarios_path.mkdir(parents=True, exist_ok=True)

    def run(self, scenario: Scenario, auto_start: bool = True) -> bool:
        """
        Execute a scenario.

        Args:
            scenario: Scenario to execute
            auto_start: Whether to start automatically or wait for user input

        Returns:
            True if scenario completed successfully, False otherwise
        """
        print("=" * 80)
        print(f"SCENARIO: {scenario.scenario_type}")
        print("=" * 80)
        print()

        # Show instructions
        print("INSTRUCTIONS:")
        print(scenario.get_instructions())
        print()

        # Preparation phase
        prep_time = self.config.get("scenarios", {}).get("preparation_time", 10)
        if prep_time > 0:
            print(f"Preparation time: {prep_time} seconds")
            print("Get ready...")
            print()

            if auto_start:
                for i in range(prep_time, 0, -1):
                    print(f"  Starting in {i}...", end='\r')
                    time.sleep(1)
                print()
            else:
                input("Press Enter when ready to start...")

        # Generate filenames
        timestamp_str = datetime.now().strftime(
            self.config.get("data_storage", {}).get("timestamp_format", "%Y%m%d_%H%M%S")
        )
        base_filename = f"{scenario.scenario_id}_{timestamp_str}"

        eeg_file = self.raw_path / f"{base_filename}.h5"
        metadata_file = self.scenarios_path / f"{base_filename}.json"

        # Initialize metadata
        metadata = ScenarioMetadata(scenario.scenario_id, scenario.scenario_type)
        metadata.set_device_info(
            device_type=self.config["eeg_device"]["type"],
            channels=self.device.channels,
            sampling_rate=self.device.sampling_rate
        )
        metadata.set_eeg_file(eeg_file)

        # Start scenario
        scenario.on_start()
        metadata.set_start_time()

        print("[Recording] EEG data collection started")
        print()

        # Start EEG recording
        try:
            with EEGLogger(
                file_path=eeg_file,
                channels=self.device.channels,
                sampling_rate=self.device.sampling_rate,
                metadata=scenario.get_metadata(),
                compression=self.config.get("data_storage", {}).get("compression", "gzip"),
                compression_level=self.config.get("data_storage", {}).get("compression_level", 4)
            ) as logger:

                # Recording loop
                if scenario.duration_seconds:
                    # Timed scenario
                    self._run_timed(scenario, logger, metadata)
                else:
                    # Manual stop scenario
                    self._run_manual(scenario, logger, metadata)

        except KeyboardInterrupt:
            print("\n[Recording] Interrupted by user")
            metadata.add_event("interrupted")
        except Exception as e:
            print(f"\n[Recording] ERROR: {e}")
            return False

        # Stop scenario
        scenario.on_stop()
        metadata.set_end_time()

        print("[Recording] EEG data collection stopped")
        print()

        # Collect post-scenario metadata
        self._collect_metadata(metadata)

        # Save metadata
        metadata.save(metadata_file)

        print()
        print("=" * 80)
        print("SCENARIO COMPLETE")
        print("=" * 80)
        print(f"  EEG data: {eeg_file}")
        print(f"  Metadata: {metadata_file}")
        print()

        return True

    def _run_timed(
        self,
        scenario: Scenario,
        logger: EEGLogger,
        metadata: ScenarioMetadata
    ):
        """
        Run scenario with fixed duration.

        Args:
            scenario: Scenario instance
            logger: EEG logger
            metadata: Metadata instance
        """
        duration = scenario.duration_seconds
        start_time = time.time()
        last_update = start_time

        print(f"Recording for {duration} seconds...")
        print("(Press Ctrl+C to stop early)")
        print()

        while time.time() - start_time < duration:
            # Get EEG sample
            sample_data = self.device.get_sample()
            if sample_data:
                data, timestamp = sample_data
                logger.write_sample(data, timestamp)

            # Progress update every second
            elapsed = time.time() - start_time
            if elapsed - last_update >= 1.0:
                remaining = duration - elapsed
                progress = (elapsed / duration) * 100
                print(f"  Progress: {progress:.1f}% ({remaining:.0f}s remaining)", end='\r')
                last_update = elapsed

            time.sleep(0.001)  # Small delay to prevent CPU spinning

        print()

    def _run_manual(
        self,
        scenario: Scenario,
        logger: EEGLogger,
        metadata: ScenarioMetadata
    ):
        """
        Run scenario until user manually stops.

        Args:
            scenario: Scenario instance
            logger: EEG logger
            metadata: Metadata instance
        """
        print("Recording... (Press Ctrl+C to stop)")
        print()

        start_time = time.time()
        last_update = start_time

        try:
            while True:
                # Get EEG sample
                sample_data = self.device.get_sample()
                if sample_data:
                    data, timestamp = sample_data
                    logger.write_sample(data, timestamp)

                # Time update every second
                elapsed = time.time() - start_time
                if elapsed - last_update >= 1.0:
                    print(f"  Recording: {elapsed:.0f}s", end='\r')
                    last_update = elapsed

                time.sleep(0.001)

        except KeyboardInterrupt:
            print()
            pass

    def _collect_metadata(self, metadata: ScenarioMetadata):
        """
        Collect post-scenario metadata from user.

        Args:
            metadata: Metadata instance to populate
        """
        require_notes = self.config.get("scenarios", {}).get("require_notes", True)

        if not require_notes:
            return

        print("POST-SCENARIO NOTES")
        print("-" * 80)
        print()

        # Description
        description = input("Brief description of what happened (optional): ").strip()
        if description:
            metadata.set_description(description)

        # Text note
        note = input("Any observations or thoughts? (optional): ").strip()
        if note:
            metadata.add_text_note(note)

        # Tags
        tags_input = input("Tags (comma-separated, optional): ").strip()
        if tags_input:
            tags = [tag.strip() for tag in tags_input.split(",")]
            for tag in tags:
                if tag:
                    metadata.add_tag(tag)

        # Quality rating
        while True:
            rating_input = input("Data quality rating (1-5, optional): ").strip()
            if not rating_input:
                break
            try:
                rating = int(rating_input)
                if 1 <= rating <= 5:
                    metadata.set_quality_rating(rating)
                    break
                else:
                    print("  Please enter a number between 1 and 5")
            except ValueError:
                print("  Please enter a valid number")

        print()
