
"""Logging configuration for the student management application."""

import logging
from pathlib import Path
import os

APP_DATA = Path(os.getenv("LOCALAPPDATA", Path.home())) / "StudentAcademicManagement"
APP_DATA.mkdir(parents=True, exist_ok=True)

LOG_FILE = APP_DATA / "application.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

logger = logging.getLogger("StudentAcademicManagement")
