#!/usr/bin/env python3
"""
IQ Homes — static site generator.

Writes the finished .html files next to this script. Everything it produces is
plain HTML/CSS/JS with no build step needed to host it — this script exists only
so the shared header, footer and metadata stay identical across every page.

Run:  python3 build.py
"""

import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))

SITE = "https://www.iqhomes.ca"        # <-- replace once the domain is secured
PHONE_DISPLAY = "647-936-2469"
PHONE_LINK = "+16479362469"
EMAIL = "iqhomes4everyone@gmail.com"
OFFER = "Free consultation + 30% off your first install"

# ---------------------------------------------------------------------------
# Logo
# ---------------------------------------------------------------------------
LOGO_SVG = """<svg viewBox="0 0 64 64" role="img" aria-label="IQ Homes logo" focusable="false">
  <g fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M32 29 53 43.5V56.5H11V43.5Z"/>
  </g>
  <g fill="none" stroke="var(--logo-accent, #17D7C2)" stroke-width="3.2" stroke-linecap="round">
    <path d="M26.68 20.27a7.6 7.6 0 0 1 10.64 0" opacity=".95"/>
    <path d="M22.58 17.40a13.4 13.4 0 0 1 18.84 0" opacity=".72"/>
    <path d="M18.49 14.54a19.2 19.2 0 0 1 27.02 0" opacity=".48"/>
  </g>
  <circle cx="32" cy="24.6" r="2.5" fill="var(--logo-accent, #17D7C2)"/>
  <path d="M27.5 56.5V50.6a4.5 4.5 0 0 1 9 0v5.9Z" fill="var(--logo-accent, #17D7C2)"/>
</svg>"""

