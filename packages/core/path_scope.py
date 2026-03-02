from __future__ import annotations

from fnmatch import fnmatch
from pathlib import Path


def _normalize(patterns: list[str] | None) -> list[str]:
    if not patterns:
        return []
    return [pattern.strip() for pattern in patterns if pattern.strip()]


def _matches(path: str, patterns: list[str]) -> bool:
    return any(fnmatch(path, pattern) for pattern in patterns)


def iter_scoped_paths(
    repo_root: Path,
    include_paths: list[str] | None = None,
    exclude_paths: list[str] | None = None,
    *,
    files_only: bool = True,
) -> list[Path]:
    """Return deterministic relative paths constrained by include/exclude globs."""
    includes = _normalize(include_paths) or ["**"]
    excludes = _normalize(exclude_paths)

    candidates: list[Path] = []
    for entry in repo_root.rglob("*"):
        if files_only and not entry.is_file():
            continue
        rel = entry.relative_to(repo_root)
        rel_str = rel.as_posix()
        if not _matches(rel_str, includes):
            continue
        if excludes and _matches(rel_str, excludes):
            continue
        candidates.append(rel)

    return sorted(candidates, key=lambda item: item.as_posix())
