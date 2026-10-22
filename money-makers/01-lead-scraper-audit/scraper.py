"""
Local Business Lead Scraper & Digital Audit Engine
Includes Direct 1-Click WhatsApp & Email Outreach
"""

import csv
import json
import os
import sys
import urllib.parse

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

DATA_FILE = os.path.join(os.path.dirname(__file__), "leads_database.csv")
OUTPUT_HTML = os.path.join(os.path.dirname(__file__), "audit_report.html")

def calculate_opportunity_score(lead):
    score = 0
    reasons = []

    has_site = bool(lead.get("website", "").strip())
    reviews = int(lead.get("reviews_count", 0))
    rating = float(lead.get("google_rating", 0.0))
    has_ssl = lead.get("has_ssl", "False").lower() == "true"
    mobile_friendly = lead.get("mobile_friendly", "False").lower() == "true"
    instagram = lead.get("instagram_handle", "").strip()

    if not has_site:
        score += 50
        reasons.append("⚠️ NO WEBSITE: Completely invisible on Google Maps searches")
    else:
        if not has_ssl:
            score += 20
            reasons.append("🔒 NO SSL: Browser marks website as 'Not Secure'")
        if not mobile_friendly:
            score += 20
            reasons.append("📱 NOT MOBILE FRIENDLY: Broken navigation on smartphones")

    if reviews >= 50 and rating >= 4.5:
        score += 25
        reasons.append(f"⭐ TOP REPUTATION ({rating}★ / {reviews} reviews): High volume, ready to pay")
    elif reviews >= 20:
        score += 15
        reasons.append(f"👍 ESTABLISHED ({rating}★ / {reviews} reviews)")

    if not instagram:
        score += 5
        reasons.append("📸 MISSING SOCIALS: Can bundle Web + Social setup")

    return min(score, 100), reasons

def generate_cold_pitch_email(lead, reasons):
    name = lead.get("business_name")
    category = lead.get("category")
    city = lead.get("city")
    rating = lead.get("google_rating")
    reviews = lead.get("reviews_count")
    has_site = bool(lead.get("website", "").strip())

    if not has_site:
        subject = f"Quick question regarding {name}'s website in {city}"
        body = f"""Hi {name} Team,

I came across your business while looking up top-rated {category} services in {city}. Huge congratulations on your {rating}★ rating across {reviews} Google reviews—that shows you deliver great work!

However, I noticed you don't currently have an official website linked to your Google Business Profile. Right now, potential customers searching for {category} in {city} might be bouncing to competitors simply because there's no fast way to view your services or book an appointment online.

I put together a clean 1-page demo site specifically tailored for {name} with an instant booking button and mobile-ready layout.

Would you be open to a 2-minute video walkthrough showing how it looks? No pressure or sales pitch whatsoever.

Best regards,
Joseph | Web & Digital Growth
"""
        whatsapp_msg = f"Hi {name} Team! I noticed your awesome {rating}★ rating on Google in {city}. I put together a quick modern 1-page website demo for {name} to help bring in more local customers. Can I share a 1-minute video showing how it looks?"
    else:
        subject = f"Quick question regarding {name}'s website ({city})"
        body = f"""Hi {name} Team,

I recently visited your site ({lead.get('website')}) while searching top {category} businesses in {city}. You clearly have strong customer trust with {rating}★ across {reviews} reviews!

I noticed a couple of quick technical fixes that could immediately boost your customer conversions:
- The site currently lacks an active SSL certificate (browsers show "Not Secure" to visitors)
- It's not fully optimized for mobile devices, which makes booking or calling tricky on smartphones.

I created a clean mockup showing how {name} would look with a modern, high-speed design and 1-click calling.

Can I send over a quick screenshot comparison?

Best regards,
Joseph | Web Developer
"""
        whatsapp_msg = f"Hi {name} Team! I saw your {category} service in {city} with {rating}★ on Google. I noticed a quick fix on your website that could help you convert more mobile visitors. Can I send over a quick 30-second tip?"

    return subject, body, whatsapp_msg