# ---------------------------------------------------------------------------
# Icons (lucide-style, 24x24 stroke)
# ---------------------------------------------------------------------------
_I = {
    "lock": '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    "bell": '<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>',
    "camera": '<path d="M15 10.5V7a1 1 0 0 0-1-1H3a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1h11a1 1 0 0 0 1-1v-3.5l6 4.5V6Z"/>',
    "bulb": '<path d="M9 18h6"/><path d="M10 22h4"/><path d="M15.1 14c.2-1 .6-1.7 1.4-2.5A4.6 4.6 0 0 0 18 8 6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.8.8 1.2 1.5 1.4 2.5"/>',
    "blinds": '<path d="M3 3h18"/><path d="M20 7H8"/><path d="M20 11H8"/><path d="M8 15h12"/><path d="M10 19h10"/><path d="M4 3v14a2 2 0 0 0 4 0V3"/>',
    "thermo": '<path d="M14 4v10.54a4 4 0 1 1-4 0V4a2 2 0 0 1 4 0Z"/>',
    "speaker": '<rect x="4" y="2" width="16" height="20" rx="2"/><circle cx="12" cy="14" r="4"/><path d="M12 6h.01"/>',
    "plug": '<path d="M12 22v-5"/><path d="M9 8V2"/><path d="M15 8V2"/><path d="M18 8v5a4 4 0 0 1-4 4h-4a4 4 0 0 1-4-4V8Z"/>',
    "droplet": '<path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 0 0 7 7Z"/>',
    "garage": '<path d="M22 9.5V21a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V9.5a1 1 0 0 1 .55-.89l9-4.5a1 1 0 0 1 .9 0l9 4.5a1 1 0 0 1 .55.89Z"/><path d="M6 13h12"/><path d="M6 17h12"/><path d="M6 22v-9"/><path d="M18 22v-9"/>',
    "sprinkler": '<path d="M7 16.3a4 4 0 0 0 4-4c0-1.2-.6-2.3-1.7-3.2S7.3 6.8 7 5.3c-.3 1.5-1.1 2.9-2.3 3.8S3 11.1 3 12.3a4 4 0 0 0 4 4Z"/><path d="M12.6 6.6A11 11 0 0 0 14 3c.5 2.5 2 4.9 4 6.5s3 3.5 3 5.5a7 7 0 0 1-11.9 5"/>',
    "wifi": '<path d="M5 12.55a11 11 0 0 1 14.08 0"/><path d="M1.42 9a16 16 0 0 1 21.16 0"/><path d="M8.53 16.11a6 6 0 0 1 6.95 0"/><path d="M12 20h.01"/>',
    "screen": '<rect x="2" y="3" width="20" height="13" rx="2"/><path d="M12 16v4"/><path d="M8 20h8"/>',
    "phone-app": '<rect x="5" y="2" width="14" height="20" rx="2.5"/><path d="M12 18h.01"/><path d="M9 6h6"/>',
    "mic": '<path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><path d="M12 19v3"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "arrow": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.8 19.8 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.1 9.9a16 16 0 0 0 6 6l1.26-1.26a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92Z"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
    "star": '<path d="m12 2 3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01Z"/>',
    "plus": '<path d="M12 5v14"/><path d="M5 12h14"/>',
    "x": '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
    "menu": '<path d="M3 6h18"/><path d="M3 12h18"/><path d="M3 18h18"/>',
    "shield": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1Z"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "sparkle": '<path d="M12 3v3"/><path d="M12 18v3"/><path d="M4.9 4.9 7 7"/><path d="m17 17 2.1 2.1"/><path d="M3 12h3"/><path d="M18 12h3"/><path d="M4.9 19.1 7 17"/><path d="m17 7 2.1-2.1"/><circle cx="12" cy="12" r="3.5"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "wrench": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76Z"/>',
    "image": '<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.09-3.09a2 2 0 0 0-2.82 0L6 21"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 16v-4"/><path d="M12 8h.01"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4"/><path d="M8 2v4"/><path d="M3 10h18"/>',
    "pointer": '<path d="M12.034 12.681a.5.5 0 0 1 .647-.647l9 3.5a.5.5 0 0 1-.033.943l-3.444 1.068a1 1 0 0 0-.66.66l-1.067 3.443a.5.5 0 0 1-.943.033Z"/><path d="M5 3a2 2 0 0 0-2 2"/><path d="M19 3a2 2 0 0 1 2 2"/><path d="M5 21a2 2 0 0 1-2-2"/><path d="M9 3h1"/><path d="M9 21h2"/><path d="M14 3h1"/><path d="M3 9v1"/><path d="M21 9v2"/><path d="M3 14v1"/>',
    "leaf": '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/>',
    "gauge": '<path d="m12 14 4-4"/><path d="M3.34 19a10 10 0 1 1 17.32 0"/>',
    "home": '<path d="M3 9.5 12 3l9 6.5V20a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1Z"/><path d="M9 21v-8h6v8"/>',
    # Window-covering icons — each type gets its own silhouette
    "shutter": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M7 7.5h10"/><path d="M7 11h10"/><path d="M7 14.5h10"/><path d="M7 18h10"/><path d="M12 5.5v14"/>',
    "roller": '<rect x="3" y="3" width="18" height="2.6" rx="1.3"/><path d="M5.2 5.6v9.4h13.6V5.6"/><path d="M12 15v3.4"/><path d="M10 19.5h4"/>',
    "zebra": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 8h9"/><path d="M12 12h9"/><path d="M3 16h9"/>',
    "silhouette": '<path d="M3 4h18"/><path d="M5.2 4v16"/><path d="M18.8 4v16"/><path d="M6 8.5c3 2.2 9 2.2 12 0"/><path d="M6 13c3 2.2 9 2.2 12 0"/><path d="M6 17.5c3 2.2 9 2.2 12 0"/>',
}


def icon(name, cls=""):
    body = _I.get(name, "")
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" '
            f'aria-hidden="true" focusable="false">{body}</svg>')


def icon_fill(name, cls=""):
    body = _I.get(name, "")
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" '
            f'focusable="false">{body}</svg>')


def quote_link(sid, label="Get a price for just this"):
    """Deep-link into the contact form with one service pre-selected."""
    return (f'<a class="quote-link" href="contact.html?service={sid}">'
            f'{label} {icon("arrow")}</a>')


# ---------------------------------------------------------------------------
# Navigation
# ---------------------------------------------------------------------------
NAV = [
    ("index.html", "Home"),
    ("services.html", "Services"),
    ("blinds.html", "Blinds"),
    ("gallery.html", "Gallery"),
    ("about.html", "About"),
    ("service-area.html", "Service Area"),
    ("faq.html", "FAQ"),
]


