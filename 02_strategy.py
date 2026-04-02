"""
╔══════════════════════════════════════════════════════════╗
║  AGENT 02 — CHIEF STRATEGY OFFICER                       ║
║  Role: Veteran product strategist & business architect   ║
║  Task: Turn research into a precise build blueprint      ║
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

def run_strategy():
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    # Load today's research
    research_file = KNOWLEDGE / f"research_{TODAY}.json"
    research = json.loads(research_file.read_text())

    # Load performance history
    perf_file = KNOWLEDGE / "performance.json"
    performance = json.loads(perf_file.read_text()) if perf_file.exists() else {}

    print("🧠 Chief Strategy Officer analyzing research & crafting strategy...")

    prompt = f"""
You are a Chief Strategy Officer with 30 years of experience building digital product 
businesses. You have deep expertise in UX, developer tools, and the creator economy.

Today's market research:
{json.dumps(research, indent=2)}

Historical performance data (what sold well before):
{json.dumps(performance, indent=2) if performance else "No performance data yet."}

Your job: Create an ultra-precise product blueprint that the development team will 
execute PERFECTLY.

Return ONLY a JSON object with this EXACT structure:
{{
  "date": "{TODAY}",
  "product_blueprint": {{
    "template_name": "NovaSaaS — Modern SaaS Landing Page",
    "file_name_slug": "novasaas-landing-page",
    "template_type": "HTML/CSS/JS",
    "price_usd": 19,
    "tagline": "Launch your SaaS in minutes with a stunning, conversion-optimized page",
    "color_palette": ["#0F0F1A", "#7C3AED", "#06B6D4", "#F8FAFC"],
    "typography": {{
      "heading_font": "Clash Display",
      "body_font": "Inter"
    }},
    "sections_to_include": [
      "Hero with animated gradient + CTA",
      "Features grid (6 features with icons)",
      "Pricing table (3 tiers)",
      "Testimonials carousel",
      "FAQ accordion",
      "Footer with newsletter"
    ],
    "must_have_features": [
      "Dark mode default",
      "Fully responsive mobile-first",
      "CSS animations on scroll",
      "Clean commented code",
      "Easy to customize variables"
    ],
    "differentiators": [
      "Animated SVG background",
      "5 color scheme variants in CSS variables",
      "One-command setup"
    ],
    "tech_stack": "HTML5 + CSS3 + Vanilla JS (zero dependencies)",
    "estimated_lines_of_code": 800,
    "target_customer": "Indie hackers, startup founders, freelancers"
  }},
  "gumroad_strategy": {{
    "category": "Design Assets",
    "tags": ["website template", "saas", "landing page", "html template", "startup"],
    "cover_image_concept": "Dark background showing the template on laptop + mobile mockup",
    "description_hook": "Stop spending weeks building your landing page from scratch.",
    "bundle_opportunity": false,
    "discount_strategy": "Launch at $19, raise to $29 after 10 sales"
  }},
  "quality_checklist": [
    "Code must be production-ready",
    "Must include detailed README.md",
    "All assets must be royalty-free",
    "Must pass W3C HTML validation"
  ],
  "strategy_notes": "SaaS templates with dark mode are undersupplied. Going aggressive on animations."
}}

Think like the best product strategist alive. Every decision must maximize revenue.
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

    strategy = json.loads(raw.strip())

    # Save strategy
    strategy_file = KNOWLEDGE / f"strategy_{TODAY}.json"
    strategy_file.write_text(json.dumps(strategy, indent=2))

    log = {
        "agent": "02_strategy",
        "date": TODAY,
        "status": "success",
        "product_name": strategy["product_blueprint"]["template_name"],
        "price": strategy["product_blueprint"]["price_usd"],
        "tech_stack": strategy["product_blueprint"]["tech_stack"]
    }
    (LOGS / f"agent02_{TODAY}.json").write_text(json.dumps(log, indent=2))

    print(f"✅ Strategy locked: {strategy['product_blueprint']['template_name']}")
    print(f"💰 Price: ${strategy['product_blueprint']['price_usd']}")
    print(f"🛠️  Stack: {strategy['product_blueprint']['tech_stack']}")
    print("✅ Agent 02 done.")

if __name__ == "__main__":
    run_strategy()
