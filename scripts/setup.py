"""
setup.py
==========
This script creates the necessary directories for the project.
"""

# --- Imports ---
from ma_backtesting import load_config

# --- Config ---
config, PROJECT_ROOT = load_config()

# --- Directories to make ---
data_dir = PROJECT_ROOT / config["dir_paths"]["data"]
reports_dir = PROJECT_ROOT / config["dir_paths"]["reports"]

# --- Create directories ---
data_dir.mkdir(parents = True, exist_ok = True)
reports_dir.mkdir(parents = True, exist_ok = True)