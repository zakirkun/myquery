"""Configuration package for myquery."""
from config.settings import settings
from config.logging import setup_logging, get_logger

__all__ = ["settings", "setup_logging", "get_logger"]

