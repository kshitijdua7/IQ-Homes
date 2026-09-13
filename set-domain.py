#!/usr/bin/env python3
"""
Point the site at your real domain — run this once, after you've bought it.

    python3 set-domain.py iqhomesgta.ca

It updates the domain in build.py and rebuilds every page, so the canonical
URLs, social share tags, sitemap.xml, robots.txt and Google structured data
all match your real address. Nothing else about the site changes.

You can run it again any time you switch domains.
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)

    raw = sys.argv[1].strip()

    # Accept anything the user might paste: with or without scheme, www or slash
    raw = re.sub(r"^https?://", "", raw).strip("/")
    if not raw or " " in raw or "." not in raw:
        print(f"'{sys.argv[1]}' doesn't look like a domain. Try: python3 set-domain.py iqhomesgta.ca")
        sys.exit(1)

    host = raw if raw.startswith("www.") else "www." + raw
    site = "https://" + host

    build = os.path.join(HERE, "build.py")
    with open(build, encoding="utf-8") as f:
        src = f.read()

    new_src, n = re.subn(
        r'^SITE = "[^"]*"',
        f'SITE = "{site}"',
        src,
        count=1,
        flags=re.MULTILINE,
    )
    if not n:
        print("Couldn't find the SITE line in build.py — has it been edited?")
        sys.exit(1)

    with open(build, "w", encoding="utf-8") as f:
        f.write(new_src)

    print(f"Domain set to {site}")
    print("Rebuilding every page…\n")

    os.system(f'"{sys.executable}" "{build}"')

    print(f"""
Done. Every page now points at {site}.

Next:
  1. Upload the folder again (or drag it onto Netlify) so the live site picks it up.
  2. Submit https://{host}/sitemap.xml in Google Search Console.

Note: this uses the www version, which is the safer default — Netlify will
redirect the non-www address to it automatically once you set www as your
primary domain.
""")


if __name__ == "__main__":
    main()
