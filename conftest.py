"""Tells pytest where our source code lives (the src folder)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))