def logo_block(sub=True):
    subline = '<span class="logo-sub">Smart Home Automation</span>' if sub else ""
    return f"""<a class="logo" href="index.html" aria-label="IQ Homes — home">
        {LOGO_SVG}
        <span class="logo-wordmark">
          <span class="logo-text">IQ Homes</span>
          {subline}
        </span>
      </a>"""


def header(active, over_hero=False):
    links = ""
    for href, label in NAV:
        cur = ' aria-current="page"' if href == active else ""
        links += f'<li><a class="nav-link" href="{href}"{cur}>{label}</a></li>\n            '
    over = " site-header--over-hero" if over_hero else ""
    return f"""  <div class="offer-bar">
    <div class="container">
      <strong>Launch offer</strong> &nbsp;·&nbsp; Free consultation <strong>+ 30% off</strong> your first install &nbsp;·&nbsp;
      <a href="contact.html">Claim it&nbsp;&rarr;</a>
    </div>
  </div>

  <header class="site-header{over}" data-header>
    <div class="container header-inner">
      {logo_block()}

      <button class="nav-toggle" data-nav-toggle aria-expanded="false" aria-controls="site-nav" aria-label="Menu">
        {icon('menu', 'icon-open')}
        {icon('x', 'icon-close')}
      </button>

      <nav class="nav" id="site-nav" data-nav aria-label="Main">
        <ul class="nav-list">
            {links}</ul>
        <a class="btn btn--primary" href="contact.html">Book free consultation</a>
      </nav>
    </div>
  </header>"""


def cta_band(title="Ready to make your home smarter?",
             body="Book a free, no-pressure consultation. We'll walk the home with you, "
                  "talk through what actually matters to your family, and design a system "
                  "around it — then take 30% off your first install."):
    return f"""  <section class="cta-band">
    <div class="container">
      <span class="cta-offer">{icon('sparkle')} {OFFER}</span>
      <h2>{title}</h2>
      <p>{body}</p>
      <div class="btn-row">
        <a class="btn btn--primary btn--lg" href="contact.html">{icon('calendar')} Book your free consultation</a>
        <a class="btn btn--ghost-light btn--lg" href="tel:{PHONE_LINK}">{icon('phone')} {PHONE_DISPLAY}</a>
      </div>
    </div>
  </section>"""


def footer():
    svc_links = "".join(
        f'<li><a href="services.html#{sid}">{name}</a></li>'
        for sid, name in [
            ("security", "Security & access"),
            ("comfort", "Lighting & climate"),
            ("entertainment", "Audio & home theatre"),
            ("essentials", "Wi-Fi & essentials"),
        ]
    ) + ('<li><a href="blinds.html">Blinds &amp; shutters</a></li>'
         '<li><a href="blinds.html#motorised">Motorised &amp; smart blinds</a></li>')
    nav_links = "".join(f'<li><a href="{h}">{l}</a></li>' for h, l in NAV)
    return f"""  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-about">
          {logo_block()}
          <p>Custom smart home design and installation across the Greater Toronto Area. Locally owned, locally installed.</p>
        </div>

        <div class="footer-col">
          <h4>Services</h4>
          <ul>{svc_links}</ul>
        </div>

        <div class="footer-col">
          <h4>Company</h4>
          <ul>{nav_links}</ul>
        </div>

        <div class="footer-col">
          <h4>Get in touch</h4>
          <ul class="footer-contact">
            <li>{icon('phone')}<a href="tel:{PHONE_LINK}">{PHONE_DISPLAY}</a></li>
            <li>{icon('mail')}<a href="mailto:{EMAIL}">{EMAIL}</a></li>
            <li>{icon('pin')}<span>Serving the entire Greater<br>Toronto Area</span></li>
          </ul>
        </div>
      </div>

      <div class="footer-bottom">
        <p>&copy; <span data-year>2026</span> IQ Homes. All rights reserved.</p>
        <nav aria-label="Footer">
          <a href="contact.html">Book a consultation</a>
          <a href="faq.html">FAQ</a>
          <a href="service-area.html">Service area</a>
        </nav>
      </div>
    </div>
  </footer>"""


