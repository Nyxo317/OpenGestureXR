# Architecture

## System Diagram

```
┌─────────────────────────────────────────────────────┐
│                    Input Layer                       │
│  Webcam / Depth Camera / XR Device Hand Tracking    │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────┐
│               AI Detection Engine                    │
│  MediaPipe Hands → 21-point landmark extraction      │
│  Multi-hand tracking (up to 2 hands)                 │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────┐
│             Gesture Classification                   │
│  Rule-based (default) ←→ ONNX Neural Network        │
│  Pluggable: swap classifier without changing API     │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────┐
│              Streaming Server (FastAPI)               │
│  WebSocket /ws/gesture — 30fps push                  │
│  REST GET /gesture — backward-compatible polling     │
│  REST GET /gesture/multi — multi-hand data           │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────┐
│            XR Client (Unity / Unreal)                │
│  HandTrackingProvider — abstract OpenXR interface    │
│  GestureClient — WebSocket or HTTP transport         │
│  ObjectInteractor — gesture → action mapping         │
└─────────────────────────────────────────────────────┘
```

## Modules

### `ai_engine/gesture_detector.py`
Multi-hand landmark detection via MediaPipe. Returns `HandResult` dataclass with 21 normalized coordinates and handedness. Configurable via `create_detector()`.

### `ai_engine/gesture_classifier.py`
Dual-mode classifier: rule-based geometry (default) or ONNX neural network. Supports 6 gestures. Call `load_onnx_model()` to switch to learned classification.

### `ai_engine/inference/onnx_runtime.py`
ONNX Runtime wrapper with optional TensorRT acceleration for GPU inference.

### `ai_engine/training/`
End-to-end training pipeline:
- `collect_data.py` — webcam-based landmark data collection
- `train.py` — PyTorch training loop
- `export_onnx.py` — model export to ONNX format

### `gesture_api/server/main.py`
FastAPI server with WebSocket streaming at ~30fps and REST fallback endpoints. Runs detection in a background thread.

### `unity_plugin/Scripts/GestureClient.cs`
Configurable client supporting WebSocket (primary) and HTTP polling (fallback). Broadcasts gesture events to all listeners.

### `unity_plugin/Scripts/ObjectInteractor.cs`
Maps gestures to object interactions with confidence thresholding and temporal smoothing to reduce false positives.

### `unity_plugin/Scripts/XR/HandTrackingProvider.cs`
Abstract base class for hand tracking providers. Implement per-platform (Quest, Pico, HoloLens) to enable native OpenXR hand tracking.

## Data Flow

1. Camera frame captured (webcam or XR device)
2. MediaPipe extracts 21 hand landmarks per hand
3. Classifier produces gesture label + confidence
4. Server pushes result via WebSocket (or serves via REST)
5. Unity client receives, applies smoothing, fires events
6. ObjectInteractor maps gesture to scene action
