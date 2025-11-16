"""
Simulated EEG Device

Generates realistic fake EEG data for testing without physical hardware.
Simulates multiple frequency bands (delta, theta, alpha, beta, gamma).
"""

import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from collections import deque
import time

from .base import EEGDevice


class SimulatorDevice(EEGDevice):
    """
    Simulated EEG device that generates realistic synthetic data.

    Features:
    - Configurable channels matching Muse 2 (AF7, AF8, TP9, TP10)
    - Multiple frequency bands (delta, theta, alpha, beta, gamma)
    - Realistic noise
    - Precise timing at configured sampling rate
    """

    def __init__(self, config: Dict):
        """
        Initialize the simulator.

        Args:
            config: Configuration dictionary with simulator settings
        """
        super().__init__(config)

        # Load configuration
        sim_config = config.get("simulator", {})
        self._channels = sim_config.get("channels", ["AF7", "AF8", "TP9", "TP10"])
        self._sampling_rate = sim_config.get("sampling_rate", 256)
        self.noise_level = sim_config.get("noise_level", 0.1)

        # Frequency bands (Hz ranges)
        self.freq_bands = sim_config.get("frequency_bands", {
            "delta": [0.5, 4],
            "theta": [4, 8],
            "alpha": [8, 13],
            "beta": [13, 30],
            "gamma": [30, 50]
        })

        # Internal state
        self._time_offset = 0.0
        self._last_sample_time = None
        self._buffer = deque(maxlen=self._sampling_rate * 10)  # 10 second buffer
        self._streaming_thread = None

        print(f"[SimulatorDevice] Initialized with {len(self._channels)} channels @ {self._sampling_rate}Hz")

    def connect(self) -> bool:
        """Simulate connection to device."""
        if self.is_connected:
            print("[SimulatorDevice] Already connected")
            return True

        print("[SimulatorDevice] Connecting to simulator...")
        time.sleep(0.5)  # Simulate connection delay

        self.is_connected = True
        self._time_offset = 0.0
        self._last_sample_time = datetime.now()

        print(f"[SimulatorDevice] Connected successfully")
        print(f"  Channels: {', '.join(self._channels)}")
        print(f"  Sampling rate: {self._sampling_rate} Hz")

        return True

    def disconnect(self) -> bool:
        """Disconnect from simulator."""
        if not self.is_connected:
            print("[SimulatorDevice] Not connected")
            return True

        if self.is_streaming:
            self.stop_streaming()

        print("[SimulatorDevice] Disconnecting...")
        self.is_connected = False
        self._buffer.clear()

        print("[SimulatorDevice] Disconnected")
        return True

    def start_streaming(self) -> bool:
        """Start generating EEG data."""
        if not self.is_connected:
            print("[SimulatorDevice] ERROR: Not connected")
            return False

        if self.is_streaming:
            print("[SimulatorDevice] Already streaming")
            return True

        print("[SimulatorDevice] Starting data stream...")
        self.is_streaming = True
        self._last_sample_time = datetime.now()

        print(f"[SimulatorDevice] Streaming started")
        return True

    def stop_streaming(self) -> bool:
        """Stop generating EEG data."""
        if not self.is_streaming:
            print("[SimulatorDevice] Not streaming")
            return True

        print("[SimulatorDevice] Stopping data stream...")
        self.is_streaming = False

        print("[SimulatorDevice] Streaming stopped")
        return True

    def _generate_sample(self, timestamp: datetime) -> np.ndarray:
        """
        Generate a single realistic EEG sample.

        Args:
            timestamp: Current timestamp for deterministic generation

        Returns:
            Array of shape (n_channels,) with simulated EEG voltages
        """
        # Use timestamp for deterministic but realistic data
        t = self._time_offset
        self._time_offset += 1.0 / self._sampling_rate

        sample = np.zeros(len(self._channels))

        for ch_idx in range(len(self._channels)):
            # Channel-specific phase offset for variety
            phase = ch_idx * np.pi / 4

            # Combine multiple frequency bands
            signal = 0.0

            # Delta (0.5-4 Hz) - deep sleep waves
            signal += 2.0 * np.sin(2 * np.pi * 2.0 * t + phase)

            # Theta (4-8 Hz) - meditation, creativity
            signal += 1.5 * np.sin(2 * np.pi * 6.0 * t + phase * 2)

            # Alpha (8-13 Hz) - relaxed awareness (dominant in simulator)
            signal += 3.0 * np.sin(2 * np.pi * 10.0 * t + phase * 3)

            # Beta (13-30 Hz) - active thinking
            signal += 1.0 * np.sin(2 * np.pi * 20.0 * t + phase * 4)

            # Gamma (30-50 Hz) - high-level cognition
            signal += 0.5 * np.sin(2 * np.pi * 40.0 * t + phase * 5)

            # Add realistic noise
            noise = np.random.normal(0, self.noise_level)

            sample[ch_idx] = signal + noise

        return sample

    def get_sample(self) -> Optional[Tuple[np.ndarray, datetime]]:
        """Get a single EEG sample."""
        if not self.is_streaming:
            return None

        # Generate sample with current timestamp
        timestamp = datetime.now()
        sample = self._generate_sample(timestamp)

        # Add to buffer
        self._buffer.append((sample, timestamp))
        self._last_sample_time = timestamp

        return sample, timestamp

    def get_buffer(self, duration_seconds: float) -> Optional[Tuple[np.ndarray, List[datetime]]]:
        """
        Get a buffer of EEG data.

        Args:
            duration_seconds: Duration of data to retrieve

        Returns:
            Tuple of (data, timestamps) or None if insufficient data
        """
        if not self.is_streaming:
            return None

        n_samples = int(duration_seconds * self._sampling_rate)

        # Generate samples to fill the buffer if needed
        while len(self._buffer) < n_samples:
            self.get_sample()
            # Simulate real-time delay
            time.sleep(1.0 / self._sampling_rate)

        # Extract most recent n_samples
        buffer_list = list(self._buffer)[-n_samples:]

        data = np.array([s[0] for s in buffer_list])
        timestamps = [s[1] for s in buffer_list]

        return data, timestamps

    def set_simulation_mode(self, mode: str):
        """
        Change simulation characteristics (for testing different scenarios).

        Args:
            mode: "rest", "active", "meditation", "stress"
        """
        # Future enhancement: adjust frequency band amplitudes based on mode
        modes = {
            "rest": "Resting state (alpha dominant)",
            "active": "Active thinking (beta dominant)",
            "meditation": "Meditative state (theta dominant)",
            "stress": "Stressed state (beta/gamma dominant)"
        }

        if mode in modes:
            print(f"[SimulatorDevice] Simulation mode: {modes[mode]}")
        else:
            print(f"[SimulatorDevice] Unknown mode: {mode}")
