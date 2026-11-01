import json
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(); pg.goto('file:///home/claude/blogstar-site/index.html'); pg.wait_for_timeout(800)
    d = pg.evaluate('({N:NEWS,W:WORK.map(w=>({b:w.b,w:w.w,f:w.f||null,kpi:w.kpi||null,reels:w.reels.map(r=>typeof r==="string"?{url:r}:{url:r.url,who:r.who||"",tt:!!r.tt})}))})'); b.close()
json.dump(d, open('seo-data.json', 'w'), ensure_ascii=False)
