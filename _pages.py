#!/usr/bin/env python3
"""Page bodies for the IQ Homes site. Driven by build.py — run `python3 build.py`."""

from build import *   # noqa: F401,F403


# ===========================================================================
#  Reusable fragments
# ===========================================================================
def stage():
    return f"""      <div class="stage" data-stage>
          <canvas role="img" aria-label="Interactive 3D model of a smart home showing where each device is installed. Drag to rotate, or use the arrow keys."></canvas>

          <div class="stage-loader" data-stage-loader>
            <span class="ring" aria-hidden="true"></span>
            <span>Building your smart home</span>
          </div>

          <div class="stage-hint is-hidden" data-stage-hint>
            {icon('pointer')} Drag &nbsp;·&nbsp; click a glowing point
          </div>

          <div class="stage-tip" data-stage-tip aria-hidden="true"></div>

          <aside class="stage-detail" data-stage-detail aria-hidden="true" aria-live="polite">
            <button class="stage-detail-close" data-detail-close type="button" aria-label="Close">{icon('x')}</button>
            <h3 data-detail-title></h3>
            <p data-detail-body></p>
            <a class="link-arrow" href="contact.html">Book a free consultation {icon('arrow')}</a>
          </aside>

          <div class="stage-fallback">
            {LOGO_SVG}
            <p>Your browser can't display the interactive model — but everything it shows is on the <a href="services.html" class="link-arrow">services page</a>.</p>
          </div>
        </div>"""


def service_card(sid, name, ic, blurb, dark=False, focus=True, quote=True):
    cls = "card card--dark" if dark else "card"
    focus_attr = f' data-focus-device="{sid}"' if focus else ""
    q = quote_link(sid) if quote else ""
    return f"""<article class="{cls} reveal"{focus_attr} id="{sid}">
            <span class="card-icon">{icon(ic)}</span>
            <h3>{name}</h3>
            <p>{blurb}</p>
            {q}
          </article>"""


def blind_card(sid, name, ic, blurb, specs, dark=False):
    cls = "card card--dark blind-card" if dark else "card blind-card"
    items = "".join(f"<li>{icon('check')}<span>{s}</span></li>" for s in specs)
    return f"""<article class="{cls} reveal" id="{sid}">
            <span class="card-icon">{icon(ic)}</span>
            <h3>{name}</h3>
            <p>{blurb}</p>
            <ul class="blind-specs">{items}</ul>
            {quote_link(sid, "Get a price for this")}
          </article>"""


def single_jobs(text=None):
    body = text or (
        "You don't have to do the whole house. Plenty of our jobs are one thing — a video "
        "doorbell, a smart lock, blinds for two bedrooms. Tell us the one item you want and "
        "we'll price just that, no upselling and no minimum job size."
    )
    return f"""<div class="single-jobs reveal">
          <span class="single-jobs-icon">{icon('sparkle')}</span>
          <div class="single-jobs-body">
            <h3>Want just one thing? That's completely fine.</h3>
            <p>{body}</p>
          </div>
          <a class="btn btn--primary" href="contact.html">{icon('arrow')} Price a single job</a>
        </div>"""


def testimonial_block(dark=False):
    cls = "quote quote--dark" if dark else "quote"
    stars = "".join(icon_fill('star') for _ in range(5))
    out = ""
    for i, (quote_lead, role, city, text) in enumerate(TESTIMONIALS):
        initials = city[0] + role[0]
        out += f"""<figure class="{cls} reveal" data-delay="{i+1}">
            <div class="stars" aria-label="5 out of 5">{stars}</div>
            <blockquote>&ldquo;{text}&rdquo;</blockquote>
            <figcaption>
              <span class="avatar" aria-hidden="true">{initials}</span>
              <cite>{quote_lead}<small>{role} &middot; {city}</small></cite>
            </figcaption>
          </figure>
          """
    return out


def hero_headline():
    """Per-word spans so each can animate in with its own glitch delay.
       Accent words carry a stepped teal→blue ramp, which keeps the gradient
       feel of a single background-clip run while still animating cleanly."""
    plain = ["Smarter", "living,"]
    accent = ["built", "for", "the", "way", "you", "live."]

    def ramp(t):
        a, b = (0x17, 0xD7, 0xC2), (0x2E, 0x8B, 0xFF)
        return "#%02X%02X%02X" % tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))

    out = [f'<span class="hw">{w}</span>' for w in plain]
    n = len(accent) - 1
    out += [f'<span class="hw" style="color:{ramp(i / n)}">{w}</span>'
            for i, w in enumerate(accent)]
    return " ".join(out)


def city_cards(dark=False):
    """The GTA by region — Toronto plus the four regional municipalities."""
    return "".join(
        f"""<div class="city reveal" data-delay="{i+1}">
            {icon('pin')}
            <span>{name}<small>{sub}</small></span>
          </div>
          """
        for i, (_, name, sub) in enumerate(GTA_REGIONS)
    )


