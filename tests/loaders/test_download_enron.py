"""Tests for src/loaders/download_enron.py — no network access required."""

import gzip
import hashlib
from pathlib import Path
from unittest.mock import patch

from src.loaders.download_enron import (
    _OUTPUT_NAME,
    _already_downloaded,
    _decompress,
    download_enron,
)

# A tiny fake edge list standing in for the real SNAP file.
_FAKE_EDGES = b"# Directed graph\n0\t1\n1\t0\n2\t3\n"


class TestAlreadyDownloaded:
    def test_empty_dir_returns_false(self, tmp_path: Path) -> None:
        assert not _already_downloaded(tmp_path)

    def test_output_present_returns_true(self, tmp_path: Path) -> None:
        (tmp_path / _OUTPUT_NAME).touch()
        assert _already_downloaded(tmp_path)


class TestDecompress:
    def test_decompress_writes_plain_text(self, tmp_path: Path) -> None:
        gz_path = tmp_path / "src.txt.gz"
        with gzip.open(gz_path, "wb") as fh:
            fh.write(_FAKE_EDGES)

        _decompress(gz_path, tmp_path)

        assert (tmp_path / _OUTPUT_NAME).read_bytes() == _FAKE_EDGES


class TestDownload:
    def test_skips_when_already_present(self, tmp_path: Path) -> None:
        """download_enron() must not hit the network when the file exists."""
        (tmp_path / _OUTPUT_NAME).touch()
        with patch("src.loaders.download_enron.urllib.request.urlretrieve") as mock_dl:
            download_enron(dest=tmp_path)
        mock_dl.assert_not_called()

    def test_downloads_and_decompresses(self, tmp_path: Path) -> None:
        """download_enron() fetches the .gz, decompresses, and logs the digest."""
        buf = gzip.compress(_FAKE_EDGES)

        def fake_urlretrieve(url: str, dest: str, reporthook=None) -> None:
            Path(dest).write_bytes(buf)
            if reporthook:
                reporthook(1, len(buf), len(buf))

        with patch(
            "src.loaders.download_enron.urllib.request.urlretrieve",
            side_effect=fake_urlretrieve,
        ):
            download_enron(dest=tmp_path)

        assert _already_downloaded(tmp_path)
        assert (tmp_path / _OUTPUT_NAME).read_bytes() == _FAKE_EDGES

    def test_rejects_non_gzip(self, tmp_path: Path) -> None:
        """A non-gzip payload is rejected and leaves no output file behind."""

        def fake_urlretrieve(url: str, dest: str, reporthook=None) -> None:
            Path(dest).write_bytes(b"this is not gzip")

        import pytest

        with (
            patch(
                "src.loaders.download_enron.urllib.request.urlretrieve",
                side_effect=fake_urlretrieve,
            ),
            pytest.raises(gzip.BadGzipFile),
        ):
            download_enron(dest=tmp_path)

        assert not _already_downloaded(tmp_path)


class TestReuseFacebookHelpers:
    def test_sha256_matches_hashlib(self, tmp_path: Path) -> None:
        """download_enron reuses _sha256 from the Facebook downloader."""
        from src.loaders.download_enron import _sha256

        data = b"hello enron"
        p = tmp_path / "file.bin"
        p.write_bytes(data)
        assert _sha256(p) == hashlib.sha256(data).hexdigest()
