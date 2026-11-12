#!/usr/bin/env python3
"""
The Hiram Initiative, static site generator.

Renders the website/ directory from content sourced directly from
the constitution (adopted 13 May 2026), the AGM minutes (13 April 2026),
the Frontier Fusion event poster, the Builder to Business website update
brief (6 November 2026) and THI's funding pitch (October 2026). Run:

    python3 assets/build_site.py

Output: HTML pages in ../website/ (or website/ relative to CWD).
"""
import os, re, datetime

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
HERE  = os.path.dirname(os.path.abspath(__file__))
ROOT  = os.path.dirname(HERE)
SITE  = os.path.join(ROOT, "website")
os.makedirs(SITE, exist_ok=True)

# ---------------------------------------------------------------------------
# Brand
# ---------------------------------------------------------------------------
ORG = {
    "name":      "The Hiram Initiative",
    "short":     "THI",
    "tagline":   "Wisdom · Purpose · Impact",
    "thesis":    "Hiram did not build the Temple. He equipped the people who did. That is what The Hiram Initiative is doing for this generation.",
    # THI has no registered office yet: this is its workspace and seminar venue. 454A with the postcode, as the
    # operator set it on 12 Nov 2026 (the brief's "454 High Road" is superseded).
    "address":   "454A High Road, Bruce Grove, Tottenham, London N17 9JD",
    "email":     "admin@hiraminitiative.com",
    "phone":     "+44 7424 271744",
    "instagram": "@thehiraminitiative",
    "instagram_url": "https://www.instagram.com/thehiraminitiative?igsh=MWl6dDJkOGo1MjF1NA==",
    "x":         "@thehiramINT",
    "x_url":     "https://x.com/thehiramINT",
    "register_url": "https://luma.com/gitdjnje",   # Builder to Business registration (brief, 6 Nov 2026)
    "audience":  "young people aged 18 to 35",
    "base_url":  "https://hiraminitiative.com",     # the CNAME host, for absolute share image links
    "website":   "www.hiraminitiative.com",
    "adopted":   "13 May 2026",
    "agm":       "13 April 2026",
    "year":      datetime.date.today().year,
}

# Colour palette, sampled from the constitution and Frontier Fusion poster.
INK         = "#1A1A1A"   # near-black headers
ACCENT      = "#E67A2C"   # primary orange (constitution header rules)
ACCENT_DARK = "#B8581A"   # deeper orange for hover / pressed
ACCENT_LITE = "#FBE4D2"   # tinted wash
TEAL        = "#2589B5"   # section eyebrow blue (constitution "Part X" headings)
FF_BLUE     = "#2C5BFF"   # Frontier Fusion electric blue
FF_YELLOW   = "#FFD23F"   # poster location chip
PAPER       = "#FFFFFF"
MUTED       = "#5A5A5A"

# ---------------------------------------------------------------------------
# Content, sourced directly from constitution / AGM / poster
# ---------------------------------------------------------------------------
COMMITTEE = [
    ("Johnson Ogúndèjì", "Chairperson", "Overall leadership and strategic direction; 2026 roadmap; partnerships strategy."),
    ("Joseph Falano (Ohjay)", "Cofounder and Secretary", "Administration, records, communications; Expert Speaker Series; Mentorship Matching programme."),
    ("Daniel Dickson",   "Treasurer",   "Financial management and reporting, in accordance with Section 4.2 of the constitution."),
]
VOLUNTEERS = [
    ("Victor Emovon",   "Mentorship matching, operating the One to One Mentorship Matching programme that pairs members with industry practitioners"),
    ("David Tetede",    "Career pathways · technology sector accountability"),
    ("Bankole Olamide", "Awareness and representation for excluded communities"),
]

PILLARS = [
    {
        "slug": "pillar-it",
        "name": "Information Technology &amp; Digital Skills",
        "short": "IT &amp; Digital",
        "icon": "circuit",
        "tagline": "The foundational digital skills every modern workplace expects.",
        "points": [
            ("Accessible IT training",         "Foundational digital skills required in every modern workplace and business."),
            ("Inclusive curriculum",            "Introductions into AI concepts, digital literacy and practical technology skills, designed for those most at risk from technological change, including underrepresented and minority communities."),
            ("Practical workshops",             "Educational exhibits, seminars and labs that show different aspects of IT across employment, with practical materials participants can apply immediately."),
            ("Targeted, measurable delivery",   "Clear objectives, plain language formats, highlighting how society is being impacted by IT and how young people can position themselves to benefit."),
        ],
    },
    {
        "slug": "pillar-ai",
        "name": "Artificial Intelligence",
        "short": "AI",
        "icon": "spark",
        "tagline": "Practical AI for real careers, real income, real impact.",
        "points": [
            ("Practical AI education",     "Real world applications, ethical considerations, prompt engineering, AI tools and the emerging career and income opportunities AI is creating."),
            ("Applicable AI skills",        "Using AI for content creation, freelance services, business automation and productivity, skills that translate directly into work."),
            ("Updates at the speed of the field", "Continuously refreshed curriculum and programming so members keep pace with the latest developments."),
            ("Address the skills gap",      "Preparing young people for the AI driven economy the UK government is investing billions into building."),
        ],
    },
    {
        "slug": "pillar-blockchain",
        "name": "Blockchain Technology",
        "short": "Blockchain &amp; Web3",
        "icon": "chain",
        "tagline": "From fundamentals to a financially inclusive decentralised web.",
        "points": [
            ("Blockchain fundamentals",   "Decentralised systems, smart contracts, Web3 applications, and how blockchain is reshaping finance, supply chains, healthcare and governance."),
            ("Practical exposure",         "Blockchain development, cryptocurrency, DeFi, NFTs and the growing infrastructure of the decentralised web."),
            ("Connection to community",    "Partnerships with Web3 organisations, developers and industry practitioners operating at the frontier of this technology."),
            ("Financial inclusion",        "How blockchain can reduce remittance costs, expand access to financial services, and create new economic opportunities for communities historically excluded from traditional finance."),
        ],
    },
    {
        "slug": "pillar-content",
        "name": "Content Creation",
        "short": "Content",
        "icon": "lens",
        "tagline": "Storytelling, personal brand, and creator economics, done with technology.",
        "points": [
            ("Skilled creators",            "Use digital tools, AI and modern platforms to build audiences, communicate ideas and create income."),
            ("Content strategy &amp; brand",    "Storytelling and personal branding as core professional skills that translate across every industry and career path."),
            ("Tech × creativity",           "Combine AI tools, blockchain and digital platforms to build sustainable creative careers and businesses."),
            ("Production craft",            "Video, written content, social media strategy and audience building, taught by practitioners with real world experience."),
        ],
    },
    {
        "slug": "pillar-entrepreneurship",
        "name": "Entrepreneurship &amp; Business",
        "short": "Entrepreneurship",
        "icon": "rocket",
        "tagline": "Identify problems, build solutions, create value in the world.",
        "points": [
            ("Entrepreneurial thinking",      "Teach members to identify problems, build solutions and create value."),
            ("Practical business education",   "Venture building, market understanding, financial literacy, income generation, and the skills required to start and grow a business."),
            ("Barriers the UK faces",          "Address the specific barriers facing young entrepreneurs, access to funding, tools, technology and marketing support."),
            ("Modern entrepreneurship",        "Side hustles, digital businesses, freelancing and building income through the internet, accessible regardless of background or starting point."),
            ("Mentors, investors, collaborators", "Connect members with the networks and support that accelerate real business growth."),
        ],
    },
]

CROSS_CUTTING = [
    {
        "name": "Life Intelligence &amp; Modern Thinking",
        "items": [
            ("Critical thinking, EQ, adaptability", "Foundational skills for navigating a complex and rapidly changing world."),
            ("Decision making frameworks",          "First principles thinking, inversion, second order thinking, tools that apply across business, relationships and personal development."),
            ("Personal development",                "Goal setting, leadership skills, self mastery and the mindset required to create meaningful impact."),
        ],
    },
    {
        "name": "Community &amp; Access",
        "items": [
            ("Unite communities across London",     "Improve futures through IT, AI and entrepreneurship, annual events, seminars, talks and workshops."),
            ("Representation for excluded communities", "Raise the visibility of THI members and improve quality of life through technology and education."),
            ("Inclusive delivery",                  "Ensure access for those most at risk from technological change, minority communities, young people not in education or employment, and those facing socioeconomic barriers."),
        ],
    },
]

ROADMAP = [
    ("Q1 2026", "Launch four foundational workshops on blockchain and AI fundamentals. Onboard the first cohort of members and establish the mentorship matching programme."),
    ("Q2 2026", "Host six masterclasses with industry experts across the five pillars. Launch the online resource platform and expand community reach."),
    ("Q3 2026", "Deliver eight specialised seminars on advanced topics across IT, AI, blockchain, content creation and entrepreneurship. Facilitate the first major networking summit connecting members with the broader technology and Web3 community."),
    ("Q4 2026", "Deliver Builder to Business, The Final Piece, the two day finale of the B2B series, on 20 &amp; 21 November. Complete the full year's programming cycle and showcase member projects and success stories. Plan the 2027 expansion based on outcomes, member feedback and community growth."),
]

PROGRAMMES = [
    ("The B2B Series",
     "Our journey from beginner to business owner. Beginner to Builder taught AI fundamentals and agent building. Beginner to Business brought founders into the room. Builder to Business completes the journey."),
    ("Workshops &amp; Masterclasses",
     "In depth sessions on specific topics in IT, AI, blockchain, content creation, entrepreneurship and life intelligence, led by industry practitioners. Practical and directly applicable to real situations."),
    ("Expert Speaker Series",
     "Regular talks and Q&amp;A with founders, innovators, developers and thought leaders sharing their journeys, insights and real world experience at the frontier of their fields."),
    ("One to One Mentorship Matching",
     "Personalised pairing of members with experienced professionals for ongoing guidance, accountability and support, the kind that changes the direction of careers and businesses."),
    ("Networking &amp; Community Events",
     "Curated gatherings that connect members with peers, mentors and collaborators in their fields of interest, including the annual Frontier Fusion event."),
    ("Online Resources &amp; Learning Platform",
     "Accessible educational content, recorded sessions, curated materials and a digital resource library available to all members."),
]

PARTNERS_BENEFITS = [
    ("Brand recognition",       "Logo placement and acknowledgement across events, platforms and materials."),
    ("Community access",        "Connection to a network of motivated, technology literate young professionals."),
    ("Impact reporting",        "Regular updates on how investment is creating real, measurable change."),
    ("Speaking opportunities",  "Share the organisation's story and values with the THI community."),
    ("Talent pipeline",         "Early access to emerging talent from the THI member base."),
    ("Social media recognition","Features and appreciation across THI's digital channels."),
    ("Exclusive event invitations", "Flagship programmes and networking events, including Frontier Fusion."),
]

