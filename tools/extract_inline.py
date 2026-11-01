"""Move large inline base64 images out of index.html into /img/i/<hash>.<ext> (faster first load)."""
import re, base64, hashlib, pathlib, sys
p = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "index.html")
s = p.read_text(encoding="utf-8")
out = pathlib.Path("img/i"); out.mkdir(parents=True, exist_ok=True)
n = 0
def rep(m):
    global n
    ext = {"jpeg": "jpg", "png": "png", "webp": "webp", "svg+xml": "svg"}.get(m.group(1), "bin")
    raw = base64.b64decode(m.group(2)); h = hashlib.sha1(raw).hexdigest()[:12]
    f = out / f"{h}.{ext}"
    if not f.exists(): f.write_bytes(raw)
    n += 1
    return f"/img/i/{h}.{ext}"
s = re.sub(r"data:image/(jpeg|png|webp|svg\+xml);base64,([A-Za-z0-9+/=]{1500,})", rep, s)
p.write_text(s, encoding="utf-8")
print("extracted", n, "->", len(s), "bytes")
