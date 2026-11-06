"""SEO pages from site data: news articles (AZ/EN), case studies (AZ/EN), AZ + RU guides.
Run after build-pages.py and build-guide.py:  python3 build-seo-pages.py
Reads data dumped from index.html into seo-data.json (NEWS + WORK)."""
import json, re, html, pathlib, datetime

E = lambda s: html.escape(s or "", quote=True)
D = json.loads(pathlib.Path("seo-data.json").read_text(encoding="utf-8"))
TODAY = datetime.date.today().isoformat()
SITE = "https://blogstar.az"
ORG = {"@id": SITE + "/#org", "@type": "Organization", "name": "Blogstar", "url": SITE + "/", "logo": SITE + "/icon-512.png"}
ADDR = {"az": "Bakı, Azərbaycan · online agentlik", "en": "Baku, Azerbaijan · online agency", "ru": "Баку, Азербайджан · онлайн-агентство"}


def slugify(t):
    m = str.maketrans("əƏıIİiöÖüÜşŞçÇğĞ", "eEiIIioOuUsScCgG")
    t = t.translate(m).lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:70]


CSS = """@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300..600&display=swap');
:root{--ink:#000;--muted:#6B6B6B;--rule:#D9D3C9;--bordo:#5C0012;--paper:#EEEAE3;--mist:#E3DED6}
*{box-sizing:border-box}body{margin:0;font:400 17px/1.7 Montserrat,Arial,sans-serif;color:var(--ink);background:var(--paper);-webkit-font-smoothing:antialiased}
a{color:var(--bordo)}.w{max-width:820px;margin:0 auto;padding:0 20px}
header{background:#000}header .w{max-width:1240px;display:flex;justify-content:space-between;align-items:center;height:72px;gap:12px}
header img{height:18px;display:block;filter:invert(1)}header nav{display:flex;gap:18px;align-items:center;flex-wrap:wrap}header nav a{color:#fff;font-size:14px;text-decoration:none;opacity:.8}header nav a.cta{opacity:1;border:1px solid #fff;border-radius:999px;padding:9px 16px}
.bc{font-size:13px;color:var(--muted);margin:44px 0 18px}.bc a{color:inherit;text-decoration:none}
.tag{display:inline-block;font-size:13px;color:var(--bordo);margin-bottom:12px}
h1{font-weight:400;font-size:clamp(32px,5vw,52px);line-height:1.08;letter-spacing:-.03em;margin:0 0 22px}
h2{font-weight:500;font-size:22px;margin:46px 0 14px;letter-spacing:-.01em}
.lead{font-size:19px;color:#383838}
.cov{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:22px;margin:6px 0 28px;display:block}
ul.l{list-style:none;padding:0;margin:0;border-top:1px solid var(--rule)}ul.l li{padding:12px 0;border-bottom:1px solid var(--rule)}
ol.steps{padding-left:22px}ol.steps li{margin:8px 0}
.kp{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin:8px 0}
.kp div{background:#000;color:#fff;border-radius:18px;padding:20px}.kp b{display:block;font:400 34px/1.1 Montserrat;color:#fff}.kp span{font-size:13.5px;color:rgba(255,255,255,.72)}
.chips{display:flex;flex-wrap:wrap;gap:8px;list-style:none;padding:0;margin:14px 0}.chips li{font-size:14px;border:1px solid #000;border-radius:999px;padding:6px 14px}
.note{font-size:13px;color:var(--muted)}
.vids{columns:2;column-gap:24px;padding:0;list-style:none}.vids li{break-inside:avoid;padding:6px 0;font-size:15px}@media(max-width:600px){.vids{columns:1}}
.faq details{border-bottom:1px solid var(--rule);padding:14px 0}.faq summary{cursor:pointer;font-weight:500}.faq p{margin:10px 0 0;color:#383838}
.rel{display:grid;gap:10px;padding:0;list-style:none}.rel a{text-decoration:none}
.box{margin:56px 0;background:#000;color:#fff;border-radius:24px;padding:34px}.box h2{margin-top:0}.box p{color:#C8C8C8}
.btn{display:inline-block;background:#fff;color:#000;text-decoration:none;border-radius:999px;padding:13px 22px}.btn:hover{background:var(--bordo);color:#fff}
.ig{display:inline-block;margin:6px 0 10px;border:1px solid #000;color:#000;text-decoration:none;border-radius:999px;padding:10px 18px;font-size:15px}
footer{border-top:1px solid var(--rule);margin-top:70px;padding:30px 0;font-size:13px;color:var(--muted)}footer .w{max-width:1240px;display:flex;flex-wrap:wrap;gap:18px;justify-content:space-between}footer a{color:inherit;text-decoration:none}"""