# Partners and collaborators (Builder to Business brief, 6 Nov 2026, p.07; logos from THI's pitch, Oct 2026).
# EdenFi joins this list only once the partnership is signed and announced (the brief); the heading then becomes
# "Our partners".
PARTNERS_CONFIRMED = [
    ("OnChainBrits",  "Frontier Fusion co host.",                    "assets/partner-onchainbrits.png"),
    ("Superteam UK",  "Frontier Fusion co host.",                    "assets/partner-superteam-uk.png"),
    ("Encode Club",   "Venue and community collaborator.",          "assets/partner-encode-club.png"),
    ("Gosen Inc.",    "Supporter.",                                 "assets/partner-gosen.png"),
]

FRONTIER = {
    "title":   "Frontier Fusion",
    "subtitle":"AI &amp; On Chain Innovation",
    "date":    "Friday, 15 May 2026",
    "venue":   "Encode Hub, 41 Pitfield St, London N1 6DA",
    "blurb":   "THI's flagship annual gathering, bringing together AI, on chain and creator communities for a night of talks, demos and connections at the frontier of where technology is going next. Hosted in partnership with On Chain Brits and Superteam UK.",
    "rsvp":    "instagram",  # poster's QR points to Instagram
}

# Age of Agents (9 to 11 July 2026): completed; its page now points to Builder to Business (brief p.04).
AOA = {
    "title":    "Age of Agents",
    "subtitle": "An introduction into the creation of AI Agents.",
    "date":     "9th to 11th July 2026, 2pm to 6pm",
    "venue":    "454A High Road, Bruce Grove, Tottenham, London N17 9JD",
    "led_by":   "Joseph Falano (Ohjay), with Jalaaldeen Akinola (JRD)",
    "blurb":    "THI's practical introduction to building AI agents: software that decides and acts on your behalf. Three afternoons that take you from what an agent is to creating your own, so you meet the shift as a builder, not a spectator.",
}

# Builder to Business: The Final Piece. Copy from the Builder to Business website update brief (6 Nov 2026) and its
# asset pack (THI_B2B_Website_Assets.zip): the flyer, the five headshots and speaker cards, the guest's invite, the
# Beginner to Business poster, the share image and the promo video (converted to 540 x 960 H.264 for the web).
B2B = {
    "title":    "Builder to Business: The Final Piece",
    "chip":     "20 &amp; 21 November 2026 · From 10am · Tottenham",
    "tagline":  "You have built the foundation. Now it is time to scale.",
    "when":     "Friday 20th &amp; Saturday 21st November 2026, from 10am",
    "where":    "454A High Road, Bruce Grove, Tottenham, London N17 9JD",
    "entry":    "Free. Registration required.",
    "short":    "Two days that take driven young builders from ideas to fully operational businesses. Expert panels, practical workshops and intensive training in startup architecture, funding, content and the skills that turn work into income.",
    "about": [
        "Builder to Business is the final chapter of The Hiram Initiative's B2B series, following Beginner to Builder, our virtual AI programme, and Beginner to Business, our in person workshop.",
        "Across two days, we bring together founders, funders, industry experts and strategists to turn driven young builders into fully operational business owners. This is not a seminar. It is a practical accelerator of expert sessions, workshops and intensive training focused on real growth and strategic positioning.",
    ],
    "learn": [
        ("Startup Architecture",     "Structure and operationalise your startup to last.", "ledger"),
        ("Funding and Sponsorships", "Position yourself to source, pitch and secure funding and partnerships.", "globe"),
        ("Content as Currency",      "Use content and digital storytelling to market your product, build authority and attract loyal clients.", "lens"),
        ("Live Workshops",           "Hands on sessions in business model generation and video editing.", "hands"),
        ("Product Showcases",        "See real products built by real builders, and meet the founders behind them.", "rocket"),
    ],
    "for":      "Young people aged 18 to 35, builders, creators and early stage founders ready to turn skills and ideas into a working business. Whether you are scaling a service, launching a product or positioning your brand for investment, this is your toolkit, your network and your roadmap. Completed Beginner to Builder? This is your next step.",
    "speakers": [
        ("Mark Physsas", "Startup Architecture and Funding", "Positioning Your Startup for Investment in a Digital Economy",
         "Web3 strategist and advisor, former architecture studio founder and cofounder of OnChainBrits.", "assets/speaker-mark-physsas.jpg"),
        ("Jay Chen", "Funding and Sponsorships", "Funding Opportunities: Finding and Securing the Right Capital",
         "Leads Christians in Web3 UK and is building Ecclesia Ventures, helping faith driven founders build ventures for Kingdom impact.", "assets/speaker-jay-chen.jpg"),
        ("Maryann Enereba", "Content as Currency", "Content as Currency: Digital Storytelling That Builds Brands",
         "Digital storyteller, professional photographer and founder of Telling Reel Stories. CNN Academy trained fellow.", "assets/speaker-maryann-enereba.jpg"),
        ("Sodiq Davies", "Startup Architecture", "Shipping Faster with AI: Delivery Habits That Turn Ideas into Products",
         "Delivery leader with 9+ years in technology delivery, leading a portfolio of around £3M at Jaguar Land Rover, with a focus on AI augmented delivery.", "assets/speaker-sodiq-davies.jpg"),
        ("Nathan Vandy", "Startup Architecture and Funding", "Building a Company Investors Trust: Lessons on Structure, Funding and Partnerships",
         "Cofounder and CEO of bond.credit. Previously led the DAO at DappRadar and was Managing Director of the TrueFi Foundation.", "assets/speaker-nathan-vandy.jpg"),
    ],
    "days": [
        ("Day 1 · Friday 20 November", "Startup Architecture",
         ["THI: who we are and what we do", "Sodiq Davies", "Mark Physsas", "Workshop: Business Model Generation", "Product showcase", "Games and networking"]),
        ("Day 2 · Saturday 21 November", "Funding and Content",
         ["Jay Chen", "Nathan Vandy", "Maryann Enereba", "Workshop: Video Editing", "Product showcase", "Speaker Q&amp;A panel"]),
    ],
    "showcases": [("EdenFi", "Ezra Akran"), ("Gosen Inc.", "Daniel Dickson"), ("Frontier Tech Jobs", "Mark Physsas"),
                  ("Church Force", "Pastor Dami Sayinbola"), ("Signetify", "Pastor Johnson")],
    "guest":    ("Pastor Mary McCauley", "Senior Pastor of RCCG True Vine Centre, Croydon, and founder of the Alive and Happening youth camp."),
    "faq": [
        ("Is it free?", "Yes. Entry is free, but registration is required."),
        ("Do I need to attend both days?", "We recommend it. Each day covers different focus areas, and together they form the full experience."),
        ("Do I need experience?", "No. If you are building something, or ready to start, you will find practical value here."),
        ("What should I bring?", "A laptop or smartphone for the practical workshops, and ideas you want to build on."),
        ("I missed the earlier B2B sessions. Can I still come?", "Yes. Builder to Business stands on its own, and everyone is welcome."),
    ],
    # The series so far (THI's pitch, Oct 2026, "From beginner to business owner")
    "series": [
        ("01 · Virtual · October", "Beginner to Builder", "AI fundamentals and building AI agents, every Saturday."),
        ("02 · In person · 24 October", "Beginner to Business", "Workshop with Johnson Ogúndèjì and Daniel Dickson."),
        ("03 · Finale · 20 to 21 November", "Builder to Business", "A free two day accelerator for around 120 builders."),
    ],
    "page_title": "Builder to Business: The Final Piece · The Hiram Initiative",
    "page_desc":  "A free two day accelerator in London, 20 &amp; 21 November 2026, turning young builders into business owners. Register now.",
    "share":      "assets/b2b-share.jpg",
    "flyer":      "assets/b2b-flyer.jpg",
    "flyer_alt":  "The official Builder to Business flyer: The Final Piece, 20 and 21 November 2026, from 10am, Tottenham",   # the artwork's own address line is not repeated
    "video":      "assets/b2b-promo.mp4",
    "poster":     "assets/b2b-promo-poster.jpg",
    "caption":    "Every business starts out as an idea. Join us for Builder to Business: The Final Piece.",
    "guest_img":  "assets/b2b-guest-mary-mccauley.jpg",
    "series_img": "assets/b2b-beginner-to-business.jpg",
    "cards": ["mark-physsas", "jay-chen", "maryann-enereba", "sodiq-davies", "nathan-vandy"],
}

def promo_video():
    """The 34 second promo (vertical, captions burned in). Fetched only when played."""
    return (f'<video controls playsinline preload="none" poster="{B2B["poster"]}" '
            f'style="width:100%;max-width:360px;aspect-ratio:9/16;border-radius:16px;background:#F6F0E8;display:block;margin:0 auto">'
            f'<source src="{B2B["video"]}" type="video/mp4">Your browser cannot play this video.</video>')

def flyer(max_w=440):
    return (f'<img src="{B2B["flyer"]}" alt="{B2B["flyer_alt"]}" style="width:100%;max-width:{max_w}px;border-radius:16px;'
            f'box-shadow:0 14px 46px rgba(0,0,0,.35);display:block;margin:0 auto">')

# Community in numbers (brief p.06, site wide details)
STATS = [
    ("~250", "active members in our WhatsApp community"),
    ("150+", "attendees across the three days of Age of Agents"),
    ("8",    "working products built in 14 days in the Build With AI Challenge"),
    ("18 to 35", "the ages of the young people we serve"),
]

# Financial governance principles (Constitution Part Six + AGM §6)
GOVERNANCE = [
    ("Two signatory rule",
     "All payments and bank instructions must be signed by at least two authorised committee members. The Community Current Account at Metro Bank operates with three named signatories (Chairperson, Secretary, Treasurer) and a strict any two of three signing rule for every withdrawal, transfer, cheque, standing order, direct debit and electronic payment."),
    ("No personal benefit",
     "No committee member receives any payment or financial benefit from the organisation, other than reasonable out of pocket expenses incurred in the course of their duties."),
    ("Accurate records",
     "The Treasurer, with the Secretary, keeps accurate financial records covering income, expenditure and assets."),
    ("Funds used to further the aims",
     "Every pound raised by THI is used directly to further the aims, educational resources and technology, venue and events, expert speakers and mentors, and outreach to grow the community we exist to serve."),
    ("Insurance",
     "The committee may take out appropriate insurance to protect the organisation and its members."),
    ("Amendments and dissolution",
     "Constitutional amendments and any dissolution can only be carried out at a formally convened meeting with at least 75% of those present and voting in favour. On dissolution any remaining assets pass to a properly constituted body with similar aims, never to private individuals or commercial organisations."),
]