# ===========================================================================
#  Home
# ===========================================================================
def build_index():
    six = [
        ("lock", "Smart locks &amp; keyless entry", "lock", "Unlock with your phone, a code or your voice — and see exactly who came and went."),
        ("doorbell", "Video doorbells", "bell", "See and speak to whoever's at the door, from anywhere in the world."),
        ("camera", "24/7 security cameras", "camera", "Sharp day-and-night coverage, with alerts smart enough to know the mail carrier."),
        ("lighting", "Voice-controlled lighting", "bulb", "&ldquo;Movie night.&rdquo; One phrase, every fixture in the room responds."),
        ("climate", "Smart climate control", "thermo", "A house that's already warm when you walk in, and a smaller gas bill."),
        ("theatre", "Home theatre &amp; audio", "screen", "Cinema picture, properly tuned sound, and cabling you never see."),
    ]
    cards = "".join(service_card(sid, n, ic, b) for sid, n, ic, b in six)

    steps = "".join(
        f"""<div class="step reveal" data-delay="{i+1}">
            <span class="step-num">0{i+1}</span>
            <h3>{t}</h3>
            <p>{d}</p>
          </div>
          """
        for i, (t, d) in enumerate(STEPS)
    )

    diffs = "".join(
        f"""<div class="feature reveal" data-delay="{i+1}">
            <span class="feature-icon">{icon(ic)}</span>
            <div>
              <h3>{t}</h3>
              <p>{d}</p>
            </div>
          </div>
          """
        for i, (ic, t, d) in enumerate(DIFFERENTIATORS)
    )

    ads = [
        ("ad-come-home-to-smarter.jpg", "Come home to smarter", "Launch campaign"),
        ("ad-one-app-every-room.jpg", "One app. Every room.", "Unified control"),
        ("ad-24-7-eyes.jpg", "24/7 eyes on your home", "Security campaign"),
        ("ad-trusted-across-gta.jpg", "Trusted across the GTA", "Local campaign"),
    ]
    ad_grid = "".join(
        f"""<figure class="gallery-item reveal" data-delay="{i+1}">
            {img_slot('Ad creative', 'Run fetch-brand-assets.sh to drop the real image in here.',
                      src='assets/img/ads/' + f, alt=t)}
            <figcaption class="gallery-cap">{t}<small>{sub}</small></figcaption>
          </figure>
          """
        for i, (f, t, sub) in enumerate(ads)
    )

    body = f"""    <section class="hero">
      <div class="container hero-inner">
        <div class="hero-copy">
          <span class="hero-badge"><span class="pill">Launch offer</span> Free consultation + 30% off</span>
          <h1>{hero_headline()}</h1>
          <p class="lead">
            <span class="hero-sub-line" data-hero-sub>
              Smart home systems <strong>and custom blinds</strong>, designed and installed across the
              Greater Toronto Area. Not a box of gadgets — one system, one app, one voice, built
              around your home and how your family actually uses it.
            </span>
          </p>
          <div class="btn-row">
            <a class="btn btn--primary btn--lg" href="contact.html">{icon('calendar')} Book your free consultation</a>
            <a class="btn btn--ghost-light btn--lg" href="services.html">See what we install</a>
          </div>

          <div class="hero-trust">
            <div><b>{GTA_COUNT}</b><span>GTA CITIES &amp; TOWNS</span></div>
            <div><b>21</b><span>SERVICES WE OFFER</span></div>
            <div><b>30%</b><span>OFF YOUR FIRST INSTALL</span></div>
          </div>
        </div>

{stage()}
      </div>

      <a class="explore-btn" href="#one-app">
        Scroll to explore
        <span class="explore-arrow" aria-hidden="true">
          <svg viewBox="0 0 22 22" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M11 5V17" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            <path d="M6 12L11 17L16 12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          </svg>
        </span>
      </a>
    </section>

    <section class="section" id="one-app">
      <div class="container">
        <div class="split">
          <div class="split-media reveal">
            {img_slot('One app, every room',
                      'assets/img/photos/app-control-phone.jpg — run fetch-brand-assets.sh',
                      src='assets/img/photos/app-control-phone.jpg',
                      alt='The IQ Homes app controlling locks, lights, cameras and climate')}
          </div>
          <div class="reveal" data-delay="1">
            <span class="eyebrow">One app. One voice. Every room.</span>
            <h2>Most &ldquo;smart homes&rdquo; are just eleven apps in a trench coat.</h2>
            <p class="lead mt-2">
              A smart bulb here, a doorbell there, a thermostat that lives in its own app and argues with
              your phone. That's not a smart home — that's homework.
            </p>
            <p class="mt-2 text-muted">
              We design the whole thing as one system. Your locks, lights, cameras, climate, blinds and
              audio all answer to a single app and a single voice assistant — the one you already use.
              It should feel less like operating technology and more like the house simply paying attention.
            </p>
            <div class="btn-row mt-3">
              <a class="btn btn--dark" href="services.html">{icon('arrow')} Explore every service</a>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--alt">
      <div class="container">
        <div class="section-head section-head--center">
          <span class="eyebrow">What we install</span>
          <h2>Everything you'd want in a smart home — installed properly.</h2>
          <p class="lead">Click any of these to find it on the model above, or see the full list of fourteen services.</p>
        </div>

        <div class="grid grid--3">
          {cards}
        </div>

        <div class="text-center mt-4">
          <a class="btn btn--dark btn--lg" href="services.html">See all 14 smart home services {icon('arrow')}</a>
        </div>

        <div class="mt-4">
          {single_jobs()}
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="split split--reverse">
          <div class="split-media reveal">
            {img_slot('Blinds &amp; shutters',
                      'Drop a blinds install photo at assets/img/photos/blinds-hero.jpg',
                      src='assets/img/photos/blinds-hero.jpg',
                      alt='Custom motorised blinds installed in a GTA living room')}
          </div>
          <div>
            <span class="eyebrow">{icon('blinds')} Blinds &amp; shutters</span>
            <h2>We do blinds too — supply, custom order and installation.</h2>
            <p class="lead mt-2">
              Shutters, roller shades, zebra and silhouette. We measure, help you choose, arrange the
              order and fit them. Already bought blinds elsewhere? We'll install those as well.
            </p>
            <p class="mt-2 text-muted">
              And because we do automation, we're one of the few outfits in the GTA that can motorise
              them and tie them into the rest of your home — blinds that lift at sunrise, close at
              dusk, and answer to the same app as your lights.
            </p>
            <ul class="checks mt-3">
              <li class="check" style="cursor:default">{icon('check')} Plantation shutters</li>
              <li class="check" style="cursor:default">{icon('check')} Roller shades</li>
              <li class="check" style="cursor:default">{icon('check')} Zebra / dual shades</li>
              <li class="check" style="cursor:default">{icon('check')} Silhouette &amp; sheers</li>
              <li class="check" style="cursor:default">{icon('check')} Custom sizes &amp; shapes</li>
              <li class="check" style="cursor:default">{icon('check')} Motorised &amp; smart</li>
            </ul>
            <div class="btn-row mt-3">
              <a class="btn btn--primary" href="blinds.html">{icon('arrow')} Explore blinds</a>
              <a class="btn btn--ghost" href="contact.html?service=blinds-measure">Free measure &amp; quote</a>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section on-dark">
      <div class="container">
        <div class="section-head section-head--center">
          <span class="eyebrow">How it works</span>
          <h2>Three steps, and the first one is free.</h2>
        </div>
        <div class="grid grid--3">
          {steps}
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="split split--reverse">
          <div class="split-media reveal">
            {img_slot('Evening arrival',
                      'assets/img/photos/hero-dusk-unlock.jpg — run fetch-brand-assets.sh',
                      src='assets/img/photos/hero-dusk-unlock.jpg',
                      alt='A homeowner unlocking their smart front door at dusk')}
          </div>
          <div>
            <span class="eyebrow">Why IQ Homes</span>
            <h2>A local team that designs it, installs it, and answers the phone after.</h2>
            <div class="grid mt-3" style="gap:1.6rem">
              {diffs}
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--alt">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">Our work</span>
          <h2>The campaigns — and soon, the installs.</h2>
          <p class="lead">Real project photography goes here as jobs complete. In the meantime, here's the brand out in the wild.</p>
        </div>
        <div class="gallery-grid">
          {ad_grid}
        </div>
        <div class="text-center mt-4">
          <a class="btn btn--ghost btn--lg" href="gallery.html">Visit the gallery {icon('arrow')}</a>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section-head section-head--center">
          <span class="eyebrow">Homeowners</span>
          <h2>What GTA families say.</h2>
        </div>
        <div class="grid grid--3">
          {testimonial_block()}
        </div>
        <div class="mt-3">
          <p class="placeholder-note">
            {icon('info')}
            <span><strong>Note for Kshitij:</strong> these three cards are placeholder structure, ready for real reviews.
            Ask your first customers for one specific sentence about what changed day to day, then replace the text,
            names and neighbourhoods in <code>index.html</code>. Delete this note before launch.</span>
          </p>
        </div>
      </div>
    </section>

    <section class="section section--tight on-dark">
      <div class="container">
        <div class="section-head section-head--center">
          <span class="eyebrow">Where we work</span>
          <h2>The whole GTA — every region, every city.</h2>
          <p class="lead">Toronto and all four regional municipalities. If it's in the Greater Toronto Area, we cover it.</p>
        </div>
        <div class="city-grid">
          {city_cards()}
        </div>
        <div class="text-center mt-4">
          <a class="btn btn--ghost-light" href="service-area.html">Check your address {icon('arrow')}</a>
        </div>
      </div>
    </section>

{cta_band()}"""

    page("index.html",
         "IQ Homes | Smart Home Automation &amp; Installation in the GTA",
         "Custom smart home design and installation across the entire Greater Toronto Area — Toronto, "
         "Peel, York, Durham and Halton. Smart locks, cameras, lighting, climate and whole-home audio — one app, one "
         "voice. Free consultation + 30% off your first install.",
         body, "index.html", over_hero=True)


