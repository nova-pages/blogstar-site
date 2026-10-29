"""pages-data.json -> /academy/, /xidmetler/<id>/, /media/<slug>/ səhifələri və sitemap.xml.
İşə salmaq: python3 build-pages.py"""
import json, re, html, pathlib, datetime
D = json.loads(pathlib.Path("pages-data.json").read_text(encoding="utf-8"))
T = D["T"]["az"]; TODAY = datetime.date.today().isoformat()
E = lambda s: html.escape(s or "", quote=True)
def slugify(t):
    m = str.maketrans("əƏıIİiöÖüÜşŞçÇğĞ", "eEiIIioOuUsScCgG")
    t = t.translate(m).lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:70]
CSS = """@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300..600&family=Newsreader:ital@1&display=swap');
:root{--ink:#000;--muted:#6B6B6B;--rule:#E5E5E5;--bordo:#5C0012;--mist:#F4F4F4}
*{box-sizing:border-box}body{margin:0;font:400 17px/1.65 Montserrat,Arial,sans-serif;color:var(--ink);background:#fff;-webkit-font-smoothing:antialiased}
a{color:inherit}.w{max-width:820px;margin:0 auto;padding:0 20px}
header{border-bottom:1px solid var(--rule)}header .w{max-width:1240px;display:flex;justify-content:space-between;align-items:center;height:72px}
header img{height:18px;display:block}header nav a{font-size:14px;text-decoration:none;margin-left:22px}header nav a.cta{border:1px solid #000;border-radius:999px;padding:9px 16px}
.bc{font-size:13px;color:var(--muted);margin:44px 0 18px}.bc a{text-decoration:none}.bc a:hover{color:var(--bordo)}
h1{font-weight:400;font-size:clamp(34px,5vw,56px);line-height:1.06;letter-spacing:-.03em;margin:0 0 22px}
.lead{font-size:19px;color:#383838}.tag{display:inline-block;font-size:13px;color:var(--bordo);margin-bottom:12px}
.cov{width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:22px;margin:8px 0 30px;display:block}
h2{font-weight:500;font-size:22px;margin:44px 0 14px;letter-spacing:-.01em}
ul.l{list-style:none;padding:0;margin:0;border-top:1px solid var(--rule)}ul.l li{padding:14px 0;border-bottom:1px solid var(--rule)}
.mods{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}@media(max-width:600px){.mods{grid-template-columns:1fr}}
.mods div{background:var(--mist);border-radius:16px;padding:18px 20px}.mods b{display:block;font-weight:500}.mods span{font-size:14.5px;color:var(--muted)}.mods small{color:var(--bordo);font-size:12px}
.box{margin:56px 0;background:#000;color:#fff;border-radius:24px;padding:34px}.box h2{margin-top:0}.box p{color:#C8C8C8}
.btn{display:inline-block;background:#fff;color:#000;text-decoration:none;border-radius:999px;padding:13px 22px;margin-top:8px}.btn:hover{background:var(--bordo);color:#fff}
.rel{display:grid;gap:10px;padding:0;list-style:none}.rel a{text-decoration:none}.rel a:hover{color:var(--bordo)}
footer{border-top:1px solid var(--rule);margin-top:70px;padding:30px 0;font-size:13px;color:var(--muted)}footer .w{max-width:1240px;display:flex;flex-wrap:wrap;gap:18px;justify-content:space-between}footer a{text-decoration:none}"""
def page(path, title, desc, body, ld, crumbs):
    url = "https://blogstar.az" + path
    bc = " / ".join(f'<a href="{u}">{E(n)}</a>' if u else E(n) for n, u in crumbs)
    crumbld = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":"https://blogstar.az"+(u or path)} for i,(n,u) in enumerate(crumbs)]}
    doc = f"""<!doctype html>
<html lang="az"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)} | Blogstar</title><meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}"><link rel="icon" type="image/png" href="/favicon.png"><meta name="theme-color" content="#000000">
<meta property="og:type" content="website"><meta property="og:site_name" content="Blogstar"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="https://blogstar.az/og.png"><meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{json.dumps([ld, crumbld], ensure_ascii=False)}</script>
<style>{CSS}</style></head><body>
<header><div class="w"><a href="/" aria-label="Blogstar"><img src="/logo.png" alt="Blogstar"></a><nav><a href="/academy/">Academy</a><a href="/#isler">İşlərimiz</a><a class="cta" href="/#elaqe">Əlaqə</a></nav></div></header>
<main class="w"><p class="bc">{bc}</p>{body}
<div class="box"><h2>Blogstar ilə işləyək</h2><p>Kampaniya, təlim və ya əməkdaşlıq barədə sorğunuzu göndərin. info@blogstar.az</p><a class="btn" href="/#elaqe">Sorğu göndərin</a></div></main>
<footer><div class="w"><span>© 2016–2026 Blogstar · Bakı, Azərbaycan</span><span><a href="/">Ana səhifə</a> · <a href="/academy/">Influencer School</a> · <a href="/xidmetler/influencer-marketinq/">Influencer marketinq</a> · <a href="/media/">Media arxivi</a></span></div></footer>
</body></html>"""
    p = pathlib.Path("." + path); p.mkdir(parents=True, exist_ok=True); (p / "index.html").write_text(doc, encoding="utf-8")
    return url
