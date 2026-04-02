"""
╔══════════════════════════════════════════════════════════╗
║  AGENT 04 — SEO & COPYWRITING EXPERT                     ║
║  Role: 25yr copywriter + SEO strategist                  ║
║  Task: Write high-converting Gumroad listing copy        ║
╚══════════════════════════════════════════════════════════╝
"""

import json
import os
from datetime import datetime
from pathlib import Path
import anthropic

ROOT = Path(__file__).parent.parent
KNOWLEDGE = ROOT / "knowledge"
LOGS = ROOT / "logs"
TODAY = datetime.now().strftime("%Y-%m-%d")

def run_seo_copy():
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    strategy = json.loads((KNOWLEDGE / f"strategy_{TODAY}.json").read_text())
    research = json.loads((KNOWLEDGE / f"research_{TODAY}.json").read_text())
    bp = strategy["product_blueprint"]
    gs = strategy["gumroad_strategy"]

    print("🎯 SEO & Copywriting Expert crafting high-converting listing...")

    prompt = f"""
You are the world's best SEO copywriter with 25 years of experience selling digital 
products. You have personally written copy that generated $10M+ in template sales.

Product details:
{json.dumps(bp, indent=2)}

Gumroad strategy:
{json.dumps(gs, indent=2)}

Market research (what buyers want):
- Competitor weaknesses: {json.dumps(research.get('competitor_weaknesses', []))}
- Target buyer: {bp.get('target_customer')}

Write the ULTIMATE Gumroad product listing. Return ONLY JSON:

{{
  "product_title": "NovaSaaS — Modern SaaS Landing Page Template",
  "short_description": "One punchy sentence. Max 160 chars. SEO optimized.",
  "full_description": "Full Gumroad description in HTML. Use <h2>, <ul>, <strong>, <p> tags. Include:\\n- Emotional hook opening\\n- What's included (bulleted)\\n- Who it's for\\n- Why it's better than competitors\\n- Technical specs\\n- What they get after purchase\\n- Call to action\\nMake it 400-600 words. Persuasive but honest.",
  "seo_tags": ["website template", "saas landing page", "html template", "startup template", "landing page"],
  "price_usd": 19,
  "summary_line": "One line shown under CTA button",
  "cover_image_alt_text": "NovaSaaS dark mode SaaS landing page template preview",
  "social_proof_hook": "Join 500+ founders who launched with this template",
  "guarantee_text": "Instant download. Lifetime updates. 100% money-back if it doesn't open.",
  "seo_score_estimate": 9.1
}}

Write like David Ogilvy. Every word earns its place. No fluff. No corporate speak.
Pure conversion copy.
"""

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    copy = json.loads(raw.strip())

    # Save copy
    (KNOWLEDGE / f"copy_{TODAY}.json").write_text(json.dumps(copy, indent=2))

    log = {
        "agent": "04_seo_copy",
        "date": TODAY,
        "status": "success",
        "title": copy["product_title"],
        "price": copy["price_usd"],
        "seo_score": copy.get("seo_score_estimate"),
        "tags": copy["seo_tags"]
    }
    (LOGS / f"agent04_{TODAY}.json").write_text(json.dumps(log, indent=2))

    print(f"✅ Copy written: {copy['product_title']}")
    print(f"🏷️  Tags: {', '.join(copy['seo_tags'])}")
    print(f"📈 SEO score estimate: {copy.get('seo_score_estimate')}/10")
    print("✅ Agent 04 done.")

if __name__ == "__main__":
    run_seo_copy()
