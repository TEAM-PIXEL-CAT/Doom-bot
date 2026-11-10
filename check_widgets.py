"""Widget checks: Bot API 10.4 size limits and things the Telegram validator strips.

    python check_widgets.py            # every file in widgets/
"""
import re
import sys
import zlib
from pathlib import Path

MAX_RAW, MAX_ZLIB = 32768, 4096
FORBIDDEN = [
    (r"<(input|button|select|textarea|form|label)\b", "form controls are not allowed"),
    (r"<script[^>]+src=", "external scripts are not allowed"),
    (r"<link\b", "external stylesheets are not allowed"),
    (r"(src|href)\s*=\s*['\"]?https?:", "no network: only data: and #fragment"),
    (r"url\(\s*['\"]?https?:", "no network: only data: and #fragment"),
    (r"\bfetch\(|XMLHttpRequest|WebSocket", "no network"),
]


def check(path: Path) -> bool:
    raw = path.read_bytes()
    z = len(zlib.compress(raw, 9))
    text = raw.decode("utf-8")
    problems = [msg for rx, msg in FORBIDDEN if re.search(rx, text, re.I)]
    if len(raw) > MAX_RAW:
        problems.append(f"HTML > {MAX_RAW} bytes")
    if z > MAX_ZLIB:
        problems.append(f"zlib > {MAX_ZLIB} bytes")
    status = "OK " if not problems else "ERR"
    print(f"{status} {path.name:22} {len(raw):6} B  zlib {z:5} B ({z * 100 // MAX_ZLIB:3}% of limit)"
          + ("  " + "; ".join(problems) if problems else ""))
    return not problems


if __name__ == "__main__":
    files = sorted(Path(__file__).with_name("widgets").glob("*.html"))
    ok = all([check(f) for f in files])
    try:
        from themes import THEMES, pack
        for lv in range(1, len(THEMES) + 1):
            n = len(pack(lv).encode())
            print(f"OK  level pack {lv} ({THEMES[lv - 1]['name']})".ljust(36) + f"{n:5} B of 1024 (public_data / answer)")
    except AssertionError as e:
        print("ERR", e)
        ok = False
    sys.exit(0 if ok else 1)
