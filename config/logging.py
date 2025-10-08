"""Logging configuration for myquery."""
import logging
import sys
from typing import Optional
from rich.logging import RichHandler
from rich.console import Console


def setup_logging(level: str = "INFO", debug_mode: bool = False) -> None:
    """
    Setup logging configuration with Rich handler.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        debug_mode: Enable debug mode with more detailed logs
    """
    log_level = logging.DEBUG if debug_mode else getattr(logging, level.upper(), logging.INFO)
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[
            RichHandler(
                console=Console(stderr=True),
                rich_tracebacks=True,
                tracebacks_show_locals=debug_mode,
                show_time=debug_mode,
                show_path=debug_mode,
            )
        ],
    )
    
    # Set levels for third-party libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    
    if debug_mode:
        logging.getLogger("myquery").setLevel(logging.DEBUG)


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Logger instance
    """
    if name:
        return logging.getLogger(f"myquery.{name}")
    return logging.getLogger("myquery")