# ---------------------------------------------------------------------------
# Service area — the whole GTA.
#
# The Greater Toronto Area is the City of Toronto plus four regional
# municipalities. Listing it by region rather than by a handful of cities is
# both accurate and better for search: someone in Whitby searches "Whitby",
# not "GTA".
# ---------------------------------------------------------------------------
GTA_REGIONS = [
    ("Toronto", "City of Toronto",
     "Downtown, North York, Scarborough, Etobicoke, East York, York &amp; the Beaches"),
    ("Peel", "Peel Region",
     "Mississauga, Brampton &amp; Caledon"),
    ("York", "York Region",
     "Vaughan, Markham, Richmond Hill, Newmarket, Aurora, King, Whitchurch-Stouffville, "
     "East Gwillimbury &amp; Georgina"),
    ("Durham", "Durham Region",
     "Pickering, Ajax, Whitby, Oshawa, Clarington, Uxbridge, Scugog &amp; Brock"),
    ("Halton", "Halton Region",
     "Oakville, Burlington, Milton &amp; Halton Hills"),
]

# Every municipality we cover, grouped for the contact form's city dropdown.
GTA_MUNICIPALITIES = [
    ("City of Toronto", [
        "Toronto", "North York", "Scarborough", "Etobicoke", "East York", "York",
    ]),
    ("Peel Region", [
        "Mississauga", "Brampton", "Caledon",
    ]),
    ("York Region", [
        "Vaughan", "Markham", "Richmond Hill", "Newmarket", "Aurora", "King City",
        "Whitchurch-Stouffville", "East Gwillimbury", "Georgina",
    ]),
    ("Durham Region", [
        "Pickering", "Ajax", "Whitby", "Oshawa", "Clarington", "Uxbridge", "Scugog", "Brock",
    ]),
    ("Halton Region", [
        "Oakville", "Burlington", "Milton", "Halton Hills",
    ]),
]

# Total municipalities, used in the hero stat so the number can never drift
# out of sync with the list above.
GTA_COUNT = sum(len(v) for _, v in GTA_MUNICIPALITIES)

# Flat city list for structured data, generated from the list above so the two
# can never drift apart.
GTA_CITY_JSONLD = ",\n".join(
    '    { "@type": "City", "name": "%s" }' % c
    for _, cities in GTA_MUNICIPALITIES for c in cities
)


LOCAL_BUSINESS_JSONLD = f"""{{
  "@context": "https://schema.org",
  "@type": "HomeAndConstructionBusiness",
  "@id": "{SITE}/#business",
  "name": "IQ Homes",
  "description": "Smart home automation design, sales and installation across the Greater Toronto Area.",
  "url": "{SITE}",
  "telephone": "{PHONE_LINK}",
  "email": "{EMAIL}",
  "founder": {{ "@type": "Person", "name": "Kshitij Dua" }},
  "priceRange": "$$",
  "areaServed": [
    {{ "@type": "AdministrativeArea", "name": "Greater Toronto Area" }},
    {{ "@type": "AdministrativeArea", "name": "Regional Municipality of Peel" }},
    {{ "@type": "AdministrativeArea", "name": "Regional Municipality of York" }},
    {{ "@type": "AdministrativeArea", "name": "Regional Municipality of Durham" }},
    {{ "@type": "AdministrativeArea", "name": "Regional Municipality of Halton" }},
{GTA_CITY_JSONLD}
  ],
  "address": {{
    "@type": "PostalAddress",
    "addressRegion": "ON",
    "addressCountry": "CA"
  }},
  "makesOffer": {{
    "@type": "Offer",
    "name": "Free consultation + 30% off first install",
    "description": "New customers receive a free in-home smart home consultation and 30% off their first installation."
  }}
}}"""


