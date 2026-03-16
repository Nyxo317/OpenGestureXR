# Contributing

Contributions welcome! Here's how to get going.

## Setup

```bash
git clone https://github.com/sarry94118-max/ARMAX.git
cd ARMAX
pip install -r requirements.txt
```

## Adding a new gesture

1. Record training data:
   ```bash
   python -m ai_engine.training.collect_data --gesture your_gesture --output data/your_gesture.csv
   ```
2. Add the gesture name to `GESTURES` in `ai_engine/gesture_classifier.py`
3. Retrain: `python -m ai_engine.training.train --data-dir data/`
4. Open a PR with the CSV data and updated model

## Adding a hand tracking provider

If you have access to a Quest, Pico, or HoloLens, we'd love a native provider. Subclass `HandTrackingProvider` in `unity_plugin/Scripts/XR/`:

```csharp
public class QuestHandProvider : HandTrackingProvider
{
    public override bool IsTracking => ...;
    public override Vector3[] GetJointPositions(Handedness hand) => ...;
    public override Quaternion[] GetJointRotations(Handedness hand) => ...;
}
```

## Code style

- Python: PEP 8, type hints where they help readability
- C#: standard Unity conventions
- Don't over-document obvious things

## PRs

1. Fork + feature branch
2. Run the benchmark before and after to check for regressions
3. Keep commits focused — one logical change per commit
4. Describe what you changed and why in the PR description

## Help wanted

- [ ] Meta Quest native hand tracking provider
- [ ] Pico hand tracking provider
- [ ] Real WebSocket support in Unity client (NativeWebSocket integration)
- [ ] Depth camera (RealSense) input
- [ ] Unreal Engine plugin
- [ ] More training data for existing gestures
- [ ] CI pipeline (GitHub Actions)
