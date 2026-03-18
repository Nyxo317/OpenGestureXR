"""
Sensor fusion interfaces.

Defines the abstract base for fusing multiple input streams
(RGB, depth, IMU) into a unified hand-pose estimate. Concrete
implementations will use Kalman filtering or learned fusion.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional
import numpy as np


class SensorType(Enum):
    RGB = auto()
    DEPTH = auto()
    IMU = auto()


@dataclass
class SensorFrame:
    """A single timestamped reading from one sensor."""
    sensor_type: SensorType
    timestamp: float  # seconds
    data: np.ndarray  # shape depends on sensor type


@dataclass
class FusedPose:
    """Output of the fusion pipeline."""
    landmarks: np.ndarray          # (21, 3) hand keypoints in world coords
    confidence: float
    timestamp: float
    sources: list[SensorType] = field(default_factory=list)


class FusionBackend(ABC):
    """Base class for sensor fusion strategies."""

    @abstractmethod
    def update(self, frame: SensorFrame) -> None:
        """Ingest a new sensor reading."""

    @abstractmethod
    def estimate(self) -> FusedPose | None:
        """Return the current fused pose estimate, or None if not ready."""

    @abstractmethod
    def reset(self) -> None:
        """Clear internal state."""