# ---------------------------------------------------------------------------
# SVG icons (small, hand-drawn glyphs for the pillar cards)
# ---------------------------------------------------------------------------
ICONS = {
    "circuit": '<path d="M3 7h6m6 0h6M3 17h6m6 0h6" stroke-width="1.6" stroke="currentColor" stroke-linecap="round" fill="none"/><circle cx="9" cy="7" r="1.5" fill="currentColor"/><circle cx="15" cy="7" r="1.5" fill="currentColor"/><circle cx="9" cy="17" r="1.5" fill="currentColor"/><circle cx="15" cy="17" r="1.5" fill="currentColor"/><path d="M9 8.5v7M15 8.5v7" stroke-width="1.6" stroke="currentColor" fill="none"/>',
    "spark":  '<path d="M12 3v6M12 15v6M3 12h6M15 12h6M5.5 5.5l4 4M14.5 14.5l4 4M18.5 5.5l-4 4M9.5 14.5l-4 4" stroke-width="1.6" stroke="currentColor" stroke-linecap="round" fill="none"/><circle cx="12" cy="12" r="2.4" fill="currentColor"/>',
    "chain":  '<rect x="3" y="9" width="9" height="6" rx="3" stroke-width="1.6" stroke="currentColor" fill="none"/><rect x="12" y="9" width="9" height="6" rx="3" stroke-width="1.6" stroke="currentColor" fill="none"/><path d="M8 12h8" stroke-width="1.6" stroke="currentColor"/>',
    "lens":   '<circle cx="12" cy="12" r="8" stroke-width="1.6" stroke="currentColor" fill="none"/><circle cx="12" cy="12" r="3.5" fill="currentColor"/><circle cx="17" cy="8" r="1" fill="currentColor"/>',
    "rocket": '<path d="M12 3c4 3 6 7 6 11l-6 5-6-5c0-4 2-8 6-11z" stroke-width="1.6" stroke="currentColor" fill="none"/><circle cx="12" cy="11" r="2.2" fill="currentColor"/><path d="M9 18l-2 3M15 18l2 3" stroke-width="1.6" stroke="currentColor" stroke-linecap="round"/>',
    "ledger": '<rect x="4" y="4" width="16" height="16" rx="2" stroke-width="1.6" stroke="currentColor" fill="none"/><path d="M8 9h8M8 13h8M8 17h5" stroke-width="1.6" stroke="currentColor" stroke-linecap="round"/>',
    "hands":  '<path d="M5 13c0-2 1-4 3-4s3 1 3 3v3l-3 4-3-2v-4zM19 13c0-2-1-4-3-4s-3 1-3 3v3l3 4 3-2v-4z" stroke-width="1.6" stroke="currentColor" fill="none"/>',
    "globe":  '<circle cx="12" cy="12" r="8" stroke-width="1.6" stroke="currentColor" fill="none"/><path d="M4 12h16M12 4c2.5 3 2.5 13 0 16M12 4c-2.5 3-2.5 13 0 16" stroke-width="1.6" stroke="currentColor" fill="none"/>',
    "flame":  '<path d="M12 3c0 4-5 5-5 10a5 5 0 0010 0c0-2-1-3-2-4 0 2-1 3-2 3 1-3-1-6-1-9z" stroke-width="1.6" stroke="currentColor" fill="none"/>',
}
def icon(key, color=None):
    g = ICONS.get(key, ICONS["spark"])
    c = f' style="color:{color}"' if color else ""
    return f'<svg width="28" height="28" viewBox="0 0 24 24"{c}>{g}</svg>'

# THI mark, the official logo, sourced from the JPEG provided by the
# committee (assets/thi-logo.jpeg). Used at varying sizes across the site.
# `inverted=True` adds a white tile behind the logo for use on dark surfaces
# (navbar, footer, dark sections) so the satin background reads as intentional.
LOGO_PATH = "assets/thi-logo.jpeg"

def thi_mark(size=44, inverted=False):
    # On dark surfaces, give the JPEG a white tile + small inset so the
    # silk background frames cleanly as a brand card.
    if inverted:
        style = (f'width:{size}px;height:{size}px;background:#fff;border-radius:6px;'
                 f'padding:3px;box-sizing:border-box;display:block')
    else:
        style = f'width:{size}px;height:{size}px;display:block'
    return (f'<img src="{LOGO_PATH}" alt="The Hiram Initiative" '
            f'style="{style}">')

# ---------------------------------------------------------------------------
# Shared HTML scaffolding
# ---------------------------------------------------------------------------
def head(title, desc, image=None):
    share = (f'<meta property="og:image" content="{ORG["base_url"]}/{image}">\n'
             f'<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
             f'<meta name="twitter:card" content="summary_large_image">\n'
             f'<meta name="twitter:image" content="{ORG["base_url"]}/{image}">\n') if image else ""
    return f"""<!DOCTYPE html><html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
{share}<meta name="theme-color" content="{ACCENT}">
<link rel="icon" type="image/jpeg" href="{LOGO_PATH}">
<link rel="apple-touch-icon" href="{LOGO_PATH}">
<style>{css()}</style>
</head>"""

def css():
    return f"""
:root {{
  --ink:{INK}; --accent:{ACCENT}; --accent-dark:{ACCENT_DARK}; --accent-lite:{ACCENT_LITE};
  --teal:{TEAL}; --ff:{FF_BLUE}; --ff-yellow:{FF_YELLOW};
  --paper:{PAPER}; --muted:{MUTED};
  --wrap:1200px;
}}
*{{box-sizing:border-box}}
html,body{{margin:0;padding:0}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,Helvetica,Arial,sans-serif;color:var(--ink);background:var(--paper);line-height:1.55;-webkit-font-smoothing:antialiased}}
a{{color:var(--ink);text-decoration:none}}
a:hover{{color:var(--accent)}}
img,svg{{display:block;max-width:100%}}
.wrap{{max-width:var(--wrap);margin:0 auto;padding:0 24px}}
h1,h2,h3,h4{{font-weight:700;line-height:1.15;color:var(--ink);margin:0 0 .5em}}
h1{{font-size:clamp(2rem,5vw,3.4rem);letter-spacing:-.02em}}
h2{{font-size:clamp(1.5rem,3vw,2.2rem);letter-spacing:-.01em;margin-top:0}}
h3{{font-size:1.15rem}}
p{{margin:0 0 .8em}}
.lead{{font-size:1.1rem;color:var(--muted);max-width:64ch}}
.muted{{color:var(--muted)}}
.eyebrow{{display:inline-block;color:var(--teal);font-weight:700;text-transform:uppercase;letter-spacing:.12em;font-size:.78rem;margin-bottom:.6em}}
.eyebrow.orange{{color:var(--accent)}}

/* Nav */
.nav{{background:var(--ink);color:#fff;position:sticky;top:0;z-index:50;border-bottom:3px solid var(--accent)}}
.nav .wrap{{display:flex;align-items:center;gap:18px;padding-top:12px;padding-bottom:12px}}
.nav a{{color:#fff}}
.nav .brand{{display:flex;align-items:center;gap:10px;font-weight:700;font-size:1.05rem;letter-spacing:.01em;margin-right:auto}}
.nav .brand .bsub{{color:var(--accent);font-weight:700;margin-left:.25em}}
.navlinks{{display:flex;gap:22px;align-items:center;flex-wrap:wrap}}
.navlinks a{{font-size:.92rem;color:#dcdcdc}}
.navlinks a:hover, .navlinks a.active{{color:#fff}}
.navlinks .cta{{background:var(--accent);color:#fff;padding:8px 16px;border-radius:6px;font-weight:600}}
.navlinks .cta:hover{{background:var(--accent-dark);color:#fff}}
.navtoggle{{display:none;background:transparent;border:1px solid #555;color:#fff;border-radius:4px;padding:4px 10px;font-size:1.1rem;cursor:pointer}}
@media (max-width:820px){{
  .navtoggle{{display:inline-block}}
  .navlinks{{display:none;flex-basis:100%;flex-direction:column;align-items:flex-start;gap:14px;padding:14px 0}}
  .navlinks.open{{display:flex}}
}}

/* Sections */
section{{padding:64px 0}}
section.band{{background:#fafafa;border-top:1px solid #eee;border-bottom:1px solid #eee}}
section.hero{{padding:88px 0 56px;background:linear-gradient(180deg,#fff, #fafafa)}}
section.dark{{background:var(--ink);color:#fff}}
section.dark h1,section.dark h2,section.dark h3{{color:#fff}}
section.dark .muted, section.dark .lead{{color:#bdbdbd}}
section.dark .eyebrow{{color:var(--accent)}}

.sec-head{{margin-bottom:32px}}
.sec-head h2{{margin:.2em 0 .3em}}
.sec-head p{{max-width:64ch}}

/* Grids */
.grid{{display:grid;gap:22px}}
.g2{{grid-template-columns:repeat(auto-fit,minmax(280px,1fr))}}
.g3{{grid-template-columns:repeat(auto-fit,minmax(260px,1fr))}}
.g4{{grid-template-columns:repeat(auto-fit,minmax(220px,1fr))}}

.card{{background:#fff;border:1px solid #eee;border-radius:12px;padding:24px;transition:border-color .15s, transform .15s}}
.card:hover{{border-color:var(--accent)}}
.card.dark{{background:#222;border-color:#333;color:#fff}}
.card .icon-wrap{{display:inline-flex;align-items:center;justify-content:center;width:44px;height:44px;border-radius:10px;background:var(--accent-lite);color:var(--accent);margin-bottom:14px}}
.card h3{{margin-bottom:.35em}}
.card p{{margin:0;color:var(--muted);font-size:.95rem}}
.card .num{{display:inline-block;font-weight:800;font-size:.8rem;color:var(--accent);background:var(--accent-lite);border-radius:30px;padding:3px 10px;margin-bottom:10px;letter-spacing:.04em}}

/* Buttons */
.btn{{display:inline-block;padding:12px 22px;border-radius:8px;font-weight:600;font-size:.95rem;border:1.5px solid transparent;cursor:pointer;text-decoration:none}}
.btn-primary{{background:var(--accent);color:#fff}}
.btn-primary:hover{{background:var(--accent-dark);color:#fff}}
.btn-ghost{{background:transparent;color:var(--ink);border-color:var(--ink)}}
.btn-ghost:hover{{background:var(--ink);color:#fff}}
.btn-ff{{background:var(--ff);color:#fff}}
.btn-ff:hover{{filter:brightness(1.1);color:#fff}}
.cta{{display:flex;gap:12px;flex-wrap:wrap;margin-top:24px}}

/* Pillar tiles on home */
.pillar-tile{{display:block;border:1px solid #eee;border-radius:12px;padding:22px;background:#fff;transition:transform .15s,border-color .15s;color:var(--ink)}}
.pillar-tile:hover{{transform:translateY(-2px);border-color:var(--accent);color:var(--ink)}}
.pillar-tile .icon-wrap{{margin-bottom:10px}}
.pillar-tile h3{{margin:.1em 0;font-size:1.05rem}}
.pillar-tile .arrow{{color:var(--accent);font-weight:700;margin-top:14px;display:inline-block}}

/* Bullet rows */
.bullet{{display:flex;gap:14px;padding:14px 0;border-bottom:1px solid #eee}}
.bullet:last-child{{border-bottom:0}}
.bullet .b-num{{flex-shrink:0;width:36px;height:36px;border-radius:50%;background:var(--accent-lite);color:var(--accent);font-weight:800;display:flex;align-items:center;justify-content:center;font-size:.85rem}}
.bullet .b-body h4{{margin:.1em 0 .3em;font-size:1.02rem}}
.bullet .b-body p{{margin:0;color:var(--muted);font-size:.95rem}}

/* Hero variants */
.hero h1 em{{font-style:normal;color:var(--accent)}}
.hero .thesis{{font-size:1.25rem;color:var(--ink);margin:.6em 0 .4em;max-width:60ch}}
.hero .thesis em{{font-style:italic;color:var(--accent)}}

/* Frontier Fusion themed sections */
.ff-hero{{background:linear-gradient(135deg, {FF_BLUE} 0%, #1f3fb8 100%);color:#fff;padding:88px 0;position:relative;overflow:hidden}}
.ff-hero h1{{color:#fff;font-size:clamp(2.4rem,7vw,4.6rem);line-height:1.02}}
.ff-hero .ff-chip{{display:inline-block;background:{FF_YELLOW};color:{INK};padding:6px 14px;font-weight:700;border-radius:4px;letter-spacing:.04em}}
.ff-hero .ff-meta{{display:flex;flex-wrap:wrap;gap:18px;margin-top:28px}}
.ff-hero .ff-meta div{{background:rgba(0,0,0,.25);padding:14px 18px;border-radius:8px;backdrop-filter:blur(6px)}}
.ff-hero .ff-meta strong{{display:block;font-size:.78rem;text-transform:uppercase;letter-spacing:.08em;color:#cfd9ff;margin-bottom:4px}}

/* Builder to Business */
.b2b-hero{{background:var(--ink);color:#fff;padding:80px 0;border-bottom:4px solid var(--accent)}}
.b2b-hero h1{{color:#fff;font-size:clamp(2.2rem,6vw,3.8rem);line-height:1.04;margin-top:18px}}
.b2b-hero .tag{{font-size:1.3rem;font-weight:600;color:#f3d7c2;margin-top:6px}}
.b2b-chip{{display:inline-block;background:var(--accent);color:#fff;padding:6px 14px;font-weight:700;border-radius:4px;letter-spacing:.04em;font-size:.85rem;text-transform:uppercase}}
.b2b-grid{{display:grid;grid-template-columns:1.25fr .75fr;gap:40px;align-items:center}}
@media (max-width:860px){{.b2b-grid{{grid-template-columns:1fr}}}}
.b2b-logo-card{{background:#F6F0E8;border-radius:16px;padding:26px}}
.b2b-meta{{display:flex;flex-wrap:wrap;gap:14px;margin-top:26px}}
.b2b-meta div{{background:#262626;border:1px solid #333;padding:14px 18px;border-radius:8px}}
.b2b-meta strong{{display:block;font-size:.75rem;text-transform:uppercase;letter-spacing:.08em;color:var(--accent);margin-bottom:4px}}
.b2b-hero .btn-ghost{{border-color:#fff;color:#fff}}
.b2b-hero .btn-ghost:hover{{background:#fff;color:var(--ink)}}
.speaker{{display:flex;gap:18px;align-items:flex-start}}
.speaker .face{{width:96px;height:96px;border-radius:50%;object-fit:cover;flex-shrink:0}}
.speaker .initials{{width:96px;height:96px;border-radius:50%;flex-shrink:0;background:var(--accent-lite);color:var(--accent);display:flex;align-items:center;justify-content:center;font-weight:800;font-size:1.7rem;letter-spacing:.02em}}
.speaker .focus{{font-size:.78rem;font-weight:700;color:var(--teal);text-transform:uppercase;letter-spacing:.08em}}
.speaker .talk{{font-weight:600;margin:.2em 0 .4em}}
.day ul{{margin:10px 0 0;padding-left:18px;line-height:1.9;color:var(--muted)}}
.faq details{{border-bottom:1px solid #eee;padding:16px 0}}
.faq summary{{cursor:pointer;font-weight:700;font-size:1.02rem}}
.faq details p{{margin:.6em 0 0;color:var(--muted)}}
.partner-logo{{width:72px;height:72px;border-radius:12px;object-fit:cover;margin-bottom:14px;display:block}}
.photo{{width:100%;border-radius:14px;display:block;object-fit:cover}}
.caption{{font-size:.85rem;color:var(--muted);margin-top:8px}}

/* Footer */
footer{{background:var(--ink);color:#bdbdbd;padding:56px 0 32px}}
footer h5{{color:#fff;text-transform:uppercase;font-size:.78rem;letter-spacing:.1em;margin-bottom:14px}}
footer a{{color:#bdbdbd}}
footer a:hover{{color:#fff}}
footer ul{{list-style:none;padding:0;margin:0}}
footer ul li{{margin-bottom:8px}}
footer .fgrid{{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:36px}}
footer .fgrid > div:first-child p{{max-width:42ch}}
footer .legal{{border-top:1px solid #333;margin-top:36px;padding-top:20px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:16px;font-size:.85rem}}
@media (max-width:760px){{footer .fgrid{{grid-template-columns:1fr 1fr}}}}
@media (max-width:480px){{footer .fgrid{{grid-template-columns:1fr}}}}

/* Stats */
.stats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:20px;margin-top:32px}}
.stat{{background:#fff;border:1px solid #eee;border-radius:10px;padding:18px}}
.stat .big{{font-size:1.8rem;font-weight:800;color:var(--accent);letter-spacing:-.02em}}
.stat .lbl{{font-size:.82rem;color:var(--muted)}}

/* Tag chips */
.chips{{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}}
.chips span{{font-size:.78rem;background:#fff;border:1px solid #ddd;border-radius:30px;padding:5px 12px;color:var(--muted)}}
section.dark .chips span{{background:#222;border-color:#444;color:#bdbdbd}}

/* Honest status box */
.note{{border-left:4px solid var(--accent);background:var(--accent-lite);padding:16px 20px;border-radius:6px;margin-top:24px}}
.note strong{{color:var(--ink)}}

/* Roadmap timeline */
.timeline{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:20px}}
.tl{{padding:24px;background:#fff;border-radius:12px;border:1px solid #eee;position:relative}}
.tl .q{{font-size:.78rem;font-weight:800;color:var(--accent);letter-spacing:.08em;text-transform:uppercase;margin-bottom:10px;display:inline-block;background:var(--accent-lite);padding:4px 10px;border-radius:30px}}
.tl p{{margin:0;color:var(--muted);font-size:.95rem}}
"""

