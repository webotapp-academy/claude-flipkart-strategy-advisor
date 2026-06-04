from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, PageBreak, HRFlowable, KeepTogether)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate
from reportlab.pdfgen import canvas as pdfcanvas
import os

# ── Palette — monochrome executive, zero background colours ──────
BLACK   = HexColor('#0f0f0f')
INK     = HexColor('#1c1c1c')
BODY_C  = HexColor('#3a3a3a')
MUTED   = HexColor('#7a7a7a')
RULE    = HexColor('#d0d0d0')
ACCENT  = HexColor('#0f0f0f')   # pure black accent — no colour

# ── Sample data ───────────────────────────────────────────────────
OWNER    = "Paban Sharma"
BIZ      = "Outdoor Backpacker"
BIZ_TYPE = "Travel Agency / Tour Operator"
CITY     = "Guwahati, Assam"
YEARS    = "2–5 years"
TEAM     = "2–5 people"
REVENUE  = "Rs. 2,00,000 – 5,00,000 / month"
BUDGET   = "Rs. 5,000 – 20,000 / month"
GOAL     = "Get consistent leads every week"
CHALLENGE= "Not enough customers / leads"
TARGET   = "Young professionals aged 25–40 seeking Northeast India trips"
COMPETITORS = "Jungle Travels India, Seven Sisters Holidays"
SLUG     = "outdoor-backpacker"
DATE     = "June 2026"

OUTPUT = f'/mnt/user-data/outputs/flipkart_strategy_{SLUG}.pdf'
os.makedirs('/mnt/user-data/outputs', exist_ok=True)

# ── Page numbering callback ───────────────────────────────────────
class NumberedCanvas(pdfcanvas.Canvas):
    def __init__(self, *args, **kwargs):
        pdfcanvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            pdfcanvas.Canvas.showPage(self)
        pdfcanvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        page = self._pageNumber
        if page == 1:
            return
        self.setFont("Helvetica", 8)
        self.setFillColor(MUTED)
        # left: business name
        self.drawString(2*cm, 1.2*cm, BIZ.upper())
        # centre: document title
        self.drawCentredString(A4[0]/2, 1.2*cm, "FLIPKART GROWTH STRATEGY GUIDE")
        # right: page number
        self.drawRightString(A4[0] - 2*cm, 1.2*cm, f"{page} / {page_count}")
        # top rule
        self.setStrokeColor(RULE)
        self.setLineWidth(0.3)
        self.line(2*cm, A4[1] - 1.8*cm, A4[0] - 2*cm, A4[1] - 1.8*cm)
        # bottom rule
        self.line(2*cm, 1.6*cm, A4[0] - 2*cm, 1.6*cm)

doc = SimpleDocTemplate(
    OUTPUT, pagesize=A4,
    leftMargin=2.2*cm, rightMargin=2.2*cm,
    topMargin=2.8*cm, bottomMargin=2.8*cm,
    title=f'Flipkart Strategy Guide — {BIZ}',
    author='growth.webotapp.com'
)

W = A4[0] - 4.4*cm  # usable width

# ── Typography — refined, minimal ────────────────────────────────
def sty(name, font='Helvetica', size=10, color=BODY_C, leading=None,
        after=4, before=0, align=TA_LEFT, indent=0):
    return ParagraphStyle(name, fontName=font, fontSize=size,
        textColor=color, spaceAfter=after, spaceBefore=before,
        leading=leading or round(size * 1.55), alignment=align,
        leftIndent=indent)

COVER_EYEBROW = sty('CE', 'Helvetica', 8, MUTED, after=6, align=TA_LEFT)
COVER_TITLE   = sty('CT', 'Helvetica-Bold', 28, BLACK, leading=34, after=4)
COVER_SUB     = sty('CS', 'Helvetica', 11, MUTED, after=2)
COVER_META    = sty('CM', 'Helvetica', 9, MUTED, after=0)

H1 = sty('H1', 'Helvetica-Bold', 16, BLACK, leading=22, after=10, before=0)
H2 = sty('H2', 'Helvetica-Bold', 11, BLACK, leading=16, after=4, before=14)
H3 = sty('H3', 'Helvetica-Bold', 9,  BLACK, leading=13, after=3, before=8)

