# The Hiram Initiative — Website

The public website for **The Hiram Initiative** (THI), a UK community
organisation equipping young people with the skills, mindset and networks
to thrive in the modern technological economy.

> *Wisdom · Purpose · Impact*

Live at **<https://hiraminitiative.com>** (deployed from this repository
via GitHub Pages).

## What's in this repo

| Path | What it is |
|---|---|
| `assets/build_site.py` | Single-file Python generator. No dependencies. Reads the content baked into the script (sourced directly from the constitution, AGM minutes and Frontier Fusion poster) and writes static HTML to `website/`. |
| `website/` | The built site. This is what GitHub Pages serves. Regenerate any time with `python3 assets/build_site.py`. |
| `website/CNAME` | Custom-domain pointer for GitHub Pages. |
| `.github/workflows/deploy.yml` | Builds the site on every push to `main` and deploys `website/` to GitHub Pages. |

## Source documents

The site's content is drawn faithfully from three documents:

- **THI Constitution** — adopted 13 May 2026, signed by the Chairperson and Secretary.
- **AGM (Initiation Meeting) Minutes** — 13 April 2026, signed by Chair, Secretary and Treasurer.
- **Frontier Fusion 2026 poster** — flagship event, 15 May 2026, Encode Hub London.

The signed originals are held by the committee and are available on
request to <admin@hiraminitiative.com>.

## Pages

```
/                       Home — mission, five pillars, Frontier Fusion, the Hiram story
/about                  Identity, mission, vision, the name "Hiram", current committee
/programmes             The five pillars + 2026 roadmap + cross-cutting work
/pillar-it              Information Technology & Digital Skills
/pillar-ai              Artificial Intelligence
/pillar-blockchain      Blockchain Technology
/pillar-content         Content Creation
/pillar-entrepreneurship  Entrepreneurship & Business
/frontier-fusion        Frontier Fusion 2026 — AI & On-Chain Innovation
/governance             Committee, financial governance, the constitution
/constitution           Constitution summary, contents and adoption
/partners               Partnership principles, benefits, confirmed partners
/contact                Three ways in: join, mentor, partner
```

## Build locally

```bash
git clone https://github.com/<your-org>/hiram-initiative-site.git
cd hiram-initiative-site
python3 assets/build_site.py
# Output: website/*.html
# Serve locally:
python3 -m http.server -d website 8000
# open http://localhost:8000
```

The script has no third-party dependencies — just CPython 3.8+.

## Editing content

All copy lives at the top of `assets/build_site.py` in clearly-named
constants: `ORG`, `COMMITTEE`, `VOLUNTEERS`, `PILLARS`, `CROSS_CUTTING`,
`ROADMAP`, `PROGRAMMES`, `PARTNERS_BENEFITS`, `PARTNERS_CONFIRMED`,
`FRONTIER`, `GOVERNANCE`. Edit, run, commit, push — the deploy workflow
takes it from there.

Brand colours (orange `#E67A2C`, ink `#1A1A1A`, teal-blue `#2589B5`,
Frontier Fusion electric blue `#2C5BFF`) sit just below the content
constants and can be tuned in one place.

## Deploy

Every push to `main` triggers `.github/workflows/deploy.yml`:

1. Checkout
2. Run `python3 assets/build_site.py`
3. Upload `website/` as a Pages artifact
4. Deploy to GitHub Pages

First-time setup (one-off, in repo Settings → Pages):
- Source: **GitHub Actions**
- Custom domain: `hiraminitiative.com` (CNAME file is already in `website/`)
- Enforce HTTPS: on

## Contact

- Email: <admin@hiraminitiative.com>
- Phone: +44 7424 271744
- Instagram: [@thi_20_25](https://instagram.com/thi_20_25)
- Registered office: 454A High Road, Tottenham, London, N17 9JD

## Licence

Source code (the build script and any scaffolding): MIT — see [`LICENSE`](LICENSE).

The Hiram Initiative name, logo, brand assets, and the prose content
authored by THI (the constitution, AGM minutes, and the website copy
derived from them) remain the property of The Hiram Initiative. Reuse
requires permission — email the address above.
