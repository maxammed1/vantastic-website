"""Generates the Vantastic Transit static pages. Run: python3 tools/build_site.py"""
import json, pathlib
OUT = pathlib.Path(__file__).resolve().parent.parent
DOMAIN = "https://vantastictransit.net"
PHONE, TEL = "(507) 272-4901", "+15072724901"
EMAIL = "info@vantastictransit.net"
ADDR = "117 S Washington St, Suite 106, Lake City, MN 55041"
TOWNS = ["Lake City", "Wabasha", "Plainview", "Kellogg", "Winona", "St. Charles", "Lewiston", "Rochester trips"]

VAN = """<svg viewBox="0 0 320 170" role="img" aria-label="Wheelchair accessible van"><rect x="10" y="40" width="250" height="92" rx="16" fill="#fff"/><path d="M260 62h22c10 0 18 6 22 15l8 20v24c0 6-5 11-11 11h-41z" fill="#fff"/><rect x="24" y="54" width="52" height="30" rx="5" fill="#9fd6d3"/><rect x="86" y="54" width="52" height="30" rx="5" fill="#9fd6d3"/><rect x="148" y="54" width="52" height="30" rx="5" fill="#9fd6d3"/><path d="M268 70h16c5 0 9 3 11 7l6 14h-33z" fill="#9fd6d3"/><rect x="10" y="100" width="300" height="8" fill="#f2b134"/><circle cx="70" cy="134" r="20" fill="#12355b"/><circle cx="70" cy="134" r="8" fill="#cfd8e3"/><circle cx="250" cy="134" r="20" fill="#12355b"/><circle cx="250" cy="134" r="8" fill="#cfd8e3"/><g transform="translate(205 52)" fill="none" stroke="#12355b" stroke-width="4" stroke-linecap="round"><circle cx="20" cy="7" r="5" fill="#12355b" stroke="none"/><path d="M20 14v16h14l6 14"/><path d="M14 22a14 14 0 1 0 18 18"/></g></svg>"""

