"""Build the nine static GitHub Pages routes and sitemap from site-config.json."""
import json
from html import escape
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
CONFIG = json.loads((ROOT / "site-config.json").read_text(encoding="utf-8-sig"))
BASE = CONFIG["siteUrl"].rstrip("/") + "/"
BRAND = "Producing Human Encounters"
TAGLINE = "Extraordinary ordinary people. Real stories. Shared wisdom. Human possibilities."
CITIES = {
    "Mullumbimby": "The inaugural series begins in the Northern Rivers. Across four planned gatherings, we aim to invite 50 or more remarkable people to share what life has taught them.",
    "Sydney": "A gathering for people whose experiences rarely cross paths, bringing stories from across Sydney into the same room.",
    "Canberra": "A room for Canberra’s many kinds of knowledge, from the ideas that shape public life to the lessons learned quietly in families and communities.",
    "Melbourne": "A gathering for the stories Melbourne makes room for, across neighbourhoods, creative lives, trades and generations.",
    "Adelaide": "An invitation to bring the stories carried through Adelaide’s neighbourhoods, workshops and community spaces into conversation.",
    "Perth": "A gathering for the people who make and remake community in Perth, and for the wisdom they have gathered along the way.",
    "Cairns": "A Far North Queensland gathering shaped by the people who live, work, create and care in Cairns and the communities around it.",
    "Brisbane": "An evening for the ideas, experiences and quieter contributions that shape life across Brisbane.",
}
ACTIONS = {
    "I'd Love to Attend": "I’d love to hear when gathering details are announced.\n\nMy name: \nMy suburb or town (optional): ",
    "I'd Love to Participate": "I’d love to be considered as a featured guest.\n\nMy name: \nMy suburb or town: \nA little about what I’d like to share: ",
    "Nominate Someone Extraordinary": "I’d like to nominate someone for a gathering.\n\nMy name: \nWho I’m nominating and why: ",
}


def email_link(label, place, body):
    subject = quote(f"PHE — {label} — {place}")
    return f"mailto:{escape(CONFIG['contactEmail'])}?subject={subject}&amp;body={quote('Hello, ' + body)}"


def city_link(city, prefix, current=None):
    active = ' aria-current="page"' if city == current else ""
    return f'<a href="{prefix}cities/{city.lower()}/"{active}>The {city} Series</a>'


def poster_filename(city):
    return f"PHE_{city or 'National'}_Poster.png"