urls = []
ORG = {"@id": "https://blogstar.az/#org", "@type": "Organization", "name": "Blogstar", "url": "https://blogstar.az/"}
# services
for s in D["S"]:
    if s["id"] == "academy": continue
    t = s["t"]["az"]; inc = "".join(f"<li>{E(x)}</li>" for x in s["inc"]["az"])
    body = f'<span class="tag">Xidmətlər</span><h1>{E(t)}</h1><p class="lead">{E(s["s"]["az"])}</p><p>{E(s["lead"]["az"])}</p><h2>Xidmətə daxildir</h2><ul class="l">{inc}</ul>'
    if s["id"] == "influencer-marketinq":
        body += '<h2>Nəticələr</h2><p>Dreame kampaniyası: 1.7M+ baxış, 64% baxış nisbəti. Trendyol Reels seriyası: 13.3M+ baxış, 103% baxış nisbəti. Göstəricilər Instagram-ın açıq məlumatlarına əsaslanır.</p><p><a href="/#isler">Kampaniyalarımıza baxın →</a></p>'
    ld = {"@context":"https://schema.org","@type":"Service","name":t,"serviceType":t,"description":s["s"]["az"],"provider":ORG,"areaServed":"Azerbaijan"}
    urls.append(page(f"/xidmetler/{s['id']}/", f"{t} — Bakı, Azərbaycan", s["s"]["az"], body, ld, [("Ana səhifə","/"),("Xidmətlər","/#xidmetler"),(t,None)]))
# academy
ac = next(s for s in D["S"] if s["id"] == "academy")
mods = "".join(f'<div><small>0{k}</small><b>{E(T["ac.m%d"%k])}</b><span>{E(T["ac.m%dt"%k])}</span></div>' for k in range(1, 9))
body = f'<span class="tag">Blogstar Academy</span><h1>Influencer School: blogçuluq və kontent yaradıcılığı təlimi</h1><p class="lead">{E(T["ac.lead"])}</p><p>{E(ac["lead"]["az"])}</p><h2>Proqramın modulları</h2><div class="mods">{mods}</div><h2>Format</h2><ul class="l"><li>{E(T["ac.f1"])}</li><li>{E(T["ac.f2"])}</li><li>{E(T["ac.f3"])}</li></ul><p style="margin-top:28px"><a class="btn" style="background:#000;color:#fff" href="/#academy">Qeydiyyatdan keçin</a></p>'
ld = {"@context":"https://schema.org","@type":"Course","name":"Influencer School — Blogstar Academy","description":T["ac.lead"],"provider":ORG,"inLanguage":"az","hasCourseInstance":{"@type":"CourseInstance","courseMode":"onsite","location":{"@type":"Place","name":"Bakı, Azərbaycan"}}}
urls.insert(0, page("/academy/", "Influencer School — blogçuluq, fotoqrafiya, video və AI təlimi | Bakı", "Blogstar Academy: influencer və blogçuluq kursu. Şəxsi brend, fotoqrafiya, video montaj, süni intellekt alətləri, brendlərlə əməkdaşlıq. Bakı.", body, ld, [("Ana səhifə","/"),("Academy",None)]))
# articles
MO = "yanvar fevral mart aprel may iyun iyul avqust sentyabr oktyabr noyabr dekabr".split()
fd = lambda d: f"{int(d[8:])} {MO[int(d[5:7])-1]} {d[:4]}"
CAT = {"ev":"Tədbirlər","ac":"Seminar və təlimlər","ar":"Məqalələr","in":"Müsahibələr"}
arts = []
for a in D["A"]:
    sl = slugify(a["t"]); arts.append((a, sl))
