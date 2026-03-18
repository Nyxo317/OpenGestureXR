"""Tests for the sensor fusion module."""

import numpy as np
from sensor_fusion.base import SensorFrame, SensorType
from sensor_fusion.kalman import KalmanFusion


class TestKalmanFusion:
    def test_no_estimate_before_update(self):
        kf = KalmanFusion()
        assert kf.estimate() is None

    def test_single_update(self):
        kf = KalmanFusion()
        data = np.random.rand(21, 3).astype(np.float32)
        kf.update(SensorFrame(SensorType.RGB, 0.0, data))
        pose = kf.estimate()
        assert pose is not None
        assert pose.landmarks.shape == (21, 3)
        np.testing.assert_allclose(pose.landmarks, data, atol=1e-5)

    def test_multiple_updates_smooth(self):
        kf = KalmanFusion()
        d1 = np.zeros((21, 3), dtype=np.float32)
        d2 = np.ones((21, 3), dtype=np.float32)
        kf.update(SensorFrame(SensorType.RGB, 0.0, d1))
        kf.update(SensorFrame(SensorType.DEPTH, 0.033, d2))
        pose = kf.estimate()
        # should be somewhere between d1 and d2
        assert 0.0 < pose.landmarks.mean() < 1.0
        assert SensorType.RGB in pose.sources
        assert SensorType.DEPTH in pose.sources

    def test_reset(self):
        kf = KalmanFusion()
        kf.update(SensorFrame(SensorType.RGB, 0.0, np.ones((21, 3))))
        kf.reset()
        assert kf.estimate() is None