UI = {
    "az": {"home": "/", "homeT": "Ana səhifə", "media": "Media mərkəzi", "work": "İşlərimiz", "contact": "Əlaqə", "academy": "Academy",
           "box": "Blogstar ilə işləyək", "boxp": "Kampaniya, təlim və ya əməkdaşlıq barədə sorğunuzu göndərin: info@blogstar.az", "btn": "Sorğu göndərin",
           "rights": "© 2016–2026 Blogstar · Influencer marketinq agentliyi", "watch": "Videoya Instagram-da baxın ↗", "rel": "Digər məqalələr",
           "guide": ("/influencer-marketinq-azerbaycan/", "Azərbaycanda influencer marketinq")},
    "en": {"home": "/en/", "homeT": "Home", "media": "Media centre", "work": "Our work", "contact": "Contact", "academy": "Academy",
           "box": "Work with Blogstar", "boxp": "Send us your request about a campaign, training or partnership: info@blogstar.az", "btn": "Send a brief",
           "rights": "© 2016–2026 Blogstar · Influencer marketing agency", "watch": "Watch on Instagram ↗", "rel": "More articles",
           "guide": ("/en/influencer-marketing-azerbaijan/", "Influencer marketing in Azerbaijan")},
    "ru": {"home": "/en/", "homeT": "Главная", "media": "Медиа", "work": "Наши работы", "contact": "Контакты", "academy": "Academy",
           "box": "Работайте с Blogstar", "boxp": "Отправьте запрос о кампании, обучении или сотрудничестве: info@blogstar.az", "btn": "Отправить запрос",
           "rights": "© 2016–2026 Blogstar · Агентство инфлюенсер-маркетинга", "watch": "Смотреть в Instagram ↗", "rel": "Другие статьи",
           "guide": ("/ru/influencer-marketing-azerbaijan/", "Инфлюенсер-маркетинг в Азербайджане")},
}


def page(path, lang, title, desc, body, lds, crumbs, alts=None, og_image=None, og_type="website"):
    u = UI[lang]
    url = SITE + path
    bc = " / ".join(f'<a href="{h}">{E(n)}</a>' if h else E(n) for n, h in crumbs)
    crumbld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + (h or path)} for i, (n, h) in enumerate(crumbs)]}
    alt = "".join(f'<link rel="alternate" hreflang="{l}" href="{SITE + p}">' for l, p in (alts or {}).items())
    work = "/#isler" if lang == "az" else "/en/#isler"
    contact = "/#elaqe" if lang == "az" else "/en/#elaqe"
    doc = f"""<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{url}">{alt}
<link rel="icon" type="image/png" href="/favicon.png"><meta name="theme-color" content="#000000">
<meta property="og:type" content="{og_type}"><meta property="og:site_name" content="Blogstar"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{SITE + (og_image or '/og.png')}"><meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{json.dumps(lds + [crumbld], ensure_ascii=False)}</script>
<style>{CSS}</style></head><body>
<header><div class="w"><a href="{u['home']}" aria-label="Blogstar"><img src="/logo.png" alt="Blogstar" width="103" height="18"></a><nav><a href="{work}">{u['work']}</a><a href="/academy/">{u['academy']}</a><a class="cta" href="{contact}">{u['contact']}</a></nav></div></header>
<main class="w"><p class="bc">{bc}</p>{body}
<div class="box"><h2>{u['box']}</h2><p>{u['boxp']}</p><a class="btn" href="{contact}">{u['btn']}</a></div></main>
<footer><div class="w"><span>{u['rights']} · {ADDR[lang]}</span><span><a href="{u['home']}">{u['homeT']}</a> · <a href="{u['guide'][0]}">{u['guide'][1]}</a> · <a href="/academy/">Influencer School</a> · <a href="https://www.instagram.com/blogstar.az/">Instagram</a></span></div></footer>
</body></html>"""
    p = pathlib.Path("." + path)
    p.mkdir(parents=True, exist_ok=True)
    (p / "index.html").write_text(doc, encoding="utf-8")
    return url