BODY   = sty('BD', 'Helvetica',      10, BODY_C, leading=16, after=5)
BODYJ  = sty('BJ', 'Helvetica',      10, BODY_C, leading=16, after=5, align=TA_JUSTIFY)
SMALL  = sty('SM', 'Helvetica',       8, MUTED,  leading=12, after=2)
ITALIC = sty('IT', 'Helvetica-Oblique', 9, MUTED, leading=13, after=3)
LABEL  = sty('LB', 'Helvetica-Bold',  8, BLACK,  leading=10, after=3, before=10)
BULLET = sty('BU', 'Helvetica',      10, BODY_C, leading=16, after=3, indent=10)
QWIN   = sty('QW', 'Helvetica-Oblique', 9, MUTED, leading=14, after=4, indent=0)
TOC_IT = sty('TI', 'Helvetica',      10, BODY_C, leading=15, after=0)
TOC_PG = sty('TP', 'Helvetica',      10, MUTED,  leading=15, after=0, align=TA_RIGHT)
FTR    = sty('FT', 'Helvetica',       8, MUTED,  leading=12, after=0, align=TA_CENTER)
STEP_N = sty('SN', 'Helvetica-Bold', 20, MUTED,  leading=24, after=0, align=TA_RIGHT)
STEP_T = sty('ST', 'Helvetica-Bold', 13, BLACK,  leading=18, after=2)
STEP_L = sty('SL', 'Helvetica-Oblique', 8, MUTED, leading=12, after=6)

def rule(space_before=0, space_after=8, thickness=0.3, color=RULE):
    return HRFlowable(width='100%', thickness=thickness,
                      color=color, spaceAfter=space_after, spaceBefore=space_before)

def thin_rule():
    return rule(space_before=2, space_after=6, thickness=0.2, color=RULE)

story = []

# ══════════════════════════════════════════════════════════════════
# COVER PAGE — typographic, zero colour
# ══════════════════════════════════════════════════════════════════
story.append(Spacer(1, 3*cm))
story.append(Paragraph("STRATEGY GUIDE", COVER_EYEBROW))
story.append(rule(space_before=4, space_after=16, thickness=0.8, color=BLACK))
story.append(Paragraph("Flipkart Growth<br/>Strategy Guide", COVER_TITLE))
story.append(Spacer(1, 0.6*cm))
story.append(Paragraph(f"Prepared for <b>{OWNER}</b>", COVER_SUB))
story.append(Paragraph(f"<b>{BIZ}</b>  ·  {CITY}", COVER_SUB))
story.append(Spacer(1, 0.4*cm))
story.append(Paragraph(f"{BIZ_TYPE}  ·  {DATE}", COVER_META))
story.append(Spacer(1, 5*cm))
story.append(rule(thickness=0.3, color=RULE, space_after=10))
story.append(Paragraph("growth.webotapp.com  ·  @growwithpaban", FTR))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════
# TABLE OF CONTENTS
# ══════════════════════════════════════════════════════════════════
story.append(Paragraph("Contents", H1))
story.append(rule(space_after=12))
toc = [
    ("Business Summary", "3"),
    ("Step 1 — Solve the Trust Problem First", "4"),
    ("Step 2 — Start Narrow, Expand Deliberately", "5"),
    ("Step 3 — Create Scarcity and Exclusivity", "6"),
    ("Step 4 — Fix Unit Economics Before Scaling", "7"),
    ("Step 5 — Build Your Brand Before You Need It", "8"),
    ("Step 6 — Build a Customer Database", "9"),
    ("Step 7 — Kill What Is Not Working", "10"),
    ("Step 8 — Know Your Legal and Financial Structure", "11"),
    ("Step 9 — Focus on the 20% That Drives 80%", "12"),
    ("Step 10 — Protect Your Equity and Vision", "13"),
    ("90-Day Quick-Start Roadmap", "14"),
    ("1-Year Task & Assignment Calendar", "15"),
    ("Investment Table", "17"),
]
for item, pg in toc:
    story.append(Table(
        [[Paragraph(item, TOC_IT), Paragraph(pg, TOC_PG)]],
        colWidths=[W - 1.5*cm, 1.5*cm],
        style=TableStyle([
            ('LINEBELOW', (0,0), (-1,-1), 0.2, RULE),
            ('ROWPADDING', (0,0), (-1,-1), 5),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ])
    ))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════
