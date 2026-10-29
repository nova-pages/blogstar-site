"""index.html (AZ) faylından /en/index.html (EN) versiyasını yaradır.
Saytı dəyişəndən sonra işə salın: python3 build-en.py"""
import re, pathlib
src = pathlib.Path("index.html").read_text(encoding="utf-8")
h = src
def sub(old, new):
    global h
    assert old in h, old[:60]
    h = h.replace(old, new, 1)
sub('<html lang="az">', '<html lang="en">')
h = re.sub(r'<meta name="description" content="[^"]*">',
  '<meta name="description" content="Blogstar is an influencer marketing agency in Baku, Azerbaijan: influencer campaigns, branding, product and UGC production, influencer events and Blogstar Academy (Influencer School).">', h, count=1)
sub('<link rel="canonical" href="https://blogstar.az/">', '<link rel="canonical" href="https://blogstar.az/en/">')
sub('<meta property="og:locale" content="az_AZ">', '<meta property="og:locale" content="en_US">')
sub('<meta property="og:locale:alternate" content="en_US">', '<meta property="og:locale:alternate" content="az_AZ">')
h = re.sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="Blogstar — Influencer Marketing Agency in Azerbaijan">', h, count=1)
h = re.sub(r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="Trust, influence and results. Influencer marketing campaigns and Influencer School in Baku, Azerbaijan.">', h, count=1)
sub('<meta property="og:url" content="https://blogstar.az/">', '<meta property="og:url" content="https://blogstar.az/en/">')
h = re.sub(r'<meta name="twitter:title" content="[^"]*">', '<meta name="twitter:title" content="Blogstar — Influencer Marketing Agency in Azerbaijan">', h, count=1)
h = re.sub(r'<title>[^<]*</title>', '<title>Blogstar — Influencer Marketing Agency in Azerbaijan | Baku</title>', h, count=1)
sub('<b class="sr">Blogstar — influencer marketinq agentliyi. </b>', '<b class="sr">Blogstar — influencer marketing agency in Azerbaijan. </b>')
sub('let LANG=PAGE_LANG_AZ;', 'let LANG="en";')
pathlib.Path("en").mkdir(exist_ok=True)
pathlib.Path("en/index.html").write_text(h, encoding="utf-8")
print("en/index.html yaradıldı")
