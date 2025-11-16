# Embodied AI EEG Foundation

A modular, privacy-first system for collecting EEG data during real-world scenarios. Designed for grounded, embodied AI learning where Claude learns from your actual experiences in the physical world.

## 🧠 Project Vision

This system enables you to:
- Collect EEG brain activity data during real-world scenarios
- Combine multimodal data (EEG + GPS + audio notes + timestamps)
- Build a grounded dataset of embodied experiences
- Eventually train AI models on situated, real-world cognitive data

**Privacy First**: All data stays local on your machine. Nothing is uploaded without your explicit control.

## 📋 Phase 1 Status (Current)

✅ **IMPLEMENTED:**
- Abstract EEG device interface
- Simulated EEG data generator (for testing before Muse 2 arrives)
- HDF5 data logger with compression
- JSON metadata management
- Scenario execution framework
- CLI tools for testing and data collection
- Configuration system (YAML)
- Cross-platform Python architecture

⏳ **PLANNED (Next Phases):**
- Real Muse 2 device integration (when hardware arrives)
- GPS track parsing and synchronization
- Audio note integration
- Data visualization tools
- Web interface for mobile access
- Claude AI analysis integration

## 🏗️ Architecture

```
embodied_ai/
├── devices/           # EEG device interfaces
│   ├── base.py       # Abstract EEGDevice class
│   ├── simulator.py  # Fake data generator (for testing)
│   └── muse.py       # Muse 2 integration (stub)
│
├── data/             # Data logging
│   ├── logger.py     # HDF5 EEG logger
│   └── metadata.py   # JSON metadata manager
│
├── scenarios/        # Scenario framework
│   ├── base.py       # Scenario base class
│   └── runner.py     # Scenario execution engine
│
└── utils/            # Utilities
    ├── config.py     # YAML config loader
    └── sync.py       # Timestamp synchronization

data/                 # Data storage (gitignored)
├── raw/             # EEG data (HDF5)
├── scenarios/       # Scenario metadata (JSON)
├── gps/             # GPS tracks (GPX)
├── audio/           # Voice recordings
└── logs/            # System logs

scripts/             # CLI tools
├── test_connection.py  # Device tester
├── run_scenario.py     # Scenario runner
└── view_data.py        # Data viewer
```

### Design Patterns

**Abstract Device Interface**: Easy to swap between simulator and real Muse 2 when it arrives.

**Modular Data Storage**:
- EEG data → HDF5 (efficient, compressed, industry standard)
- Metadata → JSON (human-readable, easy to edit)
- Config → YAML (user-friendly)

**Scenario Framework**: Extensible base class for custom scenarios.

## 🚀 Quick Start

### 1. Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Verify installation
python scripts/test_connection.py
```

### 2. Test EEG Connection

```bash
# Test with simulator (no hardware needed)
python scripts/test_connection.py
```

This verifies:
- Device connection
- Data streaming
- Sample data quality

### 3. Run Your First Scenario

```bash
# List available scenarios
python scripts/run_scenario.py --list

# Run baseline resting state (5 minutes)
python scripts/run_scenario.py baseline_rest

# Run with custom duration (300 seconds)
python scripts/run_scenario.py meditation --duration 300

# Run until manually stopped (Ctrl+C)
python scripts/run_scenario.py focused_task --manual
```

### 4. View Recorded Data

```bash
# List all recordings
python scripts/view_data.py --list

# View specific recording
python scripts/view_data.py data/scenarios/baseline_rest_20250116_120000.json
python scripts/view_data.py data/raw/baseline_rest_20250116_120000.h5
```

## 📖 Predefined Scenarios

### baseline_rest (5 min)
Resting state baseline. Sit quietly with eyes closed. Establishes your baseline brain activity.

### focused_task (10 min)
Work on a challenging cognitive task. Measures focused attention and problem-solving states.

### meditation (10 min)
Meditation session. Measures calm, mindful awareness states.

### physical_activity (15 min)
Light exercise or walking. Measures brain activity during movement.

### creative_work (15 min)
Creative activities (writing, drawing, brainstorming). Measures creative cognitive states.

## 🔧 Configuration

Edit `config.yaml` to customize:

```yaml
# Switch between simulator and real device
eeg_device:
  type: "simulator"  # or "muse2" when device arrives

# Adjust data storage
data_storage:
  base_path: "./data"
  compression: "gzip"
  compression_level: 4

# Scenario settings
scenarios:
  default_duration: 300  # seconds
  preparation_time: 10
  require_notes: true
```

## 📊 Data Format

### EEG Data (HDF5)

```python
# Structure
/eeg_data       # (n_samples, n_channels) float32 array
/timestamps     # (n_samples,) Unix timestamps
/attributes     # Metadata (channels, sampling_rate, etc.)

# Example
import h5py
with h5py.File('data/raw/scenario.h5', 'r') as f:
    eeg = f['eeg_data'][:]      # Shape: (76800, 4) for 5min @ 256Hz
    times = f['timestamps'][:]
    channels = f.attrs['channels']  # ["AF7", "AF8", "TP9", "TP10"]
