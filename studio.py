"""Shared page shell and data-driven product showcase. No runtime dependencies."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PRODUCTS = json.loads((ROOT / 'products.json').read_text())
PUBLIC_PRODUCTS = [a for a in PRODUCTS if a.get('published', False)]
E = html.escape


def legacy_apps():
    return [dict(a, name={'en': a['name'], 'ru': a['name']}, tag={'en': a['description'], 'ru': a['description']}) for a in PRODUCTS]


def href(a):
    return a.get('external') or '/' + a['slug'] + '/'


def phone(a, detail=False, eager=False):
    src = a.get('detail_screen', a['screen']) if detail else a['screen']
    return f'<img class="device" src="{src}" alt="{E(a["name"])} app interface" width="368" height="800" loading="{"eager" if eager else "lazy"}" decoding="async">'


def shell(path, title, body, desc='', sub='', kind='document'):
    owner = next((a for a in PRODUCTS if path.startswith('/' + a['slug'] + '/')), None)
    if owner and not owner.get('published', False):
        return
    canonical = 'https://kohone.net' + path
    content = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc or title)}"><meta name="theme-color" content="#f7f8f2">
<link rel="canonical" href="{canonical}"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc or title)}"><meta property="og:type" content="website"><meta property="og:url" content="{canonical}">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/site.css"><script src="/assets/site.js" defer></script></head>
<body class="{kind}"><a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="wide header-row"><a class="brand" href="/" aria-label="Kohone home"><span class="brand-mark" aria-hidden="true">k</span>kohone<span class="brand-dot">.</span></a><nav aria-label="Main navigation"><a href="/#apps">The apps</a><a href="/#about">The maker</a><a class="nav-contact" href="mailto:support@kohone.net">Say hello <span aria-hidden="true">↗</span></a></nav></div></header>
{('<div class="wide subbar">'+sub+'</div>') if sub else ''}
<main id="main">{body}</main>
<footer class="site-footer"><div class="wide"><div class="footer-top"><a class="brand" href="/">kohone.</a><p>Independent apps.<br>Considered down to the details.</p><a href="mailto:support@kohone.net">Let’s talk <span aria-hidden="true">↗</span><small>support@kohone.net</small></a></div><div class="footer-bottom"><span>© 2026 Maks Beskrovnyi</span><a href="/#apps">All apps</a><span>Made with care. Built to be used.</span></div></div></footer></body></html>'''
    rel = path.lstrip('/')
    if not rel or rel.endswith('/'): rel += 'index.html'
    elif not rel.endswith('.html'): rel += '.html'
    out = ROOT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content)


def write_page(path, title, body, desc='', sub=''):
    product = next((a for a in PRODUCTS if path == '/' + a['slug'] + '/' and not a.get('external')), None)
    if product and product['slug'] == 'fair-dice':
        shell(path, title, '<div class="fair-landing wood">'+body+'</div>', desc, sub, kind='product')
    elif product:
        product_page(product)
    else:
        shell(path, title, '<article class="document-body">'+body+'</article>', desc, sub)


def card(a):
    return f'''<a class="product-card {a['theme']}" href="{href(a)}" data-category="{E(a['category'])}" data-search="{E((a['name']+' '+a['description']+' '+a['category']).lower())}">
<div class="card-art"><span class="card-category">{E(a['category'])}</span>{phone(a)}<span class="card-arrow" aria-hidden="true">↗</span></div>
<div class="card-info"><img src="{a['icon']}" alt="" width="48" height="48" loading="lazy"><div><h3>{E(a['short'])}</h3><p>{E(a['tag'])}</p></div></div><div class="card-status">{E(a['status'])}<span>{'Visit website ↗' if a.get('external') else 'Explore app →'}</span></div></a>'''


def home():
    featured = [a for a in PUBLIC_PRODUCTS if a.get('featured')] or PUBLIC_PRODUCTS
    first = featured[0]
    second = featured[1] if len(featured) > 1 else first
    floating = next((a for a in featured[2:] if a.get('external')), featured[-1])
    categories = list(dict.fromkeys(a['category'] for a in PUBLIC_PRODUCTS))
    filters = ''.join(f'<button type="button" data-filter="{E(c)}" aria-pressed="false">{E(c)}</button>' for c in categories)
    tools = f'''<div class="catalog-tools" hidden><div class="filters" role="group" aria-label="Filter apps by category"><button type="button" data-filter="All" aria-pressed="true">All apps <span>{len(PUBLIC_PRODUCTS):02}</span></button>{filters}</div><label class="search"><input type="search" placeholder="Find an app…" autocomplete="off" aria-label="Search apps"></label></div>''' if len(PUBLIC_PRODUCTS) > 4 else ''
    body = f'''<section class="home-hero wide"><div class="hero-copy"><p class="eyebrow"><span class="live-dot"></span> INDEPENDENT APPS, THOUGHTFULLY MADE</p><h1>Small details.<br><span class="serif">Better apps.</span></h1><p class="hero-description">For your next move, your everyday rhythms,<br class="desktop-break"> and the things that make life yours.</p><a class="button primary" href="#apps">Find your next app <span aria-hidden="true">↗</span></a><div class="maker-sign"><span class="maker-initials">mb.</span><span>Designed & built by<br><strong>Maks Beskrovnyi</strong></span></div></div>
<div class="hero-stage" aria-label="A selection of apps by Maks Beskrovnyi"><span class="orbit orbit-one"></span><span class="orbit orbit-two"></span><span class="stage-note note-top">A LITTLE MORE THOUGHT<br>IN EVERY TAP.</span><a class="hero-phone back" href="{href(second)}" aria-label="Explore {E(second['name'])}">{phone(second,eager=True)}</a><a class="hero-phone front" href="{href(first)}" aria-label="Explore {E(first['name'])}">{phone(first,eager=True)}</a><a class="floating-icon" href="{href(floating)}" aria-label="Explore {E(floating['name'])}"><img src="{floating['icon']}" alt="" width="74" height="74"></a><span class="stage-note note-bottom"><span class="tiny-star">✳</span> MADE FOR REAL LIFE.</span></div></section>
<div class="principle-strip wide"><span>Built for iPhone</span><span>Purpose in every feature</span><span>A person behind every app</span></div>
<section class="wide collection" id="apps"><div class="section-heading"><div><p class="eyebrow">THE COLLECTION</p><h2>A few good apps.<br><span class="serif">A world of possibilities.</span></h2></div><p>Different interests. The same care.<br>Explore what I’m working on.</p></div>
{tools}
<p class="results sr-only" aria-live="polite"></p><div class="product-grid{' collection-small' if len(PUBLIC_PRODUCTS) <= 2 else ''}">{''.join(card(a) for a in PUBLIC_PRODUCTS)}</div><p class="empty-state" hidden>No apps found. Try another name or category.</p>
</section>
<section class="maker-section" id="about"><div class="wide maker-grid"><div><p class="eyebrow">THE PERSON BEHIND THE PIXELS</p><h2>One developer.<br><span class="serif">Many little obsessions.</span></h2></div><div><p class="maker-lead">Hi, I’m Maks. I build apps for people who care about the details.</p><p>The right move on a backgammon board. A clearer picture of your own patterns. Small things deserve good software, too.</p><a class="text-link" href="mailto:support@kohone.net">Have a question? You’ll reach me. ↗</a></div></div><div class="wide maker-values"><div><span>01</span><h3>A reason to exist.</h3><p>Each app starts with a particular problem and the person trying to solve it.</p></div><div><span>02</span><h3>Care below the surface.</h3><p>From verifiable dice to a clearer picture of your own patterns, the details are part of the product.</p></div><div><span>03</span><h3>Always a work in progress.</h3><p>A growing collection, built and refined one thoughtful app at a time.</p></div></div></section>'''
    shell('/', 'Kohone — Thoughtfully made apps by Maks Beskrovnyi', body, 'Independent iPhone apps and games by Maks Beskrovnyi. Explore Cycle Ally and Backgammon: Fair Dice.', kind='home')


def product_page(a):
    base = '/' + a['slug'] + '/'
    cta = f'<a class="button primary" href="{E(a["store"])}">Download on the App Store ↗</a>' if a.get('store') else '<span class="release-status"><span class="live-dot"></span> In development · Coming to the App Store</span>'
    special = '<a class="text-link" href="/fair-dice/verify">Verify a game’s dice →</a><a class="text-link" href="/fair-dice/dice-report">Read the dice report →</a>' if a['slug']=='fair-dice' else ''
    features = ''.join(f'<article><span class="feature-number">0{i+1}</span><h3>{E(title)}</h3><p>{E(text)}</p></article>' for i,(title,text) in enumerate(a['features']))
    related = [p for p in PUBLIC_PRODUCTS if p['slug']!=a['slug']][:3]
    body = f'''<div class="product-page {a['theme']}"><div class="wide product-nav"><a href="/#apps">← All apps</a><span>{E(a['short'])}</span><a href="{base}support">Support ↗</a></div>
<section class="wide product-hero"><div><div class="product-identity"><img src="{a['icon']}" alt="" width="54" height="54"><span>{E(a['name'])}<small>{E(a['category'])} / Made for iPhone</small></span></div><h1>{E(a['headline']).replace(chr(10),'<br>')}</h1><p class="hero-description">{E(a['description'])}</p>{cta}<div class="product-facts">{''.join(f'<span>{E(x)}</span>' for x in a['facts'])}</div></div><div class="product-stage"><span class="orbit"></span>{phone(a,eager=True)}<span class="stage-caption">A CLOSER LOOK AT {E(a['short'].upper())}</span></div></section></div>
<section class="wide story"><div class="story-image {a['theme']}">{phone(a,detail=True)}</div><div><p class="eyebrow">MADE FOR THE WAY YOU USE IT</p><h2>{E(a['story_title'])}</h2><p>{E(a['story'])}</p><div class="story-links">{special}</div></div></section>
<section class="wide feature-section"><p class="eyebrow">THE DETAILS THAT MAKE A DIFFERENCE</p><div class="feature-grid">{features}</div></section>
<section class="wide practical"><div><p class="eyebrow">SIMPLE & UPFRONT</p><h2>Good to know.</h2></div><div><details open><summary>What does it cost?</summary><p>{E(a['pricing'])}</p></details><details><summary>What happens to my data?</summary><p>{E(a['privacy'])}</p><a href="{base}privacy">Read the privacy policy →</a></details><details><summary>How can I get help?</summary><p>Email <a href="mailto:support@kohone.net">support@kohone.net</a>. You’ll hear directly from the developer.</p><a href="{base}support">App support →</a></details>{f'<p class="product-note">{E(a["note"])}</p>' if a.get('note') else ''}<div class="legal-links"><a href="{base}privacy">Privacy policy</a>{f'<a href="{base}terms">Terms of use</a>' if a['slug']!='fair-dice' else ''}<a href="{base}support">Support</a></div></div></section>
<section class="more-apps wide"><div class="section-heading"><div><p class="eyebrow">FROM THE SAME MAKER</p><h2>More to explore.</h2></div><a class="text-link" href="/#apps">All apps ↗</a></div><div class="related-grid">{''.join(f'<a href="{href(p)}"><img src="{p["icon"]}" alt="" width="54" height="54"><span>{E(p["short"])}<small>{E(p["category"])}</small></span><b aria-hidden="true">↗</b></a>' for p in related)}</div></section>'''
    shell(base, a['name']+' — Kohone', body, a['description'], kind='product')