def head(title, desc, path, extra=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{DOMAIN}{path}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Vantastic Transit">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{DOMAIN}{path}">
<meta name="theme-color" content="#12355b">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&family=Outfit:wght@600;800&display=swap">
<link rel="stylesheet" href="/styles.css?v=1">
{extra}</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap header-inner">
  <a class="brand" href="/"><img src="/favicon.svg" alt="" width="40" height="40"><span>Vantastic Transit<small>Lake City, Minnesota</small></span></a>
  <nav aria-label="Main"><a class="hide-sm" href="/#services">Rides</a><a class="hide-sm" href="/facilities/">Hospitals &amp; care homes</a><a class="hide-sm" href="/drive/">Drive with us</a>
  <a class="btn btn-call" href="tel:{TEL}"><span aria-hidden="true">📞</span> {PHONE}</a></nav>
</div></header>
<main id="main">
"""

FOOT = f"""</main>
<footer class="site-footer"><div class="wrap foot-grid">
  <div><strong>Vantastic Transit LLC</strong><br>{ADDR}<br><a href="tel:{TEL}">{PHONE}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a><br>Office hours: Monday to Friday, 8 AM to 5 PM</div>
  <div><strong>Serving</strong><br>Wabasha and Winona counties: {", ".join(TOWNS[:-1])}, with trips to Rochester, Red Wing and La Crosse.</div>
  <div><strong>Pages</strong><br><a href="/#request">Book a ride</a> · <a href="/facilities/">For hospitals and care homes</a> · <a href="/drive/">Drive with us</a></div>
</div><p class="wrap small">© 2026 Vantastic Transit LLC</p></footer>
<script src="/form.js" defer></script>
</body>
</html>
"""

def field(label, name, kind="text", req=False, auto="", opts=None, full=False):
    r = " required" if req else ""
    star = ' <span aria-hidden="true">*</span>' if req else ""
    cls = ' class="full"' if full else ""
    if opts:
        o = "".join(f"<option>{x}</option>" for x in opts)
        return f'<label{cls}><span>{label}{star}</span><select name="{name}"{r}><option value="">Choose one</option>{o}</select></label>'
    if kind == "textarea":
        return f'<label class="full"><span>{label}{star}</span><textarea name="{name}" rows="4"{r}></textarea></label>'
    a = f' autocomplete="{auto}"' if auto else ""
    return f'<label{cls}><span>{label}{star}</span><input type="{kind}" name="{name}"{a}{r}></label>'

def form(kind, title, fields, button, anchor):
    hp = '<label class="hp" aria-hidden="true">Leave this empty<input name="website" tabindex="-1" autocomplete="off"></label>'
    return f"""<form class="lead-form card" id="{anchor}" action="/api/request" method="post">
<h2>{title}</h2>
<input type="hidden" name="kind" value="{kind}">
<div class="grid2">
{field("Your name","name",req=True,auto="name")}
{field("Phone","phone","tel",True,"tel")}
{field("Email (optional)","email","email",auto="email",full=True)}
{"".join(fields)}
</div>{hp}
<button class="btn btn-primary" type="submit">{button}</button>
<p class="form-status" role="status" aria-live="polite"></p>
<p class="small">Or call <a href="tel:{TEL}">{PHONE}</a>. We call you back the same business day.</p>
</form>"""

LB = {
 "@context":"https://schema.org","@type":"LocalBusiness","additionalType":"https://schema.org/MedicalBusiness",
 "@id":f"{DOMAIN}/#business","name":"Vantastic Transit","url":f"{DOMAIN}/","telephone":TEL,"email":EMAIL,
 "logo":f"{DOMAIN}/favicon.svg",
 "address":{"@type":"PostalAddress","streetAddress":"117 S Washington St, Suite 106","addressLocality":"Lake City","addressRegion":"MN","postalCode":"55041","addressCountry":"US"},
 "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"08:00","closes":"17:00"}],
 "areaServed":["Lake City, MN","Wabasha, MN","Plainview, MN","Winona, MN","St. Charles, MN","Wabasha County, MN","Winona County, MN"],
 "description":"Wheelchair-accessible van rides and rides to medical appointments in Wabasha and Winona counties, Minnesota, including trips to Rochester."}
FAQ = [
 ("Do you take wheelchairs?","Yes. Our vans have a ramp or lift and wheelchair tie-downs, and our drivers help you on and off."),
 ("Where do you go?","We pick up in Lake City, Wabasha, Plainview, Kellogg, Winona, St. Charles, Lewiston and nearby towns, and drive to appointments locally and in Rochester, Red Wing and La Crosse."),
 ("How do I pay?","You can pay yourself, or a hospital, care home, workers' comp or other program may pay for the ride. Call us and we'll tell you the price before you book."),
 ("Do you take Medical Assistance?","Call us and ask. We'll tell you whether your ride can be covered and how to set it up."),
 ("How far ahead should I book?","Two business days is best. Call us for same-day rides, like a ride home from the hospital, and we'll do our best."),
 ("Can someone ride with me?","Yes. A family member or helper can ride along. Tell us when you book."),
]
FAQLD = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]}
ld = lambda o: f'<script type="application/ld+json">{json.dumps(o, indent=1)}</script>\n'

ride_fields = [
 field("Type of ride","ride_type",opts=["Wheelchair van","Ride to an appointment (no wheelchair)","Ride home from the hospital","Dialysis (regular rides)","Airport","Other"]),
 field("Wheelchair?","wheelchair",opts=["Yes, I stay in my wheelchair","I can walk with help","No wheelchair"]),
 field("Pick-up town","pickup",auto="address-level2"),
 field("Going to (clinic or address)","dropoff"),
 field("Date and time","when"),
 field("Round trip?","round_trip",opts=["Yes, round trip","One way"]),
 field("How will the ride be paid?","payer",opts=["I'll pay myself","Hospital or care home","Workers' comp","VA","Medical Assistance / health plan","Not sure"],full=True),
 field("Anything we should know?","message","textarea"),
]
home = head("Vantastic Transit | Wheelchair Van & Medical Rides, Lake City MN",
  f"Wheelchair-accessible van rides and rides to medical appointments in Lake City, Wabasha, Plainview and Winona, including trips to Rochester. Call {PHONE}.", "/", ld(LB)+ld(FAQLD)) + f"""
<section class="hero"><div class="wrap hero-grid">
<div><p class="kicker">Lake City · Wabasha · Winona · trips to Rochester</p>
<h1>Safe rides to your appointments, wheelchair or not</h1>
<p class="lead">Vantastic Transit drives older adults and people with disabilities to the doctor, dialysis, therapy and back home from the hospital. Door to door, with a driver who helps.</p>
<p class="cta"><a class="btn btn-primary" href="#request">Book a ride</a> <a class="btn btn-ghost" href="tel:{TEL}">Call {PHONE}</a></p></div>
<div class="hero-art">{VAN}</div></div></section>

<section id="services" class="wrap section"><h2>Rides we give</h2>
<div class="cards">
<article class="card"><h3>Wheelchair van rides</h3><p>Ramp or lift, secure tie-downs. Stay in your own wheelchair the whole trip.</p></article>
<article class="card"><h3>Medical appointments</h3><p>Doctor visits, therapy, cancer treatment and tests, locally or at Mayo Clinic in Rochester.</p></article>
<article class="card"><h3>Dialysis rides</h3><p>The same pick-up time every week, so you never worry about getting there.</p></article>
<article class="card"><h3>Home from the hospital</h3><p>Hospital or care home ready to send you home? Call us for a same-day ride.</p></article>
<article class="card"><h3>Airport and longer trips</h3><p>Rides to Rochester (RST) and Minneapolis (MSP) airports and family visits.</p></article>
<article class="card"><h3>Group outings</h3><p>Care homes and senior groups: shopping trips and outings in one van.</p></article>
</div></section>

<section class="band"><div class="wrap steps"><div><span>1</span><h3>Call or fill the form</h3><p>Tell us where and when.</p></div><div><span>2</span><h3>Get your price</h3><p>We confirm the time and price before the ride.</p></div><div><span>3</span><h3>Ride door to door</h3><p>Your driver helps you in, out and to the door.</p></div></div></section>

<section class="wrap section two-col">
<div><h2>Where we drive</h2><p>We're based at {ADDR}. We pick up in:</p><ul class="towns">{"".join(f"<li>{t}</li>" for t in TOWNS)}</ul>
<h2>Questions</h2><div class="faq">{"".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q,a in FAQ)}</div></div>
<div>{form("ride","Book a ride",ride_fields,"Send ride request","request")}</div>
</section>

