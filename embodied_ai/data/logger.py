"""
EEG Data Logger

Efficiently logs EEG data to HDF5 files with compression.
Handles real-time streaming data with buffering.
"""

import h5py
import numpy as np
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict
import json


class EEGLogger:
    """
    Logs EEG data to HDF5 format with metadata.

    File structure:
    - /eeg_data: (n_samples, n_channels) array of EEG voltages
    - /timestamps: (n_samples,) array of Unix timestamps
    - /channels: Channel names
    - /metadata: JSON-encoded metadata
    """

    def __init__(
        self,
        file_path: Path,
        channels: List[str],
        sampling_rate: int,
        metadata: Optional[Dict] = None,
        compression: str = "gzip",
        compression_level: int = 4
    ):
        """
        Initialize EEG logger.

        Args:
            file_path: Output HDF5 file path
            channels: List of channel names
            sampling_rate: Sampling rate in Hz
            metadata: Optional metadata dictionary
            compression: HDF5 compression type
            compression_level: Compression level (0-9)
        """
        self.file_path = Path(file_path)
        self.channels = channels
        self.sampling_rate = sampling_rate
        self.metadata = metadata or {}
        self.compression = compression
        self.compression_level = compression_level

        self.h5file = None
        self.eeg_dataset = None
        self.timestamps_dataset = None
        self.sample_count = 0

        # Buffering for efficient writes
        self.buffer_size = sampling_rate * 10  # 10 seconds
        self.eeg_buffer = []
        self.timestamp_buffer = []

    def open(self):
        """Open HDF5 file for writing."""
        if self.h5file is not None:
            print("[EEGLogger] WARNING: File already open")
            return

        # Ensure parent directory exists
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        # Create HDF5 file
        self.h5file = h5py.File(self.file_path, 'w')

        # Create datasets (initially small, will resize as needed)
        self.eeg_dataset = self.h5file.create_dataset(
            'eeg_data',
            shape=(0, len(self.channels)),
            maxshape=(None, len(self.channels)),
            dtype='float32',
            compression=self.compression,
            compression_opts=self.compression_level,
            chunks=(self.buffer_size, len(self.channels))
        )

        self.timestamps_dataset = self.h5file.create_dataset(
            'timestamps',
            shape=(0,),
            maxshape=(None,),
            dtype='float64',
            compression=self.compression,
            compression_opts=self.compression_level,
            chunks=(self.buffer_size,)
        )

        # Store metadata as attributes
        self.h5file.attrs['channels'] = json.dumps(self.channels)
        self.h5file.attrs['sampling_rate'] = self.sampling_rate
        self.h5file.attrs['n_channels'] = len(self.channels)
        self.h5file.attrs['created_at'] = datetime.now().isoformat()

        # Store custom metadata
        if self.metadata:
            self.h5file.attrs['metadata'] = json.dumps(self.metadata)

        print(f"[EEGLogger] Opened file: {self.file_path}")
        print(f"  Channels: {', '.join(self.channels)}")
        print(f"  Sampling rate: {self.sampling_rate} Hz")

    def write_sample(self, data: np.ndarray, timestamp: datetime):
        """
        Write a single EEG sample.

        Args:
            data: EEG data array of shape (n_channels,)
            timestamp: Sample timestamp
        """
        if self.h5file is None:
            raise RuntimeError("Logger not opened. Call open() first.")

        # Add to buffer
        self.eeg_buffer.append(data)
        self.timestamp_buffer.append(timestamp.timestamp())

        # Flush buffer if full
        if len(self.eeg_buffer) >= self.buffer_size:
            self._flush_buffer()

    def write_buffer(self, data: np.ndarray, timestamps: List[datetime]):
        """
        Write multiple EEG samples at once.

        Args:
            data: EEG data array of shape (n_samples, n_channels)
            timestamps: List of timestamps
        """
        if self.h5file is None:
            raise RuntimeError("Logger not opened. Call open() first.")

        n_samples = len(timestamps)

        # Resize datasets
        current_size = self.eeg_dataset.shape[0]
        new_size = current_size + n_samples

        self.eeg_dataset.resize(new_size, axis=0)
        self.timestamps_dataset.resize(new_size, axis=0)

        # Write data
        self.eeg_dataset[current_size:new_size] = data
        self.timestamps_dataset[current_size:new_size] = [t.timestamp() for t in timestamps]

        self.sample_count += n_samples

        print(f"[EEGLogger] Wrote {n_samples} samples (total: {self.sample_count})")

    def _flush_buffer(self):
        """Flush buffered samples to disk."""
        if not self.eeg_buffer:
            return

        # Convert buffer to arrays
        eeg_array = np.array(self.eeg_buffer, dtype='float32')
        timestamp_array = np.array(self.timestamp_buffer, dtype='float64')

        # Resize datasets
        current_size = self.eeg_dataset.shape[0]
        new_size = current_size + len(self.eeg_buffer)

        self.eeg_dataset.resize(new_size, axis=0)
        self.timestamps_dataset.resize(new_size, axis=0)

        # Write data
        self.eeg_dataset[current_size:new_size] = eeg_array
        self.timestamps_dataset[current_size:new_size] = timestamp_array

        self.sample_count += len(self.eeg_buffer)

        # Clear buffers
        self.eeg_buffer.clear()
        self.timestamp_buffer.clear()

    def close(self):
        """Close HDF5 file and flush any remaining data."""
        if self.h5file is None:
            return

        # Flush remaining buffer
        self._flush_buffer()

        # Update final metadata
        self.h5file.attrs['n_samples'] = self.sample_count
        self.h5file.attrs['duration_seconds'] = self.sample_count / self.sampling_rate
        self.h5file.attrs['closed_at'] = datetime.now().isoformat()

        # Close file
        self.h5file.close()
        self.h5file = None

        print(f"[EEGLogger] Closed file: {self.file_path}")
        print(f"  Total samples: {self.sample_count}")
        print(f"  Duration: {self.sample_count / self.sampling_rate:.1f} seconds")

    def __enter__(self):
        """Context manager entry."""
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
        return False


def load_eeg_data(file_path: Path) -> Dict:
    """
    Load EEG data from HDF5 file.

    Args:
        file_path: Path to HDF5 file

    Returns:
        Dictionary with EEG data and metadata
    """
    with h5py.File(file_path, 'r') as f:
        data = {
            'eeg_data': f['eeg_data'][:],
            'timestamps': f['timestamps'][:],
            'channels': json.loads(f.attrs['channels']),
            'sampling_rate': f.attrs['sampling_rate'],
            'n_samples': f.attrs.get('n_samples', len(f['timestamps'])),
            'duration': f.attrs.get('duration_seconds', 0)
        }

        # Load metadata if available
        if 'metadata' in f.attrs:
            data['metadata'] = json.loads(f.attrs['metadata'])

    return data
