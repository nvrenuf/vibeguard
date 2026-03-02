import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CLI_ROOT = ROOT / "apps" / "cli"

for path in (str(ROOT), str(CLI_ROOT)):
    if path not in sys.path:
        sys.path.insert(0, path)