def navbar(active=""):
    def cls(n): return ' class="active"' if n == active else ''
    links = [
        ("about",            "About",            "About"),
        ("programmes",       "Programmes",       "Programmes"),
        ("builder-to-business", "Builder to Business", "Builder to Business"),
        ("frontier-fusion",  "Frontier Fusion",  "Frontier Fusion"),
        ("governance",       "Governance",       "Governance"),
        ("partners",         "Partners",         "Partners"),
    ]
    rendered = "".join(f'<a href="{slug}.html"{cls(slug)}>{label}</a>' for slug, _, label in links)
    return f"""<header class="nav"><div class="wrap">
<a class="brand" href="index.html">{thi_mark(40, inverted=True)} <span>The Hiram<span class="bsub">Initiative</span></span></a>
<button class="navtoggle" aria-label="Menu" onclick="document.getElementById('nl').classList.toggle('open')">≡</button>
<nav class="navlinks" id="nl">{rendered}
<a class="cta" href="contact.html">Get involved</a>
</nav></div></header>"""

def footer():
    nav_links = "".join([
        '<li><a href="about.html">About</a></li>',
        '<li><a href="programmes.html">Programmes</a></li>',
        '<li><a href="builder-to-business.html">Builder to Business</a></li>',
        '<li><a href="age-of-agents.html">Age of Agents</a></li>',
        '<li><a href="frontier-fusion.html">Frontier Fusion</a></li>',
        '<li><a href="governance.html">Governance</a></li>',
        '<li><a href="partners.html">Partners</a></li>',
        '<li><a href="contact.html">Contact</a></li>',
    ])
    pillar_links = "".join(f'<li><a href="{p["slug"]}.html">{p["short"]}</a></li>' for p in PILLARS)
    return f"""<footer><div class="wrap">
<div class="fgrid">
  <div>{thi_mark(64, inverted=True)}
    <h5 style="margin-top:14px">The Hiram Initiative</h5>
    <p>{ORG['tagline']}</p>
    <p style="margin-top:14px">A community of {ORG['audience']} in the United Kingdom who aren't waiting for opportunities, they're creating them.</p>
    <p class="muted" style="font-size:.82rem;margin-top:14px">Workspace and seminar venue<br>{ORG['address']}</p>
  </div>
  <div>
    <h5>The site</h5>
    <ul>{nav_links}</ul>
  </div>
  <div>
    <h5>Five pillars</h5>
    <ul>{pillar_links}</ul>
  </div>
  <div>
    <h5>Reach us</h5>
    <ul>
      <li><a href="mailto:{ORG['email']}">{ORG['email']}</a></li>
      <li><a href="tel:{ORG['phone'].replace(' ', '')}">{ORG['phone']}</a></li>
      <li><a href="{ORG['instagram_url']}" target="_blank" rel="noopener">Instagram {ORG['instagram']} ↗</a></li>
      <li><a href="{ORG['x_url']}" target="_blank" rel="noopener">X {ORG['x']} ↗</a></li>
    </ul>
  </div>
</div>
<div class="legal">
  <span>© {ORG['year']} The Hiram Initiative · Constitution adopted {ORG['adopted']}</span>
  <span><a href="constitution.html">Constitution &amp; framework →</a></span>
</div>
</div></footer>
<script>document.querySelectorAll('.navlinks a').forEach(a=>a.addEventListener('click',()=>document.getElementById('nl').classList.remove('open')));</script>
</body></html>"""

def page(fname, title, desc, body, active="", image=None, extra_head=""):
    out = head(title, desc, image) + "<body>" + navbar(active) + body + footer()
    if extra_head:
        out = out.replace("</head>", extra_head + "\n</head>", 1)
    # canonical
    slug = fname[:-5]
    canon = f"https://{ORG['website']}/" + ("" if slug == "index" else slug)
    out = out.replace("</head>", f'<link rel="canonical" href="{canon}">\n<meta property="og:url" content="{canon}"></head>', 1)
    # Clean URLs: drop .html from every internal page link. The files on disk
    # stay flat (about.html etc.); GitHub Pages serves /about from about.html
    # natively. Skips external (has "://"), mailto, asset paths (.jpeg/.png/
    # .svg/.css/.js, those have no .html), and bare anchors.
    out = re.sub(r'href="index\.html(#[^"]*)?"',
                 lambda m: f'href="/{m.group(1) or ""}"', out)
    out = re.sub(r'href="([a-z0-9][a-z0-9-]*)\.html(#[^"]*)?"', r'href="\1\2"', out)
    with open(os.path.join(SITE, fname), "w", encoding="utf-8") as f:
        f.write(out)

