"""
╔══════════════════════════════════════════════════════════╗
║  AGENT 03 — SENIOR DEVELOPER                             ║
║  Role: Principal engineer, 20yr veteran                  ║
║  Task: Generate production-quality website template      ║
╚══════════════════════════════════════════════════════════╝
"""

import json
import os
from datetime import datetime
from pathlib import Path
import anthropic

ROOT = Path(__file__).parent.parent
KNOWLEDGE = ROOT / "knowledge"
TEMPLATES = ROOT / "templates"
LOGS = ROOT / "logs"
TEMPLATES.mkdir(exist_ok=True)
TODAY = datetime.now().strftime("%Y-%m-%d")

def run_generation():
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    strategy_file = KNOWLEDGE / f"strategy_{TODAY}.json"
    strategy = json.loads(strategy_file.read_text())
    bp = strategy["product_blueprint"]

    slug = bp["file_name_slug"]
    output_dir = TEMPLATES / f"{slug}_{TODAY}"
    output_dir.mkdir(exist_ok=True)

    print(f"👨‍💻 Senior Developer building: {bp['template_name']}...")

    # ── Generate main HTML ───────────────────────────────────
    html_prompt = f"""
You are a principal software engineer and UI/UX expert with 20 years of experience 
building world-class web products. You have shipped templates that earned $100k+.

Build this template EXACTLY to spec:
{json.dumps(bp, indent=2)}

Rules:
- Write COMPLETE, PRODUCTION-READY code. No placeholders, no "// add your code here"
- Every section listed in sections_to_include must be fully built
- CSS must be embedded in <style> tags (single file)
- JS must be embedded in <script> tags (single file)  
- Use Google Fonts via CDN link (free)
- Use Font Awesome via CDN for icons (free)
- Code must be beautiful, well-commented, professional
- Include smooth scroll animations using Intersection Observer API
- Mobile responsive with proper media queries
- All CSS variables defined at :root for easy customization
- Add a "Powered by template" comment at bottom only

Return ONLY the complete HTML file content. No explanation. No markdown. Just pure HTML.
"""

    print("  → Generating HTML template (this takes ~60 seconds)...")
    html_response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=8000,
        messages=[{"role": "user", "content": html_prompt}]
    )

    html_content = html_response.content[0].text.strip()
    # Remove markdown if present
    if html_content.startswith("```"):
        lines = html_content.split("\n")
        html_content = "\n".join(lines[1:-1])

    (output_dir / "index.html").write_text(html_content)
    print(f"  ✅ index.html generated ({len(html_content)} chars)")

    # ── Generate README.md ──────────────────────────────────
    readme_prompt = f"""
Write a professional, detailed README.md for this template product:

Template name: {bp['template_name']}
Tech stack: {bp['tech_stack']}
Features: {json.dumps(bp['must_have_features'])}
Differentiators: {json.dumps(bp['differentiators'])}

Include: 
- Eye-catching header with badges
- Feature list with emojis
- Setup instructions (3 steps max)
- Customization guide (CSS variables)
- File structure
- License section (MIT)
- Support section

Make it look extremely professional. Return ONLY the markdown content.
"""

    readme_response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2000,
        messages=[{"role": "user", "content": readme_prompt}]
    )

    readme_content = readme_response.content[0].text.strip()
    if readme_content.startswith("```"):
        lines = readme_content.split("\n")
        readme_content = "\n".join(lines[1:-1])

    (output_dir / "README.md").write_text(readme_content)
    print("  ✅ README.md generated")

    # ── Generate LICENSE ────────────────────────────────────
    license_text = f"""MIT License

Copyright (c) {datetime.now().year} AutoBusiness

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
"""
    (output_dir / "LICENSE").write_text(license_text)
    print("  ✅ LICENSE generated")

    # ── Generate CUSTOMIZATION.md ───────────────────────────
    custom_prompt = f"""
Write a CUSTOMIZATION.md guide for: {bp['template_name']}

Cover:
- How to change colors (CSS variables)
- How to change fonts
- How to add/remove sections
- How to deploy to Netlify/Vercel (free hosting)
- Common customizations with code examples

Be super friendly and clear. Return ONLY markdown. No backtick wrapper.
"""

    custom_response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1500,
        messages=[{"role": "user", "content": custom_prompt}]
    )
    (output_dir / "CUSTOMIZATION.md").write_text(custom_response.content[0].text.strip())
    print("  ✅ CUSTOMIZATION.md generated")

    # Save template path to knowledge
    knowledge_update = {
        "template_dir": str(output_dir),
        "slug": slug,
        "files": ["index.html", "README.md", "LICENSE", "CUSTOMIZATION.md"]
    }
    (KNOWLEDGE / f"template_path_{TODAY}.json").write_text(json.dumps(knowledge_update, indent=2))

    log = {
        "agent": "03_generate_template",
        "date": TODAY,
        "status": "success",
        "template_name": bp["template_name"],
        "files_generated": 4,
        "html_size_chars": len(html_content)
    }
    (LOGS / f"agent03_{TODAY}.json").write_text(json.dumps(log, indent=2))

    print(f"✅ Agent 03 done. Template saved to: {output_dir}")

if __name__ == "__main__":
    run_generation()
