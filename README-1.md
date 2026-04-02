# 🤖 Zero-Cost Gumroad Template Automation

> Fully automated: Market Research → Template Generation → SEO → Publish to Gumroad
> **$0 cost. Zero human involvement. Runs daily on GitHub Actions.**

---

## 🏗️ System Architecture

```
GitHub Actions (Daily Cron)
        │
        ▼
1. 🔍 MARKET RESEARCH      ← Scrapes trending templates, competitor pricing
        │
        ▼
2. 🧠 AI STRATEGY          ← Claude picks best niche, title, price, tags
        │
        ▼
3. 🎨 TEMPLATE GENERATION  ← Generates full HTML/CSS/JS/React template
        │
        ▼
4. 📦 PACKAGE & ZIP        ← Zips template + README + license
        │
        ▼
5. 🚀 PUBLISH TO GUMROAD   ← Playwright browser automation (no API needed)
        │
        ▼
6. 📊 LOG & IMPROVE        ← Saves results, improves daily prompts
```

---

## 📁 Repository Structure

```
your-repo/
├── .github/
│   └── workflows/
│       └── daily-automation.yml     ← GitHub Actions cron job
├── scripts/
│   ├── 1_market_research.py         ← Scrapes trends & competitors
│   ├── 2_ai_strategy.py             ← Claude picks niche & strategy
│   ├── 3_generate_template.py       ← Claude generates the template
│   ├── 4_package.py                 ← Zips everything up
│   ├── 5_publish_gumroad.py         ← Playwright publishes to Gumroad
│   └── 6_log_results.py             ← Logs & self-improves
├── templates/                       ← Generated templates stored here
├── logs/                            ← Daily run logs
├── knowledge/
│   ├── trends.json                  ← Accumulated market knowledge
│   └── performance.json             ← What sold, what didn't
└── requirements.txt
```

---

## 