# ---------------------------------------------------------------------------
# Page bodies
# ---------------------------------------------------------------------------
def home():
    pillar_tiles = "".join(
        f'<a class="pillar-tile" href="{p["slug"]}.html"><span class="icon-wrap">{icon(p["icon"])}</span>'
        f'<h3>{p["name"]}</h3><p class="muted" style="font-size:.92rem;margin:0">{p["tagline"]}</p>'
        f'<span class="arrow">Explore →</span></a>'
        for p in PILLARS
    )
    programmes_rows = "".join(
        f'<div class="bullet"><div class="b-num">{i+1:02d}</div><div class="b-body"><h4>{t}</h4><p>{p}</p></div></div>'
        for i, (t, p) in enumerate(PROGRAMMES)
    )
    stats = "".join(f'<div class="stat"><div class="big">{n}</div><div class="lbl">{l}</div></div>' for n, l in STATS)
    speakers = ", ".join(sp[0] for sp in B2B["speakers"][:-1]) + " and " + B2B["speakers"][-1][0]
    body = f"""
<section class="hero"><div class="wrap">
<span class="eyebrow orange">{ORG['tagline']}</span>
<h1>A generation that is not waiting for opportunities.<br><em>They are creating them.</em></h1>
<p class="thesis">{ORG['thesis']}</p>
<p class="lead">The Hiram Initiative exists to bridge the gap between traditional education and the rapidly evolving demands of the modern world, through practical education in IT, AI, blockchain, content creation and entrepreneurship, direct access to industry professionals, and a community built around shared purpose.</p>
<div class="cta">
  <a class="btn btn-primary" href="programmes.html">See the programmes →</a>
  <a class="btn btn-ghost" href="builder-to-business.html">Builder to Business · 20 &amp; 21 Nov ↗</a>
</div>
<div class="stats">{stats}</div>
</div></section>

<section class="band"><div class="wrap">
<div class="sec-head"><span class="eyebrow">The five pillars</span><h2>Built around what young people actually need</h2>
<p class="lead">Each pillar is a working programme, workshops, masterclasses, mentorship and community, designed for those most at risk from technological change, and most ready to shape what comes next.</p></div>
<div class="grid g3">{pillar_tiles}</div>
</div></section>

<section><div class="wrap">
<div class="sec-head"><span class="eyebrow">Programmes</span><h2>How we deliver</h2>
<p class="lead">Six running programmes, each grounded in practice, led by people who have done the thing they teach.</p></div>
{programmes_rows}
<div class="cta"><a class="btn btn-primary" href="programmes.html">The 2026 roadmap →</a></div>
</div></section>

<section class="b2b-hero"><div class="wrap b2b-grid">
<div>
<span class="b2b-chip">Next up · The Final Piece</span>
<h1>Builder to Business</h1>
<p class="tag">The final chapter of the B2B series.</p>
<p style="font-size:1.1rem;max-width:60ch;margin-top:16px;color:#e6e6e6">{B2B['short']}</p>
<div class="b2b-meta">
  <div><strong>When</strong>{B2B['when']}</div>
  <div><strong>Where</strong>{B2B['where']}</div>
  <div><strong>Speakers</strong>{speakers}</div>
</div>
<p style="margin-top:18px;color:#f3d7c2;font-weight:600">Free entry. Registration required.</p>
<div class="cta">
  <a class="btn btn-ghost" href="builder-to-business.html">Event details →</a>
  <a class="btn btn-primary" href="{ORG['register_url']}" target="_blank" rel="noopener">Register now ↗</a>
</div>
</div>
<div>{flyer(400)}</div>
</div></section>

<section class="band"><div class="wrap" style="text-align:center">
<div class="sec-head" style="margin:0 auto 24px"><span class="eyebrow">Watch</span><h2>From an idea to a business</h2></div>
{promo_video()}
<p class="caption" style="max-width:46ch;margin:12px auto 0">{B2B['caption']}</p>
</div></section>

<section><div class="wrap">
<div class="sec-head"><span class="eyebrow">The Hiram story</span><h2>Why "Hiram"</h2></div>
<div class="grid g2">
  <div>
    <p>The name comes from the Hebrew, meaning <em>Brother of the Exalted. Noble. Free.</em></p>
    <p>In 1 Kings 5, Hiram was a king who sent his finest craftsmen, resources and skills to help Solomon build the Temple, the most significant structure of a generation. He crossed national and cultural lines to equip the people around him with what they needed to build something that would outlast them all.</p>
    <p><strong>Hiram did not build the Temple. He equipped the people who did.</strong> That is what The Hiram Initiative is doing for this generation.</p>
    <a class="btn btn-ghost" href="about.html" style="margin-top:8px">Read the full identity →</a>
  </div>
  <div class="card" style="background:#fafafa">
    <h3>Where we operate</h3>
    <p class="muted">Our workspace, seminar venue, mentorship hub and community base.</p>
    <p style="margin-top:14px"><strong>{ORG['address']}</strong></p>
    <p class="muted" style="margin-top:14px;font-size:.92rem">Programmes are delivered across London with a particular focus on accessibility for young people most at risk from technological change.</p>
  </div>
</div>
</div></section>
"""
    page("index.html", f"{ORG['name']}, {ORG['tagline']}",
         "The Hiram Initiative equips young people in the UK with IT, AI, blockchain, content creation and entrepreneurship skills, through workshops, masterclasses, mentorship and community.",
         body, "")

def about():
    com_cards = "".join(
        f'<div class="card"><div class="num">{role.upper()}</div><h3>{name}</h3><p>{bio}</p></div>'
        for name, role, bio in COMMITTEE
    )
    vol_lines = "".join(
        f'<li><strong>{n}</strong>, <span class="muted">{r}</span></li>' for n, r in VOLUNTEERS
    )
    body = f"""
<section class="hero"><div class="wrap">
<span class="eyebrow">About</span>
<h1>Identity and purpose</h1>
<p class="thesis">We bridge the gap between traditional education and the demands of the modern world, and the gap between where young people are and where they're <em>capable of going</em>.</p>
</div></section>

<section><div class="wrap">
<div class="sec-head"><span class="eyebrow">Mission</span><h2>What we do</h2></div>
<p class="lead">The Hiram Initiative exists to close the gap between where young people are and where they are capable of going. We do this by focusing on the skills, mindset and networks that define success in the modern world, delivered through practical education, direct access to industry professionals, and a community built around shared purpose.</p>
</div></section>

<section class="band"><div class="wrap">
<div class="sec-head"><span class="eyebrow">Vision</span><h2>The community we are building</h2></div>
<p class="lead">A generation of {ORG['audience']} in the United Kingdom who are not waiting for opportunities. They are creating them. A community where every member grows, contributes and leads with purpose.</p>
</div></section>

<section><div class="wrap">
<div class="sec-head"><span class="eyebrow">The name</span><h2>Why "Hiram"</h2></div>
<p>The name <em>Hiram</em> comes from the Hebrew meaning <em>Brother of the Exalted. Noble. Free.</em></p>
<p>In 1 Kings 5, Hiram was a king who sent his finest craftsmen, resources and skills to help Solomon build the Temple, the most significant structure of a generation. He crossed national and cultural lines to equip the people around him with what they needed to build something that would outlast them all.</p>
<p style="font-size:1.2rem;font-weight:600">Hiram did not build the Temple. He equipped the people who did. That is what The Hiram Initiative is doing for this generation.</p>
</div></section>

<section class="band"><div class="wrap">
<div class="sec-head"><span class="eyebrow">Core aim</span><h2>Equipping young people to face the technological wave</h2></div>
<p class="lead">Our aim is to support young people in attaining their full potential through education in Information Technology, Artificial Intelligence, Blockchain, Content Creation and Entrepreneurship, equipping them to confidently face the social, economic and community challenges that increasingly emerge through technological development.</p>
<div class="cta"><a class="btn btn-primary" href="programmes.html">See the five pillars →</a></div>
</div></section>

<section class="band"><div class="wrap">
<img class="photo" src="assets/community.jpg" alt="A Hiram Initiative session, with the THI banner beside the speakers" loading="lazy" style="max-height:440px">
<p class="caption">A THI session. Around 250 active members meet in our WhatsApp community and at our events.</p>
</div></section>

<section><div class="wrap">
<div class="sec-head"><span class="eyebrow">Who runs THI</span><h2>Current committee</h2>
<p class="lead">A small founding committee responsible for the overall direction, oversight and operational management of the organisation, appointed for an initial three year term in line with Section 4.4 of the constitution.</p></div>
<div class="grid g3">{com_cards}</div>
<div style="margin-top:32px">
  <h3>Volunteers contributing to the work</h3>
  <ul style="margin-top:10px;line-height:1.9">{vol_lines}</ul>
</div>
<div class="note"><strong>How the committee operates.</strong> Anyone can apply to join the committee. Vacancies can be filled by the committee appointing a new member. Election or removal happens at a formally convened committee meeting. Members serve three year terms and can stand for election again. A member may resign at any time, provided their resignation does not leave fewer than three members on the committee.</div>
</div></section>
"""
    page("about.html", f"About, {ORG['name']}",
         "The Hiram Initiative's identity, mission, vision and current committee, adopted under the constitution of 13 May 2026.",
         body, "about")