def page(filename, title, description, body, active, over_hero=False, extra_jsonld=None,
         noindex=False):
    """Assemble one complete HTML file."""
    jsonld = f'<script type="application/ld+json">{LOCAL_BUSINESS_JSONLD}</script>'
    if extra_jsonld:
        jsonld += f'\n  <script type="application/ld+json">{extra_jsonld}</script>'
    if noindex:
        # Thank-you and error pages should never appear in search results
        jsonld = '<meta name="robots" content="noindex, follow">\n  ' + jsonld

    canonical = f"{SITE}/{'' if filename == 'index.html' else filename}"

    html = f"""<!DOCTYPE html>
<html lang="en-CA">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{canonical}">

  <meta property="og:type" content="website">
  <meta property="og:site_name" content="IQ Homes">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{SITE}/assets/img/photos/hero-dusk-unlock.jpg">
  <meta property="og:locale" content="en_CA">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#0B2545">

  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="assets/favicon.svg">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700&family=Lato:wght@400;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/css/style.css">

  {jsonld}
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>

{header(active, over_hero)}

  <main id="main">
{body}
  </main>

{footer()}

  <script type="importmap">
  {{ "imports": {{ "three": "./assets/js/vendor/three.module.js" }} }}
  </script>
  <script type="module" src="assets/js/main.js"></script>
</body>
</html>
"""
    with open(os.path.join(HERE, filename), "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  wrote {filename}  ({len(html):,} bytes)")


def page_hero(title, lead, crumb):
    return f"""    <section class="page-hero">
      <div class="container">
        <nav class="breadcrumb" aria-label="Breadcrumb">
          <a href="index.html">Home</a> <span>/</span> <span>{crumb}</span>
        </nav>
        <h1>{title}</h1>
        <p class="lead">{lead}</p>
      </div>
    </section>"""


def img_slot(label, hint, src=None, alt=""):
    """A styled placeholder that a real photo drops straight into."""
    # onerror removes the <img> so the styled placeholder shows through until
    # the real photo is dropped into assets/img/.
    real = (f'<img src="{src}" alt="{alt}" loading="lazy" decoding="async" '
            f'onerror="this.remove()">') if src else ""
    return f"""<div class="img-slot">
            {icon('image')}
            <b>{label}</b>
            <span>{hint}</span>
            {real}
          </div>"""


# ---------------------------------------------------------------------------
# Shared content data
# ---------------------------------------------------------------------------
SERVICE_GROUPS = [
    ("security", "Security &amp; access", "shield",
     "Know who's at the door, who came in, and that everything is locked — from anywhere.", [
         ("lock", "Smart locks &amp; keyless entry", "lock",
          "Unlock with your phone, a code, or your voice. Give the dog walker their own access and see exactly when it was used. No more hiding a key under the mat."),
         ("doorbell", "Video doorbells", "bell",
          "See and speak to whoever's at your door, whether you're upstairs or in another country. Every delivery and visitor recorded to your phone."),
         ("cameras", "24/7 security cameras &amp; monitoring", "camera",
          "Sharp day-and-night coverage of every approach to the house, with motion alerts smart enough to tell the mail carrier from a stranger."),
         ("garage", "Garage door control", "garage",
          "Never drive back to check again. See its status from anywhere, close it with a tap, and have it open as you pull into the driveway."),
     ]),
    ("comfort", "Lighting, comfort &amp; climate", "bulb",
     "The part your family notices every single day — a house that adjusts itself around you.", [
         ("lighting", "Voice-controlled lighting", "bulb",
          '"Movie night." The room dims, the lamps warm up, the rest of the house drops to a low glow. One phrase, every fixture — or set it on a schedule and forget it.'),
         ("blinds", "Motorized blinds &amp; curtains", "blinds",
          "Blinds that lift with the sunrise and close at dusk. Silent, wire-free options for existing windows, and hardwired runs for new builds."),
         ("climate", "Smart climate control", "thermo",
          "A thermostat that learns your schedule and has the house warm before you walk in. Room-by-room comfort, and a noticeably smaller gas bill."),
         ("irrigation", "Smart irrigation", "sprinkler",
          "Watering that checks the forecast before it runs. Keeps the lawn green through a GTA August without soaking it the morning after a storm."),
     ]),
    ("entertainment", "Audio &amp; home theatre", "speaker",
     "Sound and picture done properly — installed clean, with nothing left dangling.", [
         ("av", "Whole-home entertainment &amp; audio", "speaker",
          "Music that follows you from the kitchen to the deck, in-ceiling speakers that disappear into the room, and one remote instead of five."),
         ("theatre", "Home theatre installation", "screen",
          "From a tidy wall-mounted TV with hidden cabling to a full dedicated theatre room — screen, seating layout, acoustics and calibration."),
     ]),
    ("essentials", "Essentials &amp; efficiency", "wifi",
     "The unglamorous layer that decides whether everything else actually works.", [
         ("wifi", "Whole-home Wi-Fi &amp; mesh networking", "wifi",
          "Most smart home problems are really Wi-Fi problems. We survey the house and build a mesh network that holds up in the basement and the backyard."),
         ("energy", "Smart plugs &amp; energy monitoring", "plug",
          "See what's actually costing you money, shut the big draws off on a schedule, and stop leaving the space heater running all day."),
         ("sensors", "Water leak &amp; smoke/CO sensors", "droplet",
          "A burst washer hose is a five-figure repair. Sensors under the sinks and by the tank tell you in seconds, not when the ceiling comes down."),
         ("hub", "One app, one voice — unified control", "phone-app",
          "The piece that makes it a smart home instead of eleven smart gadgets. Every system on one hub, one app, and the voice assistant you already use."),
     ]),
]

