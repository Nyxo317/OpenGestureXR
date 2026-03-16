# Developer Guide

## Prerequisites

- Python 3.10+
- A webcam
- Unity 2022 LTS with XR Interaction Toolkit and OpenXR plugin (for Unity integration)

## Running the Gesture Server

### Install dependencies

```bash
pip install -r requirements.txt
```

### Start the server

```bash
uvicorn gesture_api.server.main:app --reload
```

### Verify endpoints

```bash
# REST (backward compatible)
curl http://localhost:8000/gesture

# Multi-hand REST
curl http://localhost:8000/gesture/multi

# Health check
curl http://localhost:8000/health

# WebSocket (use wscat: npm install -g wscat)
wscat -c ws://localhost:8000/ws/gesture
```

## Training a Custom Model

### Step 1: Collect data

Record samples for each gesture. Hold the gesture in front of your webcam and the collector will save landmark coordinates to CSV.

```bash
mkdir -p data
python -m ai_engine.training.collect_data --gesture grab --output data/grab.csv
python -m ai_engine.training.collect_data --gesture open_hand --output data/open_hand.csv
python -m ai_engine.training.collect_data --gesture pinch --output data/pinch.csv
python -m ai_engine.training.collect_data --gesture point --output data/point.csv
python -m ai_engine.training.collect_data --gesture thumbs_up --output data/thumbs_up.csv
python -m ai_engine.training.collect_data --gesture peace --output data/peace.csv
```

### Step 2: Train and export

```bash
python -m ai_engine.training.train --data-dir data/ --epochs 50
```

This produces `ai_engine/models/gesture_classifier.onnx`.

### Step 3: Benchmark

```bash
python -m ai_engine.utils.benchmark --frames 100
```

## Unity Integration

1. Copy `unity_plugin/Scripts/` into `Assets/OpenGestureXR/Scripts/`
2. Add `GestureClient` to a GameObject:
   - Set `useWebSocket = true` for low-latency streaming
   - Set `host` and `port` to match your server
3. Add `ObjectInteractor` to interactable objects:
   - Set `handAnchor` to your XR hand transform
   - Adjust `confidenceThreshold` (default: 0.7)
4. See [`demo/unity_scene_description.md`](../demo/unity_scene_description.md) for scene setup

## Project Layout

```
ai_engine/
├── gesture_detector.py          # Multi-hand landmark detection
├── gesture_classifier.py        # Rule-based + ONNX classification
├── inference/
│   ├── gesture_detector.py      # Standalone detection loop
│   └── onnx_runtime.py          # ONNX Runtime wrapper
├── training/
│   ├── collect_data.py          # Data collector
│   ├── train.py                 # Training script
│   └── export_onnx.py           # ONNX export
├── models/                      # Model artifacts
└── utils/
    └── benchmark.py             # Latency benchmarking
gesture_api/server/main.py       # FastAPI server
unity_plugin/Scripts/            # Unity C# scripts
```