def programmes():
    pillar_cards = "".join(
        f'<a class="pillar-tile" href="{p["slug"]}.html">'
        f'<span class="icon-wrap">{icon(p["icon"])}</span>'
        f'<h3>{p["name"]}</h3>'
        f'<p class="muted">{p["tagline"]}</p>'
        f'<span class="arrow">Explore →</span></a>'
        for p in PILLARS
    )
    prog_rows = "".join(
        f'<div class="bullet"><div class="b-num">{i+1:02d}</div><div class="b-body"><h4>{t}</h4><p>{p}</p></div></div>'
        for i, (t, p) in enumerate(PROGRAMMES)
    )
    timeline = "".join(
        f'<div class="tl"><span class="q">{q}</span><p>{d}</p></div>'
        for q, d in ROADMAP
    )
    cross_html = "".join(
        f'<div class="card"><h3>{c["name"]}</h3>' +
        "".join(f'<p style="margin-top:10px"><strong>{t}.</strong> <span class="muted">{p}</span></p>' for t, p in c["items"]) +
        '</div>'
        for c in CROSS_CUTTING
    )
    body = f"""
<section class="hero"><div class="wrap">
<span class="eyebrow">Programmes</span>
<h1>Five pillars, one community</h1>
<p class="lead">The Hiram Initiative organises its work into five core pillars: Information Technology, Artificial Intelligence, Blockchain, Content Creation and Entrepreneurship, supported by Life Intelligence and Community Access running across them all.</p>
</div></section>

<section><div class="wrap">
<div class="sec-head"><span class="eyebrow">The pillars</span><h2>What we teach</h2></div>
<div class="grid g3">{pillar_cards}</div>
</div></section>

<section class="band"><div class="wrap">
<div class="sec-head"><span class="eyebrow">How we deliver</span><h2>Six running programmes</h2>
<p class="lead">Programmes are designed to be practical and directly applicable to real situations.</p></div>
{prog_rows}
</div></section>

<section><div class="wrap">
<div class="sec-head"><span class="eyebrow">Events</span><h2>Upcoming and recent</h2>
<p class="lead">The B2B series reaches its finale in November. Earlier in 2026, Age of Agents and Frontier Fusion filled the room.</p></div>
<div class="grid g3">
  <a class="pillar-tile" href="builder-to-business.html"><span class="num">Next up · 20 &amp; 21 Nov</span><h3>Builder to Business</h3><p class="muted">The Final Piece: a free two day accelerator in Tottenham.</p><span class="arrow">Event details →</span></a>
  <a class="pillar-tile" href="age-of-agents.html"><span class="num">Completed · July 2026</span><h3>Age of Agents</h3><p class="muted">Three afternoons building AI agents. Sold out, with over 150 attendees.</p><span class="arrow">Recap →</span></a>
  <a class="pillar-tile" href="frontier-fusion.html"><span class="num">Completed · May 2026</span><h3>Frontier Fusion</h3><p class="muted">AI, on chain and creator communities at Encode Hub, London.</p><span class="arrow">Recap →</span></a>
</div>
</div></section>

<section><div class="wrap">
<div class="sec-head"><span class="eyebrow">2026 roadmap</span><h2>Quarter by quarter</h2>
<p class="lead">Set out by the Chairperson at the initiation meeting on {ORG['agm']} and recorded in the AGM minutes.</p></div>
<div class="timeline">{timeline}</div>
</div></section>

<section class="band"><div class="wrap">
<div class="sec-head"><span class="eyebrow">Across every pillar</span><h2>Life intelligence &amp; community</h2>
<p class="lead">Two threads run through everything we deliver, mindset frameworks for navigating change, and inclusive access for the communities most at risk of being left behind.</p></div>
<div class="grid g2">{cross_html}</div>
</div></section>
"""
    page("programmes.html", f"Programmes, {ORG['name']}",
         "The five pillars of The Hiram Initiative: IT, AI, Blockchain, Content Creation, Entrepreneurship, with the 2026 roadmap of workshops, masterclasses, mentorship and community events.",
         body, "programmes")

def pillar_page(p):
    points = "".join(
        f'<div class="bullet"><div class="b-num">{i+1:02d}</div><div class="b-body"><h4>{t}</h4><p>{d}</p></div></div>'
        for i, (t, d) in enumerate(p["points"])
    )
    other = "".join(
        f'<a class="pillar-tile" href="{x["slug"]}.html"><span class="icon-wrap">{icon(x["icon"])}</span><h3>{x["name"]}</h3><p class="muted">{x["tagline"]}</p><span class="arrow">→</span></a>'
        for x in PILLARS if x["slug"] != p["slug"]
    )
    body = f"""
<section class="hero"><div class="wrap">
<span class="icon-wrap" style="background:var(--accent-lite);color:var(--accent);width:56px;height:56px;display:inline-flex;align-items:center;justify-content:center;border-radius:12px;margin-bottom:12px">{icon(p["icon"])}</span>
<span class="eyebrow">Pillar · One of five</span>
<h1>{p["name"]}</h1>
<p class="lead" style="font-size:1.2rem;color:var(--ink)">{p["tagline"]}</p>
<div class="cta">
  <a class="btn btn-primary" href="contact.html">Join the next cohort →</a>
  <a class="btn btn-ghost" href="programmes.html">← All programmes</a>
</div>
</div></section>

<section><div class="wrap">
<div class="sec-head"><span class="eyebrow">What we deliver</span><h2>Core focus areas</h2></div>
{points}
</div></section>

<section class="band"><div class="wrap">
<div class="sec-head"><span class="eyebrow">The other pillars</span><h2>How this fits with the rest</h2></div>
<div class="grid g4">{other}</div>
</div></section>
"""
    page(f"{p['slug']}.html", f"{re.sub('<.*?>', '', p['name'])}, {ORG['name']}",
         f"The {re.sub('<.*?>', '', p['name'])} pillar of The Hiram Initiative, {re.sub('<.*?>', '', p['tagline'])}",
         body, "programmes")

def frontier_fusion():
    gallery = "".join(
        f'<img src="assets/ff-{i:02d}.jpg" alt="Frontier Fusion 2026, Encode Hub London" loading="lazy" '
        'style="width:100%;height:240px;object-fit:cover;border-radius:12px;display:block">'
        for i in range(1, 8)
    )
    body = f"""
<section class="ff-hero"><div class="wrap">
<span class="ff-chip">Recap · {FRONTIER['date']}</span>
<h1 style="margin-top:18px">Frontier<br>Fusion</h1>
<p style="font-size:1.6rem;margin-top:8px;font-weight:600;color:#dde7ff">{FRONTIER['subtitle']}</p>
<p style="font-size:1.1rem;max-width:62ch;margin-top:24px;color:#e7edff">{FRONTIER['blurb']}</p>
<div class="ff-meta">
  <div><strong>When</strong>{FRONTIER['date']}, 6pm</div>
  <div><strong>Where</strong>{FRONTIER['venue']}</div>
  <div><strong>Hosts</strong>THI, OnChainBrits and Superteam UK</div>
</div>
<div class="cta">
  <a class="btn" style="background:{FF_YELLOW};color:{INK}" href="#gallery">See the photos ↓</a>
  <a class="btn btn-ghost" style="border-color:#fff;color:#fff" href="{ORG['instagram_url']}" target="_blank" rel="noopener">On Instagram ↗</a>
</div>
</div></section>

<section><div class="wrap" style="display:flex;gap:36px;flex-wrap:wrap;align-items:center;justify-content:center">
  <img src="assets/ff-flier.jpg" alt="Frontier Fusion 2026 flier" loading="lazy" style="width:100%;max-width:320px;border-radius:16px;box-shadow:0 14px 46px rgba(0,0,0,.22)">
  <div style="flex:1;min-width:280px;max-width:460px">
    <span class="eyebrow">The invitation</span>
    <h2>The night, on one page</h2>
    <p class="lead">The flier that drew the London frontier tech community to Encode Hub for an evening of AI, on chain and creator conversations.</p>
  </div>
</div></section>

<section><div class="wrap">
<div class="sec-head"><span class="eyebrow">The night</span><h2>An evening at the intersection</h2>
<p class="lead">Frontier Fusion was a memorable evening at Encode Hub, bringing creators, builders, founders and community members together around Solana, AI, blockchain, content creation and Internet Capital Markets. The room was packed, not a seat left, and by the end nobody felt like a stranger.</p></div>
<div class="grid g3">
  <div class="card"><div class="icon-wrap">{icon("lens")}</div><h3>Content on three levels</h3><p>How content really works, across Discovery, Trust and Community, and why each level compounds the next.</p></div>
  <div class="card"><div class="icon-wrap">{icon("spark")}</div><h3>The evolution of AI prompting</h3><p>A walk through the history and craft of prompting, from first principles to where it is heading next.</p></div>
  <div class="card"><div class="icon-wrap">{icon("chain")}</div><h3>Owning assets with a phone</h3><p>Owning real assets, including AI agents, with nothing more than a mobile phone and an internet connection.</p></div>
</div>
</div></section>

<section class="band" id="gallery"><div class="wrap">
<div class="sec-head"><span class="eyebrow">The room</span><h2>Photos from the night</h2>
<p class="lead">A packed house at Encode Hub, London.</p></div>
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px;margin-top:8px">{gallery}</div>
</div></section>

<section><div class="wrap">
<div class="sec-head"><span class="eyebrow">Who made it</span><h2>Hosts and collaborators</h2>
<p class="lead">Hosted by The Hiram Initiative together with the UK's most active on chain communities.</p></div>
<div class="grid g4">
  <div class="card"><h3>The Hiram Initiative</h3><p>Host: the community programme, built for young people, behind the event.</p></div>
  <div class="card"><h3>OnChainBrits</h3><p>UK on chain community partner: programming, network and reach.</p></div>
  <div class="card"><h3>Superteam UK</h3><p>The Solana ecosystem in the UK, bringing builders, founders and operators.</p></div>
  <div class="card"><h3>Onchain Hub and Encode Club</h3><p>Venue and community collaborators, with support from Chewie and Ohjay.</p></div>
</div>
</div></section>

<section class="band"><div class="wrap" style="text-align:center">
<div class="sec-head" style="margin:0 auto"><span class="eyebrow">The takeaway</span><h2>Still early. Just go build.</h2>
<p class="lead" style="margin:0 auto">Attendees left energised, with a clear message: it is still early, and the moment to build is now. Frontier Fusion strengthened the London frontier tech scene and built excitement ahead of Breakpoint 2026.</p></div>
<div class="cta" style="justify-content:center"><a class="btn btn-primary" href="contact.html">Get involved →</a><a class="btn btn-ghost" href="builder-to-business.html">Builder to Business →</a></div>
</div></section>
"""
    page("frontier-fusion.html", f"Frontier Fusion 2026: AI &amp; On Chain Innovation · {ORG['name']}",
         "Frontier Fusion 2026 recap: THI's flagship night at Encode Hub, London, with OnchainBrits and Superteam UK. Solana, AI, content and Internet Capital Markets. 15 May 2026.",
         body, "frontier-fusion")

