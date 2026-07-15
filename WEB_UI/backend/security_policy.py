class SecurityPolicy:
    def __init__(self):
        self.max_failed_attempts = 5
        self.lockout_duration_seconds = 300 # 5 minutes
        self.session_timeout_seconds = 3600 # 1 hour
        self.jwt_secret = "RECON_ROVER_V2_MOCK_SECRET_DO_NOT_USE_IN_PROD"
        self.password_min_length = 8
