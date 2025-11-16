#!/usr/bin/env python3
"""
EEG Device Connection Tester

Tests connection to EEG device and displays real-time data samples.
Useful for verifying device setup before running scenarios.
"""

import sys
import time
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from embodied_ai.utils.config import load_config
from embodied_ai.devices import SimulatorDevice
from embodied_ai.devices.muse import Muse2Device


def test_connection(config):
    """
    Test EEG device connection and display sample data.

    Args:
        config: Configuration dictionary
    """
    print("=" * 80)
    print("EEG DEVICE CONNECTION TESTER")
    print("=" * 80)
    print()

    # Get device configuration
    device_type = config["eeg_device"]["type"]
    print(f"Device type: {device_type}")
    print()

    # Create device instance
    if device_type == "simulator":
        device = SimulatorDevice(config["eeg_device"])
    elif device_type == "muse2":
        device = Muse2Device(config["eeg_device"])
    else:
        print(f"ERROR: Unknown device type: {device_type}")
        return False

    # Test connection
    print("[1/4] Testing connection...")
    if not device.connect():
        print("ERROR: Failed to connect to device")
        return False

    print("SUCCESS: Connected to device")
    print()

    # Check device info
    print("[2/4] Device information:")
    print(f"  Channels: {', '.join(device.channels)}")
    print(f"  Sampling rate: {device.sampling_rate} Hz")
    print()

    # Start streaming
    print("[3/4] Starting data stream...")
    if not device.start_streaming():
        print("ERROR: Failed to start streaming")
        device.disconnect()
        return False

    print("SUCCESS: Streaming started")
    print()

    # Display sample data
    print("[4/4] Displaying sample data (10 samples)...")
    print()
    print("Sample | " + " | ".join([f"{ch:>8s}" for ch in device.channels]))
    print("-" * (9 + len(device.channels) * 12))

    for i in range(10):
        sample_data = device.get_sample()
        if sample_data:
            data, timestamp = sample_data
            values_str = " | ".join([f"{val:8.3f}" for val in data])
            print(f"{i+1:6d} | {values_str}")
            time.sleep(0.1)
        else:
            print(f"{i+1:6d} | No data")

    print()

    # Check buffer capability
    print("[BONUS] Testing buffer read (1 second of data)...")
    buffer_data = device.get_buffer(1.0)
    if buffer_data:
        data, timestamps = buffer_data
        print(f"SUCCESS: Retrieved {len(timestamps)} samples")
        print(f"  Expected: ~{device.sampling_rate} samples")
        print(f"  Shape: {data.shape}")
    else:
        print("WARNING: Buffer read returned no data")

    print()

    # Cleanup
    print("Cleaning up...")
    device.stop_streaming()
    device.disconnect()

    print()
    print("=" * 80)
    print("CONNECTION TEST COMPLETE")
    print("=" * 80)
    print()
    print("All systems operational! Ready to run scenarios.")
    print()

    return True


def main():
    """Main entry point."""
    try:
        # Load configuration
        config = load_config("config.yaml")

        # Run connection test
        success = test_connection(config)

        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