def age_of_agents():
    body = f"""
<section style="padding:20px 0;background:var(--accent-lite);border-bottom:1px solid #f0d2bb"><div class="wrap">
<p style="margin:0"><strong>Completed · July 2026.</strong> Thank you to everyone who built with us. Next up is Builder to Business: The Final Piece on 20 &amp; 21 November. <a href="builder-to-business.html" style="color:var(--accent-dark);font-weight:700">See the event →</a></p>
</div></section>

<section class="ff-hero"><div class="wrap">
<span class="ff-chip">Completed · 9 to 11 July 2026 · 2pm to 6pm</span>
<h1 style="margin-top:18px">Age of<br>Agents</h1>
<p style="font-size:1.6rem;margin-top:8px;font-weight:600;color:#dde7ff">{AOA['subtitle']}</p>
<p style="font-size:1.1rem;max-width:64ch;margin-top:24px;color:#e7edff">{AOA['blurb']}</p>
<div class="ff-meta">
  <div><strong>When</strong>{AOA['date']}</div>
  <div><strong>Where</strong>{AOA['venue']}</div>
  <div><strong>Led by</strong>{AOA['led_by']}</div>
</div>
<div class="cta">
  <a class="btn" style="background:{FF_YELLOW};color:{INK}" href="builder-to-business.html">See Builder to Business →</a>
  <a class="btn btn-ghost" style="border-color:#fff;color:#fff" href="programmes.html">All programmes →</a>
</div>
</div></section>

<section><div class="wrap">
<div class="sec-head"><span class="eyebrow">The recap</span><h2>Sold out, three days running</h2>
<p class="lead">Over 150 people across three days, an average of 40 a day, building AI agents in Tottenham.</p></div>
<img class="photo" src="assets/aoa-group.jpg" alt="Age of Agents participants together in Tottenham, July 2026" loading="lazy">
<p class="caption">Age of Agents, Tottenham, July 2026.</p>
</div></section>

<section class="band"><div class="wrap">
<div class="sec-head"><span class="eyebrow">What we covered</span><h2>From first principles to your own agent</h2>
<p class="lead">Four tracks across the three afternoons, taught by people building in the field.</p></div>
<div class="grid g4">
  <div class="card"><div class="icon-wrap">{icon("lens")}</div><h3>Understand agents</h3><p>What an AI agent actually is, how it reasons and acts, and where it fits alongside the tools you already use.</p></div>
  <div class="card"><div class="icon-wrap">{icon("spark")}</div><h3>Build your first agent</h3><p>Practical, from a prompt to a working agent that completes real tasks, with the craft of prompting and tools.</p></div>
  <div class="card"><div class="icon-wrap">{icon("hands")}</div><h3>Own your agents</h3><p>Operating and owning agents with a mobile phone and an internet connection, no gatekeeper required.</p></div>
  <div class="card"><div class="icon-wrap">{icon("chain")}</div><h3>Agents on chain</h3><p>Where agents meet Solana, payments and Internet Capital Markets, and the new economics that opens up.</p></div>
</div>
</div></section>

<section><div class="wrap" style="display:flex;gap:36px;flex-wrap:wrap;align-items:center;justify-content:center">
  <img src="assets/aoa-flier.jpg" alt="The Age of the Agents flier: an introduction into the creation of AI Agents, 9th to 11th July 2026, hosted by Joseph Falano (Ohjay) with facilitator Jalaaldeen Akinola (JRD)" loading="lazy" style="width:100%;max-width:360px;border-radius:16px;box-shadow:0 14px 46px rgba(0,0,0,.22)">
  <div style="flex:1;min-width:280px;max-width:460px">
    <span class="eyebrow">Who it was for</span>
    <h2>Built for beginners, useful to builders</h2>
    <p class="lead">No prior experience was needed. We started from first principles and built up, so everyone left with an agent they made and the confidence to keep going.</p>
    <div class="cta"><a class="btn btn-primary" href="builder-to-business.html">Next: Builder to Business →</a><a class="btn btn-ghost" href="contact.html">Ask a question →</a></div>
  </div>
</div></section>
"""
    page("age-of-agents.html", f"Age of Agents: an introduction to creating AI agents · {ORG['name']}",
         "Age of Agents, The Hiram Initiative's practical introduction to creating AI agents, 9 to 11 July 2026 at 454A High Road, Bruce Grove, Tottenham, London N17 9JD. Sold out, with over 150 attendees. Led by Joseph Falano (Ohjay) with Jalaaldeen Akinola (JRD).",
         body, "programmes")

def governance():
    rows = "".join(
        f'<div class="bullet"><div class="b-num">{i+1:02d}</div><div class="b-body"><h4>{t}</h4><p>{d}</p></div></div>'
        for i, (t, d) in enumerate(GOVERNANCE)
    )
    com = "".join(
        f'<div class="card"><div class="num">{role.upper()}</div><h3>{name}</h3><p>{bio}</p></div>'
        for name, role, bio in COMMITTEE
    )
    body = f"""
<section class="hero"><div class="wrap">
<span class="eyebrow">Governance</span>
<h1>How THI is run</h1>
<p class="lead">A constitution adopted on {ORG['adopted']}, a committee accountable for the direction, oversight and operational management of the organisation, and financial governance that puts every pound raised back into the aim.</p>
</div></section>

<section><div class="wrap">
<div class="sec-head"><span class="eyebrow">The committee</span><h2>Who is accountable</h2></div>
<div class="grid g3">{com}</div>
</div></section>

<section class="band"><div class="wrap">
<div class="sec-head"><span class="eyebrow">Financial governance</span><h2>Six things that don't change</h2>
<p class="lead">Drawn from Part Six of the constitution and reaffirmed at the initiation meeting on {ORG['agm']}.</p></div>
{rows}
</div></section>

<section><div class="wrap">
<div class="sec-head"><span class="eyebrow">The constitution</span><h2>Adopted {ORG['adopted']}</h2>
<p class="lead">The constitution is the source of truth for how THI is structured, governed and operated. It covers identity, aims, programmes, governance, powers, finances, partnerships, amendments and dissolution.</p></div>
<div class="grid g2">
  <div class="card"><h3>Part One: Identity and Purpose</h3><p>Name, address, mission, vision, tagline, and the meaning of Hiram.</p></div>
  <div class="card"><h3>Part Two: Aims and Objectives</h3><p>The core aim, strategic objectives across the five pillars, and the work on Life Intelligence and Community Access that runs across them.</p></div>
  <div class="card"><h3>Part Three: Programmes and Delivery</h3><p>Workshops, masterclasses, Expert Speaker Series, mentorship matching, networking events, and the 2026 roadmap.</p></div>
  <div class="card"><h3>Part Four: Governance and Committee</h3><p>Committee structure, composition, current committee, and rules for membership, election, appointment by the committee and resignation.</p></div>
  <div class="card"><h3>Part Five: Powers of the Committee</h3><p>What the committee may do in furtherance of the aims, raise funds, hold an account, run programmes, partner, employ, consult.</p></div>
  <div class="card"><h3>Part Six: Finances and Funds</h3><p>Two signatory rule, no personal benefit, accurate records, and how funds are used across resources, events, mentors and outreach.</p></div>
  <div class="card"><h3>Part Seven: Partnerships and Collaboration</h3><p>Partnership principles, benefits to partners, and alignment with future workforce needs.</p></div>
  <div class="card"><h3>Part Eight: Amendments and Dissolution</h3><p>Any change requires a 75% vote at a formally convened meeting; on dissolution, assets pass to a body with similar aims.</p></div>
</div>
<div class="note"><strong>Want to see the signed original?</strong> Email <a href="mailto:{ORG['email']}">{ORG['email']}</a> and we'll share a copy of the signed constitution PDF (adopted {ORG['adopted']}).</div>
</div></section>
"""
    page("governance.html", f"Governance, {ORG['name']}",
         "How The Hiram Initiative is governed: committee, financial governance, and the constitution adopted 13 May 2026.",
         body, "governance")

def partners():
    benefits = "".join(
        f'<div class="bullet"><div class="b-num">{i+1:02d}</div><div class="b-body"><h4>{t}</h4><p>{d}</p></div></div>'
        for i, (t, d) in enumerate(PARTNERS_BENEFITS)
    )
    confirmed = "".join(
        f'<div class="card"><img class="partner-logo" src="{logo}" alt="{n} logo" loading="lazy"><h3>{n}</h3><p>{d}</p></div>'
        for n, d, logo in PARTNERS_CONFIRMED
    )
    body = f"""
<section class="hero"><div class="wrap">
<span class="eyebrow">Partnerships</span>
<h1>Build the talent pipeline your industry needs</h1>
<p class="lead">The Hiram Initiative actively seeks partnerships with organisations that share a commitment to youth empowerment, technological education, and community development. Partnerships are a core mechanism for expanding the reach, quality and impact of THI's programmes.</p>
<div class="cta">
  <a class="btn btn-primary" href="contact.html">Talk to us →</a>
  <a class="btn btn-ghost" href="frontier-fusion.html">See Frontier Fusion 2026 →</a>
</div>
</div></section>

<section><div class="wrap">
<img class="photo" src="assets/team.jpg" alt="Members of The Hiram Initiative community at an event" loading="lazy" style="max-height:460px">
<p class="caption">The Hiram Initiative community.</p>
</div></section>

<section><div class="wrap">
<div class="sec-head"><span class="eyebrow">What partners receive</span><h2>Benefits, stated honestly</h2>
<p class="lead">From the constitution, Part Seven, the practical benefits of supporting THI's work.</p></div>
{benefits}
</div></section>

<section class="band"><div class="wrap">
<div class="sec-head"><span class="eyebrow">Already with us</span><h2>Partners and collaborators</h2>
<p class="lead">The organisations that have hosted, housed and backed our 2026 events.</p></div>
<div class="grid g4">{confirmed}</div>
</div></section>

<section><div class="wrap">
<div class="sec-head"><span class="eyebrow">Why it matters</span><h2>Alignment with future workforce needs</h2></div>
<p class="lead">Every sector needs employees and builders who understand AI, blockchain and digital technology. By supporting The Hiram Initiative, partners contribute directly to building the talent pipeline their industries need, while positioning themselves as champions of youth empowerment and inclusive technological education.</p>
<div class="cta"><a class="btn btn-primary" href="contact.html">Become a partner →</a></div>
</div></section>
"""
    page("partners.html", f"Partners, {ORG['name']}",
         "Partner with The Hiram Initiative: brand recognition, community access, talent pipeline and impact reporting, alongside OnChainBrits, Superteam UK, Encode Club and Gosen Inc.",
         body, "partners")

def contact():
    body = f"""
<section class="hero"><div class="wrap">
<span class="eyebrow">Get involved</span>
<h1>Three ways in</h1>
<p class="lead">Whether you're a young person ready to build, a professional with knowledge to share, or an organisation looking to back the work, here's how to reach us.</p>
</div></section>

<section><div class="wrap">
<div class="grid g3">
  <div class="card">
    <div class="icon-wrap">{icon("rocket")}</div>
    <h3>Join the community</h3>
    <p>You're a young person aged 18 to 35 in the UK, ready to invest in your IT, AI, blockchain, content or entrepreneurship skills. We're onboarding cohorts now.</p>
    <p style="margin-top:14px"><a class="btn btn-primary" href="mailto:{ORG['email']}?subject=Joining%20THI" style="padding:10px 18px;font-size:.9rem">Email to join →</a></p>
  </div>
  <div class="card">
    <div class="icon-wrap">{icon("hands")}</div>
    <h3>Mentor or speak</h3>
    <p>You've built something. You'd give an hour back, or run a masterclass, or join the Expert Speaker Series. We pair you with members who can use what you know.</p>
    <p style="margin-top:14px"><a class="btn btn-ghost" href="mailto:{ORG['email']}?subject=Mentorship%20%2F%20Speaking" style="padding:10px 18px;font-size:.9rem">Offer your time →</a></p>
  </div>
  <div class="card">
    <div class="icon-wrap">{icon("globe")}</div>
    <h3>Partner with us</h3>
    <p>Your organisation wants access to the talent pipeline, the THI community, and the platform of Frontier Fusion. See the partnership page first.</p>
    <p style="margin-top:14px"><a class="btn btn-ghost" href="partners.html" style="padding:10px 18px;font-size:.9rem">Partner page →</a></p>
  </div>
</div>
</div></section>

<section class="band"><div class="wrap">
<div class="sec-head"><span class="eyebrow">Direct lines</span><h2>Reach us</h2></div>
<div class="grid g4">
  <div class="card">
    <h3>Email</h3>
    <p><a href="mailto:{ORG['email']}">{ORG['email']}</a></p>
    <p class="muted">Fastest channel for joining, mentoring, partnering, or asking anything.</p>
  </div>
  <div class="card">
    <h3>Phone</h3>
    <p><a href="tel:{ORG['phone'].replace(' ','')}">{ORG['phone']}</a></p>
    <p class="muted">Office hours, leave a message and we'll come back the same week.</p>
  </div>
  <div class="card">
    <h3>Instagram</h3>
    <p><a href="{ORG['instagram_url']}" target="_blank" rel="noopener">{ORG['instagram']} ↗</a></p>
    <p class="muted">Event announcements and member highlights. Registration for each event is on its page.</p>
  </div>
  <div class="card">
    <h3>X</h3>
    <p><a href="{ORG['x_url']}" target="_blank" rel="noopener">{ORG['x']} ↗</a></p>
    <p class="muted">News, threads and updates from the community.</p>
  </div>
</div>
<div class="note" style="margin-top:32px"><strong>Workspace and seminar venue.</strong> {ORG['address']}. Visits by appointment, please email ahead.</div>
</div></section>
"""
    page("contact.html", f"Contact, {ORG['name']}",
         "Join, mentor, partner, or reach The Hiram Initiative directly. Email, phone, Instagram, X and our workspace in Tottenham, London.",
         body, "")

