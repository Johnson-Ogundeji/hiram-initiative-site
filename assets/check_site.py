#!/usr/bin/env python3
"""
Checks the built site (website/) against the Builder to Business website update brief (6 Nov 2026).

    python3 assets/check_site.py

1. No hyphen or dash in visible copy: text, image alt text, page titles and share descriptions (THI house style,
   brief page 06). Addresses, links and code are not copy and are not checked.
2. The address is "454A High Road, Bruce Grove, Tottenham, London N17 9JD" (the operator, 12 Nov 2026, superseding the brief's "454 High Road"):
   it is on every page, and no bare "454 High Road" is left in the copy, alt text, metadata or event data.
3. Every link whose text says "Register" goes to the Luma registration page; no registration goes to Instagram.
4. Every internal link resolves to a page, and every image exists.
5. The main menu has Builder to Business and not Age of Agents (which now sits under Programmes).
6. The event page carries the brief's title, description and share image, and its event data parses.
7. The footer links to X; Joseph Falano is named Cofounder; the home page names the 18 to 35 audience.
8. The asset pack is in: every speaker has a headshot (no initials), the official flyer is on the event page and the
   home page, and the promo video's source and poster exist, with the video fetched only when played.
9. No page claims a registered office or address: THI has none yet (operator, 12 Nov 2026); 454A High Road is its
   workspace and seminar venue.
Prints SITE-CHECK-PASS or SITE-CHECK-FAIL and exits 0 or 1. Standard library only.
"""
import html.parser, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "website")
REGISTER = "https://luma.com/gitdjnje"
DASHES = re.compile("[-‐‑‒–—―−]")