# BUSINESS SUMMARY
# ══════════════════════════════════════════════════════════════════
story.append(Paragraph("Business Summary", H1))
story.append(rule(space_after=10))
rows = [
    ("Owner",            OWNER),
    ("Business",         BIZ),
    ("Type",             BIZ_TYPE),
    ("Location",         CITY),
    ("Operating since",  YEARS),
    ("Team size",        TEAM),
    ("Monthly revenue",  REVENUE),
    ("Marketing budget", BUDGET),
    ("Primary goal",     GOAL),
    ("Biggest challenge",CHALLENGE),
    ("Target customer",  TARGET),
    ("Main competitors", COMPETITORS),
]
tdata = [[
    Paragraph(k, sty('TK','Helvetica-Bold',9,BLACK,leading=14)),
    Paragraph(v, sty('TV','Helvetica',9,BODY_C,leading=14)),
] for k,v in rows]
t = Table(tdata, colWidths=[4.5*cm, W - 4.5*cm])
t.setStyle(TableStyle([
    ('LINEBELOW', (0,0), (-1,-2), 0.2, RULE),
    ('ROWPADDING', (0,0), (-1,-1), 6),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
]))
story.append(t)
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════
# STEPS 1–10
# ══════════════════════════════════════════════════════════════════
steps = [
    (1, "Solve the Trust Problem First",
     "Cash-on-Delivery unlocked India — Flipkart removed the payment fear before anything else.",
     f"<b>{OWNER}</b>, a traveller booking with <b>{BIZ}</b> is spending Rs. 30,000–1,00,000+ on a trip they have never done before. The barrier is not price — it is trust. They fear losing money on an experience that does not match expectations. Northeast India travel is trust-first by nature, and your marketing must lead with evidence, not promises.",
     [
         "Publish a transparent cancellation and refund policy on your website and WhatsApp bio",
         "Share 5 real client testimonial videos from past Meghalaya and Assam trips on Instagram",
         "Show actual photos of accommodation, transport, and food that clients will experience — no stock imagery",
         f"Create a 'Real Experience Guarantee' statement for <b>{BIZ}</b> — visible on every client-facing touchpoint",
     ],
     f"Collect 3 WhatsApp testimonials from past travellers this week and post them as Instagram Stories."),

    (2, "Start Narrow, Expand Deliberately",
     "Flipkart sold only books for 2 years — half a million books — before expanding to electronics.",
     f"<b>{OWNER}</b>, <b>{BIZ}</b> has access to 8 states and dozens of destinations. But marketing all of them equally dilutes your brand to nothing. Flipkart's lesson is absolute: own one thing first. For a travel agency, this means owning one signature destination before expanding.",
     [
         "Designate Meghalaya as your flagship destination for the next 90 days based on past bookings",
         "All Instagram content, Reels, WhatsApp status: Meghalaya only for the next 90 days",
         f"Name your hero package something ownable: 'The Real Meghalaya Experience by <b>{BIZ}</b>'",
         "Once Meghalaya enquiries are consistent and converting, expand to Arunachal Pradesh as the second pillar",
     ],
     f"Update <b>{BIZ}</b>'s Instagram bio today: 'Northeast India's trusted travel partner — Meghalaya specialists.'"),

    (3, "Create Scarcity and Exclusivity",
     "Moto G flash sale sold 1,00,000 phones in a single day using urgency and limited availability.",
     f"<b>{OWNER}</b>, tour packages are one of the most natural products for scarcity marketing — group size is genuinely limited. <b>{BIZ}</b> can replicate the flash sale strategy directly. Most travel agencies let customers 'think about it' and lose them. The cure is structured urgency.",
     [
         "Launch a 'Only 8 seats — Meghalaya Monsoon Special' offer this week on WhatsApp and Instagram",
         "Create a WhatsApp-exclusive early bird rate: 'Book before [date] and save Rs. 3,000 per person'",
         f"Use an Instagram comment trigger: 'Comment MEGA to receive the <b>{BIZ}</b> Meghalaya package details in DM'",
         "Keep group size at 8–12 people genuinely — small group travel is a real differentiator worth pricing into",
     ],
     "Post an Instagram Story today: 'Only 5 seats left for our July Meghalaya trip. DM to book.'"),

    (4, "Fix Unit Economics Before Scaling",
     "Flipkart lost Rs. 45+ billion chasing GMV — scale without margin is just a bigger loss.",
     f"<b>{OWNER}</b>, before <b>{BIZ}</b> increases marketing spend, you must know exactly what you earn per confirmed booking after every direct cost. Travel agencies frequently undercharge because they forget to include their own time, follow-up hours, and the occasional refund or amendment.",
     [
         "Calculate net per package: Package price − Hotel − Transport − Guide − Your time − Ads = Net",
         "Set a minimum margin rule: never price a package below 25% net margin",
         "Stop offering discounts without calculating impact — a 10% discount on Rs. 50,000 is Rs. 5,000 lost per booking",
         "Track Cost Per Lead monthly: Ad spend ÷ Number of qualified enquiries. If it exceeds Rs. 500, fix the content before spending more",
     ],
     f"Write down <b>{BIZ}</b>'s last 3 confirmed bookings. Calculate actual net profit on each one today."),

    (5, "Build Your Brand Before You Need It",
     "Flipkart's Kids campaign was tested on Facebook organically — only then did they spend nationally.",
     f"<b>{OWNER}</b>, <b>{BIZ}</b> has the most visual product imaginable — the Northeast's landscapes, waterfalls, living root bridges, and tribal culture. Yet most travel agencies in the region look identical online. Your brand should make someone feel the trip before they ever enquire.",
     [
         "Post 3 Reels per week: one destination showcase, one face-forward travel tip from <b>Paban</b>, one past client story",
         "Your face is your brand — the audience books Paban's curation, not just the itinerary",
         "Consistent visual identity: choose 2 colours and one font across all posts using Canva Brand Kit (free)",
         "Add 'Northeast India travel expert' to every bio — establish authority, not just availability",
     ],
     "Record a 45-second Reel today: 'Why Meghalaya in July is unlike anywhere else — and most people miss it.'"),

    (6, "Build a Customer Database, Not Just an Audience",
     "Flipkart's flash sale registrations created an owned customer list they could market to directly.",
     f"<b>{OWNER}</b>, <b>{BIZ}</b>'s Instagram followers are a rented audience. A past traveller who books again is worth five times a cold enquiry. Your customer database — WhatsApp contacts, emails, enquiry records — is your most valuable and most overlooked business asset.",
     [
         "Create a WhatsApp Broadcast list of every past client and warm enquiry — start this today",
         "Offer a free 'Northeast India Travel Starter Guide' PDF in exchange for a WhatsApp number on Instagram",
         "Send a monthly WhatsApp status update: seasonal packages, new itineraries, limited slots",
         "Set up a simple Google Form enquiry page and place the link in every bio and story",
     ],
     f"Create a WhatsApp Broadcast list for <b>{BIZ}</b> today. Send one message: 'Hi, we have a new Meghalaya package ready. Reply YES for details.'"),

    (7, "Kill What Is Not Working",
     "Flipkart shut down Flyte, PayZippy, Nearby, and Ping fast — no ego about sunk costs.",
     f"<b>{OWNER}</b>, be honest about which activities at <b>{BIZ}</b> are generating real bookings versus which merely keep you occupied. Most travel agencies spread effort across platforms that never convert a single trip.",
     [
         "List every marketing activity. Mark each: does it generate direct enquiries or bookings? Yes or No",
         "If Facebook Page posts generate zero enquiries — stop. Redirect that time to Instagram Reels or WhatsApp",
         "If Google Ads cost exceeds Rs. 3,000 per confirmed booking — pause and fix the landing page first",
         "Track every enquiry source for 30 days: WhatsApp / Instagram DM / Google / Referral. Double down on the top source",
     ],
     "Stop one marketing activity this week that you do out of habit but cannot trace to a single booking."),

    (8, "Know Your Legal and Financial Structure",
     "Flipkart nearly faced a Rs. 1,400 crore FEMA fine — a legal blindspot that almost ended the company.",
     f"<b>{OWNER}</b>, as <b>{BIZ}</b> grows, financial and legal hygiene protects everything you are building. Most travel entrepreneurs ignore this until it becomes a crisis — at which point it costs far more to fix than to prevent.",
     [
         "Open a dedicated business current account for all Outdoor Backpacker transactions — fully separate from personal",
         "Register under GST if annual turnover is approaching or crossing Rs. 20 lakh",
         "Use a proper invoice format for every booking — both professional and tax-compliant",
         "Trademark 'Outdoor Backpacker' — brand theft in the travel niche is common and entirely preventable",
     ],
     f"Open a business current account for <b>{BIZ}</b> this week. Every rupee in and out must be trackable."),

    (9, "Focus on the 20% That Drives 80% of Revenue",
     "Kalyan used the Pareto principle to rescue Flipkart — concentrated resources on the categories generating most GMV.",
     f"<b>{OWNER}</b>, <b>{BIZ}</b> likely has 2–3 packages responsible for most bookings. Yet equal energy goes into promoting everything. The Pareto audit is the single most clarifying exercise you can do this quarter.",
     [
         "Identify your top 3 best-selling packages in the past 12 months — these receive 80% of your marketing attention",
         "Identify your top 10–15 repeat or referring clients — nurture them with exclusive early access and personal messages",
         "Identify your top 1–2 lead sources — invest more there, pause the rest",
         "Remove packages not booked in the past 6 months from all active marketing",
     ],
     f"This week: promote only your top 2 packages across every channel. Remove everything else from the bio link."),

    (10, "Protect Your Equity and Your Vision",
     "Sachin and Binny built India's largest e-commerce company — and both exited without choosing to.",
     f"<b>{OWNER}</b>, if <b>{BIZ}</b> cannot operate without you for 30 days, it is not a business — it is a job. The most important strategic move you can make in Year 2–3 is building systems that run independently of any single person, including yourself.",
     [
         "Write an SOP for: how we handle a new travel enquiry (step-by-step from first DM to booking confirmed)",
         "Write an SOP for: how we build a custom itinerary (checklist format, replicable by a team member)",
         "Train one team member or part-time assistant to handle WhatsApp enquiries using these SOPs",
         f"Your role at <b>{BIZ}</b> should be vision, product quality, and key relationships — not every WhatsApp reply",
     ],
     f"Write one SOP for <b>{BIZ}</b> today. Start with: 'When a customer contacts us, here is exactly what happens next.'"),
]

