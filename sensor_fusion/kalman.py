"""
Kalman-filter-based sensor fusion.

Fuses RGB landmark detections with optional depth and IMU readings
to produce smoothed, low-latency hand pose estimates.

This is a skeleton — the predict/update matrices need tuning once
real depth + IMU hardware is available for testing.
"""

from __future__ import annotations
import numpy as np
from .base import FusionBackend, SensorFrame, SensorType, FusedPose


class KalmanFusion(FusionBackend):
    """Simple Kalman filter over 21 3D keypoints (63-dim state)."""

    def __init__(self, process_noise=1e-3, measurement_noise=1e-2):
        self._dim = 63  # 21 joints * 3 coords
        self._state = np.zeros(self._dim)
        self._cov = np.eye(self._dim)
        self._Q = np.eye(self._dim) * process_noise
        self._R = np.eye(self._dim) * measurement_noise
        self._initialized = False
        self._timestamp = 0.0
        self._sources: list[SensorType] = []

    def update(self, frame: SensorFrame) -> None:
        measurement = frame.data.flatten()[:self._dim]
        if len(measurement) < self._dim:
            return

        if not self._initialized:
            self._state = measurement.copy()
            self._initialized = True
        else:
            # predict (identity transition — assumes slow motion between frames)
            pred_cov = self._cov + self._Q
            # update
            K = pred_cov @ np.linalg.inv(pred_cov + self._R)
            self._state = self._state + K @ (measurement - self._state)
            self._cov = (np.eye(self._dim) - K) @ pred_cov

        self._timestamp = frame.timestamp
        if frame.sensor_type not in self._sources:
            self._sources.append(frame.sensor_type)

    def estimate(self) -> FusedPose | None:
        if not self._initialized:
            return None
        return FusedPose(
            landmarks=self._state.reshape(21, 3),
            confidence=min(1.0, 1.0 / (1.0 + np.trace(self._cov))),
            timestamp=self._timestamp,
            sources=list(self._sources),
        )

    def reset(self) -> None:
        self._state = np.zeros(self._dim)
        self._cov = np.eye(self._dim)
        self._initialized = False
        self._sources.clear()
