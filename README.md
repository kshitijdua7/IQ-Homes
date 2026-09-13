# IQ Homes — website

An eight-page marketing site for IQ Homes — smart home automation and blinds across
the Greater Toronto Area — built around an interactive 3D smart home in the hero.
Plain HTML, CSS and JavaScript. No framework, no backend, no build step required to
host it. Upload the folder and it works.

**Going live? Read `DEPLOY.md`.**

---

## Contents

```
index.html            Home — 3D house, services, blinds, process, reviews
services.html         All 14 smart home services, grouped into four categories
blinds.html           Blinds & shutters — 7 types, how to buy, room guide, FAQs
gallery.html          Before/after sliders, install photo grid, ad creatives
about.html            Founder story, mission, why local
service-area.html     Coverage checker + all 30 GTA cities and towns
faq.html              25 questions across six groups (with FAQ schema for Google)
contact.html          Consultation booking form

assets/css/style.css        All styling, driven by CSS custom properties
assets/js/main.js           Nav, accordion, form, coverage checker, scroll reveals
assets/js/house3d.js        The interactive 3D house
assets/js/vendor/           Three.js (self-hosted — no CDN dependency)
assets/img/photos/          Your photography goes here
assets/img/ads/             Campaign creatives go here
assets/favicon.svg          Logo mark on a navy tile

build.py + _pages.py        Optional generator (see "Editing content")
thank-you.html              Where the form lands on success
404.html                    Friendly not-found page
fetch-brand-assets.sh       Pulls your Bloom creatives into assets/img/
netlify.toml                Hosting config — headers, caching, clean URLs
set-domain.py               Points the site at your real domain in one command
sitemap.xml, robots.txt     SEO basics
DEPLOY.md                   Full step-by-step guide to going live
```

---

## 1. First thing to run

Your ad creatives live in Bloom, not in this folder yet. From inside this folder:

```bash
bash fetch-brand-assets.sh
```

That downloads all eight images into the right places. Reload the site and the
image placeholders disappear.

---

## 2. Putting it online

**See `DEPLOY.md`** — it's the full step-by-step: buying a domain, deploying to
Netlify, connecting DNS, switching the form on, and registering with Google.
About an hour of your time and roughly $20/year all in.

