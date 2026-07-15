"""
Localization Engine Module
Recon Rover V2 - Phase 3.3
"""
from .pose_estimator import PoseEstimator
from .odometry import Odometry
from .orientation_tracker import OrientationTracker
from .velocity_estimator import VelocityEstimator
from .pose_history import PoseHistory

class LocalizationEngine:
    """Orchestrates the individual state estimators into a coherent localization pipeline."""
    def __init__(self):
        self.estimator = PoseEstimator()
        self.odometry = Odometry()
        self.orientation = OrientationTracker()
        self.velocity = VelocityEstimator()
        self.history = PoseHistory()
        
    def tick(self) -> tuple:
        """
        Calculates the current cycle's pose.
        Returns: (x, y, theta, confidence, linear_vel, angular_vel, history_size)
        """
        # Get latest angular state
        theta = self.orientation.get_theta()
        
        # Get latest velocity state
        lin_vel, ang_vel = self.velocity.get_velocity()
        
        # Integrate dead-reckoning
        self.odometry.integrate_velocity(lin_vel, theta)
        
        # Extract 2D grid position
        x, y = self.odometry.get_position()
        
        # Apply estimation filters (Placeholder)
        est_x, est_y, est_theta, conf = self.estimator.estimate(x, y, theta)
        
        # Log to sliding window
        self.history.add_pose(est_x, est_y, est_theta, conf)
        
        return est_x, est_y, est_theta, conf, lin_vel, ang_vel, self.history.get_size()
