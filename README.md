# OpenGestureXR

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![OpenXR](https://img.shields.io/badge/OpenXR-1.0-green.svg)](https://www.khronos.org/openxr/)

Open-source SDK for AI-powered hand gesture interaction in XR (AR/VR).

The goal is to provide real-time hand tracking and gesture recognition that works across XR platforms (Meta Quest, Pico, HoloLens, ARCore) through a single API built on OpenXR. Right now it's a working prototype with webcam-based tracking — native device support is on the roadmap.

## How it works

```
┌──────────────────────────────────────────────────┐
│  Input: Webcam / Depth Camera / XR Hand Tracking │
└────────────────────┬─────────────────────────────┘
                     ▼
┌──────────────────────────────────────────────────┐
│  MediaPipe Hands → 21-point landmarks (per hand) │
└────────────────────┬─────────────────────────────┘
                     ▼
┌──────────────────────────────────────────────────┐
│  Gesture Classifier (rule-based or ONNX model)   │
│  open_hand, grab, pinch, point, thumbs_up, peace │
└────────────────────┬─────────────────────────────┘
                     ▼
┌──────────────────────────────────────────────────┐
│  FastAPI Server                                   │
│  ws://localhost:8000/ws/gesture  (streaming)      │
│  GET /gesture                    (polling)        │
│  GET /gesture/multi              (multi-hand)     │
└────────────────────┬─────────────────────────────┘
                     ▼
┌──────────────────────────────────────────────────┐
│  Unity Client → Object Interaction               │
│  (OpenXR provider abstraction for portability)    │
└──────────────────────────────────────────────────┘
```

## What's working

- Multi-hand tracking (up to 2 hands)
- WebSocket streaming at ~30fps
- Rule-based classifier for 6 gestures + pluggable ONNX model support
- Training pipeline: collect data → train → export ONNX
- Unity client with gesture smoothing and confidence thresholds
- OpenXR abstraction layer (`HandTrackingProvider` base class)
- Latency benchmarking tool

## Gestures

| Gesture | Action | Notes |
|---------|--------|-------|
| `grab` | Attach object to hand | All fingers curled |
| `open_hand` | Release object | All fingers extended |
| `pinch` | Select object | Thumb + index close together |
| `point` | Highlight object | Only index extended |
| `thumbs_up` | Confirm | Only thumb up |
| `peace` | Reset | Index + middle extended |

## Quick start

```bash
git clone https://github.com/sarry94118-max/ARMAX.git
cd ARMAX
pip install -r requirements.txt

# start the server
uvicorn gesture_api.server.main:app --reload

# test it
curl http://localhost:8000/gesture

# or connect via websocket
wscat -c ws://localhost:8000/ws/gesture
```

## Training your own model

The rule-based classifier works fine for demos, but if you want better accuracy you can train a small neural net:

```bash
# collect ~500 samples per gesture (hold gesture in front of webcam)
mkdir data
python -m ai_engine.training.collect_data --gesture grab --output data/grab.csv
python -m ai_engine.training.collect_data --gesture open_hand --output data/open_hand.csv
# ... etc for each gesture

# train + export
python -m ai_engine.training.train --data-dir data/ --epochs 50

# check latency
python -m ai_engine.utils.benchmark --frames 200
```

## Unity setup

1. Copy `unity_plugin/Scripts/` into your Unity project under `Assets/OpenGestureXR/`
2. Add `GestureClient` to a GameObject, set `useWebSocket = true`
3. Add `ObjectInteractor` to objects you want to interact with
4. Details in [`demo/unity_scene_description.md`](demo/unity_scene_description.md)

**Note:** The Unity "WebSocket" mode currently uses fast HTTP polling under the hood because Unity doesn't have a built-in WS client. For real WebSocket support, drop in [NativeWebSocket](https://github.com/endel/NativeWebSocket). This is on the TODO list.

## Project layout

```
ai_engine/
├── gesture_detector.py        # MediaPipe multi-hand detection
├── gesture_classifier.py      # rule-based + ONNX classification
├── inference/
│   ├── gesture_detector.py    # standalone detection loop
│   └── onnx_runtime.py        # ONNX Runtime wrapper
├── training/
│   ├── collect_data.py        # landmark data collector
│   ├── train.py               # training script
│   └── export_onnx.py         # PyTorch → ONNX export
├── models/                    # model artifacts (gitignored)
└── utils/
    └── benchmark.py           # latency benchmarking
gesture_api/
└── server/main.py             # FastAPI server
unity_plugin/
├── Scripts/
│   ├── GestureClient.cs       # server connection (WS + HTTP)
│   ├── ObjectInteractor.cs    # gesture → action mapping
│   └── XR/
│       └── HandTrackingProvider.cs  # OpenXR abstraction
└── Prefabs/
```

## Roadmap

| Phase | When | What |
|-------|------|------|
| ✅ Foundation | 0–6 mo | Multi-hand, WebSocket, ONNX pipeline, training tools |
| 🔲 Alpha | 6–12 mo | Native OpenXR plugin, Unity package manager support, Quest + Pico testing |
| 🔲 Beta | 12–18 mo | Depth + IMU fusion, Open3D integration, perf optimization |
| 🔲 v1.0 | 18–24 mo | API freeze, full docs, MIT release |
| 🔲 Paper | 24–30 mo | IEEE VR / SIGGRAPH submission, Unreal plugin |

## Built with

[MediaPipe](https://github.com/google/mediapipe) · [PyTorch](https://pytorch.org/) · [ONNX Runtime](https://github.com/microsoft/onnxruntime) · [FastAPI](https://fastapi.tiangolo.com/) · [OpenXR](https://www.khronos.org/openxr/)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Main areas where help is needed:
- Native `HandTrackingProvider` for Quest / Pico / HoloLens
- More gesture training data
- Unreal Engine plugin
- Performance profiling on mobile XR

## License

MIT — see [LICENSE](LICENSE).
