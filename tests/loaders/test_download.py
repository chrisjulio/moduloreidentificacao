"""Tests for src/loaders/download.py — no network access required."""

import io
import tarfile
from pathlib import Path
from unittest.mock import patch

from src.loaders.download import (
    _EGO_IDS,
    _FILE_SUFFIXES,
    _already_downloaded,
    _sha256,
    download,
)


def _make_full_dataset(root: Path) -> None:
    """Populate *root* with all expected ego-network files."""
    for ego_id in _EGO_IDS:
        ego_dir = root / str(ego_id)
        ego_dir.mkdir(parents=True)
        for suffix in _FILE_SUFFIXES:
            (ego_dir / f"{ego_id}{suffix}").touch()


class TestAlreadyDownloaded:
    def test_empty_dir_returns_false(self, tmp_path: Path) -> None:
        assert not _already_downloaded(tmp_path)

    def test_partial_files_returns_false(self, tmp_path: Path) -> None:
        ego_id = next(iter(_EGO_IDS))
        ego_dir = tmp_path / str(ego_id)
        ego_dir.mkdir()
        (ego_dir / f"{ego_id}.edges").touch()
        assert not _already_downloaded(tmp_path)

    def test_all_files_present_returns_true(self, tmp_path: Path) -> None:
        _make_full_dataset(tmp_path)
        assert _already_downloaded(tmp_path)


class TestSha256:
    def test_known_digest(self, tmp_path: Path) -> None:
        import hashlib

        data = b"hello snap"
        p = tmp_path / "file.bin"
        p.write_bytes(data)
        expected = hashlib.sha256(data).hexdigest()
        assert _sha256(p) == expected


class TestDownload:
    def test_skips_when_already_present(self, tmp_path: Path) -> None:
        """download() must not call urlretrieve when dataset is complete."""
        _make_full_dataset(tmp_path)
        with patch("src.loaders.download.urllib.request.urlretrieve") as mock_dl:
            download(dest=tmp_path)
        mock_dl.assert_not_called()

    def test_extracts_files_from_tarball(self, tmp_path: Path) -> None:
        """download() extracts and organises files from a fake tarball."""
        # Build an in-memory tar.gz containing the expected files
        buf = io.BytesIO()
        with tarfile.open(fileobj=buf, mode="w:gz") as tf:
            for ego_id in _EGO_IDS:
                for suffix in _FILE_SUFFIXES:
                    name = f"facebook/{ego_id}{suffix}"
                    content = f"{ego_id}{suffix}".encode()
                    info = tarfile.TarInfo(name=name)
                    info.size = len(content)
                    tf.addfile(info, io.BytesIO(content))
        tarball_bytes = buf.getvalue()

        def fake_urlretrieve(url: str, dest: str, reporthook=None) -> None:
            Path(dest).write_bytes(tarball_bytes)
            if reporthook:
                reporthook(1, len(tarball_bytes), len(tarball_bytes))

        with patch("src.loaders.download.urllib.request.urlretrieve", side_effect=fake_urlretrieve):
            download(dest=tmp_path)

        assert _already_downloaded(tmp_path)