for n, title, lesson, body, actions, qw in steps:
    block = []
    # step number + title row — number on right, title left
    block.append(Table([[
        Paragraph(f"<b>{title}</b>", STEP_T),
        Paragraph(f"{n:02d}", STEP_N),
    ]], colWidths=[W - 2*cm, 2*cm],
    style=TableStyle([
        ('VALIGN',(0,0),(-1,-1),'BOTTOM'),
        ('ROWPADDING',(0,0),(-1,-1),0),
        ('LINEBELOW',(0,0),(-1,-1),0.5,BLACK),
    ])))
    block.append(Spacer(1, 5))
    block.append(Paragraph(f"Flipkart lesson — {lesson}", STEP_L))
    block.append(Paragraph(body, BODYJ))
    block.append(Paragraph("Actions", LABEL))
    for a in actions:
        block.append(Paragraph(f"— {a}", BULLET))
    block.append(Spacer(1, 5))
    block.append(Paragraph(f"Quick win  /  {qw}", QWIN))
    block.append(Spacer(1, 10))
    story.append(KeepTogether(block[:4]))  # keep header + body together
    story.extend(block[4:])
    story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════
# 90-DAY ROADMAP
# ══════════════════════════════════════════════════════════════════
story.append(Paragraph("90-Day Quick-Start Roadmap", H1))
story.append(rule(space_after=14))
for period, tasks in [
    ("Month 1 — Fix & Build Trust", [
        f"Implement trust mechanism for <b>{BIZ}</b>: refund policy + 5 testimonial posts (Step 1)",
        "Designate Meghalaya as flagship destination — all content pivots here (Step 2)",
        "Launch 'Only 8 seats' flash offer on WhatsApp and Instagram (Step 3)",
        f"Calculate unit economics on top 3 <b>{BIZ}</b> packages (Step 4)",
        "Create WhatsApp Broadcast list of all past clients (Step 6)",
    ]),
    ("Month 2 — Visibility & Consistency", [
        "Post 3× per week: one Reel, one Story, one carousel (Step 5)",
        f"Launch face-forward video: <b>Paban</b> explains why to choose <b>{BIZ}</b>",
        "Kill one non-converting channel — redirect that time to WhatsApp (Step 7)",
        "Run the 80/20 audit: top packages, top clients, top lead source (Step 9)",
        "Target 10 new Google reviews this month using the request template",
    ]),
    ("Month 3 — Systemise & Scale", [
        f"Write 3 SOPs for <b>{BIZ}</b>: enquiry handling, itinerary building, client follow-up (Step 10)",
        "Business bank account + GST registration check (Step 8)",
        "Review Month 1–2 data: double down on what is working (Step 7)",
        "Launch free lead magnet: Northeast India Travel Starter Guide PDF (Step 6)",
        f"Set <b>{BIZ}</b>'s Q2 marketing budget allocation by channel (Step 4)",
    ]),
]:
    story.append(Paragraph(period, H2))
    for t in tasks:
        story.append(Paragraph(f"— {t}", BULLET))
    story.append(Spacer(1, 6))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════