urls = []
MO = {"Yanvar": 1, "Fevral": 2, "Mart": 3, "Aprel": 4, "May": 5, "İyun": 6, "İyul": 7, "Avqust": 8, "Sentyabr": 9, "Oktyabr": 10, "Noyabr": 11, "Dekabr": 12}


def iso(n):
    m, y = n["d"]["az"].split()
    return f"{y}-{MO[m]:02d}-01"


# ---------- news articles ----------
taken = {p.name for p in pathlib.Path("media").iterdir() if p.is_dir()}
news = []
for n in D["N"]:
    sl = slugify(n["t"]["az"])
    if sl in taken and not pathlib.Path(f"media/{sl}/.news").exists():
        sl = sl + "-" + iso(n)[:4]
    news.append((n, sl))
for i, (n, sl) in enumerate(news):
    rel = [x for x in news if x[1] != sl][:0] + [news[(i + k) % len(news)] for k in (1, 2, 3)]
    for lang in ("az", "en"):
        path = f"/media/{sl}/" if lang == "az" else f"/en/media/{sl}/"
        t, x, d, tag = n["t"][lang], n["x"][lang], n["d"][lang], n["tag"][lang]
        paras = "".join(f"<p>{E(p)}</p>" for p in x.split("\n\n") if p.strip())
        cov = f'<img class="cov" src="{E(n["cover"])}" alt="{E(t)}" loading="eager" width="1200" height="900">' if n.get("cover") else ""
        ig = f'<a class="ig" href="{E(n["ig"])}" target="_blank" rel="noopener">{UI[lang]["watch"]}</a>' if n.get("ig") else ""
        relp = "/media/" if lang == "az" else "/en/media/"
        relh = f'<h2>{UI[lang]["rel"]}</h2><ul class="rel">' + "".join(f'<li><a href="{relp}{s2}/">{E(b["t"][lang])} →</a></li>' for b, s2 in rel) + "</ul>"
        body = f'<span class="tag">{E(tag)} · <time datetime="{iso(n)}">{E(d)}</time></span><h1>{E(t)}</h1>{cov}{paras}{ig}{relh}'
        desc = re.sub(r"\s+", " ", x)[:155].rsplit(" ", 1)[0] + "…"
        ld = {"@context": "https://schema.org", "@type": "Article", "headline": t[:110], "description": desc, "inLanguage": lang,
              "datePublished": iso(n), "dateModified": TODAY, "author": ORG, "publisher": ORG, "mainEntityOfPage": SITE + path}
        if n.get("cover"):
            ld["image"] = SITE + n["cover"]
        if n.get("ig"):
            ld["video"] = {"@type": "VideoObject", "name": t, "description": desc, "embedUrl": n["ig"], "uploadDate": iso(n), "thumbnailUrl": SITE + (n.get("cover") or "/og.png")}
        crumbs = [(UI[lang]["homeT"], UI[lang]["home"]), (UI[lang]["media"], "/#media" if lang == "az" else "/en/#media"), (t, None)]
        urls.append(page(path, lang, f"{t} | Blogstar", desc, body, [ld], crumbs,
                         alts={"az": f"/media/{sl}/", "en": f"/en/media/{sl}/", "x-default": f"/media/{sl}/"}, og_image=n.get("cover"), og_type="article"))
    pathlib.Path(f"media/{sl}/.news").write_text("1")

