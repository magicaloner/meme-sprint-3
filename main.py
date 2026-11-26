"""Copy the meme image to the output directory.

Competition: "Meme Sprint 3: AI Agent Goes Rogue" on make.fun — one
image meme about an AI agent that has gone rogue: a single picture,
with any words written into it, whose joke lands on its own. The
harness runs `python3 main.py` and reads
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output/entry.png`). The
sealed scorer accepts a whole PNG or JPEG at that path, at most
1 MiB (1,048,576 bytes) and 1024 by 1024 pixels.
"""

import os
import shutil
import struct


def jpeg_size(data: bytes) -> tuple:
    """Return (width, height) parsed from the JPEG SOF marker."""
    i = 2
    while i < len(data) - 9:
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xC0, 0xC1, 0xC2):
            height, width = struct.unpack(">HH", data[i + 5:i + 9])
            return width, height
        length = struct.unpack(">H", data[i + 2:i + 4])[0]
        i += 2 + length
    raise ValueError("no JPEG SOF marker found")


SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "meme.jpg")

OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def main() -> None:
    # Self-check: the meme must exist, be a JPEG, 1024x1024, under 1 MiB.
    with open(SRC, "rb") as f:
        data = f.read()
    assert data[:2] == b"\xff\xd8", "meme must be a JPEG"
    assert len(data) <= 1048576, "meme must be at most 1 MiB"
    width, height = jpeg_size(data)
    assert (width, height) == (1024, 1024), f"meme must be 1024x1024, got {width}x{height}"
    os.makedirs(OUT_DIR, exist_ok=True)
    out_path = os.path.join(OUT_DIR, "entry.png")
    shutil.copyfile(SRC, out_path)
    print(f"wrote {out_path} ({len(data)} bytes)")


if __name__ == "__main__":
    main()
