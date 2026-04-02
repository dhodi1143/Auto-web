"""
╔══════════════════════════════════════════════════════════╗
║  AGENT 04 — SEO & COPYWRITING EXPERT                     ║
║  API: Google Gemini (Free Forever)                       ║
║  Role: 25yr copywriter + SEO strategist                  ║
║  Task: Write high-converting Gumroad listing copy        ║
╚══════════════════════════════════════════════════════════╝
"""

import json
import os
from datetime import datetime
from pathlib import Path
import google.generativeai as genai

ROOT = Path(__file__).parent.parent
KNOWLEDGE = ROOT / "knowledge"
LOGS = ROOT / "logs"
TODAY = datetime.now().strftime("%Y-%m-%d")

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

def ask_gemini(prompt):
    response = model.generate_content(prompt)
    raw = response.text.strip()
    if "```" in raw:
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return raw.strip()

def run_seo_copy():
    print("🎯 Agent 04 — SEO & Copywriting Expert writing listing...")

    strategy = json.loads((KNOWLEDGE / f"strategy_{TODAY}.json").read_text())
    research = json.loads((KNOWLEDGE / f"research_{TODAY}.json").read_text())
    bp = strategy["product_blueprint"]
    gs = strategy["gumroad_strategy"]

    prompt = f"""
You are the world's best direct response copywriter and SEO expert.
You have 25 years of experience selling digital products online.
Your copy has generated over $10 million in template sales.
You write like David Ogilvy — every word earns its place.

Product details:
Name: {bp['template_name']}
Tagline: {bp['tagline']}
Price: ${bp['price_usd']}
Tech: {bp['tech_stack']}
Features: {json.dumps(bp['must_have_features'])}
Differentiators: {json.dumps(bp['differentiators'])}
Sections: {json.dumps(bp['sections'])}
Target customer: {bp['target_customer']}
Competitor weaknesses: {json.dumps(research['competitor_weaknesses'])}

Write the ULTIMATE Gumroad product listing. Return ONLY valid JSON, no backticks:
{{
  "product_title": "NovaSaaS — Premium Dark SaaS Landing Page Template",
  "short_description": "Launch your SaaS in hours, not weeks. Stunning dark mode landing page with animations. HTML/CSS/JS — zero dependencies.",
  "full_description": "<h2>Stop Spending Weeks On Your Landing Page</h2>\\n<p>You have a brilliant SaaS idea. But every day you spend building your landing page is a day you're not talking to customers. <strong>NovaSaaS gives you a stunning, conversion-optimized landing page in minutes.</strong></p>\\n<h2>✨ What's Included</h2>\\n<ul>\\n<li>🎨 <strong>10 fully built sections</strong> — Hero, Features, Pricing, Testimonials, FAQ + more</li>\\n<li>🌙 <strong>Dark mode first design</strong> — Modern and premium</li>\\n<li>📱 <strong>100% mobile responsive</strong> — Looks perfect on every device</li>\\n<li>⚡ <strong>Zero dependencies</strong> — Pure HTML/CSS/JS, no npm needed</li>\\n<li>🎭 <strong>Smooth scroll animations</strong> — Professional entrance effects</li>\\n<li>🎨 <strong>5 color themes</strong> — Change your brand color in seconds</li>\\n<li>📄 <strong>Detailed docs</strong> — README + Customization guide included</li>\\n</ul>\\n<h2>👥 Perfect For</h2>\\n<p>Indie hackers launching their first SaaS, startup founders who need to move fast, and freelancers building client sites.</p>\\n<h2>🚀 Get Live in 3 Steps</h2>\\n<p>1. Download the ZIP → 2. Edit your content → 3. Deploy free to Netlify. <strong>Done.</strong></p>\\n<h2>💎 Why Better Than Others</h2>\\n<p>Most templates on Gumroad are outdated, lack mobile support, and have zero documentation. NovaSaaS is built in 2025 with modern design standards, includes step-by-step docs, and requires absolutely zero technical setup.</p>\\n<p><strong>⚡ Instant download. MIT License. Use on unlimited projects.</strong></p>",
  "seo_tags": ["website template", "saas landing page", "html template", "startup template", "landing page html css"],
  "price_usd": 19,
  "summary_line": "Instant download • MIT License • Works in 5 minutes",
  "cover_image_alt": "NovaSaaS dark SaaS landing page template preview on laptop and mobile",
  "social_proof_hook": "Built with the same patterns used by $1M+ SaaS products",
  "guarantee_text": "Instant download. If the file doesn't open, full refund — no questions asked.",
  "seo_score_estimate": 9.2
}}

Write conversion copy that makes people FEEL they need this. No fluff. Pure persuasion.
"""

    print("  → Gemini AI writing conversion copy...")
    raw = ask_gemini(prompt)
    copy = json.loads(raw)

    (KNOWLEDGE / f"copy_{TODAY}.json").write_text(json.dumps(copy, indent=2))
    (LOGS / f"agent04_{TODAY}.json").write_text(json.dumps({
        "agent": "04_seo_copy", "date": TODAY, "status": "success",
        "api": "gemini-1.5-flash (FREE)",
        "title": copy["product_title"],
        "price": copy["price_usd"],
        "seo_score": copy.get("seo_score_estimate"),
        "tags": copy["seo_tags"]
    }, indent=2))

    print(f"  ✅ Title: {copy['product_title']}")
    print(f"  🏷️  Tags: {', '.join(copy['seo_tags'][:3])}...")
    print(f"  📈 SEO score: {copy.get('seo_score_estimate')}/10")
    print("✅ Agent 04 complete.\n")

if __name__ == "__main__":
    run_seo_copy()
