"""
╔══════════════════════════════════════════════════════════╗
║  AGENT 02 — CHIEF STRATEGY OFFICER                       ║
║  API: Google Gemini (Free Forever)                       ║
║  Role: Veteran product strategist & business architect   ║
║  Task: Turn research into a precise product blueprint    ║
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

def run_strategy():
    print("🧠 Agent 02 — Chief Strategy Officer thinking...")

    research = json.loads((KNOWLEDGE / f"research_{TODAY}.json").read_text())
    perf_file = KNOWLEDGE / "performance.json"
    performance = json.loads(perf_file.read_text()) if perf_file.exists() else {}
    past_knowledge = performance.get("knowledge", {})

    prompt = f"""
You are a Chief Strategy Officer with 30 years building digital product businesses.
You have launched 500+ digital products and know exactly what makes templates sell.

Today's market research:
{json.dumps(research, indent=2)}

Accumulated business knowledge from past runs:
{json.dumps(past_knowledge, indent=2) if past_knowledge else "First run — build foundational strategy."}

Create a PRECISE product blueprint. Every detail matters. The developer will build
EXACTLY what you specify. Make it specific, modern, and highly sellable.

Return ONLY valid JSON, zero explanation, zero backticks:
{{
  "date": "{TODAY}",
  "product_blueprint": {{
    "template_name": "NovaSaaS — Modern Dark SaaS Landing Page",
    "file_name_slug": "novasaas-landing-page",
    "template_type": "HTML/CSS/JS",
    "price_usd": 19,
    "tagline": "Launch your SaaS in minutes with a stunning conversion-optimized page",
    "color_palette": {{
      "background": "#0A0A0F",
      "primary": "#7C3AED",
      "accent": "#06B6D4",
      "text": "#F8FAFC",
      "surface": "#1A1A2E"
    }},
    "typography": {{
      "heading_font": "Clash Display",
      "body_font": "Inter",
      "google_fonts_url": "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap"
    }},
    "sections": [
      "Sticky navigation with CTA button",
      "Hero section with animated gradient background and particles",
      "Logo strip (social proof — trusted by companies)",
      "Features grid (6 features with icons and descriptions)",
      "How it works (3 steps with illustrations)",
      "Pricing table (3 tiers — Starter, Pro, Enterprise)",
      "Testimonials carousel (3 customer reviews)",
      "FAQ accordion (6 questions)",
      "CTA banner with email signup",
      "Footer with links and social icons"
    ],
    "must_have_features": [
      "Dark mode as default",
      "Fully responsive — mobile first",
      "CSS scroll animations using Intersection Observer",
      "CSS variables for easy color customization",
      "Hamburger menu for mobile",
      "Smooth scrolling navigation",
      "Clean well-commented code",
      "Zero external dependencies"
    ],
    "differentiators": [
      "Animated SVG mesh gradient background",
      "Glassmorphism card effects",
      "5 pre-built color schemes via CSS variables",
      "Particle animation in hero section",
      "Staggered entrance animations on scroll"
    ],
    "tech_stack": "HTML5 + CSS3 + Vanilla JS (zero npm, zero dependencies)",
    "target_customer": "Indie hackers, SaaS founders, startup teams, freelancers",
    "estimated_lines": 900
  }},
  "gumroad_strategy": {{
    "category": "Design Assets",
    "tags": ["website template", "saas template", "landing page", "html template", "startup"],
    "cover_concept": "Dark laptop mockup showing template with purple glow effect",
    "bundle_opportunity": false,
    "launch_price": 19,
    "raise_price_after": "10 sales — raise to $29"
  }},
  "quality_checklist": [
    "All 10 sections fully built — no placeholders",
    "Works in Chrome, Firefox, Safari, Edge",
    "Passes W3C HTML validation",
    "Mobile responsive at 320px, 768px, 1024px, 1440px",
    "Detailed README with setup instructions",
    "CUSTOMIZATION.md explaining CSS variables"
  ],
  "strategy_notes": "Dark SaaS templates are hot right now. Glassmorphism + animations = premium feel."
}}
"""

    print("  → Gemini AI crafting product strategy...")
    raw = ask_gemini(prompt)
    strategy = json.loads(raw)

    (KNOWLEDGE / f"strategy_{TODAY}.json").write_text(json.dumps(strategy, indent=2))
    (LOGS / f"agent02_{TODAY}.json").write_text(json.dumps({
        "agent": "02_strategy", "date": TODAY, "status": "success",
        "api": "gemini-1.5-flash (FREE)",
        "product_name": strategy["product_blueprint"]["template_name"],
        "price": strategy["product_blueprint"]["price_usd"],
        "sections_count": len(strategy["product_blueprint"]["sections"])
    }, indent=2))

    print(f"  ✅ Blueprint: {strategy['product_blueprint']['template_name']}")
    print(f"  💰 Price: ${strategy['product_blueprint']['price_usd']}")
    print(f"  📋 Sections: {len(strategy['product_blueprint']['sections'])}")
    print("✅ Agent 02 complete.\n")

if __name__ == "__main__":
    run_strategy()
