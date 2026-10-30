import re, sys, urllib.request, pathlib
IDS = sys.argv[1:]
out = pathlib.Path("media/xeber/raw"); out.mkdir(parents=True, exist_ok=True)
H = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36", "Accept-Language": "en-US,en"}
def get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=30).read()
for i in IDS:
    try:
        t = get(f"https://www.instagram.com/p/{i}/embed/captioned/").decode("utf8", "ignore")
        m = re.search(r'display_url\\?":\\?"([^"]+?)\\?"', t) or re.search(r'class="EmbeddedMediaImage"[^>]+src="([^"]+)"', t)
        if not m:
            print(i, "NO_URL", len(t)); continue
        u = m.group(1).replace("\\/", "/").replace("\\u0026", "&").replace("&amp;", "&").replace("\\", "")
        (out / f"{i}.jpg").write_bytes(get(u)); print(i, "OK")
    except Exception as e:
        print(i, "ERR", e)
