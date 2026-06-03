"""Download the Email-Enron network from SNAP.

Mirrors :mod:`src.loaders.download` (Facebook) but targets a single gzipped
edge list rather than a tar archive. The downloaded ``email-Enron.txt.gz`` is
decompressed to ``email-Enron.txt`` under :data:`RAW_DIR`.
"""

import gzip
import logging
import shutil
import tempfile
import urllib.request
from pathlib import Path

from src.loaders.download import _ProgressHook, _sha256

SNAP_URL = "https://snap.stanford.edu/data/email-Enron.txt.gz"
RAW_DIR = Path(__file__).resolve().parents[2] / "data" / "raw" / "enron"

# Name of the decompressed edge list expected under RAW_DIR.
_OUTPUT_NAME = "email-Enron.txt"

log = logging.getLogger(__name__)


def _already_downloaded(dest: Path) -> bool:
    """Return True when the decompressed edge list is already present."""
    return (dest / _OUTPUT_NAME).exists()


def _decompress(gz_path: Path, dest: Path) -> None:
    """Decompress *gz_path* into *dest/email-Enron.txt*."""
    out_path = dest / _OUTPUT_NAME
    log.info("Decompressing %s -> %s", gz_path.name, out_path)
    with gzip.open(gz_path, "rb") as src_fh, out_path.open("wb") as out_fh:
        shutil.copyfileobj(src_fh, out_fh)
    log.info("Decompression complete.")


def download_enron(dest: Path = RAW_DIR) -> None:
    """Download and decompress the Email-Enron network from SNAP.

    Parameters
    ----------
    dest:
        Directory where the decompressed edge list is placed
        (``dest/email-Enron.txt``).

    Notes
    -----
    Idempotent: exits early when the decompressed file is already present.
    Logs the SHA-256 digest and byte size of the downloaded ``.gz`` for
    manual verification, mirroring the Facebook downloader.
    """
    if _already_downloaded(dest):
        log.info("Dataset already present at %s — skipping download.", dest)
        return

    dest.mkdir(parents=True, exist_ok=True)

    tmp_path = Path(tempfile.mktemp(suffix=".txt.gz"))
    try:
        log.info("Downloading Email-Enron from %s", SNAP_URL)
        hook = _ProgressHook("email-Enron.txt.gz")
        urllib.request.urlretrieve(SNAP_URL, tmp_path, reporthook=hook)
        hook.close()

        size = tmp_path.stat().st_size
        digest = _sha256(tmp_path)
        log.info("SHA-256: %s  size: %d B", digest, size)

        # gzip.open raises BadGzipFile lazily on read; surface a clear error early.
        with gzip.open(tmp_path, "rb") as fh:
            fh.read(1)

        _decompress(tmp_path, dest)
        log.info("Done. Dataset stored in %s", dest)

    finally:
        tmp_path.unlink(missing_ok=True)


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        level=logging.INFO,
    )
    download_enron()
