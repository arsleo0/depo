"""
Embodied AI EEG Foundation

A modular system for collecting and analyzing EEG data during real-world scenarios.
Designed for privacy-first, multimodal data collection with mobile execution.
"""

__version__ = "0.1.0"
__author__ = "Embodied AI Research"

from .utils.config import load_config

__all__ = ["load_config"]
