#!/usr/bin/env python3
"""
EEG Data Viewer

Simple CLI tool to view recorded EEG data and metadata.
"""

import sys
import json
from pathlib import Path
import argparse

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from embodied_ai.data.logger import load_eeg_data
from embodied_ai.data.metadata import ScenarioMetadata


def view_eeg_file(file_path: Path):
    """
    Display EEG data file information.

    Args:
        file_path: Path to HDF5 file
    """
    print("=" * 80)
    print("EEG DATA FILE")
    print("=" * 80)
    print(f"File: {file_path}")
    print()

    try:
        data = load_eeg_data(file_path)

        print("RECORDING INFO:")
        print(f"  Channels: {', '.join(data['channels'])}")
        print(f"  Sampling rate: {data['sampling_rate']} Hz")
        print(f"  Number of samples: {data['n_samples']:,}")
        print(f"  Duration: {data['duration']:.1f} seconds ({data['duration']/60:.1f} minutes)")
        print()

        print("DATA SHAPE:")
        print(f"  EEG data: {data['eeg_data'].shape}")
        print(f"  Timestamps: {data['timestamps'].shape}")
        print()

        print("SAMPLE STATISTICS (first 1000 samples):")
        sample_data = data['eeg_data'][:1000]
        for i, channel in enumerate(data['channels']):
            channel_data = sample_data[:, i]
            print(f"  {channel}:")
            print(f"    Mean: {channel_data.mean():.3f}")
            print(f"    Std:  {channel_data.std():.3f}")
            print(f"    Min:  {channel_data.min():.3f}")
            print(f"    Max:  {channel_data.max():.3f}")

        print()

        if 'metadata' in data:
            print("EMBEDDED METADATA:")
            print(json.dumps(data['metadata'], indent=2))
            print()

    except Exception as e:
        print(f"ERROR reading file: {e}")


def view_metadata_file(file_path: Path):
    """
    Display metadata file information.

    Args:
        file_path: Path to JSON metadata file
    """
    print("=" * 80)
    print("SCENARIO METADATA")
    print("=" * 80)
    print(f"File: {file_path}")
    print()

    try:
        metadata = ScenarioMetadata.load(file_path)
        data = metadata.to_dict()

        print("SCENARIO INFO:")
        print(f"  ID: {data['scenario_id']}")
        print(f"  Type: {data['scenario_type']}")
        print(f"  Created: {data['created_at']}")
        print()

        print("TIMESTAMPS:")
        print(f"  Start: {data['timestamps']['start']}")
        print(f"  End: {data['timestamps']['end']}")
        if data['timestamps']['duration_seconds']:
            duration = data['timestamps']['duration_seconds']
            print(f"  Duration: {duration:.1f}s ({duration/60:.1f} min)")
        print()

        if data['timestamps']['events']:
            print("EVENTS:")
            for event in data['timestamps']['events']:
                print(f"  [{event['timestamp']}] {event['name']}")
            print()

        print("MULTIMODAL DATA:")
        print(f"  EEG file: {data['multimodal']['eeg_file']}")
        print(f"  GPS file: {data['multimodal']['gps_file']}")
        print(f"  Audio files: {len(data['multimodal']['audio_files'])}")
        print(f"  Text notes: {len(data['multimodal']['text_notes'])}")
        print()

        if data['multimodal']['text_notes']:
            print("TEXT NOTES:")
            for note in data['multimodal']['text_notes']:
                print(f"  [{note['timestamp']}]")
                print(f"    {note['note']}")
            print()

        print("ANNOTATIONS:")
        if data['annotations']['description']:
            print(f"  Description: {data['annotations']['description']}")
        if data['annotations']['tags']:
            print(f"  Tags: {', '.join(data['annotations']['tags'])}")
        if data['annotations']['quality_rating']:
            print(f"  Quality: {data['annotations']['quality_rating']}/5")
        if data['annotations']['notes']:
            print(f"  Notes: {data['annotations']['notes']}")
        print()

        print("DEVICE INFO:")
        print(f"  Device: {data['device_info']['eeg_device']}")
        print(f"  Channels: {', '.join(data['device_info']['channels'])}")
        print(f"  Sampling rate: {data['device_info']['sampling_rate']} Hz")
        print()

    except Exception as e:
        print(f"ERROR reading file: {e}")


def list_recordings(data_path: Path):
    """
    List all recordings in the data directory.

    Args:
        data_path: Base data path
    """
    print("=" * 80)
    print("RECORDED SCENARIOS")
    print("=" * 80)
    print()

    # Find all metadata files
    scenarios_path = data_path / "scenarios"
    if not scenarios_path.exists():
        print(f"No scenarios directory found at {scenarios_path}")
        return

    metadata_files = sorted(scenarios_path.glob("*.json"))

    if not metadata_files:
        print("No recordings found")
        return

    print(f"Found {len(metadata_files)} recording(s):\n")

    for i, meta_file in enumerate(metadata_files, 1):
        try:
            with open(meta_file, 'r') as f:
                data = json.load(f)

            scenario_type = data.get('scenario_type', 'unknown')
            created_at = data.get('created_at', 'unknown')
            duration = data.get('timestamps', {}).get('duration_seconds')
            duration_str = f"{duration:.1f}s" if duration else "unknown"

            print(f"{i}. {meta_file.stem}")
            print(f"   Type: {scenario_type}")
            print(f"   Date: {created_at}")
            print(f"   Duration: {duration_str}")
            print()

        except Exception as e:
            print(f"{i}. {meta_file.stem} (ERROR: {e})")
            print()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="View EEG data and metadata files"
    )

    parser.add_argument(
        "file",
        nargs="?",
        help="HDF5 or JSON file to view"
    )

    parser.add_argument(
        "--list",
        action="store_true",
        help="List all recordings"
    )

    parser.add_argument(
        "--data-path",
        default="./data",
        help="Base data path (default: ./data)"
    )

    args = parser.parse_args()

    try:
        if args.list:
            list_recordings(Path(args.data_path))
        elif args.file:
            file_path = Path(args.file)
            if not file_path.exists():
                print(f"ERROR: File not found: {file_path}")
                sys.exit(1)

            if file_path.suffix == '.h5':
                view_eeg_file(file_path)
            elif file_path.suffix == '.json':
                view_metadata_file(file_path)
            else:
                print(f"ERROR: Unknown file type: {file_path.suffix}")
                print("Supported: .h5 (EEG data), .json (metadata)")
                sys.exit(1)
        else:
            parser.error("Provide a file path or use --list")

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
