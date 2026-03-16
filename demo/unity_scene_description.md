# Unity Demo Scene

## Scene Objects

| Object    | Type     | Position        |
|-----------|----------|-----------------|
| XR Camera | XR Rig   | (0, 1.6, 0)     |
| Cube      | Mesh     | (0.3, 1.0, 1.5) |
| Sphere    | Mesh     | (-0.3, 1.0, 1.5)|

## Setup

1. Create a Unity 2022 LTS project with **XR Interaction Toolkit** and **OpenXR** plugin enabled.
2. Copy `unity_plugin/Scripts/` into `Assets/OpenGestureXR/Scripts/`.
3. Add an empty GameObject **GestureManager** → attach `GestureClient.cs`.
4. Attach `ObjectInteractor.cs` to **Cube** and **Sphere** separately.
   - Set `handAnchor` on each to the XR camera's right-hand anchor.

## Gesture Interactions

| Gesture      | Object | Action                        |
|--------------|--------|-------------------------------|
| `grab`       | Cube   | Cube attaches to hand — moves with hand |
| `open_hand`  | Cube   | Cube detaches and stays in place        |
| `pinch`      | Sphere | Sphere is selected                      |
| `point`      | Sphere | Sphere is highlighted                   |
