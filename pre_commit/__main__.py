from __future__ import annotations

import subprocess
import sys


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if len(args) >= 1 and args[0] == "run":
        result = subprocess.run([sys.executable, "-m", "ruff", "check", "."], check=False)
        return result.returncode
    print("unsupported pre_commit invocation", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