items = []
for i, (a, sl) in enumerate(arts):
    paras = "".join(f"<p>{E(x)}</p>" for x in a["x"].split("\n\n") if x.strip())
    cov = f'<img class="cov" src="{E(a["cov"])}" alt="{E(a["t"])}">' if a["cov"] else ""
    rel = [x for x in arts if x[0]["c"] == a["c"] and x[1] != sl][:4]
    relh = "<h2>Oxşar materiallar</h2><ul class=\"rel\">" + "".join(f'<li><a href="/media/{s2}/">{E(b["t"])} →</a></li>' for b, s2 in rel) + "</ul>" if rel else ""
    body = f'<span class="tag">{CAT[a["c"]]} · <time datetime="{a["d"]}">{fd(a["d"])}</time></span><h1>{E(a["t"])}</h1>{cov}{paras}{relh}'
    desc = re.sub(r"\s+", " ", a["x"])[:155].rsplit(" ", 1)[0] + "…"
    ld = {"@context":"https://schema.org","@type":"Article","headline":a["t"][:110],"description":desc,"publisher":ORG,"author":ORG,"inLanguage":"az","datePublished":a["d"],"image":("https://blogstar.az"+a["cov"]) if a["cov"] else "https://blogstar.az/og.png","mainEntityOfPage":f"https://blogstar.az/media/{sl}/"}
    urls.append(page(f"/media/{sl}/", a["t"], desc, body, ld, [("Ana səhifə","/"),("Media arxivi","/media/"),(a["t"],None)]))
    items.append(f'<li><span class="tag">{CAT[a["c"]]} · {fd(a["d"])}</span><br><a href="/media/{sl}/">{E(a["t"])}</a></li>')
body = '<span class="tag">Media mərkəzi</span><h1>Blogstar arxivi: tədbirlər, seminarlar və məqalələr</h1><p class="lead">Blogstar-ın 2016–2020-ci illərdə təşkil etdiyi tədbirlər, influencer seminarları, təlimlər və blogçuluq haqqında məqalələr.</p><ul class="l">' + "".join(items) + "</ul>"
urls.insert(1, page("/media/", "Media arxivi — tədbirlər, seminarlar və məqalələr", "Blogstar-ın tədbirləri, influencer seminarları və blogçuluq məqalələri arxivi.", body, {"@context":"https://schema.org","@type":"CollectionPage","name":"Blogstar media arxivi","publisher":ORG}, [("Ana səhifə","/"),("Media arxivi",None)]))
pathlib.Path("pages-slugs.json").write_text(json.dumps({a["t"]: sl for a, sl in arts}, ensure_ascii=False), encoding="utf-8")
# sitemap
sm = ['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
for loc, pr in [("https://blogstar.az/", "1.0"), ("https://blogstar.az/en/", "0.9")]:
    sm.append(f'  <url><loc>{loc}</loc><lastmod>{TODAY}</lastmod><changefreq>weekly</changefreq><priority>{pr}</priority>\n    <xhtml:link rel="alternate" hreflang="az" href="https://blogstar.az/"/>\n    <xhtml:link rel="alternate" hreflang="en" href="https://blogstar.az/en/"/></url>')
for u in urls:
    pr = "0.9" if u.endswith(("/academy/", "/influencer-marketinq/")) else ("0.7" if "/xidmetler/" in u or u.endswith("/media/") else "0.5")
    sm.append(f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>")
sm.append("</urlset>")
pathlib.Path("sitemap.xml").write_text("\n".join(sm) + "\n", encoding="utf-8")
print(len(urls), "səhifə yaradıldı")
