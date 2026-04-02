"""
╔══════════════════════════════════════════════════════════╗
║  AGENT 01 — MARKET RESEARCH DIRECTOR                     ║
║  Role: 30-year veteran market analyst                    ║
║  Task: Scrape trends, competitors, gaps, pricing         ║
╚══════════════════════════════════════════════════════════╝
"""

import json
import os
import time
import random
from datetime import datetime
from pathlib import Path
import anthropic

# ── Paths ──────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent
KNOWLEDGE = ROOT / "knowledge"
LOGS = ROOT / "logs"
KNOWLEDGE.mkdir(exist_ok=True)
LOGS.mkdir(exist_ok=True)

TODAY = datetime.now().strftime("%Y-%m-%d")

# ── Competitor & trend sources to monitor ─────────────────
SOURCES = {
    "gumroad_search_urls": [
        "https://gumroad.com/discover?query=website+template",
        "https://gumroad.com/discover?query=landing+page+template",
        "https://gumroad.com/discover?query=react+template",
        "https://gumroad.com/discover?query=tailwind+template",
        "https://gumroad.com/discover?query=portfolio+template",
        "https://gumroad.com/discover?query=saas+template",
        "https://gumroad.com/discover?query=dashboard+template",
    ],
    "trend_keywords": [
        "website templates 2025 trending",
        "best selling HTML templates gumroad",
        "saas landing page template demand",
        "react dashboard template popular",
        "portfolio template developer 2025",
    ]
}

def run_market_research():
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    # Load historical knowledge
    trends_file = KNOWLEDGE / "trends.json"
    history = json.loads(trends_file.read_text()) if trends_file.exists() else {}

    print("🔍 Market Research Director starting deep analysis...")

    # ── Step 1: AI-powered market intelligence ──────────────
    prompt = f"""
You are a 30-year veteran market research director specializing in digital products, 
template marketplaces, and online creator economies.

Today's date: {TODAY}
Your job: Perform the most thorough market research possible for website template products 
being sold on Gumroad.

Historical data from previous runs:
{json.dumps(history, indent=2) if history else "No history yet — this is Day 1."}

Analyze and return a JSON object with this EXACT structure (return ONLY JSON, no markdown):
{{
  "date": "{TODAY}",
  "top_niches": [
    {{
      "niche": "SaaS Landing Page",
      "demand_score": 9.2,
      "competition_level": "medium",
      "avg_price_usd": 19,
      "gap_opportunity": "Most templates lack dark mode + animations",
      "trending_reason": "AI startup boom driving SaaS product launches",
      "target_buyer": "indie hackers, startup founders"
    }}
  ],
  "winning_keywords": ["saas template", "landing page html", "startup template"],
  "pricing_intelligence": {{
    "budget_range": "$5-$9",
    "mid_range": "$10-$25",
    "premium_range": "$29-$49",
    "recommendation": "Price at $19 for max conversions — sweet spot",
    "upsell_strategy": "Offer bundle of 3 templates at $39"
  }},
  "competitor_weaknesses": [
    "Most templates don't include mobile-first design",
    "Poor documentation / README files",
    "No dark mode variants"
  ],
  "todays_recommendation": {{
    "template_type": "SaaS Landing Page",
    "unique_angle": "Include animated hero, dark mode, and 5 color variants",
    "suggested_title": "NovaSaaS — Premium SaaS Landing Page Template",
    "suggested_price": 19,
    "confidence": 0.91
  }},
  "upcoming_trends": [
    "AI tool landing pages",
    "Mobile-first one-pagers",
    "Glassmorphism UI kits"
  ],
  "self_learning_notes": "Based on analysis, SaaS + dark mode templates are undersupplied."
}}

Think deeply. Be specific. Identify real gaps in the market. 
Act like the best analyst in the world — your research determines today's revenue.
"""

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.content[0].text.strip()
    # Clean JSON if wrapped in backticks
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    
    research = json.loads(raw.strip())
    print(f"✅ Research complete. Top niche today: {research['todays_recommendation']['template_type']}")

    # ── Step 2: Save results ────────────────────────────────
    # Save today's research
    today_file = KNOWLEDGE / f"research_{TODAY}.json"
    today_file.write_text(json.dumps(research, indent=2))

    # Update running trends file
    if "history" not in history:
        history["history"] = []
    history["history"].append({
        "date": TODAY,
        "recommendation": research["todays_recommendation"],
        "top_niches": [n["niche"] for n in research["top_niches"][:3]]
    })
    # Keep last 30 days only
    history["history"] = history["history"][-30:]
    history["latest"] = research
    trends_file.write_text(json.dumps(history, indent=2))

    # ── Step 3: Log ─────────────────────────────────────────
    log = {
        "agent": "01_market_research",
        "date": TODAY,
        "status": "success",
        "recommendation": research["todays_recommendation"],
        "niches_analyzed": len(research["top_niches"]),
        "confidence": research["todays_recommendation"]["confidence"]
    }
    (LOGS / f"agent01_{TODAY}.json").write_text(json.dumps(log, indent=2))
    
    print(f"💡 Recommendation: {research['todays_recommendation']['suggested_title']}")
    print(f"💰 Suggested price: ${research['todays_recommendation']['suggested_price']}")
    print(f"📊 Confidence: {research['todays_recommendation']['confidence'] * 100:.0f}%")
    print("✅ Agent 01 done. Knowledge saved.")

if __name__ == "__main__":
    run_market_research()
