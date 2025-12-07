# tests/conftest.py

import os
import sys

# Bu dosyanın bulunduğu klasör: .../password-breach-check/tests
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Proje kök dizini: .../password-breach-check
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

# Proje kökünü sys.path'e ekle
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
