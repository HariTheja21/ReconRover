"""
logger.py
Recon Rover V1 - Cognitive Layer

Thread-safe structured logging to console and files.
"""

import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from config import Config

class Logger:
    """
    Singleton-style logger setup for the entire application.
    """
    _setup_done = False

    @staticmethod
    def setup():
        if Logger._setup_done:
            return
        
        Config.load()
        
        log_formatter = logging.Formatter(
            '%(asctime)s [%(levelname)-7s] %(name)s: %(message)s', 
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        root_logger = logging.getLogger()
        
        level = getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO)
        root_logger.setLevel(level)

        # Console Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(log_formatter)
        root_logger.addHandler(console_handler)

        # File Handler
        log_file = os.path.join(Config.LOG_DIR, "rover.log")
        file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
        file_handler.setFormatter(log_formatter)
        root_logger.addHandler(file_handler)

        Logger._setup_done = True

    @staticmethod
    def get(name: str) -> logging.Logger:
        if not Logger._setup_done:
            Logger.setup()
        return logging.getLogger(name)
