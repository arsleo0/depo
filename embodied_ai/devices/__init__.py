"""
EEG Device Interfaces

Abstract base class and implementations for various EEG devices.
"""

from .base import EEGDevice
from .simulator import SimulatorDevice

__all__ = ["EEGDevice", "SimulatorDevice"]