# ---------------------------------------------------------------------------
# Blinds — the second business line
# ---------------------------------------------------------------------------
BLIND_TYPES = [
    ("shutters", "Plantation shutters", "shutter",
     "The most substantial option. Real or composite wood louvres built to the exact window, "
     "framed and hinged like joinery. They insulate, they never need replacing, and they read as "
     "part of the house rather than something hung in front of it.",
     ["Real wood or moisture-safe composite", "Best insulation of any covering",
      "Adds resale value", "Bathrooms &amp; kitchens included"]),

    ("roller", "Roller shades", "roller",
     "Clean, minimal and the most versatile thing we fit. One roll of fabric, hundreds of "
     "choices — from a sheer that keeps the view and kills the glare, to a full blackout that "
     "makes a bedroom genuinely dark at 7am in June.",
     ["Sheer, light-filtering or blackout", "Hundreds of fabrics", "Slimmest stack when open",
      "Best value per window"]),

    ("zebra", "Zebra (dual) shades", "zebra",
     "Alternating sheer and solid bands that slide over one another. Line them up and you have "
     "a sheer; offset them and you have privacy — all from the same blind, without swapping "
     "anything. The most-requested covering in new GTA builds, and it's not close.",
     ["Light control without changing blinds", "Modern, architectural look",
      "Great for street-facing rooms", "Most popular choice"]),

    ("silhouette", "Silhouette &amp; sheer shades", "silhouette",
     "Soft fabric vanes floating between two sheers. They turn hard afternoon sun into diffused "
     "light and give you privacy without going dark — the reason they end up in front-facing "
     "living rooms more than anywhere else.",
     ["Diffuses harsh direct sun", "Privacy while staying light",
      "UV protection for floors &amp; furniture", "The premium finish"]),

    ("custom", "Custom sizes &amp; shapes", "wrench",
     "Bay windows, arches, angled ceilings, oversized patio doors, that awkward stairwell "
     "window. Measured on site and manufactured to fit — never a stock size cut down and hoped "
     "for the best.",
     ["Bay, arched &amp; angled windows", "Oversized patio &amp; slider doors",
      "Free on-site measure", "Made to the millimetre"]),

    ("motorised", "Motorised blinds", "gauge",
     "Quiet motors, rechargeable battery or hardwired. Raise a whole room from one remote. No "
     "cords anywhere, which is also why they're the right call in any home with young children "
     "or pets.",
     ["Battery or hardwired", "Whole-room and whole-house remotes",
      "Completely cordless — child safe", "Retrofit to most existing blinds"]),

    ("smart-blinds", "Smart blinds", "phone-app",
     "Motorised blinds wired into the rest of your home. They lift with sunrise, close at dusk, "
     "and drop on their own when the afternoon sun hits the south side. Same app, same voice "
     "assistant, same schedule as your lights.",
     ["Sunrise / sunset schedules", "Voice and app control",
      "Drops automatically on hot afternoons", "Works with your existing setup"]),
]

# How someone can buy blinds from IQ Homes
BLIND_MODELS = [
    ("sparkle", "Supply &amp; install — the usual route",
     "We measure, help you choose the type and fabric, place the order with our suppliers, and "
     "come back to fit them. One point of contact, one invoice, and if anything's wrong with the "
     "product it's our problem to sort out, not yours."),
    ("wrench", "Installation only — you already bought them",
     "Ordered from a big-box store or online and now they're sitting in boxes? We'll fit them "
     "properly. Bring us the blinds and the windows and we'll do the rest — no judgement about "
     "where they came from."),
    ("gauge", "Motorising what you already have",
     "Plenty of existing roller and cellular blinds can take a retrofit motor without replacing "
     "the blind itself. Cheaper than starting over, and it gets you the cordless, scheduled "
     "version of what's already on the window."),
]