# ===========================================================================
#  Services
# ===========================================================================
def build_services():
    groups = ""
    for gi, (gid, gname, gicon, gblurb, items) in enumerate(SERVICE_GROUPS):
        cards = "".join(service_card(sid, n, ic, b) for sid, n, ic, b in items)
        # Pick a column count that leaves no orphan card on the last row
        gcls = {2: "grid--2", 4: "grid--4"}.get(len(items), "grid--3")
        alt = " section--alt" if gi % 2 == 1 else ""
        groups += f"""    <section class="section{alt}" id="{gid}">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">{icon(gicon)} {gname}</span>
          <h2>{gblurb}</h2>
        </div>
        <div class="grid {gcls}">
          {cards}
        </div>
      </div>
    </section>

"""

    steps = "".join(
        f"""<div class="step reveal" data-delay="{i+1}">
            <span class="step-num">0{i+1}</span>
            <h3>{t}</h3>
            <p>{d}</p>
          </div>
          """
        for i, (t, d) in enumerate(STEPS)
    )

    nav_chips = "".join(
        f'<a class="btn btn--ghost" href="#{gid}">{gname}</a>'
        for gid, gname, _, _, _ in SERVICE_GROUPS
    )

    body = f"""{page_hero(
        "Fourteen ways to make your home pay attention.",
        "Every system below is designed for your specific home, installed by our own GTA team, and tied "
        "together so you control all of it from one app and one voice assistant.",
        "Services")}

    <section class="section section--tight" style="padding-bottom:0">
      <div class="container">
        <div class="btn-row">{nav_chips}</div>
      </div>
    </section>

{groups}    <section class="section section--alt" style="padding-top:0">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">{icon('blinds')} Also from IQ Homes</span>
          <h2>Blinds, shutters and motorised shades.</h2>
          <p class="lead">Beyond the automation, we supply and fit window coverings across the GTA — shutters, roller shades, zebra and silhouette, in custom sizes. We'll install blinds you bought elsewhere too, and we can motorise almost any of it.</p>
        </div>
        <div class="btn-row">
          <a class="btn btn--dark btn--lg" href="blinds.html">{icon('arrow')} See all blinds &amp; shutters</a>
          <a class="btn btn--ghost btn--lg" href="contact.html?service=blinds-measure">Free measure &amp; quote</a>
        </div>
      </div>
    </section>

    <section class="section section--tight">
      <div class="container">
        {single_jobs()}
      </div>
    </section>

    <section class="section on-dark">
      <div class="container">
        <div class="section-head section-head--center">
          <span class="eyebrow">How it works</span>
          <h2>However much of this you want, it starts the same way.</h2>
        </div>
        <div class="grid grid--3">
          {steps}
        </div>
      </div>
    </section>

{cta_band("Not sure which of these you actually need?",
          "That's exactly what the free consultation is for. We'll walk your home, listen to what "
          "annoys you about it, and tell you honestly which of these is worth doing first — and "
          "which can wait.")}"""

    page("services.html",
         "Smart Home Services | Locks, Cameras, Lighting &amp; Audio | IQ Homes GTA",
         "Smart locks, video doorbells, security cameras, voice lighting, motorized blinds, smart "
         "climate, home theatre, mesh Wi-Fi and more — designed and installed across the Greater "
         "Toronto Area by IQ Homes.",
         body, "services.html", over_hero=True)


# ===========================================================================
#  Blinds
# ===========================================================================
def build_blinds():
    types = "".join(blind_card(*b) for b in BLIND_TYPES)

    models = "".join(
        f"""<div class="feature reveal" data-delay="{i+1}">
            <span class="feature-icon">{icon(ic)}</span>
            <div><h3>{t}</h3><p>{d}</p></div>
          </div>
          """
        for i, (ic, t, d) in enumerate(BLIND_MODELS)
    )

    steps = [
        ("Free in-home measure",
         "We come to you and measure every window properly. You'll see samples of the fabrics and "
         "types in your own light, against your own walls — which matters more than you'd think."),
        ("Choose and order",
         "We help you narrow it down by room: blackout where you sleep, sheer where you sit, "
         "moisture-safe where it's wet. Then we place the order and handle the supplier."),
        ("Fitted and finished",
         "Usually two to four weeks later we're back to install. Brackets level, blinds square, "
         "packaging taken away with us. If they're motorised, we set the schedules before we go."),
    ]
    step_html = "".join(
        f"""<div class="step reveal" data-delay="{i+1}">
            <span class="step-num">0{i+1}</span>
            <h3>{t}</h3>
            <p>{d}</p>
          </div>
          """
        for i, (t, d) in enumerate(steps)
    )

    rooms = [
        ("Bedrooms", "Blackout roller or a shutter. The one room where light control genuinely affects your sleep."),
        ("Living &amp; family rooms", "Zebra or silhouette — privacy from the street without giving up the daylight."),
        ("Kitchens &amp; bathrooms", "Composite shutters or moisture-safe fabrics that won't warp or hold damp."),
        ("Home offices", "Light-filtering rollers that kill screen glare without making you sit in the dark."),
        ("Patio &amp; slider doors", "Wide-format rollers or vertical panels made to the full opening."),
        ("Bays, arches &amp; stairwells", "Custom-shaped orders — the windows nothing off the shelf ever fits."),
    ]
    room_html = "".join(
        f"""<div class="card reveal" data-delay="{(i % 3) + 1}">
            <h3>{t}</h3>
            <p>{d}</p>
          </div>
          """
        for i, (t, d) in enumerate(rooms)
    )

    faq_blinds = next(qs for name, qs in FAQS if name == "Blinds")
    faq_html = ""
    for n, (q, a) in enumerate(faq_blinds, start=1):
        faq_html += f"""<div class="faq-item">
              <h3>
                <button class="faq-q" type="button" aria-expanded="false" aria-controls="bfaq-a-{n}" id="bfaq-q-{n}">
                  <span>{q}</span><span class="faq-icon">{icon('plus')}</span>
                </button>
              </h3>
              <div class="faq-a" id="bfaq-a-{n}" role="region" aria-labelledby="bfaq-q-{n}">
                <div><p>{a}</p></div>
              </div>
            </div>
            """

    body = f"""{page_hero(
        "Blinds, shutters and shades — measured, made and fitted.",
        "Shutters, roller shades, zebra and silhouette, in any size or shape your windows happen "
        "to be. We supply and install, we install what you've already bought, and because we do "
        "smart homes we can motorise any of it.",
        "Blinds")}

    <section class="section section--tight">
      <div class="container">
        {single_jobs(
          "Blinds for one bedroom is a perfectly normal job for us. So is installing a set you "
          "already ordered from somewhere else, or motorising the blinds you've had for years. "
          "Tell us the one thing you need and we'll price just that."
        )}
      </div>
    </section>

    <section class="section" style="padding-top:0">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">{icon('blinds')} What we fit</span>
          <h2>Seven ways to cover a window properly.</h2>
          <p class="lead">Each one suits a different room and a different problem. If you're not sure which, that's what the free measure is for — we'll tell you honestly which is worth the money in your house.</p>
        </div>
        <div class="grid grid--3">
          {types}
        </div>
      </div>
    </section>

    <section class="section on-dark" id="motorised">
      <div class="container">
        <div class="split">
          <div>
            <span class="eyebrow">The part nobody else does</span>
            <h2>Blinds that behave like part of the house.</h2>
            <p class="lead mt-2">
              Most blinds companies can sell you a motor. Very few can tie that motor into your
              lighting, your climate and your voice assistant — because that's a different trade.
              We do both, which is the whole reason we sell blinds at all.
            </p>
            <p class="mt-2">
              Set the west-facing blinds to drop at 2pm in July and the house stays cooler without
              touching the air conditioning. Have the bedroom lift gently with the sunrise. Say
              "goodnight" once and watch every blind in the house close along with the lights.
            </p>
            <div class="btn-row mt-3">
              <a class="btn btn--primary" href="contact.html?service=smart-blinds">{icon('arrow')} Price smart blinds</a>
              <a class="btn btn--ghost-light" href="services.html">See the automation side</a>
            </div>
          </div>
          <div class="split-media reveal">
            {img_slot('Motorised blinds',
                      'Drop a motorised blind photo at assets/img/photos/blinds-motorised.jpg',
                      src='assets/img/photos/blinds-motorised.jpg',
                      alt='Motorised blinds lowering in a bright living room')}
          </div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">How you can buy</span>
          <h2>Three ways to work with us on blinds.</h2>
        </div>
        <div class="grid mt-2" style="gap:1.8rem">
          {models}
        </div>
      </div>
    </section>

    <section class="section section--alt">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">Room by room</span>
          <h2>What we'd put where.</h2>
          <p class="lead">A rough starting point. Your windows, your light and your street decide the rest.</p>
        </div>
        <div class="grid grid--3">
          {room_html}
        </div>
      </div>
    </section>

    <section class="section on-dark">
      <div class="container">
        <div class="section-head section-head--center">
          <span class="eyebrow">The process</span>
          <h2>Measure, choose, fit.</h2>
        </div>
        <div class="grid grid--3">
          {step_html}
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container container--narrow">
        <span class="eyebrow">Blinds questions</span>
        <h2>The things people ask before ordering.</h2>
        <div class="faq-list mt-3">
          {faq_html}
        </div>
        <p class="mt-3"><a class="link-arrow" href="faq.html">See every FAQ {icon('arrow')}</a></p>
      </div>
    </section>

{cta_band("Book a free in-home measure.",
          "No charge, no obligation, and you'll see the fabrics in your own light before you decide "
          "anything. 30% off your first install applies to blinds too.")}"""

    page("blinds.html",
         "Custom Blinds, Shutters &amp; Motorised Shades | GTA | IQ Homes",
         "Custom blinds and shutters across the GTA — plantation shutters, roller shades, zebra, "
         "silhouette, plus motorised and smart blinds. Supply and install, or installation only. "
         "Free in-home measure anywhere in the Greater Toronto Area.",
         body, "blinds.html", over_hero=True)


