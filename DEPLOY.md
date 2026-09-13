# Getting IQ Homes online

Start to finish this is about an hour of your time, and roughly **$20 a year**.
Everything except the domain is free.

**You do not need a backend.** No server, no database, no monthly hosting bill.
Your site is plain files. The only thing that needs handling is the consultation
form, and Netlify does that for you at no cost.

Do these five steps in order.

---

## Step 1 — Buy a domain (~15 min, ~$20/yr)

### First, the bad news

I checked: **`iqhomes.ca` and `iqhomes.com` are both already registered by
someone else.** (`iqhomes.com` is the site your Bloom brand accidentally
scraped — that's why the brand record had the wrong logo and colours.)

So you need a variant. These read well for a GTA home services business:

| Domain | Why it works |
|---|---|
| `iqhomesgta.ca` | Says exactly who you are and where. Strong for local search. |
| `iqsmarthomes.ca` | Explains the business in the name itself. |
| `iqhomeautomation.ca` | Longest, but unmistakable and great for SEO. |
| `goiqhomes.ca` | Short, brandable, easy to say on the phone. |
| `iqhomes.io` | Clean and short, but `.io` reads tech-startup, not local trade. |

**I could only check DNS from here, not the registry** — a domain with no DNS
record can still be registered and parked. Treat the list above as candidates,
not confirmed availability. The registrar will tell you for certain in one search.

### Buying it

Use **[Namecheap](https://www.namecheap.com)** or **[Cloudflare Registrar](https://domains.cloudflare.com)**.
Both are honest on price. Avoid GoDaddy — the first year is cheap and the renewal
is not.

- A `.ca` costs roughly **$15–20 CAD/year** and requires you to be a Canadian
  citizen, permanent resident, or a Canadian-registered business. You qualify.
- **Turn on WHOIS privacy** if offered (usually free). Otherwise your home
  address ends up in a public database that spammers scrape.
- **Skip every upsell.** You don't need their hosting, their email, their SSL,
  or their "site builder". Netlify gives you hosting and SSL free.

### Prefer `.ca` over `.com`

For a business serving only the GTA, a `.ca` signals local, which is exactly what
you want a homeowner in Whitby to feel. It also has far better availability.

---

## Step 2 — Get the site online (~10 min, free)

You don't need an account for the first deploy. This gets you a live URL in about
two minutes.

1. Unzip the site folder somewhere you can find it.
2. Run `bash fetch-brand-assets.sh` inside it first, so your ad images are included.
3. Go to **[app.netlify.com/drop](https://app.netlify.com/drop)**.
4. **Drag the whole `iqhomes` folder** onto that page. Not the zip — the folder,
   and make sure `index.html` is directly inside it, not nested another level down.
5. Wait about 30 seconds. You'll get a URL like `random-name-123456.netlify.app`.

**Open it on your phone right now.** Check the 3D house loads, the menu opens, and
the pages work. This is your site, live on the internet.

6. Create a free account when it prompts you (sign up with the Google account for
   `iqhomes4everyone@gmail.com` — one less password). This claims the site so it
   doesn't expire.
7. In **Site configuration → Change site name**, rename it to something like
   `iqhomes` so the temporary URL is `iqhomes.netlify.app`.

> **Deploying updates later:** in your Netlify dashboard go to **Deploys** and drag
> the folder onto the drop zone at the bottom. It replaces the live site in seconds.
> The old version stays available to roll back to if you break something.

---

## Step 3 — Connect your domain (~10 min + waiting)

1. In Netlify: **Domain management → Add a domain** → type your domain → **Verify**.
2. Netlify shows you **nameservers** — four addresses like `dns1.p05.nsone.net`.
3. Log into your registrar, find **Nameservers** (Namecheap: Domain tab →
   Nameservers → Custom DNS), and replace what's there with Netlify's four.
4. Save, then wait. Usually 15 minutes to 2 hours; occasionally up to 24.
5. Back in Netlify, set **www** as the primary domain. It'll redirect the bare
   domain to it automatically.
6. SSL turns itself on once DNS resolves — you'll see "Your site has HTTPS enabled".
   Don't skip verifying this. A browser warning on a home services site kills trust
   instantly.

### Then tell the site its own address

Once the domain works, run this in the site folder:

```bash
python3 set-domain.py yourdomain.ca
```

It rewrites the canonical URLs, social share tags, sitemap and Google structured
data to match, then rebuilds every page. **Redeploy afterwards** (drag the folder
onto Netlify again) so the live site picks it up.

---

## Step 4 — Turn the form on (~5 min, free)

The form is already wired. Netlify detects it automatically on deploy — you just
need to tell it where to send submissions.

1. In your Netlify dashboard, go to **Forms**. You should see a form called
   **consultation** listed.
2. Click it → **Settings and usage** → **Form notifications** → **Add notification**
   → **Email notification**.
3. Enter `iqhomes4everyone@gmail.com`. Save.

**Now test it.** Go to your live site, fill in the consultation form with your own
details, and submit. You should land on the thank-you page and get an email within
a minute. Check spam if it doesn't appear.

Once that works:

- Delete the blue "Note for Kshitij" box in `contact.html` and redeploy.
- Submissions are also stored in the Netlify dashboard forever, so nothing is lost
  if an email goes astray.

### If the form doesn't appear in Netlify

Almost always one of two things:

- You dragged the **zip** instead of the folder. Netlify can't read inside a zip.
- `index.html` was nested one folder too deep. Netlify needs it at the top level.

Redeploy correctly and the form appears.

### Spam

There's a hidden honeypot field that catches most bots. If real spam gets through,
Netlify → Forms → Settings → enable **reCAPTCHA**. Only do this if you actually get
spam — every extra step costs you real enquiries.

**Free tier: 100 submissions/month.** That is a lot of consultation requests. If
you ever exceed it, that's a very good problem.

---

## Step 5 — Tell Google you exist (~20 min, free)

This is the step people skip, and it's the one that actually brings customers.

### Google Business Profile — do this first

**[business.google.com](https://business.google.com)**

For a local trade business this matters **more than your website's own SEO**. It's
what puts you in the map results when someone searches "smart home installer near me".

- Choose a **service-area business** (you go to customers) — you don't need a
  storefront address, and you can hide your home address.
- Set your service area to the GTA regions you cover.
- Add your phone, your website URL, and your hours.
- **Add photos.** Profiles with photos get dramatically more calls. Use your ad
  creatives now and real install photos as you get them.
- Verification is usually by postcard or video call and takes a few days. Start it
  early.

### Google Search Console

**[search.google.com/search-console](https://search.google.com/search-console)**

1. Add your domain as a property.
2. Verify (easiest via the DNS TXT record Netlify lets you add under
   Domain management → DNS records).
3. Go to **Sitemaps** and submit: `sitemap.xml`

Google will start indexing within a few days. Search Console also tells you what
people searched to find you, which is genuinely useful for deciding what to write
about next.

### Then, ask for reviews

Your first three customers are the most valuable marketing you will ever get. Ask
each one for a Google review and one sentence you can put on the site. Replace the
placeholder testimonials on the home page with those — and delete the blue note
beneath them.

---

## What it costs

| | Cost |
|---|---|
| Domain | ~$20 CAD/year |
| Netlify hosting | Free (100GB/month bandwidth — far beyond what you'll use) |
| SSL certificate | Free, automatic |
| Form handling | Free (100 submissions/month) |
| Google Business Profile | Free |
| **Total** | **~$20/year** |

You'd only ever pay Netlify if the site got genuinely popular, and by then it's
paying for itself.

---

## Launch checklist

Work down this list. Don't run ads until it's all ticked.

- [ ] `bash fetch-brand-assets.sh` run, ad images visible on the site
- [ ] Domain bought and connected, **HTTPS confirmed working**
- [ ] `python3 set-domain.py yourdomain.ca` run, and redeployed
- [ ] Form tested end-to-end — you received the email
- [ ] Blue "Note for Kshitij" deleted from `contact.html`
- [ ] Placeholder reviews replaced with real ones, blue note deleted from `index.html`
- [ ] Founder photo added at `assets/img/photos/founder.jpg`
- [ ] At least one real before/after pair in the gallery
- [ ] Every page opened on your phone
- [ ] Google Business Profile created and verification started
- [ ] `sitemap.xml` submitted in Search Console

---

## Troubleshooting

**The 3D house doesn't load.**
It needs to be served over http/https, not opened as a file. If it fails on the
live site, check the browser console (right-click → Inspect → Console). A very old
browser without WebGL gets the fallback panel by design.

**My changes aren't showing.**
Browsers cache. Hard-refresh with Ctrl+Shift+R (Cmd+Shift+R on Mac). HTML is set
to never cache hard, so one refresh should do it.

**The site works but the fonts look wrong.**
Poppins and Lato load from Google Fonts. If they don't appear, something is
blocking that request — check on another network before assuming it's the site.

**I deployed and now something is broken.**
Netlify → **Deploys** → find the previous working deploy → **Publish deploy**.
You're rolled back in seconds. Then fix it and redeploy.

**I want to change wording.**
Edit the `.html` files directly, or edit `build.py`/`_pages.py` and run
`python3 build.py`. Pick one approach — running the build overwrites direct edits.
See `README.md` section 8.