DIFFERENTIATORS = [
    ("wrench", "Designed for your home, not out of a box",
     "We don't arrive with a fixed kit. We walk the house, look at how you actually live in it, and specify the equipment that suits your layout, your budget and your habits."),
    ("users", "A local GTA team, not a call centre",
     "The person who designs your system is the person who installs it and picks up the phone afterward. No national chain, no ticket queue, no contractor you've never met."),
    ("phone-app", "One app. One voice. Every room.",
     "Anyone can sell you a smart plug. The value is in making the lock, the lights, the thermostat and the cameras behave like one system you can actually control."),
    ("sparkle", "A genuinely low-risk first step",
     "The consultation is free and there's no obligation at the end of it. Go ahead with the install and we take 30% off — so trying us costs you an hour, not a deposit."),
]

STEPS = [
    ("Free consultation",
     "We come to you, anywhere in the GTA. We walk the home, ask how your day actually runs, and find the friction worth automating. No charge, no pressure, no obligation."),
    ("A design and a straight price",
     "You get a clear plan: what goes where, which equipment, what it does, and one itemised price with the 30% first-install discount already applied. Nothing hidden."),
    ("Installed, tuned and handed over",
     "We install clean — cables concealed, everything tested. Then we sit down with you and your family until everyone can actually use it. Support doesn't end at the door."),
]

TESTIMONIALS = [
    ("Placeholder — replace with a real review", "Homeowner", "Mississauga",
     "This is where a real customer review will go. Ask your first few clients for a sentence or two about what changed for them day to day — those specifics convert far better than generic praise."),
    ("Placeholder — replace with a real review", "Homeowner", "Vaughan",
     "A second review slot. Reviews that name the actual problem solved (\"we stopped worrying about the door\") outperform ones that just say \"great service\"."),
    ("Placeholder — replace with a real review", "Homeowner", "Toronto",
     "A third slot. Once you have Google reviews coming in, these can be swapped for real quotes with names, neighbourhoods and a link to the Google listing."),
]