# ===========================================================================
#  Gallery
# ===========================================================================
def build_gallery():
    ads = [
        ("ad-come-home-to-smarter.jpg", "Come home to smarter", "Launch campaign · hero creative"),
        ("ad-one-app-every-room.jpg", "One app. Every room. Total control.", "Unified control campaign"),
        ("ad-24-7-eyes.jpg", "24/7 eyes on your home", "Security campaign"),
        ("ad-trusted-across-gta.jpg", "Trusted by homeowners across the GTA", "Local trust campaign"),
    ]
    ad_grid = "".join(
        f"""<figure class="gallery-item reveal" data-delay="{(i % 4) + 1}">
            {img_slot('Ad creative', 'Run fetch-brand-assets.sh to pull this in from Bloom.',
                      src='assets/img/ads/' + f, alt=t)}
            <figcaption class="gallery-cap">{t}<small>{sub}</small></figcaption>
          </figure>
          """
        for i, (f, t, sub) in enumerate(ads)
    )

    installs = [
        ("install-01.jpg", "Entryway", "Smart lock &amp; video doorbell"),
        ("install-02.jpg", "Living room", "In-ceiling audio &amp; wall-mounted display"),
        ("install-03.jpg", "Kitchen", "Voice lighting &amp; under-cabinet accent"),
        ("install-04.jpg", "Primary bedroom", "Motorized blackout blinds"),
        ("install-05.jpg", "Exterior", "Camera coverage &amp; landscape lighting"),
        ("install-06.jpg", "Utility", "Network rack &amp; leak sensors"),
    ]
    install_grid = "".join(
        f"""<figure class="gallery-item reveal" data-delay="{(i % 4) + 1}">
            {img_slot('Install photo', 'Drop a job photo at assets/img/photos/' + f,
                      src='assets/img/photos/' + f, alt=t + ' — ' + re.sub('<[^>]+>', '', sub))}
            <figcaption class="gallery-cap">{t}<small>{sub}</small></figcaption>
          </figure>
          """
        for i, (f, t, sub) in enumerate(installs)
    )

    def ba(n, title, note):
        return f"""<div class="reveal">
            <div class="ba">
              <div class="ba-layer ba-layer--before">
                {img_slot('Before', f'ba-{n}-before.jpg',
                          src=f'assets/img/photos/ba-{n}-before.jpg', alt='Before installation')}
              </div>
              <div class="ba-layer ba-layer--after">
                {img_slot('After', f'ba-{n}-after.jpg',
                          src=f'assets/img/photos/ba-{n}-after.jpg', alt='After installation')}
              </div>
              <span class="ba-tag ba-tag--before">Before</span>
              <span class="ba-tag ba-tag--after">After</span>
              <span class="ba-handle" aria-hidden="true"></span>
              <input class="ba-range" type="range" min="0" max="100" value="50" aria-label="Drag to compare before and after">
            </div>
            <h3 class="mt-2">{title}</h3>
            <p class="text-muted mt-1">{note}</p>
          </div>"""

    body = f"""{page_hero(
        "The work, and the brand behind it.",
        "Project photography goes up here as installs complete. Below that: the campaign creative we "
        "run across the GTA.",
        "Gallery")}

    <section class="section">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">Before &amp; after</span>
          <h2>Drag the handle to see the difference.</h2>
          <p class="lead">Nothing sells an install like the same doorway, before and after. Drop matching photo pairs in and these become your strongest page.</p>
        </div>
        <div class="grid grid--2">
          {ba(1, "Front entry — Mississauga", "Replace with a real pair: the same angle before the smart lock and doorbell went in, and after.")}
          {ba(2, "Living room — Vaughan", "A second pair. Wall-mounted display and concealed cabling reads especially well in before/after.")}
        </div>
      </div>
    </section>

    <section class="section section--alt">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">Install gallery</span>
          <h2>Room by room, job by job.</h2>
          <p class="lead">Six slots ready for real project photos. Shoot wide, shoot clean, and get the finished detail up close.</p>
        </div>
        <div class="gallery-grid">
          {install_grid}
        </div>
        <div class="mt-4">
          <p class="placeholder-note">
            {icon('info')}
            <span><strong>Adding photos:</strong> drop your images into <code>assets/img/photos/</code> using the
            filenames shown on each tile — the placeholder disappears automatically once the file is there.
            Shoot at roughly 4:5 (portrait) for the best fit, around 1600&nbsp;px wide.</span>
          </p>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">Campaign creative</span>
          <h2>The ads you'll see around the GTA.</h2>
        </div>
        <div class="gallery-grid">
          {ad_grid}
        </div>
      </div>
    </section>

{cta_band("Want your home in this gallery?",
          "Book the free consultation and let's design something worth photographing. 30% off your first install.")}"""

    page("gallery.html",
         "Gallery | Smart Home Installs Across the GTA | IQ Homes",
         "Project photography and campaign creative from IQ Homes — smart home installations across "
         "the entire Greater Toronto Area.",
         body, "gallery.html", over_hero=True)


