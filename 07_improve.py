"""
╔══════════════════════════════════════════════════════════╗
║  AGENT 07 — SELF-IMPROVEMENT ENGINE                      ║
║  API: Google Gemini (Free Forever)                       ║
║  Role: AI that learns and gets smarter every day         ║
║  Task: Score today, update knowledge, plan tomorrow      ║
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

def load_safe(path):
    try:
        return json.loads(Path(path).read_text())
    except:
        return {}

def run_improvement():
    print("📊 Agent 07 — Self-Improvement Engine analyzing today...")

    # Collect all logs from today
    today_logs = {}
    for f in LOGS.glob(f"agent0*_{TODAY}.json"):
        name = f.stem.replace(f"_{TODAY}", "")
        today_logs[name] = load_safe(f)

    performance = load_safe(KNOWLEDGE / "performance.json")
    published = load_safe(KNOWLEDGE / f"published_{TODAY}.json")
    total_runs = len(list(LOGS.glob("agent07_*.json")))

    prompt = f"""
You are an AI business intelligence system running an automated digital product business.
This is day #{total_runs + 1} of operations.

Today's agent results:
{json.dumps(today_logs, indent=2)}

Product published today:
{json.dumps(published, indent=2)}

Accumulated knowledge from previous runs:
{json.dumps(performance.get("knowledge", {{}}), indent=2) if performance else "No history yet."}

Performance history (last 20 days):
{json.dumps(performance.get("history", [])[-20:], indent=2) if performance else "No history yet."}

Analyze brutally and honestly. Score everything. Identify improvements.
Return ONLY valid JSON, no backticks, no explanation:
{{
  "date": "{TODAY}",
  "run_number": {total_runs + 1},
  "todays_assessment": {{
    "overall_score": 8.5,
    "what_went_well": [
      "Strong niche selection based on market data",
      "Price point is competitive"
    ],
    "what_to_improve": [
      "Template could have more sections",
      "Description needs stronger emotional hook"
    ],
    "agent_scores": {{
      "market_research": 9.0,
      "strategy": 8.5,
      "development": 8.0,
      "seo_copy": 8.5,
      "publishing": 9.0
    }}
  }},
  "improvements_for_tomorrow": [
    "Focus on React templates — they sell 40% more than plain HTML",
    "Add FAQ section with 8 questions instead of 6",
    "Include 'trending 2025' in the product title",
    "Price at $24 instead of $19 for perceived premium quality"
  ],
  "knowledge_updates": {{
    "best_niches_proven": ["SaaS Landing Pages", "Developer Portfolios"],
    "best_price_point": 19,
    "avoid_niches": ["Generic blog templates — too saturated"],
    "best_tags": ["website template", "landing page", "html template"],
    "proven_patterns": [
      "Dark mode templates get more saves",
      "Templates with docs sell more than without",
      "Prices ending in 9 convert better"
    ],
    "avoid_patterns": [
      "Avoid Bootstrap — buyers want zero dependencies",
      "Avoid light mode only templates"
    ]
  }},
  "system_health": {{
    "total_products_published": {total_runs + 1},
    "consistency_streak": "Day {total_runs + 1}",
    "next_milestone": "10 products — enough for a catalog",
    "projected_monthly_revenue": "After 30 days: $50-$200/month passive"
  }},
  "tomorrows_focus": "React SaaS dashboard template — charts, tables, dark mode — undersupplied",
  "motivational_note": "Compound effect is real. Each product builds on the last. Stay consistent."
}}
"""

    print("  → Gemini AI analyzing performance and updating brain...")
    raw = ask_gemini(prompt)
    assessment = json.loads(raw)

    # Update performance knowledge base
    if "history" not in performance:
        performance["history"] = []

    performance["history"].append({
        "date": TODAY,
        "run_number": total_runs + 1,
        "product": published.get("product_title", "Unknown"),
        "publish_status": published.get("status", "unknown"),
        "score": assessment["todays_assessment"]["overall_score"],
        "improvements": assessment["improvements_for_tomorrow"]
    })
    performance["history"] = performance["history"][-60:]
    performance["knowledge"] = assessment["knowledge_updates"]
    performance["latest"] = assessment

    (KNOWLEDGE / "performance.json").write_text(json.dumps(performance, indent=2))
    (KNOWLEDGE / f"improvement_{TODAY}.json").write_text(json.dumps(assessment, indent=2))

    # ── Write Daily Summary Report ──────────────────────────
    score = assessment["todays_assessment"]["overall_score"]
    summary_md = f"""# 🤖 AutoBusiness Daily Report — {TODAY}
## Run #{total_runs + 1} | Score: {score}/10

### ✅ Product Published
- **Title**: {published.get('product_title', 'N/A')}
- **Price**: ${published.get('price_usd', 'N/A')}
- **Status**: {published.get('status', 'N/A').upper()}
- **URL**: {published.get('product_url', 'N/A')}

### 🔧 Improvements for Tomorrow
{chr(10).join(f"- {i}" for i in assessment['improvements_for_tomorrow'])}

### 🧠 System Knowledge Updated
- Best niches: {', '.join(assessment['knowledge_updates'].get('best_niches_proven', []))}
- Best price: ${assessment['knowledge_updates'].get('best_price_point', 'N/A')}

### 🎯 Tomorrow's Focus
{assessment.get('tomorrows_focus', 'TBD')}

### 💬 Note
{assessment.get('motivational_note', '')}

---
*AutoBusiness AI — Day #{total_runs + 1} — Zero Humans — Zero Cost*
*API: Google Gemini (Free Forever)*
"""
    (LOGS / f"daily_report_{TODAY}.md").write_text(summary_md)

    (LOGS / f"agent07_{TODAY}.json").write_text(json.dumps({
        "agent": "07_improve", "date": TODAY, "status": "success",
        "api": "gemini-1.5-flash (FREE)",
        "run_number": total_runs + 1,
        "overall_score": score,
        "improvements_count": len(assessment["improvements_for_tomorrow"])
    }, indent=2))

    print(f"  ✅ Day #{total_runs + 1} scored: {score}/10")
    print(f"  🎯 Tomorrow: {assessment.get('tomorrows_focus', 'TBD')}")
    print(f"  🧠 Knowledge base updated. System is getting smarter.")
    print(f"  💬 {assessment.get('motivational_note', '')}")
    print("✅ Agent 07 complete.\n")
    print("=" * 55)
    print(f"  🎉 DAILY RUN COMPLETE — Day #{total_runs + 1}")
    print(f"  📦 Product: {published.get('product_title', 'N/A')}")
    print(f"  💰 Price: ${published.get('price_usd', 'N/A')}")
    print(f"  🌐 Status: {published.get('status', 'N/A').upper()}")
    print("=" * 55)

if __name__ == "__main__":
    run_improvement()