FAQS = [
    ("Getting started", [
        ("Is the consultation really free?",
         "Yes — completely. We come to your home anywhere in the GTA, walk through it with you, talk about what would actually make a difference, and leave you with a written plan and price. There's no fee and no obligation to go ahead."),
        ("What happens during the consultation?",
         "We spend about an hour with you. We look at your layout, your Wi-Fi, your existing devices and your door and window situation, and we ask how your household actually runs — who gets home first, what you forget, what worries you. Then we design around that."),
        ("Do I need to know what I want before I call?",
         "Not at all. Most people start with one thing bothering them — a door they can't check, a dark driveway, a thermostat nobody agrees on. We start there and show you what else is worth doing while we're in the walls."),
    ]),
    ("Pricing &amp; the offer", [
        ("How does the 30% off first install work?",
         "New customers get 30% off their first installation. It's applied to the quote you receive after your consultation, so the number you see is the number you pay. It applies once, to your first job with us."),
        ("What does a typical system cost?",
         "It ranges widely, because we design to the home. A focused starting package — smart lock, video doorbell and a couple of rooms of lighting — is a modest few hundred dollars of equipment plus install. A whole-home system with AV, climate, blinds and cameras runs considerably higher. Your consultation gives you a real number, not a range."),
        ("Do you offer financing or payment plans?",
         "Talk to us during your consultation. For larger whole-home projects we can usually work out a staged payment schedule tied to install milestones. We'll be straight with you about what's possible before you commit to anything."),
    ]),
    ("Installation &amp; timelines", [
        ("How long does an install take?",
         "A focused install — locks, a doorbell, a few smart switches — is usually a single day. A whole-home system with networking, AV, blinds and climate typically runs two to five days depending on the size of the home and how much cabling is involved. You'll get a firm schedule with your quote."),
        ("Will you make a mess of my walls?",
         "We install clean, and we tell you upfront where anything needs to be opened. Wherever a wireless or surface-mount option does the job as well, we'll offer it. Any patching needed is discussed and priced before we start, never discovered afterward."),
        ("Do I need to be home for the install?",
         "For at least the start and the finish, yes. We walk through the plan with you before we begin, and at the end we sit down with everyone in the household and make sure they can all use it before we leave."),
    ]),
    ("Devices &amp; compatibility", [
        ("Will this work with the smart devices I already own?",
         "Usually, yes. If you've already got a few smart bulbs, a video doorbell or a thermostat, we'll try to fold them into the system rather than replace them. Where something genuinely won't play nicely with the rest, we'll tell you why and what it would take."),
        ("Does it work with Alexa, Google or Apple?",
         "Yes. We build around whichever ecosystem you already use rather than forcing you to switch. If your household is split across two, we'll design something that works for both rather than starting an argument."),
        ("What happens if my internet goes down?",
         "We design so the essentials keep working. Locks still unlock, switches still switch, and scheduled routines keep running locally. What you lose temporarily is remote access from outside the house and cloud video — both come back on their own when the connection does."),
        ("Is it secure? I don't love the idea of cameras on the internet.",
         "It's a fair concern and worth taking seriously. We set up devices on a properly segmented network, change every default credential, keep firmware current, and walk you through exactly what is stored where and who can see it. You'll know what you've got."),
    ]),
    ("Blinds", [
        ("Do you supply the blinds, or only install them?",
         "Both, and you can pick. Most people have us do the whole thing — we measure, help you "
         "choose the type and fabric, order from our suppliers and come back to fit them. But if "
         "you've already bought blinds somewhere else and they're sitting in boxes, we're happy to "
         "just install them. No judgement about where they came from."),
        ("Can you install blinds I bought from a big-box store or online?",
         "Yes, that's a normal job for us. Bring us the blinds and the windows. One honest warning: "
         "if they were ordered to the wrong size, no amount of installing fixes that — so if you "
         "haven't ordered yet, let us measure first. A free measure costs you nothing and saves a "
         "lot of returns."),
        ("What's the difference between zebra and roller shades?",
         "A roller is one continuous piece of fabric — you choose upfront how sheer or blackout it "
         "is. A zebra has alternating sheer and solid bands that slide over each other, so the same "
         "blind goes from see-through to private depending on how you set it. Zebras cost more and "
         "are more flexible; rollers are better value and better at true blackout."),
        ("How long from order to installation?",
         "Custom blinds are made to your measurements, so allow roughly two to four weeks from "
         "order to install depending on the fabric and supplier. Installation itself is usually a "
         "single visit. If you're installing blinds you already own, we can often get to you within "
         "the week."),
        ("Are motorised blinds actually worth it?",
         "For one or two easy-to-reach windows, honestly, probably not. Where they earn their keep "
         "is high or awkward windows you never bother adjusting, whole rooms you want to set at "
         "once, and any home with young children — cordless is genuinely safer. We'll tell you "
         "which of your windows are worth motorising and which aren't."),
        ("Do smart blinds need me to have a whole smart home?",
         "No. Smart blinds work perfectly well on their own with their app and schedules. But if "
         "you do have — or later add — smart lighting and climate, they fold into the same system "
         "so one routine can handle all of it. That's the advantage of buying blinds from a company "
         "that also does the automation."),
        ("Can you do bay windows, arches and odd shapes?",
         "Yes, and that's exactly where a custom order beats anything off the shelf. Bays, arched "
         "tops, angled ceilings, oversized patio sliders and awkward stairwell windows all get "
         "measured on site and manufactured to fit."),
    ]),
    ("After the install", [
        ("What if something stops working?",
         "You call us — the same local number, the same people who did the install. Most issues we can resolve remotely. If it needs a visit, we come out. We're not a chain that disappears once the invoice clears."),
        ("Can I add to the system later?",
         "That's rather the point of designing it properly. We build so you can start with one or two rooms and add blinds, cameras, audio or climate later without tearing anything out or starting over."),
        ("What if I sell the house?",
         "A well-installed smart home system is a genuine selling feature, and we'll leave you documentation to hand to the buyer. We can also come out and walk the new owners through it."),
    ]),
]


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import _pages
    _pages.build_all()