# 1-YEAR TASK CALENDAR
# ══════════════════════════════════════════════════════════════════
story.append(Paragraph("1-Year Task & Assignment Calendar", H1))
story.append(Paragraph(
    f"A week-by-week operating rhythm for <b>{OWNER}</b> and the <b>{BIZ}</b> team "
    "across 12 months. Each task maps to one of the 10 strategy steps.",
    BODY))
story.append(rule(space_before=8, space_after=10))

CAL_H = sty('CH','Helvetica-Bold', 8, BLACK, leading=11)
CAL_B = sty('CB','Helvetica',      8, BODY_C, leading=12)
CAL_M = sty('CM2','Helvetica',     8, MUTED, leading=11)

def cr(period, task, owner, freq, kpi):
    return [Paragraph(period, CAL_M), Paragraph(task, CAL_B),
            Paragraph(owner, CAL_M), Paragraph(freq, CAL_M), Paragraph(kpi, CAL_M)]

hdr = [Paragraph(h, CAL_H) for h in ['Period','Task / Assignment','Owner','Freq.','KPI']]
cal = [hdr,
  cr('Jan Wk 1', f'Collect 5 client testimonials + post on Instagram', OWNER, 'Once', '5 posts live'),
  cr('Jan Wk 2', 'Unit economics check on top 3 packages', OWNER, 'Once', 'Profit per pkg known'),
  cr('Jan Wk 3', 'Flash offer: "8 seats — Meghalaya Jan trip"', OWNER, 'Once', '10+ enquiries'),
  cr('Jan Wk 4', 'WhatsApp Broadcast list from all past clients', OWNER, 'Once', '50+ contacts'),
  cr('Feb Wk 1', 'Post 3× / week — Reel + Story + carousel', f'{OWNER} / Team', 'Weekly', '10% reach growth'),
  cr('Feb Wk 2', 'Ask 10 past clients for a Google review', OWNER, 'Weekly', '5+ new reviews'),
  cr('Feb Wk 3', 'Kill one non-converting marketing channel', OWNER, 'Once', 'Time + budget freed'),
  cr('Feb Wk 4', 'Write SOP: How we handle a new travel enquiry', OWNER, 'Once', 'Doc saved + shared'),
  cr('Mar Wk 1', 'Update Google Business Profile — photos + packages', f'{OWNER} / Team', 'Once', 'Profile 100% complete'),
  cr('Mar Wk 2', '80/20 audit — top packages, clients, lead sources', OWNER, 'Once', 'Audit report written'),
  cr('Mar Wk 3', 'Create free lead magnet: NE India Starter Guide PDF', f'{OWNER} / Team', 'Once', 'Magnet live on bio'),
  cr('Mar Wk 4', 'Q1 review — what worked, what to stop, what to scale', OWNER, 'Once', 'Q2 plan written'),
  cr('Apr Wk 1', 'Face-forward Reel: "Why I started Outdoor Backpacker"', OWNER, 'Once', '1,000+ views'),
  cr('Apr Wk 2', 'Add WhatsApp follow-up sequence for cold leads', f'{OWNER} / Team', 'Once', 'Sequence active'),
  cr('Apr Wk 3', 'Summer offer: Meghalaya pre-monsoon package', OWNER, 'Once', '5+ bookings'),
  cr('Apr Wk 4', 'WhatsApp broadcast: seasonal update to all contacts', OWNER, 'Monthly', '20%+ response rate'),
  cr('May Wk 1', 'Referral campaign: "Refer a friend — get Rs. 2,000 off"', OWNER, 'Once', '5+ referrals'),
  cr('May Wk 2', 'Pricing review: is every package at 25%+ margin?', OWNER, 'Once', 'Margins documented'),
  cr('May Wk 3', 'Educational Reel: "5 things no one tells about Meghalaya"', f'{OWNER} / Team', 'Weekly', 'Saves tracked'),
  cr('May Wk 4', 'GST check + trademark application (Step 8)', f'{OWNER} / CA', 'Once', 'Compliance complete'),
  cr('Jun Wk 1', 'Monsoon special — limited 10-seat group tour', OWNER, 'Once', 'Sold-out target'),
  cr('Jun Wk 2', 'Survey 10 clients: why did you choose Outdoor Backpacker?', OWNER, 'Once', 'Insights documented'),
  cr('Jun Wk 3', 'Write SOPs: itinerary build + client onboarding', f'{OWNER} / Team', 'Once', '2 docs saved'),
  cr('Jun Wk 4', 'H1 review + H2 strategy + full budget plan', OWNER, 'Once', 'H2 plan ready'),
  cr('Jul Wk 1', 'Launch VIP repeat-traveller club — early access', OWNER, 'Once', '20+ enrolled'),
  cr('Jul Wk 2', 'Competitor audit: what are Jungle Travels / 7 Sisters doing?', OWNER, 'Once', 'Gap list created'),
  cr('Jul Wk 3', 'Start YouTube / LinkedIn: "Paban explores NE India" series', OWNER, 'Ongoing', '4 videos live'),
  cr('Jul Wk 4', 'Update website + GMB: monsoon photos + new packages', f'{OWNER} / Team', 'Monthly', 'Content refreshed'),
  cr('Aug Wk 1', 'A/B test 2 Reel formats — compare saves and enquiries', f'{OWNER} / Team', 'Once', 'Winner identified'),
  cr('Aug Wk 2', 'Partner with 2 NE India photographers or bloggers', OWNER, 'Once', '2 collabs confirmed'),
  cr('Aug Wk 3', 'Client case study: document one epic trip with story', f'{OWNER} / Team', 'Once', 'Published on Instagram'),
  cr('Aug Wk 4', 'Review ad spend ROI — pause weak, scale winning ads', OWNER, 'Monthly', 'ROAS logged'),
  cr('Sep Wk 1', 'Durga Puja / winter campaign creatives ready', f'{OWNER} / Team', 'Once', 'Campaign live Oct 1'),
  cr('Sep Wk 2', 'Reach 100 Google reviews milestone', OWNER, 'Ongoing', '100 reviews achieved'),
  cr('Sep Wk 3', 'Train assistant on WhatsApp enquiry SOP', OWNER, 'Once', 'Team handles enquiries'),
  cr('Sep Wk 4', 'Q3 review + adjust Q4 plan based on data', OWNER, 'Once', 'Q4 plan ready'),
  cr('Oct Wk 1', 'Diwali / winter trip flash offer — 10 seats only', OWNER, 'Once', 'Best revenue week'),
  cr('Oct Wk 2', 'Re-engagement: message lapsed clients from past 6 months', OWNER, 'Once', '10%+ response rate'),
  cr('Oct Wk 3', 'Outsource one daily task — content editing or scheduling', OWNER, 'Once', '5+ hrs / week freed'),
  cr('Oct Wk 4', 'Behind-the-scenes brand video: a day at Outdoor Backpacker', OWNER, 'Once', '1,000+ views'),
  cr('Nov Wk 1', 'Cut bottom 20% of marketing activities by ROI', OWNER, 'Once', 'Efficiency improved'),
  cr('Nov Wk 2', 'Create 2026 content calendar: monthly themes + festivals', f'{OWNER} / Team', 'Once', 'Calendar finalised'),
  cr('Nov Wk 3', 'Annual client satisfaction survey — top 20 clients', OWNER, 'Once', 'NPS score tracked'),
  cr('Nov Wk 4', 'Hiring / outsourcing plan: who does the team need next?', OWNER, 'Once', 'Plan documented'),
  cr('Dec Wk 1', 'Year-end offer: reward VIP and repeat travellers', OWNER, 'Once', '30%+ repeat purchase'),
  cr('Dec Wk 2', 'Document all 2025 learnings in one master file', OWNER, 'Once', 'Learning doc saved'),
  cr('Dec Wk 3', 'Set 2026 revenue target + marketing budget allocation', OWNER, 'Once', 'Annual plan ready'),
  cr('Dec Wk 4', 'Full year review: results vs January goals', OWNER, 'Once', 'Growth % calculated'),
]
cw = [1.7*cm, 7.9*cm, 2.4*cm, 1.4*cm, 2.6*cm]
ct = Table(cal, colWidths=cw)
ct.setStyle(TableStyle([
    ('LINEBELOW', (0,0), (-1,0), 0.6, BLACK),
    ('LINEBELOW', (0,1), (-1,-1), 0.2, RULE),
    ('ROWPADDING', (0,0), (-1,-1), 5),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    # subtle quarter separators
    ('LINEABOVE', (0,13), (-1,13), 0.4, RULE),
    ('LINEABOVE', (0,25), (-1,25), 0.4, RULE),
    ('LINEABOVE', (0,37), (-1,37), 0.4, RULE),
]))
story.append(ct)
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════
# INVESTMENT TABLE
# ══════════════════════════════════════════════════════════════════
story.append(Paragraph("Estimated Investment", H1))
story.append(rule(space_after=12))
inv_h = sty('IH','Helvetica-Bold',9,BLACK,leading=13)
inv_b = sty('IB','Helvetica',     9,BODY_C,leading=13)
inv_m = sty('IM','Helvetica',     9,MUTED, leading=13)
inv_data = [
    [Paragraph(h, inv_h) for h in ['Activity','DIY (Free)','Rs. 5K–20K / mo','Rs. 20K–50K / mo']],
    *[[Paragraph(a, inv_b), Paragraph(b, inv_m), Paragraph(c, inv_m), Paragraph(d, inv_m)]
      for a,b,c,d in [
        ('Instagram Reels + content',     'Self-made',        'Freelance editor',     'Content + paid ads'),
        ('WhatsApp broadcast / CRM',      'Manual lists',     'Zoko / Interakt',      'Full automation'),
        ('Google Business Profile',       'Free setup',       'Basic management',     'Active + posts'),
        ('Paid ads — Meta / Google',      '—',                'Rs. 5K–10K spend',     'Rs. 15K–30K spend'),
        ('Website / landing page',        'Canva Sites',      'Basic WordPress',      'Custom + SEO'),
        ('Lead magnet / travel guide',    'Free (Canva)',      'Designed + written',   'Full funnel setup'),
        ('Monthly strategy review',       'Self-directed',    'Freelance consultant', 'Agency retainer'),
    ]]
]
it = Table(inv_data, colWidths=[5.5*cm, 3.4*cm, 3.4*cm, 3.7*cm])
it.setStyle(TableStyle([
    ('LINEBELOW', (0,0), (-1,0), 0.6, BLACK),
    ('LINEBELOW', (0,1), (-1,-1), 0.2, RULE),
    ('ROWPADDING', (0,0), (-1,-1), 6),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
]))
story.append(it)

# ── Final footer ──────────────────────────────────────────────────
story.append(Spacer(1, 1.8*cm))
story.append(rule(thickness=0.4, color=BLACK, space_after=10))
story.append(Paragraph(
    f"Prepared for <b>{OWNER}</b>  ·  <b>{BIZ}</b>  ·  {DATE}",
    sty('F1','Helvetica-Bold',9,BLACK,leading=13,align=TA_CENTER)))
story.append(Paragraph(
    "growth.webotapp.com  ·  @growwithpaban  ·  webotapp.com",
    FTR))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph(
    "This guide applies the 10 lessons from Flipkart's growth story to your business. "
    "Results depend on consistent implementation over 90+ days. "
    "Want this skill customised for your agency? Visit growth.webotapp.com",
    sty('DI','Helvetica-Oblique',8,MUTED,leading=12,align=TA_CENTER)))

doc.build(story, canvasmaker=NumberedCanvas)
print("PDF created:", OUTPUT)
