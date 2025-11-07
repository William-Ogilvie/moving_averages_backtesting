"""
io_utils.py
============

This modules contains helper functions for loading the config (maybe more)
"""
# TODO right the bio above

# --- Imports ---
import yaml
from pathlib import Path

# --- Constants ---

# src/ma_backtests is location of current file so go two above to get project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = PROJECT_ROOT / "config" / "settings.yml"

# --- Functions ---
def load_config() -> tuple[dict, Path]:
    """ Loads the configuration from a YAML file, returns both this and the project root.

    Returns:
        tuple[dict, Path]: A tuple the config dictionary and the project root path.
    """

    # Load config
    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)

    return config, PROJECT_ROOT