```

### Metadata (JSON)

```json
{
  "scenario_id": "baseline_rest_20250116_120000",
  "scenario_type": "baseline_rest",
  "timestamps": {
    "start": "2025-01-16T12:00:00",
    "end": "2025-01-16T12:05:00",
    "duration_seconds": 300
  },
  "multimodal": {
    "eeg_file": "data/raw/baseline_rest_20250116_120000.h5",
    "gps_file": null,
    "audio_files": [],
    "text_notes": [
      {
        "timestamp": "2025-01-16T12:05:00",
        "note": "Felt very relaxed, minimal mind wandering"
      }
    ]
  },
  "annotations": {
    "description": "Morning baseline measurement",
    "tags": ["baseline", "morning"],
    "quality_rating": 5
  },
  "device_info": {
    "eeg_device": "simulator",
    "channels": ["AF7", "AF8", "TP9", "TP10"],
    "sampling_rate": 256
  }
}
```

## 🎯 Creating Custom Scenarios

See `scenarios/examples/custom_scenario_template.py` for a template.

```python
from embodied_ai.scenarios.base import Scenario

class MyScenario(Scenario):
    def get_instructions(self):
        return "Your custom instructions..."

    def on_start(self):
        super().on_start()
        # Custom initialization

    def on_stop(self):
        # Custom cleanup
        super().on_stop()
```

## 🔌 Device Integration

### Current: Simulator

The simulator generates realistic multi-frequency EEG data for testing:
- 4 channels (AF7, AF8, TP9, TP10)
- 256 Hz sampling rate
- Multiple frequency bands (delta, theta, alpha, beta, gamma)
- Realistic noise

### Coming Soon: Muse 2

When your Muse 2 arrives:

1. Install muselsl: `pip install muselsl`
2. Update `config.yaml`:
   ```yaml
   eeg_device:
     type: "muse2"
     muse2:
       bluetooth_name: "Muse-XXXX"  # Your device name
   ```
3. The abstract interface ensures seamless switching!

## 📱 Mobile Workflow (Laptop + Phone)

### Current Setup:
1. **Laptop**: Runs main Python system, records EEG
2. **Phone**: Records GPS track using any GPX app

### Typical Outdoor Scenario:
1. Start scenario on laptop
2. Start GPS recording on phone
3. Execute scenario (walk, exercise, explore)
4. Stop both recordings
5. Transfer GPX file to laptop
6. System synchronizes timestamps

### Future: Web Interface
Simple web UI accessible from phone browser for:
- Viewing current scenario instructions
- Adding voice/text notes during execution
- Checking recording status

## 🔐 Privacy & Security

- **Local-only**: All data stored on your machine
- **No cloud**: No automatic uploads
- **No telemetry**: System doesn't "phone home"
- **Your control**: You decide what to share, when, and with whom

Optional privacy features (in config):
- GPS coordinate anonymization (round to lower precision)
- Data encryption (future)

## 🐛 Troubleshooting

### "No module named 'embodied_ai'"
Add project root to Python path or install in development mode:
```bash
pip install -e .
```

### Simulator connection fails
Check `config.yaml` device type is set to "simulator"

### Import errors
Ensure all dependencies installed:
```bash
pip install -r requirements.txt
```

### Windows-specific issues
- Use forward slashes in paths: `data/raw` not `data\raw`
- Run scripts with `python` not `python3`

## 🗺️ Roadmap

### Phase 1 (Current) ✅
- [x] Project structure
- [x] Simulator device
- [x] Data logging (HDF5 + JSON)
- [x] Scenario framework
- [x] CLI tools

### Phase 2 (After Muse 2 Arrives)
- [ ] Muse 2 integration
- [ ] Real-time data quality checks
- [ ] Signal quality indicators

### Phase 3 (Multimodal Integration)
- [ ] GPS track parsing and visualization
- [ ] Audio note integration
- [ ] Whisper speech-to-text
- [ ] Data synchronization tools

### Phase 4 (Analysis)
- [ ] Data visualization dashboard
- [ ] Frequency band analysis
- [ ] Event-triggered averaging
- [ ] Statistical summaries

### Phase 5 (Claude Integration)
- [ ] Export data for Claude analysis
- [ ] Context-aware prompts
- [ ] Pattern recognition
- [ ] Cognitive state classification

### Phase 6 (Mobile Enhancement)
- [ ] Flask web interface
- [ ] Phone-accessible scenario instructions
- [ ] Real-time status monitoring
- [ ] Remote control capabilities

## 🤝 Contributing

This is a personal research project, but contributions welcome:
1. Fork the repository
2. Create a feature branch
3. Add your enhancement
4. Submit a pull request

## 📄 License

[Choose your license - MIT, Apache 2.0, GPL, etc.]

## 🙏 Acknowledgments

- **Muse 2**: InteraXon for EEG hardware
- **muselsl**: Lab Streaming Layer integration
- **HDF5**: Hierarchical Data Format
- **Claude**: Anthropic AI for analysis tools

## 📧 Contact

[Your contact information or discussion forum]

---

**Status**: Phase 1 Complete ✅
**Next**: Awaiting Muse 2 hardware (1-2 weeks)
**Started**: January 2025