<section class="band band-accent"><div class="wrap split"><div><h2>Hospitals, clinics and care homes</h2><p>One number for discharges, a monthly account for your residents, and one invoice.</p></div><a class="btn btn-dark" href="/facilities/">Set up an account</a></div></section>
""" + FOOT

fac_fields = [
 field("Organization","organization",req=True,auto="organization",full=True),
 field("Your role","role",opts=["Discharge planner / case manager","Social worker","Care home or assisted living staff","Clinic staff","County or program staff","Other"]),
 field("About how many rides a month?","volume",opts=["1-5","6-20","21-50","More than 50"]),
 field("What do you need?","message","textarea"),
]
fac = head("Rides for Hospitals & Care Homes | Vantastic Transit",
  "Wheelchair van and medical rides for discharge planners, care homes, dialysis units and clinics in Wabasha and Winona counties. Monthly accounts, one invoice.", "/facilities/") + f"""
<section class="hero hero-sm"><div class="wrap"><p class="kicker">For hospitals, clinics, dialysis units and care homes</p>
<h1>A ride partner you can call once</h1>
<p class="lead">Discharge planners, social workers and care home staff use Vantastic to get patients and residents where they need to go, in a wheelchair van or a regular seat.</p></div></section>
<section class="wrap section two-col">
<div><h2>What you get</h2><ul class="checks">
<li><b>Discharge rides:</b> call in the morning, ride home that day when a van is open.</li>
<li><b>Standing rides:</b> dialysis and therapy on a fixed weekly schedule.</li>
<li><b>Monthly account:</b> one invoice for all your residents' trips.</li>
<li><b>Rochester days:</b> group Mayo appointments on the same van.</li>
<li><b>Trained drivers</b> with background studies, and inspected, insured vans.</li>
<li><b>Trip records</b> for every ride: pick-up, drop-off and times.</li></ul>
<p>Prices are set before the ride. Ask us for our rate sheet.</p></div>
<div>{form("facility","Set up an account",fac_fields,"Send","account")}</div></section>
""" + FOOT

drv_fields = [
 field("Town you live in","town",auto="address-level2"),
 field("Years with a driver's license","license_years",opts=["Less than 3","3-5","More than 5"]),
 field("When can you drive?","availability",opts=["Full time","Part time weekdays","Early mornings","Saturdays","On call"],full=True),
 field("Tell us about you","message","textarea"),
]
drv = head("Drive With Us | Vantastic Transit, Lake City MN",
  "Drive a wheelchair-accessible van for Vantastic Transit in Lake City, Wabasha and Winona. Help neighbors get to their appointments.", "/drive/") + f"""