# ===========================================================================
#  About
# ===========================================================================
def build_about():
    values = [
        ("users", "We show up ourselves",
         "The person who designs your system installs it and answers the phone afterward. That's not a policy — it's just how a local business this size works, and it's the main reason people choose us over a chain."),
        ("wrench", "We spec what the home needs",
         "There's no package we're pushing. If two rooms of lighting and a decent lock solves your actual problem, we'll tell you that and quote it, rather than talking you into a system you won't use."),
        ("shield", "We're straight about the trade-offs",
         "Some things are worth automating and some aren't. Some devices don't play well together. We'd rather tell you that at the consultation than have you find out after the invoice."),
        ("home", "We build it to grow",
         "Almost nobody does the whole house at once. We design so you can start with one floor and add blinds, cameras or audio in two years without tearing out what's already there."),
    ]
    vals = "".join(
        f"""<div class="feature reveal" data-delay="{i+1}">
            <span class="feature-icon">{icon(ic)}</span>
            <div><h3>{t}</h3><p>{d}</p></div>
          </div>
          """
        for i, (ic, t, d) in enumerate(values)
    )

    body = f"""{page_hero(
        "A GTA smart home company, run by someone who picks up the phone.",
        "IQ Homes was built on a simple frustration: smart home technology that's genuinely brilliant, "
        "sold and installed in a way that makes people give up on it.",
        "About")}

    <section class="section">
      <div class="container">
        <div class="split">
          <div class="split-media reveal">
            {img_slot('Founder portrait',
                      'Drop a photo of Kshitij at assets/img/photos/founder.jpg',
                      src='assets/img/photos/founder.jpg',
                      alt='Kshitij Dua, founder of IQ Homes')}
          </div>
          <div>
            <span class="eyebrow">The founder</span>
            <h2>Kshitij Dua</h2>
            <p class="lead mt-2">
              I started IQ Homes because I kept watching the same thing happen. Someone buys a smart lock,
              then a doorbell from a different brand, then a couple of bulbs on sale. Six months later
              there are four apps on their phone, two of them don't talk to each other, and the whole
              thing has quietly stopped being used.
            </p>
            <p class="mt-2 text-muted">
              The technology was never the problem. The problem was that nobody sat in the house, looked
              at how the family actually lived in it, and designed one system that fit. That's the entire
              job, and it's what IQ Homes does.
            </p>
            <p class="mt-2 text-muted">
              We're based in the GTA and we work across all of it — the City of Toronto and every
              municipality in Peel, York, Durham and Halton. Small enough that you deal with the same
              people from the first walkthrough to the call you make eighteen months later. That's
              deliberate.
            </p>
            <div class="btn-row mt-3">
              <a class="btn btn--primary" href="contact.html">{icon('calendar')} Book a free consultation</a>
              <a class="btn btn--ghost" href="tel:{PHONE_LINK}">{icon('phone')} {PHONE_DISPLAY}</a>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section on-dark">
      <div class="container container--narrow text-center">
        <span class="eyebrow">Our mission</span>
        <h2>Make the smart home feel less like technology and more like a house that pays attention.</h2>
        <p class="lead mt-3">
          When it's done right, you stop noticing it. The lights are already how you like them. The door
          is locked. The house is warm. Nobody in the family had to learn anything, and nobody is
          opening an app to make it happen.
        </p>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">How we work</span>
          <h2>Four things we don't compromise on.</h2>
        </div>
        <div class="grid grid--2" style="gap:2rem 3rem">
          {vals}
        </div>
      </div>
    </section>

    <section class="section section--alt">
      <div class="container">
        <div class="split split--reverse">
          <div class="split-media reveal">
            {img_slot('GTA neighbourhood',
                      'assets/img/photos/gta-street-daytime.jpg — run fetch-brand-assets.sh',
                      src='assets/img/photos/gta-street-daytime.jpg',
                      alt='A suburban street in the Greater Toronto Area')}
          </div>
          <div>
            <span class="eyebrow">Local matters</span>
            <h2>Why a GTA company installs a GTA home better.</h2>
            <p class="lead mt-2">
              Homes here have their own quirks — the housing stock, the winters, the way older Toronto
              semis are wired versus a new build in Springdale.
            </p>
            <p class="mt-2 text-muted">
              A national installer sends whoever is closest with a standard kit. We already know that a
              1950s East York bungalow needs a different networking approach than a four-storey Markham
              new build, and that a January install has to account for a lock that lives at minus twenty.
              That knowledge only comes from working here.
            </p>
            <div class="btn-row mt-3">
              <a class="btn btn--dark" href="service-area.html">See our service area {icon('arrow')}</a>
            </div>
          </div>
        </div>
      </div>
    </section>

{cta_band("Let's talk about your home.",
          "An hour, no charge, no obligation — and you'll come away knowing exactly what's worth doing "
          "and what it costs.")}"""

    page("about.html",
         "About IQ Homes | Smart Home Automation Founded in the GTA",
         "IQ Homes is a locally owned smart home automation company serving the Greater Toronto Area. "
         "Founded by Kshitij Dua on the belief that a smart home should be designed, not assembled.",
         body, "about.html", over_hero=True)