The short version: run `fetch-brand-assets.sh`, then drag this folder onto
[app.netlify.com/drop](https://app.netlify.com/drop).

There is **no backend to run**. No server, no database, no monthly hosting bill —
the site is plain files, and Netlify handles the form for free.

> **Local preview:** open a terminal in this folder and run `python3 -m http.server`,
> then visit `http://localhost:8000`. Don't just double-click `index.html` — the 3D
> house loads as an ES module and browsers block those on `file://` URLs.

---

## 3. Set your domain

Once the domain is bought, run this from inside the folder:

```bash
python3 set-domain.py yourdomain.ca
```

It updates the canonical URLs, social share tags, `sitemap.xml`, `robots.txt` and
the Google structured data, then rebuilds every page. Redeploy afterwards so the
live site picks it up.

The site works perfectly fine before you do this — it only affects what Google and
social previews see.

> **Heads up:** `iqhomes.ca` and `iqhomes.com` are both already registered by other
> people. `DEPLOY.md` step 1 lists alternatives that suit a GTA trade business.

---

## 4. The form

**Already wired** for Netlify Forms — the markup, the hidden `form-name` field and
a honeypot spam trap are all in `contact.html`, and successful submissions land on
`thank-you.html`.

The only thing left is telling Netlify where to email them: **Forms → Settings →
Form notifications**. That's step 4 in `DEPLOY.md`.

Submissions are also kept in the Netlify dashboard permanently, so nothing is lost
if an email goes astray. Free tier covers 100 per month.

Once you've sent yourself a test and it arrives, delete the blue "Note for Kshitij"
box in `contact.html`.

**Switching to a different host later?** Replace the `data-netlify` attributes with
`action="https://formspree.io/f/YOUR_ID"` from [formspree.io](https://formspree.io).
The JavaScript honours whatever `action` is set.

---

## 5. Adding your photos

Drop files into `assets/img/photos/` using these exact names and the placeholders
vanish automatically:

| File | Where it appears |
|---|---|
| `founder.jpg` | About page — your portrait |
| `blinds-hero.jpg` | Home page — the blinds section |
| `blinds-motorised.jpg` | Blinds page — the motorised/smart section |
| `install-01.jpg` … `install-06.jpg` | Gallery — install photo grid |
| `ba-1-before.jpg` / `ba-1-after.jpg` | Gallery — first before/after slider |
| `ba-2-before.jpg` / `ba-2-after.jpg` | Gallery — second before/after slider |

Shoot portrait, roughly 4:5, about 1600px on the long edge. Compress them before
uploading — [squoosh.app](https://squoosh.app) is free and takes seconds. Aim for
under 300KB each.

**Before/after pairs matter most.** Same camera position, same framing, one shot
before you start and one after. Nothing else on the site will sell as well.

---

## 6. The 3D house

`assets/js/house3d.js` builds the whole scene procedurally — every wall, room,
piece of furniture and glowing hotspot is generated in code, so there are no
model files to manage and the whole thing is a few hundred lines.

The nine hotspots are defined in the `DEVICES` array at the top of that file. To
change a name or description, edit it there. To move one, adjust its `pos: [x, y, z]`.

Service cards on the home page carry `data-focus-device="lock"` etc. — clicking one
swings the camera to that device on the model.

It degrades gracefully: no WebGL shows a fallback panel, `prefers-reduced-motion`
disables the auto-rotate and pulsing, and rendering pauses entirely when the hero
scrolls off screen.

---

## 6b. The hero effect (bloom + scan sweep)

The hero recreates the futuristic component effect — depth reveal, red scan line
and bloom glow — but on real 3D geometry instead of a flat photo with a depth map.
Because the house *is* 3D, the scan runs through actual world-space height rather
than a faked depth texture, which is why it wraps correctly around the roof and
walls as it climbs.

Three parts, all in `house3d.js`:

- **Bloom** — `UnrealBloomPass` near the bottom of the file. `0.52` is strength,
  `0.30` is threshold. Raise the threshold if it feels blown out, lower it for more glow.
- **The world-space scan** — the `scanUniforms` block near the top. `uScanColor` is
  the red, `uScanBoost` the teal it shifts toward at the leading edge,
  `uScanDensity` the dot size.
- **The screen scan line** — `ScanLineShader`. It runs *after* `OutputPass` on
  purpose: it owns the final alpha, which is what stops the post-processing chain
  painting a black rectangle over the hero gradient.

Speed is the `t * 0.42` in the render loop. All of it switches off automatically
under `prefers-reduced-motion`, and if the effect chain fails to compile the scene
falls back to a plain render rather than showing nothing.

> **On the React component you sent:** it needed Next.js, shadcn and Tailwind, used
> `WebGPURenderer` with no fallback (blank hero on any browser without WebGPU), and
> hotlinked two images from a free image host — including a depth map generated for
> someone else's photo. This version gets the same look with none of those liabilities,
> and works in every browser that does WebGL.

---

## 6c. Per-service pricing links

Every service and blind type has a **"Get a price for just this"** link. It goes to
`contact.html?service=<id>` and the form auto-ticks that one item and scrolls to it.

So you can use these links directly in ads, texts and Marketplace replies:

```
https://YOURDOMAIN.com/contact.html?service=doorbell
https://YOURDOMAIN.com/contact.html?service=zebra
https://YOURDOMAIN.com/contact.html?service=smart-blinds
https://YOURDOMAIN.com/contact.html?service=blinds-measure
https://YOURDOMAIN.com/contact.html?service=blinds-install-only
```

The id is whatever is in the `value=""` of the matching checkbox in `contact.html`.
To add a new one, add the service to `SERVICE_GROUPS` or `BLIND_TYPES` in `build.py`
and it appears in the form, on its page, and as a working link automatically.

There's also a **"Want just one thing?"** callout on the home, services and blinds
pages making clear you take single jobs with no minimum.

---

## 7. The logo

The logo in the header, footer and fallback panel is inline SVG (`LOGO_SVG` in
`build.py`) — a house outline with a teal door, three signal arcs and a teal dot,
matching your brand mark. Being inline SVG means it stays crisp at any size and
recolours itself: navy on light backgrounds, white on dark, no separate files.

If you'd rather use your original exported SVG, replace the `LOGO_SVG` string in
`build.py` and re-run the generator, or find-and-replace the `<svg>` block inside
`<a class="logo">` in each HTML file.

---

## 8. Editing content

You have two options.

**Edit the HTML directly.** Perfectly fine for small changes — fixing a typo,
swapping a price, changing a heading. The files are readable and well indented.

**Use the generator.** `build.py` holds the shared header, footer, icons, logo,
service list, FAQs and city list; `_pages.py` holds each page's content. Change
something there and run:

```bash
python3 build.py
```

which rewrites all seven HTML files. This is the better route for anything that
appears on multiple pages — the phone number, a new service, a nav item — because
it keeps every page in sync automatically.

**Note:** if you edit the HTML directly *and* later run `build.py`, your direct
edits are overwritten. Pick one approach and stick with it.

---

## 9. Before you launch — checklist

(The fuller version, with the domain and Google steps, is at the end of `DEPLOY.md`.)

- [ ] Run `fetch-brand-assets.sh` so the ad images are in place
- [ ] Turn on form email notifications in Netlify, send a test, then **delete the blue note in `contact.html`**
- [ ] Replace the three placeholder reviews on `index.html` with real ones, and
      **delete the blue note beneath them**
- [ ] Add at least one real before/after pair to the gallery
- [ ] Add your founder photo to `assets/img/photos/founder.jpg`
- [ ] Set your real domain (section 3)
- [ ] Submit `sitemap.xml` in [Google Search Console](https://search.google.com/search-console)
- [ ] Create a Google Business Profile for IQ Homes — for a local service business
      this drives more traffic than the website's own SEO will, at least at first

---

## 10. A note on the reviews

The three testimonial cards on the home page are **structure, not content** — the
text in them says so plainly. Don't launch with invented reviews; fabricated
testimonials are both against Google's policies and illegal to publish in Canada
under the Competition Act. Ask your first three customers for a sentence each and
swap them in. Reviews that name a specific thing that changed ("we stopped
worrying about whether the door was locked") convert far better than generic praise.

---

## Technical notes

- **Fonts** load from Google Fonts (Poppins + Lato). They'll appear once the site is
  on a real host with internet access.
- **Three.js** is self-hosted at `assets/js/vendor/three.module.js` (~1.3MB, ~350KB
  gzipped). It loads *only* on the home page, lazily, after the rest of the page —
  so the other six pages are very light. Make sure your host has gzip or brotli on.
- **Accessibility**: skip link, keyboard-operable 3D scene (arrow keys), proper
  ARIA on the accordion and mobile nav, visible focus rings, and a full
  `prefers-reduced-motion` path.
- **SEO**: unique titles and meta descriptions per page, Open Graph tags,
  `HomeAndConstructionBusiness` structured data on every page, `FAQPage` schema on
  the FAQ, canonical URLs, sitemap and robots.txt.
- **Browser support**: current Chrome, Safari, Firefox and Edge. The 3D scene needs
  WebGL; without it, visitors get a clean fallback instead.