def build_page(city=None):
    slug = city.lower() if city else "national"
    prefix = "../../" if city else "./"
    assets = prefix + "assets/"
    route = f"cities/{slug}/" if city else ""
    url = BASE + route
    place = city or "National"
    title = f"The {city} Series | {BRAND}" if city else f"{BRAND} | Australian Gathering Series"
    description = (
        f"Be part of The {city} Series. Share a story, nominate someone extraordinary or express interest in attending a live gathering in {city}."
        if city else "Be part of something extraordinary. Explore eight Australian city series, express interest in attending, share your story or nominate someone."
    )
    preview = BASE + f"assets/posters/{slug}-final-social.jpg"
    metadata = {
        "og:type": "website", "og:url": url, "og:site_name": BRAND, "og:locale": "en_AU",
        "og:title": title, "og:description": description, "og:image": preview,
        "og:image:type": "image/jpeg", "og:image:width": "1200", "og:image:height": "630",
        "og:image:alt": f"Producing Human Encounters and {place} series lettering above people gathered in conversation",
    }
    tags = "\n".join(f'<meta property="{key}" content="{escape(value)}">' for key, value in metadata.items())
    structured = json.dumps({
        "@context": "https://schema.org",
        "@type": "WebPage" if city else "WebSite",
        "name": f"The {city} Series" if city else BRAND,
        "description": description, "url": url, "inLanguage": "en-AU", "image": preview,
        **({"isPartOf": {"@type": "WebSite", "name": BRAND, "url": BASE}} if city else {}),
    }, ensure_ascii=False)
    nav_cities = "".join(city_link(name, prefix, city) for name in CITIES)
    home_current = '' if city else ' aria-current="page"'
    home = prefix
    menu_target = prefix + "#cities"
    intro = CITIES[city] if city else "People who have built, overcome, discovered, created and contributed."
    poster = f'''
    <figure class="poster">
      <img src="{assets}posters/{slug}.webp" alt="Approved Producing Human Encounters poster for {f'The {city} Series' if city else 'the national series'}, with portraits and people gathered in conversation" {'fetchpriority="high"' if city else 'loading="lazy"'}>
      <figcaption><a href="{assets}posters/{poster_filename(city)}" download>Download the approved poster (PNG)</a>
      <span>The poster QR points to our planned .com address. Share this page link for now.</span></figcaption>
    </figure>'''
    if city:
        hero = f'''
    <section class="city-hero">
      <div class="wrap city-hero-grid">
        <div><p class="eyebrow">{BRAND}</p><h1>The {city} Series</h1>
        <p class="tagline">{TAGLINE}</p><p class="city-intro">{intro}</p>
        <a class="button" href="#participate">Be Part of Something Extraordinary</a>
        <a class="text-link" href="{menu_target}">Explore all cities</a></div>
{poster}
      </div>
    </section>'''
    else:
        hero = f'''
    <section class="hero national-hero" aria-labelledby="title">
      <img class="portrait left" src="{assets}national-left.webp" alt="" fetchpriority="high">
      <img class="portrait right" src="{assets}national-right.webp" alt="" fetchpriority="high">
      <div class="hero-copy">
        <p class="eyebrow ruled">An Australian gathering series</p>
        <h1 id="title">Producing <em>Human</em> Encounters</h1>
        <p class="tagline">{TAGLINE}</p>
        <p class="hero-line">Every community is home to extraordinary people.</p>
        <p class="national-intro">{intro}</p>
        <a class="button" href="#participate">Be Part of Something Extraordinary</a>
        <a class="text-link" href="#cities">Explore Our Cities ↓</a>
      </div>
    </section>'''
    city_tiles = "".join(f'''
      <a class="city-tile" href="{prefix}cities/{name.lower()}/">
        <img src="{assets}posters/{name.lower()}-tile.webp" alt="" loading="lazy">
        <span>The {name} Series <span aria-hidden="true">↗</span></span>
      </a>''' for name in CITIES)
    gallery = f'''
    <section id="cities" class="section wrap">
      <p class="eyebrow">Across Australia</p><h2>Our Cities</h2>
      <div class="city-gallery">{city_tiles}</div>
    </section>''' if not city else ""
    related = "".join(city_link(name, prefix) for name in CITIES if name != city)
    closing = f'''
    <section class="section wrap" aria-labelledby="other-cities">
      <p class="eyebrow">Across Australia</p><h2 id="other-cities">Explore other cities</h2>
      <div class="related">{related}</div>
    </section>''' if city else ""
    contact = "".join(f'<a href="{email_link(label, place, body)}">{escape(label)} <span aria-hidden="true">↗</span></a>' for label, body in ACTIONS.items())
    partner = email_link("Venue and Community Partners", place, "I’d like to talk about working with Producing Human Encounters.\n\nMy name and organisation: \nMy idea: ")
    return f'''<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(description)}">
<link rel="canonical" href="{escape(url)}">
<meta name="robots" content="index, follow, max-image-preview:large">
{tags}
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#073b40">
<link rel="icon" href="{assets}phe_icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{assets}apple-touch-icon.png">
<link rel="stylesheet" href="{prefix}style.css">
<script type="application/ld+json">{structured}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <a class="brand" href="{home}"><img src="{assets}phe_brand_lockup.svg" alt="{BRAND} home"></a>
  <nav aria-label="Main navigation">
    <a href="{home}"{home_current}>Home</a>
    <a href="#experience">The Experience</a>
    <details class="city-menu"><summary>Our Cities</summary><div><a href="{menu_target}">All cities</a>{nav_cities}</div></details>
    <a class="nav-invite" href="#participate">Get Involved</a>
  </nav>
</header>
<main id="main">
{hero}
{gallery}
  <section class="section experience" id="experience">
    <div class="wrap idea">
      <div><p class="eyebrow">The experience</p><h2>Real stories. Shared wisdom.</h2></div>
      <div class="prose">
        <p>Each gathering brings together around 12–15 featured people from different walks of life, alongside an audience. Guests share the stories, knowledge and experience they’ve gained. Then the room opens to conversation, learning and connection.</p>
        <p>We welcome people from education, business, community, the arts, innovation, care, the environment and philosophy, and anyone with remarkable life experience to share.</p>
      </div>
    </div>
  </section>
  <section class="philosophy" aria-label="Our philosophy">
    <img src="{assets}national-gathering.webp" alt="" loading="lazy">
    <blockquote>“Sometimes the most extraordinary thing we can do is recognise the extraordinary in one another.”</blockquote>
  </section>
  <section class="invitation section" id="participate">
    <div class="wrap invite-grid">
      <div><p class="eyebrow">Get involved{f' / {city}' if city else ''}</p><h2>Be Part of Something Extraordinary</h2>
      <p class="tagline">Everyone has a story. Some stories deserve to travel further.</p>
      <p>Come to listen, share something you’ve lived or introduce us to someone whose story deserves to be heard.</p></div>
      <div class="contact-actions">{contact}
        <p>These links open a draft in your email app. Review it and send it when you’re ready.</p>
        <a class="partner-link" href="{partner}">Venue and community partner enquiries</a>
      </div>
    </div>
  </section>
{closing}
</main>
<footer><div class="wrap footer-inner">
  <div><p class="brand">{BRAND}</p><p>{TAGLINE}</p></div>
  <a href="{home}">National homepage</a>
</div></footer>
</body>
</html>
'''


for city in (None, *CITIES):
    folder = ROOT / "cities" / city.lower() if city else ROOT
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "index.html").write_text(build_page(city), encoding="utf-8")

urls = [BASE, *(f"{BASE}cities/{city.lower()}/" for city in CITIES)]
entries = "\n".join(f"  <url><loc>{escape(url)}</loc></url>" for url in urls)
(ROOT / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    f"{entries}\n</urlset>\n",
    encoding="utf-8",
)
