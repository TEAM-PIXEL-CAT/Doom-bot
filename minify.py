"""Minifies src/*.html into widgets/: JS with terser, CSS and HTML by stripping whitespace.
    python minify.py   (needs Node: npx terser)"""
import re, subprocess, zlib
from pathlib import Path
HERE = Path(__file__).parent
for src in sorted((HERE / "src").glob("*.html")):
    h = src.read_text(encoding="utf-8")
    js = re.search(r"<script>(.*?)</script>", h, re.S).group(1)
    mjs = subprocess.run(["npx", "-y", "terser", "-c", "passes=3,unsafe=true,unsafe_math=true,unsafe_arrows=false", "-m", "--toplevel"],
                         input=js, capture_output=True, text=True, check=True).stdout.strip()
    css = re.search(r"<style>(.*?)</style>", h, re.S).group(1)
    mcss = re.sub(r"\s*([{}:;,])\s*", r"\1", css).replace(";}", "}").strip()
    out = h.replace(js, mjs).replace(css, mcss)
    out = re.sub(r">\s+<", "><", out)
    (HERE / "widgets" / src.name).write_text(out, encoding="utf-8")
    raw = out.encode()
    print(f"{src.name}: {len(h.encode())} → {len(raw)} B, zlib {len(zlib.compress(h.encode(), 9))} → {len(zlib.compress(raw, 9))} B")