# ---------- case studies ----------
FACT_EN = {}
for w in D["W"]:
    if not w["reels"]:
        continue
    sl = slugify(w["b"])
    vids = w["reels"]
    for lang in ("az", "en"):
        path = f"/isler/{sl}/" if lang == "az" else f"/en/work/{sl}/"
        what = w["w"][lang] if isinstance(w["w"], dict) else w["w"]
        facts = (w["f"][lang] if isinstance(w.get("f"), dict) else w.get("f")) or []
        k = w.get("kpi") or {}
        n_ig = sum(1 for r in vids if not r.get("tt"))
        n_tt = sum(1 for r in vids if r.get("tt"))
        L = {"az": ("Ümumi baxış", "Reels", "Baxış nisbəti", "Influencer", "Kampaniya videoları", "Kampaniyanın göstəriciləri", "Bütün işlər"),
             "en": ("Total views", "Reels", "View rate", "Influencers", "Campaign videos", "Campaign results", "All work")}[lang]
        kp = ""
        if k:
            cells = [(k.get("v"), L[0]), (str(n_ig), L[1])] + ([(k["r"], L[2])] if k.get("r") else []) + [(k.get("e"), L[3])]
            kp = '<div class="kp">' + "".join(f"<div><b>{E(v)}</b><span>{E(lb)}</span></div>" for v, lb in cells if v) + "</div>"
        note = {"az": "Göstəricilər Instagram və TikTok-un açıq məlumatları və agentliyin kampaniya hesabatları əsasında hesablanıb.",
                "en": "Figures are based on public Instagram and TikTok data and the agency's campaign reports."}[lang]
        chips = "<ul class=\"chips\">" + "".join(f"<li>{E(f)}</li>" for f in facts) + "</ul>" if facts else ""
        vl = "".join(f'<li><a href="{E(r["url"])}" target="_blank" rel="noopener">{E(w["b"])}{" × @" + E(r["who"]) if r.get("who") else ""}{" · TikTok" if r.get("tt") else ""}</a></li>' for r in vids[:40])
        h1 = {"az": f"{w['b']}: influencer marketinq kampaniyası", "en": f"{w['b']}: influencer marketing campaign"}[lang]
        intro = {"az": f"{what}. Blogstar {w['b']} üçün {n_ig} Instagram Reels" + (f" və {n_tt} TikTok videosu" if n_tt else "") + " hazırlayıb və yayımlayıb.",
                 "en": f"{what}. Blogstar produced and published {n_ig} Instagram Reels" + (f" and {n_tt} TikTok videos" if n_tt else "") + f" for {w['b']}."}[lang]
        body = f'<span class="tag">{L[6]}</span><h1>{E(h1)}</h1><p class="lead">{E(intro)}</p>{chips}' + (f"<h2>{L[5]}</h2>{kp}<p class=\"note\">{note}</p>" if kp else "") + f"<h2>{L[4]}</h2><ul class=\"vids\">{vl}</ul>"
        desc = intro[:155]
        ld = {"@context": "https://schema.org", "@type": "CreativeWork", "name": h1, "description": desc, "inLanguage": lang, "creator": ORG,
              "about": {"@type": "Brand", "name": w["b"]}}
        crumbs = [(UI[lang]["homeT"], UI[lang]["home"]), (L[6], "/#isler" if lang == "az" else "/en/#isler"), (w["b"], None)]
        urls.append(page(path, lang, f"{h1} | Blogstar", desc, body, [ld], crumbs,
                         alts={"az": f"/isler/{sl}/", "en": f"/en/work/{sl}/", "x-default": f"/isler/{sl}/"}))

