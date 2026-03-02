from pathlib import Path

from packages.core.path_scope import iter_scoped_paths


def test_iter_scoped_paths_deterministic(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "b.txt").write_text("b", encoding="utf-8")
    (repo / "a.txt").write_text("a", encoding="utf-8")

    paths = iter_scoped_paths(repo)

    assert [path.as_posix() for path in paths] == ["a.txt", "b.txt"]


def test_iter_scoped_paths_include_exclude(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "src").mkdir()
    (repo / "src" / "ok.py").write_text("x", encoding="utf-8")
    (repo / "src" / "skip.py").write_text("x", encoding="utf-8")

    paths = iter_scoped_paths(repo, include_paths=["src/*.py"], exclude_paths=["src/skip.py"])

    assert [path.as_posix() for path in paths] == ["src/ok.py"]
