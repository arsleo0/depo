"""
Timestamp Synchronization Utilities

Handles synchronization between different data sources:
- EEG timestamps
- GPS timestamps
- Audio timestamps
- Manual event markers
"""

from datetime import datetime, timedelta
from typing import List, Tuple, Optional
import numpy as np


class TimestampSync:
    """
    Synchronize timestamps across multiple data sources.

    Features:
    - Align EEG and GPS data by timestamp
    - Handle timezone conversions
    - Interpolate missing data points
    """

    def __init__(self, reference_time: Optional[datetime] = None):
        """
        Initialize timestamp synchronizer.

        Args:
            reference_time: Reference timestamp (usually scenario start time)
        """
        self.reference_time = reference_time or datetime.now()

    def align_timestamps(
        self,
        eeg_timestamps: List[datetime],
        gps_timestamps: List[datetime],
        tolerance_ms: float = 100
    ) -> List[Tuple[int, int]]:
        """
        Find matching timestamp pairs between EEG and GPS data.

        Args:
            eeg_timestamps: List of EEG sample timestamps
            gps_timestamps: List of GPS point timestamps
            tolerance_ms: Maximum time difference to consider a match (milliseconds)

        Returns:
            List of (eeg_idx, gps_idx) pairs
        """
        matches = []
        tolerance = timedelta(milliseconds=tolerance_ms)

        for eeg_idx, eeg_time in enumerate(eeg_timestamps):
            for gps_idx, gps_time in enumerate(gps_timestamps):
                if abs(eeg_time - gps_time) < tolerance:
                    matches.append((eeg_idx, gps_idx))
                    break

        return matches

    def interpolate_gps(
        self,
        gps_timestamps: List[datetime],
        gps_coords: List[Tuple[float, float]],
        target_timestamps: List[datetime]
    ) -> List[Optional[Tuple[float, float]]]:
        """
        Interpolate GPS coordinates to match EEG sampling times.

        Args:
            gps_timestamps: Original GPS timestamps
            gps_coords: GPS coordinates (lat, lon) pairs
            target_timestamps: Desired timestamps (e.g., EEG sample times)

        Returns:
            Interpolated GPS coordinates for each target timestamp
        """
        if not gps_timestamps or not gps_coords:
            return [None] * len(target_timestamps)

        # Convert timestamps to seconds since reference
        ref_time = min(gps_timestamps + target_timestamps)

        gps_times_sec = np.array([
            (t - ref_time).total_seconds() for t in gps_timestamps
        ])
        target_times_sec = np.array([
            (t - ref_time).total_seconds() for t in target_timestamps
        ])

        # Interpolate latitude and longitude separately
        lats = np.array([coord[0] for coord in gps_coords])
        lons = np.array([coord[1] for coord in gps_coords])

        interp_lats = np.interp(target_times_sec, gps_times_sec, lats)
        interp_lons = np.interp(target_times_sec, gps_times_sec, lons)

        return list(zip(interp_lats, interp_lons))

    def get_relative_time(self, timestamp: datetime) -> float:
        """
        Get time in seconds relative to reference time.

        Args:
            timestamp: Absolute timestamp

        Returns:
            Seconds since reference time
        """
        return (timestamp - self.reference_time).total_seconds()

    def format_timestamp(self, timestamp: datetime, format_str: str) -> str:
        """
        Format timestamp according to configuration.

        Args:
            timestamp: Datetime to format
            format_str: strftime format string

        Returns:
            Formatted timestamp string
        """
        return timestamp.strftime(format_str)