# ===========================================================================
#  Service area
# ===========================================================================
def build_service_area():
    # Just outside the GTA proper — we'll travel for these, case by case
    surrounding = ["Hamilton", "Barrie", "Guelph", "Kitchener", "Waterloo", "Cambridge",
                   "St. Catharines", "Niagara Falls", "Orangeville", "Bradford",
                   "Innisfil", "Peterborough", "Cobourg", "Port Hope"]
    surr = "".join(f'<li class="check" style="cursor:default">{icon("pin")} {c}</li>' for c in surrounding)

    # Every municipality we cover, listed by region — the detail that makes this
    # page rank for "smart home installation <town>" searches
    full_list = "".join(
        f"""<div class="card reveal" data-delay="{i+1}" style="gap:.6rem">
            <h3 style="font-size:1.05rem">{region}</h3>
            <ul class="town-list">
              {"".join(f'<li>{icon("check")}<span>{c}</span></li>' for c in cities)}
            </ul>
          </div>
          """
        for i, (region, cities) in enumerate(GTA_MUNICIPALITIES)
    )

    body = f"""{page_hero(
        "Serving homeowners across the Greater Toronto Area.",
        "We're a local team, so our service area is a real one — not a map with a national call centre "
        "behind it. Here's exactly where we install.",
        "Service Area")}

    <section class="section">
      <div class="container container--narrow">
        <div class="checker reveal">
          <span class="eyebrow">Coverage check</span>
          <h2>Do we install where you live?</h2>
          <p class="text-muted mt-1">Type your city or neighbourhood and we'll tell you straight away.</p>
          <form class="checker-form" data-checker novalidate>
            <label class="sr-only" for="city-check">Your city or neighbourhood</label>
            <input id="city-check" type="text" placeholder="e.g. Whitby, Woodbridge, Scarborough, Oakville" autocomplete="address-level2">
            <button class="btn btn--primary" type="submit">Check coverage</button>
          </form>
          <div class="checker-result" data-checker-result role="status"></div>
        </div>
      </div>
    </section>

    <section class="section section--tight">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">Full service area</span>
          <h2>Five regions. Thirty cities and towns. The whole GTA.</h2>
          <p class="lead">The City of Toronto plus Peel, York, Durham and Halton. No travel charges anywhere in the GTA, no minimum job size, and same-week consultations throughout.</p>
        </div>
        <div class="city-grid">
          {city_cards()}
        </div>

        <div class="mt-4">
          <h2 style="font-size:var(--fs-h3)">Every city and town we cover</h2>
          <p class="text-muted mt-1">All {GTA_COUNT} of them. No travel surcharge anywhere on this list.</p>
          <div class="grid grid--3 mt-3">
            {full_list}
          </div>
        </div>
      </div>
    </section>

    <section class="section section--alt">
      <div class="container">
        <div class="split">
          <div>
            <span class="eyebrow">Outside the GTA?</span>
            <h2>We travel beyond it for the right job.</h2>
            <p class="lead mt-2">
              These are outside the Greater Toronto Area, so they're case by case rather than
              automatic. Get in touch anyway — depending on the size of the job and what else we
              have booked that week, the answer is often yes.
            </p>
            <ul class="checks mt-3">
              {surr}
            </ul>
            <div class="btn-row mt-3">
              <a class="btn btn--primary" href="tel:{PHONE_LINK}">{icon('phone')} Call {PHONE_DISPLAY}</a>
              <a class="btn btn--ghost" href="contact.html">Send a message {icon('arrow')}</a>
            </div>
          </div>
          <div class="split-media reveal">
            {img_slot('GTA coverage',
                      'assets/img/photos/gta-street-daytime.jpg — run fetch-brand-assets.sh',
                      src='assets/img/photos/gta-street-daytime.jpg',
                      alt='A Greater Toronto Area neighbourhood served by IQ Homes')}
          </div>
        </div>
      </div>
    </section>

    <section class="section on-dark">
      <div class="container">
        <div class="section-head section-head--center">
          <span class="eyebrow">What to expect</span>
          <h2>The same visit, wherever you are in the GTA.</h2>
        </div>
        <div class="grid grid--3">
          <div class="feature reveal"><span class="feature-icon">{icon('clock')}</span>
            <div><h3>Booked within the week</h3><p>Consultations are typically available within a few days anywhere in the GTA, including evenings and weekends — because that's when most families are actually home.</p></div></div>
          <div class="feature reveal" data-delay="1"><span class="feature-icon">{icon('pin')}</span>
            <div><h3>We come to you</h3><p>No showroom visit needed. Systems are designed in the home they're going into, which is the only way to get it right.</p></div></div>
          <div class="feature reveal" data-delay="2"><span class="feature-icon">{icon('gauge')}</span>
            <div><h3>A price before you commit</h3><p>You leave the consultation with an itemised quote, the 30% discount already applied, and no obligation whatsoever.</p></div></div>
        </div>
      </div>
    </section>

{cta_band("Book your free consultation.",
          "Anywhere in the Greater Toronto Area — we'll come to you, walk the home, and "
          "leave you with a plan and a price.")}"""

    page("service-area.html",
         "Service Area | Smart Home Installation Across the GTA | IQ Homes",
         "IQ Homes installs smart home systems and blinds across the entire Greater Toronto Area — "
         "Toronto, Peel, York, Durham and Halton. Check whether we cover your address.",
         body, "service-area.html", over_hero=True)


# ===========================================================================
#  FAQ
# ===========================================================================
def build_faq():
    sections = ""
    faq_entities = []
    n = 0
    for gi, (gname, qs) in enumerate(FAQS):
        items = ""
        for q, a in qs:
            n += 1
            items += f"""<div class="faq-item">
              <h3>
                <button class="faq-q" type="button" aria-expanded="false" aria-controls="faq-a-{n}" id="faq-q-{n}">
                  <span>{q}</span>
                  <span class="faq-icon">{icon('plus')}</span>
                </button>
              </h3>
              <div class="faq-a" id="faq-a-{n}" role="region" aria-labelledby="faq-q-{n}">
                <div><p>{a}</p></div>
              </div>
            </div>
            """
            clean_q = re.sub("<[^>]+>", "", q).replace('"', "'").replace("&amp;", "&")
            clean_a = re.sub("<[^>]+>", "", a).replace('"', "'").replace("&amp;", "&")
            faq_entities.append(
                '{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}'
                % (clean_q, clean_a)
            )
        alt = " section--alt" if gi % 2 == 1 else ""
        sections += f"""    <section class="section section--tight{alt}">
      <div class="container container--narrow">
        <span class="eyebrow">{gname}</span>
        <div class="faq-list mt-2">
          {items}
        </div>
      </div>
    </section>

"""

    jsonld = '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[%s]}' % ",".join(faq_entities)

    body = f"""{page_hero(
        "Questions people ask before they call.",
        "Pricing, timelines, whether it works with what you already own, and what happens when the "
        "internet goes down. Straight answers — if yours isn't here, just call.",
        "FAQ")}

{sections}    <section class="section on-dark">
      <div class="container container--narrow text-center">
        <span class="eyebrow">Still wondering?</span>
        <h2>Ask us directly — it's the fastest way.</h2>
        <p class="lead mt-2">Most questions take two minutes on the phone. No script, no sales pitch, and no charge for the consultation if you want one.</p>
        <div class="btn-row mt-3" style="justify-content:center">
          <a class="btn btn--primary btn--lg" href="tel:{PHONE_LINK}">{icon('phone')} {PHONE_DISPLAY}</a>
          <a class="btn btn--ghost-light btn--lg" href="mailto:{EMAIL}">{icon('mail')} Email us</a>
        </div>
      </div>
    </section>

{cta_band()}"""

    page("faq.html",
         "FAQ | Smart Home Installation Questions Answered | IQ Homes GTA",
         "How much does a smart home cost, how long does installation take, and will it work with the "
         "devices you already own? Straight answers from IQ Homes, serving the GTA.",
         body, "faq.html", over_hero=True, extra_jsonld=jsonld)


