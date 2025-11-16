"""
Configuration Management

Loads and validates YAML configuration files.
"""

import yaml
from pathlib import Path
from typing import Dict, Any


def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    """
    Load configuration from YAML file.

    Args:
        config_path: Path to config.yaml file

    Returns:
        Configuration dictionary

    Raises:
        FileNotFoundError: If config file doesn't exist
        yaml.YAMLError: If config file is invalid
    """
    config_file = Path(config_path)

    if not config_file.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)

    # Validate required sections
    required_sections = ["eeg_device", "data_storage", "scenarios"]
    for section in required_sections:
        if section not in config:
            raise ValueError(f"Missing required config section: {section}")

    print(f"[Config] Loaded configuration from {config_path}")
    return config


def get_device_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract device-specific configuration.

    Args:
        config: Main configuration dictionary

    Returns:
        Device configuration based on selected type
    """
    eeg_config = config["eeg_device"]
    device_type = eeg_config.get("type", "simulator")

    # Return the appropriate device config
    if device_type in eeg_config:
        return {
            "type": device_type,
            device_type: eeg_config[device_type]
        }
    else:
        raise ValueError(f"Unknown device type: {device_type}")


def get_data_paths(config: Dict[str, Any]) -> Dict[str, Path]:
    """
    Get data storage paths from configuration.

    Args:
        config: Main configuration dictionary

    Returns:
        Dictionary of Path objects for each data type
    """
    storage_config = config["data_storage"]
    base_path = Path(storage_config["base_path"])

    paths = {}
    for name, subdir in storage_config["paths"].items():
        paths[name] = base_path / subdir

    return paths


def ensure_data_directories(config: Dict[str, Any]) -> None:
    """
    Create data directories if they don't exist.

    Args:
        config: Main configuration dictionary
    """
    paths = get_data_paths(config)

    for name, path in paths.items():
        path.mkdir(parents=True, exist_ok=True)
        print(f"[Config] Data directory ready: {path}")
