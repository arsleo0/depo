"""
Abstract EEG Device Interface

Defines the contract that all EEG device implementations must follow.
This allows easy swapping between simulator, Muse 2, or other devices.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple
import numpy as np
from datetime import datetime


class EEGDevice(ABC):
    """
    Abstract base class for all EEG devices.

    All device implementations must provide:
    - Connection management (connect, disconnect)
    - Real-time data streaming
    - Channel information
    - Device status
    """

    def __init__(self, config: Dict):
        """
        Initialize the EEG device.

        Args:
            config: Device-specific configuration dictionary
        """
        self.config = config
        self.is_connected = False
        self.is_streaming = False
        self._channels = []
        self._sampling_rate = 256  # Default

    @abstractmethod
    def connect(self) -> bool:
        """
        Establish connection to the EEG device.

        Returns:
            True if connection successful, False otherwise
        """
        pass

    @abstractmethod
    def disconnect(self) -> bool:
        """
        Disconnect from the EEG device.

        Returns:
            True if disconnection successful, False otherwise
        """
        pass

    @abstractmethod
    def start_streaming(self) -> bool:
        """
        Start streaming EEG data.

        Returns:
            True if streaming started successfully, False otherwise
        """
        pass

    @abstractmethod
    def stop_streaming(self) -> bool:
        """
        Stop streaming EEG data.

        Returns:
            True if streaming stopped successfully, False otherwise
        """
        pass

    @abstractmethod
    def get_sample(self) -> Optional[Tuple[np.ndarray, datetime]]:
        """
        Get a single sample of EEG data.

        Returns:
            Tuple of (data, timestamp) where:
                - data: numpy array of shape (n_channels,)
                - timestamp: datetime object
            Returns None if no data available
        """
        pass

    @abstractmethod
    def get_buffer(self, duration_seconds: float) -> Optional[Tuple[np.ndarray, List[datetime]]]:
        """
        Get a buffer of EEG data for the specified duration.

        Args:
            duration_seconds: Duration of data to retrieve

        Returns:
            Tuple of (data, timestamps) where:
                - data: numpy array of shape (n_samples, n_channels)
                - timestamps: list of datetime objects
            Returns None if insufficient data available
        """
        pass

    @property
    def channels(self) -> List[str]:
        """Get list of channel names."""
        return self._channels

    @property
    def sampling_rate(self) -> int:
        """Get sampling rate in Hz."""
        return self._sampling_rate

    @property
    def status(self) -> Dict:
        """
        Get device status information.

        Returns:
            Dictionary with status information
        """
        return {
            "connected": self.is_connected,
            "streaming": self.is_streaming,
            "channels": self._channels,
            "sampling_rate": self._sampling_rate
        }

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        if self.is_streaming:
            self.stop_streaming()
        if self.is_connected:
            self.disconnect()
        return False