<section class="hero hero-sm"><div class="wrap"><p class="kicker">Jobs in Lake City, Wabasha and Winona</p>
<h1>Drive with Vantastic</h1>
<p class="lead">Help your neighbors get to the doctor and home safely. We train you on wheelchair loading and safety.</p></div></section>
<section class="wrap section two-col">
<div><h2>What we look for</h2><ul class="checks"><li>Valid driver's license and a clean driving record</li><li>Patient, kind and on time</li><li>Able to pass a background study</li><li>Comfortable helping riders in and out of the van</li></ul></div>
<div>{form("driver","Apply to drive",drv_fields,"Send application","apply")}</div></section>
""" + FOOT

thanks = head("Thank you | Vantastic Transit","We got your message.","/thanks/",'<meta name="robots" content="noindex">\n') + f"""
<section class="hero hero-sm"><div class="wrap"><h1>Thank you. We got it.</h1><p class="lead">We'll call you back the same business day. Need us sooner? Call <a href="tel:{TEL}">{PHONE}</a>.</p><p><a class="btn btn-primary" href="/">Back to home</a></p></div></section>
""" + FOOT
nf = head("Page not found | Vantastic Transit","Page not found.","/404",'<meta name="robots" content="noindex">\n') + f"""
<section class="hero hero-sm"><div class="wrap"><h1>We can't find that page</h1><p class="lead">Go to the <a href="/">home page</a> or call <a href="tel:{TEL}">{PHONE}</a>.</p></div></section>
""" + FOOT

for p, h in {"index.html": home, "facilities/index.html": fac, "drive/index.html": drv, "thanks/index.html": thanks, "404.html": nf}.items():
    (OUT / p).parent.mkdir(parents=True, exist_ok=True)
    (OUT / p).write_text(h)
(OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{DOMAIN}{p}</loc></url>\n" for p in ["/", "/facilities/", "/drive/"]) + "</urlset>\n")
(OUT / "llms.txt").write_text(f"# Vantastic Transit\n\nWheelchair-accessible van rides and rides to medical appointments, based in Lake City, Minnesota.\nServes Wabasha and Winona counties (Lake City, Wabasha, Plainview, Kellogg, Winona, St. Charles, Lewiston) with trips to Rochester, Red Wing and La Crosse.\nPhone: {PHONE}. Email: {EMAIL}. Address: {ADDR}. Office hours Monday to Friday, 8 AM to 5 PM.\n\n- Home and ride booking: {DOMAIN}/\n- Hospitals and care homes: {DOMAIN}/facilities/\n- Driver jobs: {DOMAIN}/drive/\n")
print("built")