class Page(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.copy, self.links, self.imgs, self.meta, self.ld = [], [], [], {}, []
        self.skip = 0; self.in_nav = False; self.nav = []; self.a = None; self.title = ""; self.in_title = False
        self.videos = []
        self.in_ld = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("style", "script"):
            self.skip += 1; self.in_ld = tag == "script" and a.get("type") == "application/ld+json"
        if tag == "title":
            self.in_title = True
        if tag == "nav":
            self.in_nav = True
        if tag == "a":
            self.a = [a.get("href", ""), ""]
        if tag == "img":
            self.imgs.append(a.get("src", "")); self.copy.append(("alt", a.get("alt", "")))
        if tag == "video":
            self.videos.append(a.get("preload", "")); self.imgs.append(a.get("poster", ""))
        if tag == "source":
            self.imgs.append(a.get("src", ""))
        if tag == "meta" and (a.get("name") or a.get("property")):
            self.meta[a.get("name") or a.get("property")] = a.get("content", "")
        if tag == "link" and a.get("rel") in ("icon", "apple-touch-icon"):
            self.imgs.append(a.get("href", ""))

    def handle_endtag(self, tag):
        if tag in ("style", "script"):
            self.skip -= 1; self.in_ld = False
        if tag == "title":
            self.in_title = False
        if tag == "nav":
            self.in_nav = False
        if tag == "a" and self.a is not None:
            self.links.append(tuple(self.a))
            if self.in_nav:
                self.nav.append(self.a[1].strip())
            self.a = None

    def handle_data(self, d):
        if self.in_ld:
            self.ld.append(d); return
        if self.skip:
            return
        if self.in_title:
            self.title += d
        self.copy.append(("text", d))
        if self.a is not None:
            self.a[1] += d


def main():
    bad = []
    pages = sorted(f for f in os.listdir(SITE) if f.endswith(".html"))
    parsed = {}
    for f in pages:
        raw = open(os.path.join(SITE, f), encoding="utf-8").read()
        p = Page(); p.feed(raw); parsed[f] = p
        if re.search(r"\b454 High ?road", raw, re.I):
            bad.append(f"{f}: a bare '454 High Road' is on the page (the address is 454A)")
        if "454A High Road, Bruce Grove, Tottenham, London N17 9JD" not in raw:
            bad.append(f"{f}: the full address with its postcode is not on the page")
        texts = [t for _, t in p.copy] + [p.title] + [p.meta.get(k, "") for k in ("description", "og:title", "og:description")]
        for t in texts:
            for m in DASHES.finditer(t):
                bad.append(f"{f}: a hyphen or dash in the copy: ...{t[max(0, m.start() - 30):m.end() + 30].strip()!r}")
        if re.search(r"registered (office|address)", " ".join(texts), re.I):
            bad.append(f"{f}: the copy claims a registered office or address (THI has none yet)")
        for href, text in p.links:
            if "register" in text.lower() and href != REGISTER:
                bad.append(f"{f}: a Register link goes to {href}, not {REGISTER}")
            if "instagram.com" in href and re.search(r"register|rsvp|sign up", text, re.I):
                bad.append(f"{f}: a registration link goes to Instagram")
            if href.startswith(("http", "mailto:", "tel:", "#")):
                continue
            target = href.split("#")[0].lstrip("/")
            if target == "":
                target = "index"
            if not (os.path.isfile(os.path.join(SITE, target)) or os.path.isfile(os.path.join(SITE, target + ".html"))):
                bad.append(f"{f}: an internal link to {href} has no page")
        for src in p.imgs:
            if not src.startswith("http") and not os.path.isfile(os.path.join(SITE, src)):
                bad.append(f"{f}: the image {src} does not exist")
        if "Builder to Business" not in p.nav:
            bad.append(f"{f}: the main menu lacks Builder to Business")
        if "Age of Agents" in p.nav:
            bad.append(f"{f}: Age of Agents is still in the main menu")
        if "x.com/thehiramINT" not in raw:
            bad.append(f"{f}: the footer has no X link")
    e = parsed.get("builder-to-business.html")
    if e is None:
        bad.append("the event page builder-to-business.html does not exist")
    else:
        if e.title != "Builder to Business: The Final Piece · The Hiram Initiative":
            bad.append(f"the event page's title is {e.title!r}")
        if e.meta.get("description") != ("A free two day accelerator in London, 20 & 21 November 2026, turning young builders "
                                         "into business owners. Register now."):
            bad.append(f"the event page's description is {e.meta.get('description')!r}")
        img = e.meta.get("og:image", "")
        if not img.endswith("/assets/b2b-share.jpg") or not os.path.isfile(os.path.join(SITE, "assets", "b2b-share.jpg")):
            bad.append(f"the event page's share image is {img!r}")
        try:
            ld = json.loads("".join(e.ld))
            if ld.get("@type") != "Event" or ld.get("startDate", "")[:10] != "2026-11-20":
                bad.append("the event data is not the event")
        except ValueError:
            bad.append("the event data does not parse")
        if sum(1 for h, t in e.links if h == REGISTER) < 3:
            bad.append("the event page has fewer than three Register links")
    for f in ("index.html", "builder-to-business.html"):
        p = parsed.get(f)
        if p is None:
            continue
        if "assets/b2b-flyer.jpg" not in p.imgs:
            bad.append(f"{f}: the official flyer is not on the page")
        if not p.videos:
            bad.append(f"{f}: the promo video is not on the page")
        elif any(v != "none" for v in p.videos):
            bad.append(f"{f}: a video is fetched before it is played (preload is not none)")
    if e is not None and 'class="initials"' in open(os.path.join(SITE, "builder-to-business.html"), encoding="utf-8").read():
        bad.append("builder-to-business.html: a speaker has initials, not a headshot")
    about = open(os.path.join(SITE, "about.html"), encoding="utf-8").read()
    if not re.search(r"cofounder", about, re.I) or "Joseph Falano" not in about:   # the card shows roles in capitals
        bad.append("the about page does not name Joseph Falano as Cofounder")
    if "18 to 35" not in open(os.path.join(SITE, "index.html"), encoding="utf-8").read():
        bad.append("the home page does not name the 18 to 35 audience")
    for b in bad:
        print("  FAIL " + b)
    print(f"{len(pages)} pages checked")
    print("SITE-CHECK-PASS" if not bad else f"SITE-CHECK-FAIL ({len(bad)})")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