# ===========================================================================
#  Contact
# ===========================================================================
def build_contact():
    def clean(s):
        return re.sub("<[^>]+>", "", s).replace("&amp;", "&")

    smart_services = [(sid, clean(name))
                      for _, _, _, _, items in SERVICE_GROUPS
                      for sid, name, _, _ in items]

    blind_services = [("blinds-measure", "Free blinds measure & quote")] + \
                     [(sid, clean(name)) for sid, name, _, _, _ in BLIND_TYPES] + \
                     [("blinds-install-only", "Install blinds I already bought")]

    def check_group(items):
        return "".join(
            f"""<label class="check">
              <input type="checkbox" name="service" value="{sid}">
              <span>{name}</span>
            </label>
            """
            for sid, name in items
        )

    checks = check_group(smart_services)
    blind_checks = check_group(blind_services)

    # Grouped by region so a 30-item dropdown stays scannable
    city_opts = "".join(
        f'<optgroup label="{region}">'
        + "".join(f'<option value="{c}">{c}</option>' for c in cities)
        + "</optgroup>"
        for region, cities in GTA_MUNICIPALITIES
    )

    body = f"""{page_hero(
        "Book your free consultation.",
        "Tell us a little about your home and what you're hoping to fix. We'll call you back to arrange "
        "a visit — usually within one business day.",
        "Contact")}

    <section class="section">
      <div class="container">
        <div class="split" style="align-items:start">
          <div class="form-card reveal">
            <!-- Netlify Forms: the name + data-netlify attributes are what Netlify's
                 build-time parser looks for. form-name must match the name attribute.
                 bot-field is an invisible honeypot — real people never fill it in, bots do. -->
            <form data-consult-form
                  name="consultation"
                  method="POST"
                  data-netlify="true"
                  netlify-honeypot="bot-field"
                  action="/thank-you.html"
                  novalidate>
              <input type="hidden" name="form-name" value="consultation">
              <p class="sr-only" aria-hidden="true">
                <label>Leave this field empty: <input name="bot-field" tabindex="-1" autocomplete="off"></label>
              </p>
              <span class="eyebrow">{icon('calendar')} Free consultation + 30% off</span>
              <h2 style="font-size:var(--fs-h3)">Request your visit</h2>
              <p class="text-muted mt-1" style="font-size:var(--fs-sm)">Fields marked <span class="req">*</span> are required.</p>

              <div class="form-grid mt-3">
                <div class="field">
                  <label for="name">Your name <span class="req">*</span></label>
                  <input id="name" name="name" type="text" autocomplete="name" placeholder="Jane Doe" required>
                  <span class="field-error">Please enter your name.</span>
                </div>

                <div class="field">
                  <label for="phone">Phone <span class="req">*</span></label>
                  <input id="phone" name="phone" type="tel" autocomplete="tel" placeholder="647-000-0000" required>
                  <span class="field-error">Please enter a valid phone number.</span>
                </div>

                <div class="field">
                  <label for="email">Email <span class="req">*</span></label>
                  <input id="email" name="email" type="email" autocomplete="email" placeholder="you@example.com" required>
                  <span class="field-error">Please enter a valid email address.</span>
                </div>

                <div class="field">
                  <label for="city">City <span class="req">*</span></label>
                  <select id="city" name="city" required>
                    <option value="">Select your city…</option>
                    {city_opts}
                    <option value="Other">Somewhere else — I'll explain below</option>
                  </select>
                  <span class="field-error">Please choose your city.</span>
                </div>

                <div class="field form-full">
                  <label for="address">Address or neighbourhood</label>
                  <input id="address" name="address" type="text" autocomplete="street-address" placeholder="Optional — helps us plan the visit">
                </div>

                <div class="field form-full">
                  <label>Smart home — what are you interested in?</label>
                  <div class="checks">
                    {checks}
                  </div>
                </div>

                <div class="field form-full">
                  <label>Blinds &amp; shutters</label>
                  <div class="checks">
                    {blind_checks}
                  </div>
                </div>

                <div class="field form-full">
                  <p class="form-note">
                    Only want one item priced? Just tick that one — single jobs are welcome and
                    there's no minimum.
                  </p>
                </div>

                <div class="field form-full">
                  <label for="message">Anything else we should know?</label>
                  <textarea id="message" name="message" placeholder="Tell us about your home — its age, size, what's bothering you, whether you already have any smart devices."></textarea>
                </div>
              </div>

              <div class="mt-3">
                <button class="btn btn--primary btn--lg btn--block" type="submit">
                  {icon('calendar')} Request my free consultation
                </button>
                <p class="form-note mt-2">
                  We'll only use your details to arrange your consultation. No marketing lists, no sharing with anyone.
                </p>
              </div>
            </form>

            <div class="form-success" data-form-success>
              <span class="tick">{icon('check')}</span>
              <h2 style="font-size:var(--fs-h3)">Thanks — we've got it.</h2>
              <p class="text-muted">We'll be in touch within one business day to arrange a time that suits you. If it's urgent, call us on <a href="tel:{PHONE_LINK}" class="link-arrow">{PHONE_DISPLAY}</a>.</p>
            </div>
          </div>

          <div>
            <span class="eyebrow">Or just call</span>
            <h2>Some things are quicker on the phone.</h2>
            <p class="lead mt-2">If you'd rather ask a couple of questions before booking anything, that's completely fine.</p>

            <div class="grid mt-3" style="gap:1.4rem">
              <div class="feature">
                <span class="feature-icon">{icon('phone')}</span>
                <div><h3>Phone</h3><p><a href="tel:{PHONE_LINK}" class="link-arrow">{PHONE_DISPLAY}</a></p></div>
              </div>
              <div class="feature">
                <span class="feature-icon">{icon('mail')}</span>
                <div><h3>Email</h3><p><a href="mailto:{EMAIL}" class="link-arrow">{EMAIL}</a></p></div>
              </div>
              <div class="feature">
                <span class="feature-icon">{icon('pin')}</span>
                <div><h3>Service area</h3><p>The entire Greater Toronto Area — Toronto, Peel, York, Durham and Halton. <a href="service-area.html" class="link-arrow">Check your address {icon('arrow')}</a></p></div>
              </div>
              <div class="feature">
                <span class="feature-icon">{icon('clock')}</span>
                <div><h3>Consultation times</h3><p>Evenings and weekends available — most families would rather we came when everyone's home.</p></div>
              </div>
            </div>

            <div class="mt-4">
              <p class="placeholder-note">
                {icon('info')}
                <span><strong>Note for Kshitij:</strong> this form is wired for Netlify Forms and will
                start working the moment the site is deployed. After your first deploy, turn on email
                notifications (Netlify → Forms → Settings) so submissions reach your inbox — see
                step 4 in <code>DEPLOY.md</code>. Send yourself a test, then delete this note.</span>
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

{cta_band("Prefer to see what's possible first?",
          "The services page walks through all fourteen systems we install, and the gallery shows the "
          "work. Either way, the consultation is free when you're ready.")}"""

    page("contact.html",
         "Book a Free Smart Home Consultation | IQ Homes GTA",
         "Book a free, no-obligation smart home consultation with IQ Homes. We serve the entire "
         "Greater Toronto Area — and take 30% off your first install.",
         body, "contact.html", over_hero=True)


