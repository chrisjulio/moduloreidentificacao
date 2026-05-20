"""Download Facebook Ego-Nets from SNAP and organise by ego-node."""

import hashlib
import logging
import shutil
import tarfile
import tempfile
import urllib.request
from pathlib import Path

from tqdm import tqdm

SNAP_URL = "https://snap.stanford.edu/data/facebook.tar.gz"
RAW_DIR = Path(__file__).resolve().parents[2] / "data" / "raw" / "facebook"

# All ego-node IDs present in the SNAP Facebook archive.
# Verified against facebook.tar.gz on 2026-05-20.
_EGO_IDS: frozenset[int] = frozenset({0, 107, 348, 414, 686, 698, 1684, 1912, 3437, 3980})
_FILE_SUFFIXES: frozenset[str] = frozenset(
    {".circles", ".edges", ".egofeat", ".feat", ".featnames"}
)

log = logging.getLogger(__name__)


class _ProgressHook:
    """urllib reporthook that drives a tqdm progress bar."""

    def __init__(self, desc: str) -> None:
        self._bar: tqdm | None = None
        self._desc = desc

    def __call__(self, blocknum: int, blocksize: int, totalsize: int) -> None:
        if self._bar is None:
            self._bar = tqdm(
                total=totalsize if totalsize > 0 else None,
                unit="B",
                unit_scale=True,
                desc=self._desc,
                leave=True,
            )
        self._bar.update(blocksize)

    def close(self) -> None:
        if self._bar is not None:
            self._bar.close()


def _already_downloaded(dest: Path) -> bool:
    """Return True when every expected ego-network file is present under *dest*."""
    for ego_id in _EGO_IDS:
        ego_dir = dest / str(ego_id)
        for suffix in _FILE_SUFFIXES:
            if not (ego_dir / f"{ego_id}{suffix}").exists():
                return False
    return True


def _sha256(path: Path) -> str:
    """Return the hex-encoded SHA-256 digest of *path*."""
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _extract_and_organise(tarball: Path, dest: Path) -> None:
    """Extract *tarball* and place each ego-network in its own subdirectory."""
    log.info("Extracting %s -> %s", tarball.name, dest)
    with tarfile.open(tarball, "r:gz") as tf, tempfile.TemporaryDirectory() as tmp:
        tf.extractall(tmp, filter="data")
        tmp_path = Path(tmp)
        # The SNAP archive nests files under facebook/
        src_dir = tmp_path / "facebook"
        if not src_dir.is_dir():
            src_dir = tmp_path

        dest.mkdir(parents=True, exist_ok=True)
        for ego_id in _EGO_IDS:
            ego_dir = dest / str(ego_id)
            ego_dir.mkdir(exist_ok=True)
            for suffix in _FILE_SUFFIXES:
                src_file = src_dir / f"{ego_id}{suffix}"
                if src_file.exists():
                    shutil.copy2(src_file, ego_dir / src_file.name)
                else:
                    log.warning("Expected file not found in archive: %s", src_file.name)

    log.info("Extraction complete.")


def download(dest: Path = RAW_DIR) -> None:
    """Download and extract Facebook Ego-Nets from SNAP.

    Parameters
    ----------
    dest:
        Root directory where extracted files are placed.
        Each ego-network lands in *dest/<ego_id>/*.

    Notes
    -----
    Idempotent: exits early when all expected files are already present.
    Logs the SHA-256 digest of the downloaded tarball for manual verification.
    """
    if _already_downloaded(dest):
        log.info("Dataset already present at %s — skipping download.", dest)
        return

    dest.mkdir(parents=True, exist_ok=True)

    tmp_path = Path(tempfile.mktemp(suffix=".tar.gz"))
    try:
        log.info("Downloading Facebook Ego-Nets from %s", SNAP_URL)
        hook = _ProgressHook("facebook.tar.gz")
        urllib.request.urlretrieve(SNAP_URL, tmp_path, reporthook=hook)
        hook.close()

        size = tmp_path.stat().st_size
        digest = _sha256(tmp_path)
        log.info("SHA-256: %s  size: %d B", digest, size)

        if not tarfile.is_tarfile(tmp_path):
            raise ValueError(f"Downloaded file is not a valid tar archive: {tmp_path}")

        _extract_and_organise(tmp_path, dest)
        log.info("Done. Dataset stored in %s", dest)

    finally:
        tmp_path.unlink(missing_ok=True)


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        level=logging.INFO,
    )
    download()