# ---------- guides (AZ + RU); EN guide is built by build-guide.py ----------
G = {
 "az": dict(path="/influencer-marketinq-azerbaycan/",
  title="Azərbaycanda influencer marketinq — Blogstar agentliyi, 2016-cı ildən",
  desc="Azərbaycanda influencer marketinq: strategiya, influencer seçimi, Reels, Stories, TikTok və UGC kampaniyaları, influencer tədbirləri və hesabat. Bakıda 2016-cı ildən fəaliyyət göstərən agentlik.",
  h1="Azərbaycanda influencer marketinq",
  lead="Blogstar 2016-cı ildən Bakıda fəaliyyət göstərən influencer marketinq agentliyidir. Brendləri Azərbaycanın kontent yaradıcıları ilə birləşdirir və hər kampaniyanı strategiyadan yekun hesabata qədər idarə edirik.",
  why="Azərbaycanda influencer marketinq niyə işləyir",
  whyp=["Azərbaycanda istehlakçılar alış qərarlarını getdikcə daha çox sosial mediada verir və izlədikləri insanlara ənənəvi reklamdan daha çox etibar edir. Auditoriyanın tanıdığı yaradıcının tövsiyəsi banner və ya sponsorlu paylaşımın nadir hallarda əldə etdiyi inandırıcılığa malikdir. Prinsipimiz sadədir: insanlar reklama deyil, etibar etdikləri insanlara inanır.",
        "Instagram Azərbaycanda brend əməkdaşlıqları üçün əsas platforma olaraq qalır, TikTok isə gənc auditoriyaya çıxış üçün vacib kanala çevrilib. Effektiv kampaniyalar hər iki platformanı birləşdirir və mesajı hər formata uyğunlaşdırır."],
  how="Kampaniyanı necə qururuq: beş mərhələ",
  steps=[("Analiz.", "Brendi, onun auditoriyasını, rəqibləri və əvvəlki kommunikasiyanı öyrənirik."), ("Strategiya.", "Kampaniyanın məqsədini, əsas mesajları, formatları, vaxtı və uğur göstəricilərini müəyyən edirik."), ("Seçim.", "Influencerləri yalnız izləyici sayına görə deyil, auditoriya uyğunluğuna, kontentin keyfiyyətinə və aktivliyə görə seçirik."), ("İcra.", "Yaradıcılara brif veririk, ssenari və kontenti təsdiqləyirik, paylaşımları koordinasiya edirik."), ("Nəticə.", "Baxış, əhatə və aktivlik məlumatlarını toplayır, şəffaf yekun hesabat təqdim edirik.")],
  fmt="Formatlar", fmts=["Instagram Reels — əhatə və brend tanınması üçün qısa videolar", "Instagram Stories — birbaşa çağırış, link və promo kodlar", "TikTok — gənc auditoriyaya təbii, trendlərə uyğun kontentlə çıxış", "UGC — brendin öz reklamında istifadə edə biləcəyi yaradıcı kontenti", "Influencer tədbirləri — masterklasslar, məhsul təqdimatları və açılışlar", "Affiliate kampaniyalar — satışa bağlı nəticəyə əsaslanan əməkdaşlıq"],
  res="Seçilmiş nəticələr",
  kp=[("13.3M+", "baxış · Trendyol Reels seriyası, 2023-cü ildən tərəfdaş"), ("5M+", "baxış · Birbank, 2023-cü ildən tərəfdaş, 2 tender qalibi"), ("1.7M+", "baxış · Dreame, 2026-cı ildə 3 kampaniya")],
  note="Trendyol və Dreame göstəriciləri Instagram-ın açıq məlumatlarına (oktyabr 2026), Birbank göstəricisi agentliyin kampaniya hesabatlarına əsaslanır.",
  brands="Əməkdaşlıq etdiyimiz brendlər: Trendyol, Birbank, Birbank Biznes, Kapital Bank, Dreame, Yango, Flormar, Lviv Chocolate, Kontakt Home, Garnier.",
  school="Influencer School", schoolp="Blogstar Academy kampaniyalarla yanaşı Azərbaycanda ilk influencer məktəbi olan Influencer School-u həyata keçirir. Proqram şəxsi brend, storytelling, fotoqrafiya və videoqrafiya, AI alətləri, rəqəmsal marketinq və brendlərlə əməkdaşlıq üzrə təlim verir.",
  faqh="Tez-tez verilən suallar",
  faq=[("Azərbaycanda influencer marketinq necə işləyir?", "Brendlər Instagram və TikTok-da yerli kontent yaradıcıları ilə əməkdaşlıq edir; onlar məhsulu və ya xidməti artıq onlara etibar edən auditoriyaya təqdim edir. Blogstar kimi agentlik kampaniyanı planlayır, uyğun influencerləri seçir, istehsalı və paylaşımları idarə edir, nəticələri hesabatla təqdim edir."),
       ("Hansı platformalar daha effektivdir?", "Əksər brendlər üçün əsas formatlar Instagram Reels və Stories, eləcə də TikTok videolarıdır. Reels və TikTok əhatə yaradır, Stories linklər vasitəsilə birbaşa hərəkətə yönəldir, UGC kontenti isə brendin öz reklamında yenidən istifadə oluna bilər."),
       ("Influencerlər necə seçilir?", "Blogstar influencerləri yalnız izləyici sayına görə deyil, auditoriyanın demoqrafiyası və yeri, kontentin keyfiyyəti, aktivlik, əvvəlki brend əməkdaşlıqları və yaradıcının səmimiliyi əsasında seçir."),
       ("Influencer kampaniyası neçəyə başa gəlir?", "Büdcə influencerlərin sayından və əhatəsindən, formatlardan, istehsal tələblərindən və kampaniyanın müddətindən asılıdır. Blogstar brifdən sonra fərdi təklif hazırlayır: sorğunuzu info@blogstar.az ünvanına göndərin."),
       ("Nəticələr necə ölçülür?", "Hər kampaniya baxışları, əhatəni, aktivliyi və baxışların influencerlərin ümumi izləyici sayına nisbətini əks etdirən hesabatla yekunlaşır."),
       ("Blogstar influencerlərə təlim keçirmi?", "Bəli. Blogstar Academy Azərbaycanda ilk influencer məktəbi olan Influencer School-u həyata keçirir.")]),
 "ru": dict(path="/ru/influencer-marketing-azerbaijan/",
  title="Инфлюенсер-маркетинг в Азербайджане — агентство Blogstar, с 2016 года",
  desc="Инфлюенсер-маркетинг в Азербайджане: стратегия, подбор блогеров, кампании в Reels, Stories, TikTok и UGC, мероприятия и отчётность. Агентство в Баку с 2016 года.",
  h1="Инфлюенсер-маркетинг в Азербайджане",
  lead="Blogstar — агентство инфлюенсер-маркетинга в Баку, основанное в 2016 году. Мы связываем бренды с азербайджанскими блогерами и ведём каждую кампанию от стратегии до итогового отчёта.",
  why="Почему инфлюенсер-маркетинг работает в Азербайджане",
  whyp=["Аудитория в Азербайджане всё чаще принимает решения о покупке в социальных сетях и доверяет людям, на которых подписана, больше, чем традиционной рекламе. Рекомендация автора, чей голос аудитория уже знает, обладает убедительностью, которой редко достигает баннер или рекламный пост. Наш принцип прост: люди верят не рекламе, а тем, кому доверяют.",
        "Instagram остаётся ключевой платформой для сотрудничества брендов с блогерами в Азербайджане, а TikTok стал важным каналом охвата молодой аудитории. Эффективные кампании объединяют обе платформы и адаптируют сообщение под каждый формат."],
  how="Как мы строим кампанию: пять этапов",
  steps=[("Анализ.", "Изучаем бренд, его аудиторию, конкурентов и предыдущие коммуникации."), ("Стратегия.", "Определяем цель кампании, ключевые сообщения, форматы, сроки и метрики успеха."), ("Подбор.", "Выбираем блогеров по соответствию аудитории, качеству контента и вовлечённости, а не только по числу подписчиков."), ("Реализация.", "Брифуем авторов, согласовываем сценарии и контент, координируем публикации."), ("Результаты.", "Собираем данные о просмотрах, охвате и вовлечённости и предоставляем прозрачный итоговый отчёт.")],
  fmt="Форматы", fmts=["Instagram Reels — короткие видео для охвата и узнаваемости", "Instagram Stories — прямые призывы к действию, ссылки и промокоды", "TikTok — охват молодой аудитории нативным контентом", "UGC — контент от авторов, который бренд может использовать в своей рекламе", "Мероприятия с блогерами — мастер-классы, презентации и открытия", "Партнёрские (affiliate) кампании — сотрудничество с оплатой за продажи"],
  res="Избранные результаты",
  kp=[("13.3M+", "просмотров · серия Reels для Trendyol, партнёр с 2023 года"), ("5M+", "просмотров · Birbank, партнёр с 2023 года, 2 выигранных тендера"), ("1.7M+", "просмотров · Dreame, 3 кампании в 2026 году")],
  note="Показатели Trendyol и Dreame основаны на открытых данных Instagram (октябрь 2026), показатель Birbank — на отчётах агентства.",
  brands="Бренды, с которыми мы работаем: Trendyol, Birbank, Birbank Biznes, Kapital Bank, Dreame, Yango, Flormar, Lviv Chocolate, Kontakt Home, Garnier.",
  school="Influencer School", schoolp="Помимо кампаний, Blogstar Academy проводит Influencer School — первую школу инфлюенсеров в Азербайджане: личный бренд, сторителлинг, фото и видео, AI-инструменты, digital-маркетинг и работа с брендами.",
  faqh="Частые вопросы",
  faq=[("Как работает инфлюенсер-маркетинг в Азербайджане?", "Бренды сотрудничают с местными авторами в Instagram и TikTok, которые представляют продукт аудитории, уже доверяющей им. Агентство Blogstar планирует кампанию, подбирает блогеров, управляет производством и публикациями и отчитывается о результатах."),
       ("Какие платформы наиболее эффективны?", "Для большинства брендов основные форматы — Instagram Reels и Stories, а также видео в TikTok."),
       ("Как подбираются блогеры?", "По соответствию аудитории (демография, география), качеству контента, вовлечённости, предыдущим коллаборациям и искренности автора — а не только по числу подписчиков."),
       ("Сколько стоит кампания с блогерами?", "Бюджет зависит от количества и охвата блогеров, форматов, требований к производству и длительности кампании. Blogstar готовит индивидуальное предложение после брифа: info@blogstar.az."),
       ("Как измеряются результаты?", "Каждая кампания завершается отчётом о просмотрах, охвате, вовлечённости и соотношении просмотров к суммарной аудитории блогеров."),
       ("Обучает ли Blogstar блогеров?", "Да. Blogstar Academy проводит Influencer School — первую школу инфлюенсеров в Азербайджане.")]),
}
for lang, g in G.items():
    body = (f'<span class="tag">{"Bələdçi · Bakı, Azərbaycan" if lang == "az" else "Гид · Баку, Азербайджан"}</span><h1>{E(g["h1"])}</h1><p class="lead">{E(g["lead"])}</p>'
            f'<h2>{E(g["why"])}</h2>' + "".join(f"<p>{E(p)}</p>" for p in g["whyp"]) +
            f'<h2>{E(g["how"])}</h2><ol class="steps">' + "".join(f"<li><b>{E(a)}</b> {E(b)}</li>" for a, b in g["steps"]) + "</ol>" +
            f'<h2>{E(g["fmt"])}</h2><ul class="l">' + "".join(f"<li>{E(x)}</li>" for x in g["fmts"]) + "</ul>" +
            f'<h2>{E(g["res"])}</h2><div class="kp">' + "".join(f"<div><b>{a}</b><span>{E(b)}</span></div>" for a, b in g["kp"]) + f'</div><p class="note">{E(g["note"])}</p><p>{E(g["brands"])}</p>' +
            f'<h2>{E(g["school"])}</h2><p>{E(g["schoolp"])} <a href="/academy/">→</a></p>' +
            f'<h2>{E(g["faqh"])}</h2><div class="faq">' + "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in g["faq"]) + "</div>")
    lds = [{"@context": "https://schema.org", "@type": "Service", "name": g["h1"], "serviceType": "Influencer marketing", "areaServed": {"@type": "Country", "name": "Azerbaijan"}, "provider": ORG, "inLanguage": lang},
           {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": lang, "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in g["faq"]]}]
    alts = {"az": G["az"]["path"], "en": "/en/influencer-marketing-azerbaijan/", "ru": G["ru"]["path"], "x-default": G["az"]["path"]}
    urls.append(page(g["path"], lang, g["title"], g["desc"], body, lds, [(UI[lang]["homeT"], UI[lang]["home"]), (g["h1"], None)], alts=alts))

# ---------- sitemap ----------
sm = pathlib.Path("sitemap.xml").read_text(encoding="utf-8")
add = "".join(f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod><priority>{'0.9' if 'azerba' in u else '0.7' if ('/isler/' in u or '/work/' in u) else '0.6'}</priority></url>\n" for u in urls if u not in sm)
sm = sm.replace("</urlset>", add + "</urlset>")
pathlib.Path("sitemap.xml").write_text(sm, encoding="utf-8")
print(len(urls), "SEO səhifəsi")
