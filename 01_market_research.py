"""
╔══════════════════════════════════════════════════════════╗
║  AGENT 01 — MARKET RESEARCH DIRECTOR                     ║
║  API: Google Gemini (Free Forever)                       ║
║  Role: 30-year veteran market analyst                    ║
║  Task: Deep research — trends, gaps, pricing, demand     ║
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
KNOWLEDGE.mkdir(exist_ok=True)
LOGS.mkdir(exist_ok=True)
TODAY = datetime.now().strftime("%Y-%m-%d")

# ── Configure Gemini (Free Forever) ────────────────────────
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

def run_market_research():
    print("🔍 Agent 01 — Market Research Director starting...")

    trends_file = KNOWLEDGE / "trends.json"
    history = json.loads(trends_file.read_text()) if trends_file.exists() else {}
    past = history.get("history", [])[-10:]

    prompt = f"""
You are a 30-year veteran market research director. You specialize in digital product
marketplaces, specifically template sales on Gumroad. You have helped creators earn
millions. Your research is precise, data-driven, and always finds hidden opportunities.

Today: {TODAY}
Past 10 days of research: {json.dumps(past, indent=2) if past else "Day 1 — no history."}

Your job: Find the single best website template niche to build TODAY on Gumroad.
Consider: demand, competition gaps, trending topics, buyer pain points, pricing sweet spots.

Return ONLY valid JSON, zero explanation, zero backticks:
{{
  "date": "{TODAY}",
  "top_niches": [
    {{
      "niche": "SaaS Landing Page",
      "demand_score": 9.2,
      "competition_level": "medium",
      "avg_price_usd": 19,
      "gap_opportunity": "Most lack dark mode + modern animations",
      "trending_reason": "AI startup boom driving SaaS product launches globally",
      "target_buyer": "indie hackers, startup founders, freelancers"
    }},
    {{
      "niche": "Developer Portfolio",
      "demand_score": 8.7,
      "competition_level": "high",
      "avg_price_usd": 14,
      "gap_opportunity": "Clean minimal dark mode portfolios are rare",
      "trending_reason": "Remote work boom, every dev needs online presence",
      "target_buyer": "junior developers, CS students, freelancers"
    }},
    {{
      "niche": "Agency Website",
      "demand_score": 8.1,
      "competition_level": "low",
      "avg_price_usd": 24,
      "gap_opportunity": "Modern glassmorphism agency sites are rare",
      "trending_reason": "Rise of micro-agencies and freelance studios",
      "target_buyer": "marketing agencies, creative studios, consultants"
    }}
  ],
  "winning_keywords": [
    "website template", "saas landing page", "html template",
    "portfolio template", "landing page html css", "startup template"
  ],
  "pricing_intelligence": {{
    "budget_range": "$5-$9",
    "mid_range": "$10-$25",
    "premium_range": "$29-$49",
    "recommendation": "$19 is the sweet spot — max conversions",
    "upsell_strategy": "Bundle 3 templates at $39 for 2x revenue"
  }},
  "competitor_weaknesses": [
    "Most templates have poor mobile responsiveness",
    "Outdated designs from 2021-2022",
    "Zero dark mode support",
    "No customization guide or documentation",
    "Boring generic layouts with no personality"
  ],
  "todays_recommendation": {{
    "template_type": "SaaS Landing Page",
    "unique_angle": "Dark mode first, animated gradient hero, 5 color variants, scroll animations",
    "suggested_title": "NovaSaaS — Premium Dark SaaS Landing Page Template",
    "suggested_price": 19,
    "tech_stack": "HTML5 + CSS3 + Vanilla JS",
    "confidence": 0.93
  }},
  "upcoming_trends": [
    "AI product landing pages are the hottest niche",
    "Glassmorphism + dark mode combinations",
    "One-page mobile-first sites",
    "Minimal brutalist developer portfolios"
  ],
  "self_learning_notes": "Avoid oversaturated blog templates. Focus on SaaS and developer tools."
}}
"""

    print("  → Gemini AI analyzing global market trends...")
    raw = ask_gemini(prompt)
    research = json.loads(raw)

    # Save results
    (KNOWLEDGE / f"research_{TODAY}.json").write_text(json.dumps(research, indent=2))

    if "history" not in history:
        history["history"] = []
    history["history"].append({
        "date": TODAY,
        "recommendation": research["todays_recommendation"],
        "top_niches": [n["niche"] for n in research["top_niches"][:3]]
    })
    history["history"] = history["history"][-30:]
    history["latest"] = research
    (KNOWLEDGE / "trends.json").write_text(json.dumps(history, indent=2))

    (LOGS / f"agent01_{TODAY}.json").write_text(json.dumps({
        "agent": "01_market_research", "date": TODAY, "status": "success",
        "api": "gemini-1.5-flash (FREE)",
        "recommendation": research["todays_recommendation"],
        "confidence": research["todays_recommendation"]["confidence"]
    }, indent=2))

    print(f"  ✅ Best niche today: {research['todays_recommendation']['template_type']}")
    print(f"  💰 Target price: ${research['todays_recommendation']['suggested_price']}")
    print(f"  📊 Confidence: {int(research['todays_recommendation']['confidence']*100)}%")
    print("✅ Agent 01 complete.\n")

if __name__ == "__main__":
    run_market_research()
