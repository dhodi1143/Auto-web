"""
╔══════════════════════════════════════════════════════════╗
║  AGENT 07 — ANALYTICS & SELF-IMPROVEMENT ENGINE         ║
║  Role: AI that learns, adapts, and makes the system     ║
║        smarter every single day                          ║
║  Task: Analyze results, update knowledge, improve        ║
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

def load_json_safe(path):
    try:
        return json.loads(Path(path).read_text())
    except:
        return {}

def run_improvement():
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    # Gather all today's logs
    today_logs = {}
    for log_file in LOGS.glob(f"*_{TODAY}.json"):
        agent_name = log_file.stem.replace(f"_{TODAY}", "")
        today_logs[agent_name] = load_json_safe(log_file)

    # Load all historical knowledge
    trends = load_json_safe(KNOWLEDGE / "trends.json")
    performance = load_json_safe(KNOWLEDGE / "performance.json")
    published = load_json_safe(KNOWLEDGE / f"published_{TODAY}.json")

    # Count historical runs
    all_logs = list(LOGS.glob("agent07_*.json"))
    total_runs = len(all_logs)

    print(f"📊 Self-Improvement Engine running (Day #{total_runs + 1})...")

    prompt = f"""
You are an AI business intelligence system that has been running an automated 
template business for {total_runs} days.

Today's run summary:
{json.dumps(today_logs, indent=2)}

Product published today:
{json.dumps(published, indent=2)}

Historical performance data:
{json.dumps(performance, indent=2) if performance else "No historical data yet."}

Trend history (last 30 days):
{json.dumps(trends.get('history', []), indent=2)}

Your job: Be brutally honest. Analyze what worked, what didn't, and write 
instructions to make tomorrow's run BETTER.

Return ONLY JSON:
{{
  "date": "{TODAY}",
  "run_number": {total_runs + 1},
  "todays_assessment": {{
    "overall_score": 8.5,
    "strengths": ["Strong niche selection", "Good pricing"],
    "weaknesses": ["Description could be more emotional"],
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
    "Add preview screenshots to product listing",
    "Include 'trending' keyword in title"
  ],
  "knowledge_updates": {{
    "best_niches_so_far": ["SaaS Landing Pages", "Portfolio Templates"],
    "best_price_point": 19,
    "avoid_niches": ["Generic blog templates — oversaturated"],
    "best_tags": ["website template", "landing page", "html template"],
    "pattern_recognition": "Dark mode templates get more saves/wishlists"
  }},
  "system_health": {{
    "total_products_published": {total_runs + 1},
    "estimated_store_value": "Growing",
    "next_milestone": "10 products published",
    "recommendation": "Stay consistent — compound effect kicks in at Day 30+"
  }},
  "tomorrows_focus": "React SaaS dashboard with charts — undersupplied in market"
}}

Think deeply. This self-analysis makes the system smarter every day.
Your improvements compound over time into a dominant automated business.
"""

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=3000,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    assessment = json.loads(raw.strip())

    # ── Update performance knowledge base ──────────────────
    if "history" not in performance:
        performance["history"] = []

    performance["history"].append({
        "date": TODAY,
        "run_number": total_runs + 1,
        "product_published": published.get("product_title", "Unknown"),
        "score": assessment["todays_assessment"]["overall_score"],
        "improvements": assessment["improvements_for_tomorrow"]
    })
    performance["history"] = performance["history"][-60:]  # Keep last 60 days
    performance["knowledge"] = assessment["knowledge_updates"]
    performance["latest_assessment"] = assessment

    # Save updated performance
    (KNOWLEDGE / "performance.json").write_text(json.dumps(performance, indent=2))

    # Save today's improvement report
    (KNOWLEDGE / f"improvement_{TODAY}.json").write_text(json.dumps(assessment, indent=2))

    # ── Generate daily summary report ──────────────────────
    summary = f"""
# 🤖 AutoBusiness Daily Report — {TODAY}
## Run #{total_runs + 1}

### ✅ Today's Product
- **Title**: {published.get('product_title', 'N/A')}
- **Price**: ${published.get('price_usd', 'N/A')}
- **Status**: {published.get('status', 'N/A')}
- **URL**: {published.get('product_url', 'N/A')}

### 📊 Performance Score: {assessment['todays_assessment']['overall_score']}/10

### 🎯 Tomorrow's Focus
{assessment.get('tomorrows_focus', 'TBD')}

### 🔧 Improvements for Tomorrow
{chr(10).join(f"- {imp}" for imp in assessment['improvements_for_tomorrow'])}

### 🧠 System Learning
Total Products: {total_runs + 1}
Best Niches: {', '.join(assessment['knowledge_updates'].get('best_niches_so_far', []))}

---
*Generated by AutoBusiness AI — Zero Human Involvement*
"""
    (LOGS / f"daily_report_{TODAY}.md").write_text(summary)

    log = {
        "agent": "07_improve",
        "date": TODAY,
        "run_number": total_runs + 1,
        "status": "success",
        "overall_score": assessment["todays_assessment"]["overall_score"],
        "improvements_count": len(assessment["improvements_for_tomorrow"])
    }
    (LOGS / f"agent07_{TODAY}.json").write_text(json.dumps(log, indent=2))

    print(f"✅ Day #{total_runs + 1} complete!")
    print(f"📈 Score: {assessment['todays_assessment']['overall_score']}/10")
    print(f"🎯 Tomorrow's focus: {assessment.get('tomorrows_focus')}")
    print(f"🧠 System is learning. Getting smarter every day.")
    print("✅ Agent 07 done. Business knowledge updated.")

if __name__ == "__main__":
    run_improvement()
