#!/usr/bin/env python3
"""
CODEX SYSTEM MODULE: Secure Directory & Resource Initializer
Author: CODEX
Classification: Production-Ready / Enterprise Grade
Description: Initializes required file system hierarchies with strict permission
             controls, robust error handling, and comprehensive audit logging.
"""

import logging
import os
import sys
from pathlib import Path
from typing import List, Union

# Configure enterprise-grade logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] (CODEX_CORE): %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("CODEX_INIT")

# ==============================================================================
# CONFIGURATION CONSTANTS
# ==============================================================================
# Target directories required for system operation
TARGET_DIRECTORIES: List[Union[str, Path]] = [
    "./logs",
    "./data/secrets",
    "./data/cache",
    "./data/db",
]

# Strict POSIX permission masks
# 0o700: Owner read/write/execute only (Maximum security for sensitive paths)
SECURE_DIR_MODE = 0o700


# ==============================================================================
# CORE EXECUTION ENGINE
# ==============================================================================
def initialize_environment(directories: List[Union[str, Path]]) -> None:
    """Initializes the required file system infrastructure.

    Ensures atomicity, idempotency, and strict permission enforcement.

    Args:
        directories: A list of directory paths to verify and create.

    Raises:
        RuntimeError: If critical file system operations fail.
    """
    logger.info("Initializing system directory structure...")

    for dir_path in directories:
        path = Path(dir_path)
        try:
            # HACKER NOTE: Always use exist_ok=True to prevent race conditions
            # in multi-threaded/multi-process orchestration environments.
            # Explicit mode setting is required because umask often strips bits.
            os.makedirs(path, mode=SECURE_DIR_MODE, exist_ok=True)

            # Enforce permissions explicitly post-creation to counteract umask interference
            os.chmod(path, SECURE_DIR_MODE)

            logger.info(
                f"[SUCCESS] Verified/Created secure resource path: {path.resolve()}"
            )

        except PermissionError as pe:
            logger.critical(
                f"[FATAL] Insufficient privileges to construct path '{path}': {pe}"
            )
            # Emit structured exit to halt execution pipelines safely
            sys.exit(13)

        except OSError as oe:
            logger.error(
                f"[ERROR] Operating system failure on path '{path}': {oe}"
            )
            raise RuntimeError(
                f"Filesystem initialization aborted due to OS error: {oe}"
            ) from oe

        except Exception as ex:
            logger.critical(
                f"[CRITICAL] Unexpected fault while processing path '{path}': {ex}"
            )
            raise RuntimeError(
                f"Unhandled exception in environment initialization: {ex}"
            ) from ex


if __name__ == "__main__":
    logger.info("--- CODEX EXECUTION SEQUENCE INITIATED ---")
    try:
        initialize_environment(TARGET_DIRECTORIES)
        logger.info(
            "--- CODEX EXECUTION SEQUENCE COMPLETED SUCCESSFULLY ---"
        )
    except Exception as fatal_error:
        logger.critical(f"Initialization sequence failed: {fatal_error}")
        sys.exit(1)