def builder_to_business():
    def face(name, img):
        if img:
            return f'<img class="face" src="{img}" alt="{name}" loading="lazy">'
        return f'<span class="initials" aria-hidden="true">{"".join(w[0] for w in name.split()[:2])}</span>'
    speakers = "".join(
        f'<div class="card speaker">{face(n, img)}<div><span class="focus">{focus}</span><h3 style="margin:.2em 0 .1em">{n}</h3>'
        f'<p class="talk">{talk}</p><p>{bio}</p></div></div>'
        for n, focus, talk, bio, img in B2B["speakers"]
    )
    learn = "".join(
        f'<div class="card"><div class="icon-wrap">{icon(ic)}</div><h3>{t}</h3><p>{d}</p></div>' for t, d, ic in B2B["learn"]
    )
    days = "".join(
        f'<div class="card day"><span class="num">{d}</span><h3>{focus}</h3><ul>' + "".join(f"<li>{x}</li>" for x in items) + "</ul></div>"
        for d, focus, items in B2B["days"]
    )
    shows = "".join(f'<div class="card"><h3>{n}</h3><p>{who}</p></div>' for n, who in B2B["showcases"])
    faq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in B2B["faq"])
    names = {sp[4]: sp[0] for sp in B2B["speakers"]}
    cards = "".join(
        f'<a href="assets/speaker-card-{c}.jpg" target="_blank" rel="noopener"><img class="photo" src="assets/speaker-card-{c}.jpg" '
        f'alt="Speaker card: {names[f"assets/speaker-{c}.jpg"]}" loading="lazy"></a>'
        for c in B2B["cards"]
    )
    series = "".join(
        f'<div class="tl"><span class="q">{k}</span><h3 style="margin:.2em 0 .3em">{t}</h3><p>{d}</p></div>' for k, t, d in B2B["series"]
    )
    about = "".join(f'<p class="lead">{x}</p>' for x in B2B["about"])
    reg = ORG["register_url"]
    body = f"""
<section class="b2b-hero"><div class="wrap b2b-grid">
<div>
<span class="b2b-chip">{B2B['chip']}</span>
<h1>{B2B['title']}</h1>
<p class="tag">{B2B['tagline']}</p>
<div class="b2b-meta">
  <div><strong>When</strong>{B2B['when']}</div>
  <div><strong>Where</strong>{B2B['where']}</div>
  <div><strong>Entry</strong>{B2B['entry']}</div>
</div>
<div class="cta">
  <a class="btn btn-primary" href="{reg}" target="_blank" rel="noopener">Register now ↗</a>
  <a class="btn btn-ghost" href="contact.html">Ask a question →</a>
</div>
</div>
<div>{flyer(440)}</div>
</div></section>

<section><div class="wrap b2b-grid" style="align-items:start">
<div>
<div class="sec-head"><span class="eyebrow">About the event</span><h2>The final chapter of the B2B series</h2></div>
{about}
</div>
<div>{promo_video()}<p class="caption" style="text-align:center">{B2B['caption']}</p></div>
</div></section>

<section class="band"><div class="wrap">
<div class="sec-head"><span class="eyebrow">What you will learn</span><h2>Two days, five tracks</h2></div>
<div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(200px,1fr))">{learn}</div>
</div></section>

<section><div class="wrap">
<div class="sec-head"><span class="eyebrow">Who it is for</span><h2>Builders ready to become business owners</h2>
<p class="lead">{B2B['for']}</p></div>
<div class="cta"><a class="btn btn-primary" href="{reg}" target="_blank" rel="noopener">Register now ↗</a></div>
</div></section>

<section class="band"><div class="wrap">
<div class="sec-head"><span class="eyebrow">Speakers</span><h2>Who you will learn from</h2></div>
<div class="grid g2">{speakers}</div>
<h3 style="margin-top:36px">Meet our speakers</h3>
<div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(170px,1fr));margin-top:14px">{cards}</div>
</div></section>

<section><div class="wrap">
<div class="sec-head"><span class="eyebrow">Programme highlights</span><h2>Two days, two focus areas</h2>
<p class="lead">Times to be confirmed. Doors from 10am on both days.</p></div>
<div class="grid g2">{days}</div>
</div></section>

<section class="band"><div class="wrap">
<div class="sec-head"><span class="eyebrow">Product showcases</span><h2>Real products, built by real builders</h2>
<p class="lead">Meet the founders behind them.</p></div>
<div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(200px,1fr))">{shows}</div>
<div class="grid g2" style="margin-top:32px;align-items:center">
  <img src="{B2B['guest_img']}" alt="{B2B['guest'][0]} invites you to Builder to Business: The Final Piece" loading="lazy" style="width:100%;max-width:360px;border-radius:16px;box-shadow:0 14px 46px rgba(0,0,0,.2);margin:0 auto">
  <div><span class="eyebrow orange">Special guest</span><h3 style="font-size:1.4rem">{B2B['guest'][0]}</h3><p class="lead">{B2B['guest'][1]}</p></div>
</div>
</div></section>

<section><div class="wrap">
<div class="sec-head"><span class="eyebrow">The B2B series</span><h2>The series so far</h2></div>
<div class="timeline">{series}</div>
<img class="photo" src="{B2B['series_img']}" alt="The Beginner to Business workshop poster, 24 October, Tottenham" loading="lazy" style="margin-top:24px">
<p class="caption">Beginner to Business, 24 October: the second chapter of the series.</p>
</div></section>

<section class="band"><div class="wrap faq">
<div class="sec-head"><span class="eyebrow">Questions</span><h2>Frequently asked</h2></div>
{faq}
</div></section>

<section class="b2b-hero" style="text-align:center"><div class="wrap">
<h2 style="color:#fff">Secure your spot. Let's take you from builder to business.</h2>
<div class="cta" style="justify-content:center"><a class="btn btn-primary" href="{reg}" target="_blank" rel="noopener">Register now ↗</a></div>
</div></section>
"""
    # schema.org Event: start and end dates only (end times are not yet confirmed)
    import json
    ld = {
        "@context": "https://schema.org", "@type": "Event", "name": re.sub("<.*?>", "", B2B["title"]),
        "description": re.sub("&amp;", "&", B2B["page_desc"]),
        "startDate": "2026-11-20T10:00:00+00:00", "endDate": "2026-11-21",
        "eventStatus": "https://schema.org/EventScheduled",
        "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
        "location": {"@type": "Place", "name": "454A High Road, Bruce Grove",
                     "address": {"@type": "PostalAddress", "streetAddress": "454A High Road, Bruce Grove, Tottenham", "postalCode": "N17 9JD",
                                 "addressLocality": "London", "addressCountry": "GB"}},
        "image": [f"{ORG['base_url']}/{B2B['share']}"],
        "organizer": {"@type": "Organization", "name": ORG["name"], "url": ORG["base_url"]},
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "GBP", "url": reg, "availability": "https://schema.org/InStock"},
        "performer": [{"@type": "Person", "name": sp[0]} for sp in B2B["speakers"]],
    }
    extra = '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>"
    page("builder-to-business.html", B2B["page_title"], B2B["page_desc"], body, "builder-to-business",
         image=B2B["share"], extra_head=extra)

def constitution_page():
    body = f"""
<section class="hero"><div class="wrap">
<span class="eyebrow">Constitution and organisational framework</span>
<h1>The Hiram Initiative</h1>
<p class="lead">Adopted by the founding committee on <strong>{ORG['adopted']}</strong>. The constitution is the source of truth for how THI is structured, governed and operated. This page is a public summary; the signed PDF is available on request.</p>
<div class="cta"><a class="btn btn-primary" href="mailto:{ORG['email']}?subject=Constitution%20PDF%20request">Request signed PDF →</a><a class="btn btn-ghost" href="governance.html">Governance overview →</a></div>
</div></section>

<section><div class="wrap">
<div class="sec-head"><span class="eyebrow">Contents</span><h2>What's inside</h2></div>
<ol style="line-height:2;font-size:1.05rem">
  <li><strong>Part One</strong>: Identity and Purpose</li>
  <li><strong>Part Two</strong>: Aims and Objectives</li>
  <li><strong>Part Three</strong>: Programmes and Delivery</li>
  <li><strong>Part Four</strong>: Governance and Committee</li>
  <li><strong>Part Five</strong>: Powers of the Committee</li>
  <li><strong>Part Six</strong>: Finances and Funds</li>
  <li><strong>Part Seven</strong>: Partnerships and Collaboration</li>
  <li><strong>Part Eight</strong>: Amendments and Dissolution</li>
  <li><strong>Part Nine</strong>: Adoption and Signatures</li>
</ol>
</div></section>

<section class="band"><div class="wrap">
<div class="sec-head"><span class="eyebrow">Adoption</span><h2>Signed and dated</h2></div>
<div class="grid g2">
  <div class="card"><h3>Chairperson</h3><p><strong>Johnson Ogúndèjì</strong></p><p class="muted">Signed {ORG['adopted']}</p></div>
  <div class="card"><h3>Secretary</h3><p><strong>Joseph Falano</strong></p><p class="muted">Signed {ORG['adopted']}</p></div>
</div>
<div class="note"><strong>Amendments.</strong> Alterations may only be made at a formally convened meeting with at least 75% of those present and voting in favour. Proposed amendments must be submitted in writing to the Secretary at least 14 days before the meeting.</div>
</div></section>
"""
    page("constitution.html", f"Constitution and organisational framework, {ORG['name']}",
         f"Public summary of The Hiram Initiative's constitution, adopted {ORG['adopted']}. Signed copy on request.",
         body, "governance")

# ---------------------------------------------------------------------------
# Build everything
# ---------------------------------------------------------------------------
def build():
    home()
    about()
    programmes()
    builder_to_business()
    for p in PILLARS: pillar_page(p)
    frontier_fusion()
    age_of_agents()
    governance()
    partners()
    contact()
    constitution_page()
    print(f"Site built: {len(os.listdir(SITE))} pages → {SITE}")

if __name__ == "__main__":
    build()
