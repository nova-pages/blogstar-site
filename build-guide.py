"""EN landing page: /en/influencer-marketing-azerbaijan/  (python3 build-guide.py)"""
import json, pathlib, html, datetime
E = lambda s: html.escape(s, quote=True)
URL = "https://blogstar.az/en/influencer-marketing-azerbaijan/"
TITLE = "Influencer Marketing in Azerbaijan — Blogstar, Agency Since 2016"
DESC = "Influencer marketing in Azerbaijan with Blogstar: strategy, influencer selection, Reels, Stories, TikTok and UGC campaigns, events and reporting. Baku-based agency since 2016."
FAQ = [
("How does influencer marketing work in Azerbaijan?",
 "Brands partner with local content creators on Instagram and TikTok, who present a product or service to an audience that already trusts them. In Azerbaijan, Instagram remains the leading platform for this, with TikTok growing quickly. An agency such as Blogstar plans the campaign, selects suitable influencers, manages production and publication, and reports the results."),
("Which platforms are most effective?",
 "For most brands the core formats are Instagram Reels and Stories, complemented by TikTok videos. Reels and TikTok build reach, Stories drive direct action through links, and UGC content can be reused in a brand's own advertising."),
("How are influencers selected?",
 "Blogstar selects influencers on the basis of audience fit rather than follower count alone: audience demographics and location, content quality, engagement, previous brand collaborations and the authenticity of the creator's voice."),
("How much does an influencer campaign cost?",
 "The budget depends on the number and reach of influencers, the formats, production requirements and the length of the campaign. Blogstar prepares an individual proposal after a brief; send your request to info@blogstar.az."),
("How are results measured?",
 "Every campaign ends with a report covering views, reach, engagement and the ratio of views to the participating influencers' combined followers. For example, the Trendyol Reels series reached 13.3M+ views and the Dreame campaign 1.7M+ views on public Instagram data."),
("Does Blogstar train influencers?",
 "Yes. Blogstar Academy runs Influencer School, the first influencer school in Azerbaijan, covering personal branding, content and storytelling, photography and videography, AI tools, digital marketing and working with brands."),
]
body = f"""
<p class="bc"><a href="/en/">Home</a> / Influencer marketing in Azerbaijan</p>
<span class="tag">Guide · Baku, Azerbaijan</span>
<h1>Influencer marketing in Azerbaijan</h1>
<p class="lead">Blogstar is a Baku-based influencer marketing agency, founded in 2016. We connect brands with Azerbaijani content creators and manage every campaign from strategy to the final report.</p>

<h2>Why influencer marketing works in Azerbaijan</h2>
<p>Audiences in Azerbaijan increasingly make purchasing decisions on social media, and they place more trust in people they follow than in conventional advertising. A recommendation from a creator whose voice the audience already knows carries a credibility that a banner or a paid post rarely achieves. Our principle is simple: people do not believe advertising — they believe the people they trust.</p>
<p>Instagram remains the leading platform for brand collaborations in Azerbaijan, while TikTok has become an essential channel for reach among younger audiences. Effective campaigns combine both and adapt the message to each format.</p>

<h2>How we run a campaign: five stages</h2>
<ol class="steps">
<li><b>Analysis.</b> We study the brand, its audience, competitors and previous communication.</li>
<li><b>Strategy.</b> We define the campaign goal, key messages, formats, timing and success metrics.</li>
<li><b>Selection.</b> We choose influencers by audience fit, content quality and engagement, not follower count alone.</li>
<li><b>Execution.</b> We brief creators, approve scripts and content, and coordinate publication.</li>
<li><b>Results.</b> We collect views, reach and engagement data and deliver a transparent final report.</li>
</ol>

<h2>Formats</h2>
<ul class="l">
<li><b>Instagram Reels</b> — short-form video for reach and brand awareness.</li>
<li><b>Instagram Stories</b> — direct calls to action, links and promotional codes.</li>
<li><b>TikTok</b> — reach among younger audiences through native, trend-led content.</li>
<li><b>UGC</b> — creator-made content that brands can reuse in their own advertising.</li>
<li><b>Influencer events</b> — masterclasses, product launches and openings with influencers.</li>
<li><b>Affiliate campaigns</b> — performance-based collaboration tied to sales.</li>
</ul>

<h2>Selected results</h2>
<div class="kp">
<div><b>13.3M+</b><span>views · Trendyol Reels series, partner since 2023</span></div>
<div><b>5M+</b><span>views · Birbank, partner since 2023, two tenders won</span></div>
<div><b>1.7M+</b><span>views · Dreame, three campaigns in 2026</span></div>
</div>
<p class="note">Trendyol and Dreame figures are based on public Instagram data (October 2026); the Birbank figure is based on the agency's campaign reports.</p>
<p>Brands we have worked with include Trendyol, Birbank, Birbank Biznes, Kapital Bank, Dreame, Yango, Flormar, Lviv Chocolate, Kontakt Home and Garnier. <a href="/en/#isler">See our work →</a></p>

<h2>Influencer School</h2>
<p>Alongside campaigns, Blogstar Academy runs Influencer School — the first influencer school in Azerbaijan. The programme trains new creators in personal branding, storytelling, photography and videography, AI tools, digital marketing and working with brands. <a href="/academy/">About the programme →</a></p>

<h2>Frequently asked questions</h2>
<div class="faq">{"".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q,a in FAQ)}</div>
"""
ld = [
 {"@context":"https://schema.org","@type":"WebPage","name":TITLE,"url":URL,"inLanguage":"en","description":DESC,"about":{"@id":"https://blogstar.az/#org"}},
 {"@context":"https://schema.org","@type":"Service","name":"Influencer marketing in Azerbaijan","serviceType":"Influencer marketing","areaServed":{"@type":"Country","name":"Azerbaijan"},"provider":{"@id":"https://blogstar.az/#org","@type":"Organization","name":"Blogstar","url":"https://blogstar.az/"}},
 {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]},
 {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://blogstar.az/en/"},{"@type":"ListItem","position":2,"name":"Influencer marketing in Azerbaijan","item":URL}]}]
CSS = """@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300..600&display=swap');
:root{--ink:#000;--muted:#6B6B6B;--rule:#D9D3C9;--bordo:#5C0012;--paper:#EEEAE3;--mist:#E3DED6}
*{box-sizing:border-box}body{margin:0;font:400 17px/1.7 Montserrat,Arial,sans-serif;color:var(--ink);background:var(--paper);-webkit-font-smoothing:antialiased}
a{color:var(--bordo)}.w{max-width:820px;margin:0 auto;padding:0 20px}
header{background:#000}header .w{max-width:1240px;display:flex;justify-content:space-between;align-items:center;height:72px}
header img{height:18px;display:block;filter:invert(1)}header nav a{color:#fff;font-size:14px;text-decoration:none;margin-left:22px;opacity:.8}header nav a.cta{opacity:1;border:1px solid #fff;border-radius:999px;padding:9px 16px}
.bc{font-size:13px;color:var(--muted);margin:44px 0 18px}.bc a{color:inherit;text-decoration:none}
.tag{display:inline-block;font-size:13px;color:var(--bordo);margin-bottom:12px}
h1{font-weight:400;font-size:clamp(34px,5vw,54px);line-height:1.06;letter-spacing:-.03em;margin:0 0 22px}
h2{font-weight:500;font-size:22px;margin:48px 0 14px;letter-spacing:-.01em}
.lead{font-size:19px;color:#383838}
ol.steps{padding-left:22px}ol.steps li{margin:8px 0}
ul.l{list-style:none;padding:0;margin:0;border-top:1px solid var(--rule)}ul.l li{padding:12px 0;border-bottom:1px solid var(--rule)}
.kp{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}@media(max-width:640px){.kp{grid-template-columns:1fr}}
.kp div{background:#000;color:#fff;border-radius:18px;padding:20px}.kp b{display:block;font:400 34px/1.1 Montserrat;color:#fff}.kp span{font-size:13.5px;color:rgba(255,255,255,.72)}
.note{font-size:13px;color:var(--muted)}
.faq details{border-bottom:1px solid var(--rule);padding:14px 0}.faq summary{cursor:pointer;font-weight:500}.faq p{margin:10px 0 0;color:#383838}
.box{margin:56px 0;background:#000;color:#fff;border-radius:24px;padding:34px}.box h2{margin-top:0}.box p{color:#C8C8C8}
.btn{display:inline-block;background:#fff;color:#000;text-decoration:none;border-radius:999px;padding:13px 22px}.btn:hover{background:var(--bordo);color:#fff}
footer{border-top:1px solid var(--rule);margin-top:70px;padding:30px 0;font-size:13px;color:var(--muted)}footer .w{max-width:1240px;display:flex;flex-wrap:wrap;gap:18px;justify-content:space-between}footer a{color:inherit;text-decoration:none}"""
doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(TITLE)}</title><meta name="description" content="{E(DESC)}">
<link rel="canonical" href="{URL}"><link rel="alternate" hreflang="en" href="{URL}"><link rel="alternate" hreflang="az" href="https://blogstar.az/influencer-marketinq-azerbaycan/"><link rel="alternate" hreflang="ru" href="https://blogstar.az/ru/influencer-marketing-azerbaijan/"><link rel="alternate" hreflang="x-default" href="https://blogstar.az/influencer-marketinq-azerbaycan/">
<link rel="icon" type="image/png" href="/favicon.png"><meta name="theme-color" content="#000000">
<meta property="og:type" content="article"><meta property="og:site_name" content="Blogstar"><meta property="og:title" content="{E(TITLE)}"><meta property="og:description" content="{E(DESC)}"><meta property="og:url" content="{URL}"><meta property="og:image" content="https://blogstar.az/og.png"><meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<style>{CSS}</style></head><body>
<header><div class="w"><a href="/en/" aria-label="Blogstar"><img src="/logo.png" alt="Blogstar"></a><nav><a href="/en/#isler">Work</a><a href="/academy/">Academy</a><a class="cta" href="/en/#elaqe">Contact</a></nav></div></header>
<main class="w">{body}
<div class="box"><h2>Plan your campaign with Blogstar</h2><p>Tell us about your brand, goals and timing — we will prepare an influencer marketing proposal for the Azerbaijani market. info@blogstar.az</p><a class="btn" href="/en/#elaqe">Send a brief</a></div></main>
<footer><div class="w"><span>© 2016–2026 Blogstar · Influencer marketing agency · Baku, Azerbaijan · online agency</span><span><a href="/en/">Home</a> · <a href="/academy/">Influencer School</a> · <a href="https://www.instagram.com/blogstar.az/">Instagram</a></span></div></footer>
</body></html>"""
p = pathlib.Path("en/influencer-marketing-azerbaijan"); p.mkdir(parents=True, exist_ok=True)
(p / "index.html").write_text(doc, encoding="utf-8")
sm = pathlib.Path("sitemap.xml").read_text(encoding="utf-8")
if URL not in sm:
    sm = sm.replace("</urlset>", f"  <url><loc>{URL}</loc><lastmod>{datetime.date.today().isoformat()}</lastmod><priority>0.9</priority></url>\n</urlset>")
    pathlib.Path("sitemap.xml").write_text(sm, encoding="utf-8")
print("guide ok")