def run_audit():
    with open(DATA_FILE, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        leads = list(reader)

    audited = []
    for lead in leads:
        score, reasons = calculate_opportunity_score(lead)
        subj, email_body, wa_msg = generate_cold_pitch_email(lead, reasons)
        audited.append({
            "lead": lead,
            "score": score,
            "reasons": reasons,
            "email_subject": subj,
            "email_body": email_body,
            "wa_msg": wa_msg
        })

    html_cards = ""
    for item in sorted(audited, key=lambda x: x["score"], reverse=True):
        l = item["lead"]
        reasons_html = "".join([f"<li>{r}</li>" for r in item["reasons"]])
        badge_color = "#10b981" if item["score"] >= 75 else "#f59e0b"
        
        # URL Encoded links
        clean_phone = l['phone'].replace("+", "").replace("-", "").replace(" ", "")
        wa_url = f"https://api.whatsapp.com/send?phone={clean_phone}&text={urllib.parse.quote(item['wa_msg'])}"
        mailto_url = f"mailto:{l['email']}?subject={urllib.parse.quote(item['email_subject'])}&body={urllib.parse.quote(item['email_body'])}"

        html_cards += f"""
        <div class="lead-card">
            <div class="lead-header">
                <div>
                    <h3>{l['business_name']}</h3>
                    <p class="category">{l['category']} • {l['city']}</p>
                    <p class="contact-line">
                        <span>✉️ <strong>{l['email']}</strong></span> • 
                        <span>📞 <strong>{l['phone']}</strong></span>
                    </p>
                </div>
                <div class="score-badge" style="background:{badge_color}">
                    <span>{item['score']}</span>
                    <small>Opportunity</small>
                </div>
            </div>

            <div class="stats-row">
                <span>⭐ <strong>{l['google_rating']}★</strong> ({l['reviews_count']} reviews)</span>
                <span>🌐 {l['website'] if l['website'] else '<strong style=\"color:#ef4444\">NO WEBSITE</strong>'}</span>
            </div>

            <ul class="reasons-list">
                {reasons_html}
            </ul>

            <div class="action-buttons-bar">
                <a href="{wa_url}" target="_blank" class="contact-btn wa-btn">
                    <i class="fa-brands fa-whatsapp"></i> 1-Click WhatsApp Chat
                </a>
                <a href="{mailto_url}" class="contact-btn email-btn">
                    <i class="fa-solid fa-paper-plane"></i> 1-Click Send Email
                </a>
                <button class="contact-btn copy-btn" onclick="copyPitch(this, `{item['email_subject']}`, `{item['email_body'].replace('`', "'")}`)">
                    <i class="fa-solid fa-copy"></i> Copy Full Email
                </button>
            </div>

            <div class="email-preview">
                <div class="email-subject">Subject: {item['email_subject']}</div>
                <pre>{item['email_body']}</pre>
            </div>
        </div>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Local Business Outreach & Direct Contacts</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        * {{ box-sizing: border-box; margin:0; padding:0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0b1120; color: #f8fafc; padding: 2rem 1rem; }}
        .container {{ max-width: 960px; margin: 0 auto; }}
        header {{ margin-bottom: 2rem; text-align: center; }}
        h1 {{ font-size: 2.2rem; color: #38bdf8; margin-bottom: 0.5rem; }}
        p.subtitle {{ color: #94a3b8; font-size: 1.05rem; }}
        .lead-card {{ background: #1e293b; border: 1px solid #334155; border-radius: 14px; padding: 1.75rem; margin-bottom: 2rem; box-shadow: 0 10px 25px rgba(0,0,0,0.3); }}
        .lead-header {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem; flex-wrap: wrap; gap: 1rem; }}
        .lead-header h3 {{ font-size: 1.5rem; color: #f1f5f9; }}
        .category {{ color: #94a3b8; font-size: 0.95rem; margin-top: 0.25rem; }}
        .contact-line {{ color: #38bdf8; font-size: 0.95rem; margin-top: 0.4rem; }}
        .score-badge {{ padding: 0.6rem 1rem; border-radius: 10px; text-align: center; color: white; min-width: 90px; }}
        .score-badge span {{ font-size: 1.6rem; font-weight: bold; display: block; }}
        .score-badge small {{ font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.5px; }}
        .stats-row {{ display: flex; gap: 1.5rem; margin-bottom: 1rem; color: #cbd5e1; font-size: 0.95rem; }}
        .reasons-list {{ list-style: none; margin-bottom: 1.25rem; padding-left: 0; }}
        .reasons-list li {{ background: #0f172a; padding: 0.6rem 0.9rem; border-radius: 8px; margin-bottom: 0.4rem; font-size: 0.9rem; color: #facc15; border-left: 3px solid #facc15; }}
        
        .action-buttons-bar {{ display: flex; gap: 0.75rem; margin-bottom: 1.25rem; flex-wrap: wrap; }}
        .contact-btn {{ display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.7rem 1.25rem; border-radius: 8px; font-weight: 700; font-size: 0.9rem; text-decoration: none; cursor: pointer; border: none; transition: transform 0.15s, opacity 0.15s; }}
        .contact-btn:hover {{ transform: translateY(-2px); opacity: 0.95; }}
        .wa-btn {{ background: #25d366; color: #000; box-shadow: 0 4px 15px rgba(37, 211, 102, 0.3); }}
        .email-btn {{ background: #0284c7; color: #fff; box-shadow: 0 4px 15px rgba(2, 132, 199, 0.3); }}
        .copy-btn {{ background: #334155; color: #f8fafc; border: 1px solid #475569; }}
        
        .email-preview {{ background: #090e1a; border: 1px solid #1e293b; border-radius: 10px; padding: 1.25rem; }}
        .email-subject {{ font-weight: bold; color: #38bdf8; margin-bottom: 0.75rem; font-size: 0.95rem; border-bottom: 1px solid #1e293b; padding-bottom: 0.5rem; }}
        pre {{ white-space: pre-wrap; font-family: monospace; font-size: 0.9rem; color: #cbd5e1; line-height: 1.6; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>⚡ Direct Client Outreach & Radar</h1>
            <p class="subtitle">Click 1 button to message on WhatsApp or send a pre-filled email to high-ticket local businesses</p>
        </header>
        {html_cards}
    </div>

    <script>
        function copyPitch(btn, subject, body) {{
            const fullText = "Subject: " + subject + "\\n\\n" + body;
            navigator.clipboard.writeText(fullText).then(() => {{
                const original = btn.innerHTML;
                btn.innerHTML = '<i class="fa-solid fa-check"></i> Copied to Clipboard!';
                btn.style.background = '#10b981';
                setTimeout(() => {{
                    btn.innerHTML = original;
                    btn.style.background = '#334155';
                }}, 2000);
            }});
        }}
    </script>
</body>
</html>
"""

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)

    print("[+] Updated audit_report.html with direct WhatsApp & Email 1-click buttons!")

if __name__ == "__main__":
    run_audit()