# ===========================================================================
#  Thank you / 404
# ===========================================================================
def build_thankyou():
    body = f"""    <section class="page-hero" style="padding-bottom:clamp(4rem,3rem+5vw,7rem)">
      <div class="container container--narrow text-center">
        <span class="tick-big">{icon('check')}</span>
        <h1 style="margin-top:1.5rem">Thanks — we've got your request.</h1>
        <p class="lead" style="margin-inline:auto">
          One of us will call you back within one business day to arrange a time that suits you.
          Evenings and weekends are usually easiest for everyone.
        </p>
        <div class="btn-row mt-3" style="justify-content:center">
          <a class="btn btn--primary btn--lg" href="tel:{PHONE_LINK}">{icon('phone')} Call us now instead</a>
          <a class="btn btn--ghost-light btn--lg" href="index.html">Back to the site</a>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section-head section-head--center">
          <span class="eyebrow">While you wait</span>
          <h2>Worth a look before we speak.</h2>
        </div>
        <div class="grid grid--3">
          <article class="card">
            <span class="card-icon">{icon('wifi')}</span>
            <h3>What we install</h3>
            <p>All fourteen smart home systems, from locks and cameras to whole-home audio and mesh Wi-Fi.</p>
            <a class="quote-link" href="services.html">Browse services {icon('arrow')}</a>
          </article>
          <article class="card">
            <span class="card-icon">{icon('shutter')}</span>
            <h3>Blinds &amp; shutters</h3>
            <p>Shutters, roller, zebra and silhouette — custom made, and motorised if you want them.</p>
            <a class="quote-link" href="blinds.html">See blinds {icon('arrow')}</a>
          </article>
          <article class="card">
            <span class="card-icon">{icon('info')}</span>
            <h3>Common questions</h3>
            <p>Pricing, timelines, financing and whether it all works with the devices you already own.</p>
            <a class="quote-link" href="faq.html">Read the FAQ {icon('arrow')}</a>
          </article>
        </div>
      </div>
    </section>"""

    page("thank-you.html",
         "Thanks — we'll be in touch | IQ Homes",
         "Your consultation request has been received. IQ Homes will call you back within one "
         "business day.",
         body, "", over_hero=True, noindex=True)


def build_404():
    body = f"""    <section class="page-hero" style="padding-bottom:clamp(4rem,3rem+5vw,7rem)">
      <div class="container container--narrow text-center">
        <p class="eyebrow" style="justify-content:center">Error 404</p>
        <h1>That page seems to have moved.</h1>
        <p class="lead" style="margin-inline:auto">
          The link you followed doesn't lead anywhere on our site. Here's the way back.
        </p>
        <div class="btn-row mt-3" style="justify-content:center">
          <a class="btn btn--primary btn--lg" href="index.html">{icon('home')} Go to the home page</a>
          <a class="btn btn--ghost-light btn--lg" href="contact.html">Book a consultation</a>
        </div>
        <p class="mt-3" style="font-size:var(--fs-sm)">
          Or call us on <a class="link-arrow" href="tel:{PHONE_LINK}">{PHONE_DISPLAY}</a>
        </p>
      </div>
    </section>"""

    page("404.html",
         "Page not found | IQ Homes",
         "That page could not be found.",
         body, "", over_hero=True, noindex=True)


# ===========================================================================
#  Static extras
# ===========================================================================
def build_extras():
    # Favicon — the logo mark on a navy tile
    favicon = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <rect width="64" height="64" rx="14" fill="#0B2545"/>
  <g fill="none" stroke="#FFFFFF" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round">
    <path d="M32 31 51 44v11.5H13V44Z"/>
  </g>
  <g fill="none" stroke="#17D7C2" stroke-width="3.4" stroke-linecap="round">
    <path d="M27 23.5a7 7 0 0 1 10 0" opacity=".95"/>
    <path d="M23.2 20.8a12.6 12.6 0 0 1 17.6 0" opacity=".7"/>
    <path d="M19.4 18.1a18.2 18.2 0 0 1 25.2 0" opacity=".45"/>
  </g>
  <circle cx="32" cy="27.4" r="2.4" fill="#17D7C2"/>
  <path d="M28 55.5v-5.6a4 4 0 0 1 8 0v5.6Z" fill="#17D7C2"/>
</svg>"""
    with open(os.path.join(HERE, "assets", "favicon.svg"), "w", encoding="utf-8") as f:
        f.write(favicon)
    print("  wrote assets/favicon.svg")

    pages = ["", "services.html", "blinds.html", "gallery.html", "about.html",
             "service-area.html", "faq.html", "contact.html"]
    urls = "".join(
        f"""  <url>
    <loc>{SITE}/{p}</loc>
    <changefreq>monthly</changefreq>
    <priority>{'1.0' if p == '' else '0.9' if p in ('services.html', 'blinds.html', 'contact.html') else '0.7'}</priority>
  </url>
"""
        for p in pages
    )
    with open(os.path.join(HERE, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}</urlset>
""")
    print("  wrote sitemap.xml")

    with open(os.path.join(HERE, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    print("  wrote robots.txt")

    # Script that pulls the Bloom creatives down onto Kshitij's machine
    fetch = """#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# IQ Homes — pull the brand creatives out of Bloom into this site.
# Run once from the site folder:   bash fetch-brand-assets.sh
# ---------------------------------------------------------------------------
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p assets/img/photos assets/img/ads

echo "Fetching IQ Homes brand creatives…"

get () { curl -fsSL -o "$2" "$1" && echo "  ✓ $2" || echo "  ✗ $2 (failed — grab it manually from trybloom.ai)"; }

# Photoreal base creatives — used across the site
get "https://www.trybloom.ai/img/afa5d031-c600-4014-963b-908fee0e1499" "assets/img/photos/hero-dusk-unlock.jpg"
get "https://www.trybloom.ai/img/d48e7ee3-9489-439c-b3c7-4f2d4383cb0f" "assets/img/photos/app-control-phone.jpg"
get "https://www.trybloom.ai/img/a8527e66-6c5b-41dd-9bba-7cfe0b0a028c" "assets/img/photos/doorbell-night.jpg"
get "https://www.trybloom.ai/img/c6a6fe1a-09dd-48c0-9df4-1b312c9e1dda" "assets/img/photos/gta-street-daytime.jpg"

# Finished ad posters — shown in the gallery
get "https://www.trybloom.ai/img/f1073616-4655-4e64-84ef-0fcb6640c7d9" "assets/img/ads/ad-come-home-to-smarter.jpg"
get "https://www.trybloom.ai/img/08a20635-9b69-41fb-b16d-157071e4e117" "assets/img/ads/ad-one-app-every-room.jpg"
get "https://www.trybloom.ai/img/30792d25-78b8-48ac-ba35-58721710db5d" "assets/img/ads/ad-24-7-eyes.jpg"
get "https://www.trybloom.ai/img/629474ea-b9b2-4cce-ab21-5b77b366ae12" "assets/img/ads/ad-trusted-across-gta.jpg"

echo
echo "Done. Reload the site — the placeholders will be gone."
"""
    p = os.path.join(HERE, "fetch-brand-assets.sh")
    with open(p, "w", encoding="utf-8") as f:
        f.write(fetch)
    os.chmod(p, 0o755)
    print("  wrote fetch-brand-assets.sh")


def build_all():
    print("Building IQ Homes…")
    build_index()
    build_services()
    build_blinds()
    build_gallery()
    build_about()
    build_service_area()
    build_faq()
    build_contact()
    build_thankyou()
    build_404()
    build_extras()
    print("Done.")
