"""
Scenario Metadata Management

Handles JSON metadata for scenarios including:
- Scenario description and type
- Timestamps (start, end, events)
- GPS data references
- Audio notes
- User annotations
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any


class ScenarioMetadata:
    """
    Manages metadata for a single scenario execution.

    Stores all non-EEG data in JSON format:
    - Scenario information
    - Timestamps and duration
    - GPS track reference
    - Audio notes
    - Text annotations
    - Custom fields
    """

    def __init__(self, scenario_id: str, scenario_type: str):
        """
        Initialize scenario metadata.

        Args:
            scenario_id: Unique identifier for this scenario
            scenario_type: Type of scenario (e.g., "baseline_rest", "focused_task")
        """
        self.scenario_id = scenario_id
        self.scenario_type = scenario_type

        # Core metadata
        self.data = {
            "scenario_id": scenario_id,
            "scenario_type": scenario_type,
            "created_at": datetime.now().isoformat(),
            "version": "0.1.0"
        }

        # Timestamps
        self.data["timestamps"] = {
            "start": None,
            "end": None,
            "duration_seconds": None,
            "events": []  # List of (timestamp, event_name) tuples
        }

        # Multimodal data
        self.data["multimodal"] = {
            "eeg_file": None,
            "gps_file": None,
            "audio_files": [],
            "text_notes": []
        }

        # User annotations
        self.data["annotations"] = {
            "description": "",
            "tags": [],
            "quality_rating": None,  # 1-5 scale
            "notes": ""
        }

        # Device information
        self.data["device_info"] = {
            "eeg_device": None,
            "channels": [],
            "sampling_rate": None
        }

    def set_start_time(self, start_time: Optional[datetime] = None):
        """Set scenario start timestamp."""
        if start_time is None:
            start_time = datetime.now()
        self.data["timestamps"]["start"] = start_time.isoformat()

    def set_end_time(self, end_time: Optional[datetime] = None):
        """Set scenario end timestamp and calculate duration."""
        if end_time is None:
            end_time = datetime.now()

        self.data["timestamps"]["end"] = end_time.isoformat()

        # Calculate duration if start time is set
        if self.data["timestamps"]["start"]:
            start = datetime.fromisoformat(self.data["timestamps"]["start"])
            duration = (end_time - start).total_seconds()
            self.data["timestamps"]["duration_seconds"] = duration

    def add_event(self, event_name: str, timestamp: Optional[datetime] = None):
        """
        Add a timestamped event marker.

        Args:
            event_name: Description of the event
            timestamp: Event timestamp (defaults to now)
        """
        if timestamp is None:
            timestamp = datetime.now()

        self.data["timestamps"]["events"].append({
            "name": event_name,
            "timestamp": timestamp.isoformat()
        })

    def set_eeg_file(self, file_path: Path):
        """Set reference to EEG data file."""
        self.data["multimodal"]["eeg_file"] = str(file_path)

    def set_gps_file(self, file_path: Path):
        """Set reference to GPS data file."""
        self.data["multimodal"]["gps_file"] = str(file_path)

    def add_audio_file(self, file_path: Path):
        """Add reference to audio recording."""
        self.data["multimodal"]["audio_files"].append(str(file_path))

    def add_text_note(self, note: str, timestamp: Optional[datetime] = None):
        """
        Add a text note.

        Args:
            note: Text content
            timestamp: Note timestamp (defaults to now)
        """
        if timestamp is None:
            timestamp = datetime.now()

        self.data["multimodal"]["text_notes"].append({
            "timestamp": timestamp.isoformat(),
            "note": note
        })

    def set_description(self, description: str):
        """Set scenario description."""
        self.data["annotations"]["description"] = description

    def add_tag(self, tag: str):
        """Add a tag for categorization."""
        if tag not in self.data["annotations"]["tags"]:
            self.data["annotations"]["tags"].append(tag)

    def set_quality_rating(self, rating: int):
        """
        Set data quality rating.

        Args:
            rating: Quality rating (1-5)
        """
        if 1 <= rating <= 5:
            self.data["annotations"]["quality_rating"] = rating
        else:
            raise ValueError("Quality rating must be between 1 and 5")

    def set_device_info(self, device_type: str, channels: List[str], sampling_rate: int):
        """Set EEG device information."""
        self.data["device_info"] = {
            "eeg_device": device_type,
            "channels": channels,
            "sampling_rate": sampling_rate
        }

    def set_custom_field(self, key: str, value: Any):
        """Add custom metadata field."""
        if "custom" not in self.data:
            self.data["custom"] = {}
        self.data["custom"][key] = value

    def save(self, file_path: Path):
        """
        Save metadata to JSON file.

        Args:
            file_path: Output JSON file path
        """
        # Ensure directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Write JSON with pretty formatting
        with open(file_path, 'w') as f:
            json.dump(self.data, f, indent=2)

        print(f"[ScenarioMetadata] Saved: {file_path}")

    @classmethod
    def load(cls, file_path: Path) -> 'ScenarioMetadata':
        """
        Load metadata from JSON file.

        Args:
            file_path: JSON file path

        Returns:
            ScenarioMetadata instance
        """
        with open(file_path, 'r') as f:
            data = json.load(f)

        # Create instance
        metadata = cls(
            scenario_id=data["scenario_id"],
            scenario_type=data["scenario_type"]
        )
        metadata.data = data

        print(f"[ScenarioMetadata] Loaded: {file_path}")
        return metadata

    def to_dict(self) -> Dict:
        """Return metadata as dictionary."""
        return self.data.copy()

    def __repr__(self):
        return f"ScenarioMetadata(id={self.scenario_id}, type={self.scenario_type})"
