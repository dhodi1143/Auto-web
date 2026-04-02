"""
╔══════════════════════════════════════════════════════════╗
║  AGENT 03 — SENIOR DEVELOPER                             ║
║  API: Google Gemini (Free Forever)                       ║
║  Role: Principal engineer, 20yr veteran                  ║
║  Task: Generate production-quality website template      ║
╚══════════════════════════════════════════════════════════╝
"""

import json
import os
from datetime import datetime
from pathlib import Path
import google.generativeai as genai

ROOT = Path(__file__).parent.parent
KNOWLEDGE = ROOT / "knowledge"
TEMPLATES = ROOT / "templates"
LOGS = ROOT / "logs"
TEMPLATES.mkdir(exist_ok=True)
TODAY = datetime.now().strftime("%Y-%m-%d")

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
# Use Pro for best code quality — still free tier
model = genai.GenerativeModel(
    "gemini-1.5-pro",
    generation_config={"max_output_tokens": 8192, "temperature": 0.7}
)

def ask_gemini(prompt):
    response = model.generate_content(prompt)
    raw = response.text.strip()
    if raw.startswith("```"):
        lines = raw.split("\n")
        raw = "\n".join(lines[1:-1])
        if raw.startswith("html") or raw.startswith("css") or raw.startswith("markdown"):
            raw = "\n".join(raw.split("\n")[1:])
    return raw.strip()

def run_generation():
    print("👨‍💻 Agent 03 — Senior Developer building template...")

    strategy = json.loads((KNOWLEDGE / f"strategy_{TODAY}.json").read_text())
    bp = strategy["product_blueprint"]
    slug = bp["file_name_slug"]

    output_dir = TEMPLATES / f"{slug}_{TODAY}"
    output_dir.mkdir(exist_ok=True)

    # ── Generate Full HTML Template ─────────────────────────
    html_prompt = f"""
You are the world's best frontend developer with 20 years of experience.
You have built templates that earned $500k+ on marketplaces like Gumroad and ThemeForest.

Build this COMPLETE, PRODUCTION-READY template from the blueprint below.
Every detail must be perfect. No shortcuts. No placeholders. Real content.

BLUEPRINT:
Name: {bp['template_name']}
Tagline: {bp['tagline']}
Colors: {json.dumps(bp['color_palette'])}
Fonts: {bp['typography']['heading_font']} for headings, {bp['typography']['body_font']} for body
Sections to build: {json.dumps(bp['sections'], indent=2)}
Must-have features: {json.dumps(bp['must_have_features'], indent=2)}
Differentiators: {json.dumps(bp['differentiators'], indent=2)}
Tech stack: {bp['tech_stack']}

RULES (strictly follow all):
1. Single HTML file with all CSS in <style> and JS in <script> tags
2. Import Google Fonts via CDN: {bp['typography']['google_fonts_url']}
3. Import Font Awesome 6 via CDN for icons: https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css
4. Define ALL colors as CSS variables in :root
5. Build ALL {len(bp['sections'])} sections completely — real text, real content, no "lorem ipsum"
6. Add smooth scroll animations with Intersection Observer API
7. Add hamburger menu for mobile
8. Make it fully responsive with media queries for 480px, 768px, 1024px
9. Add particle animation in hero section using pure JS canvas
10. CSS glassmorphism effects on cards
11. Write clean, well-commented code
12. Target customers: {bp['target_customer']}

Return ONLY the complete HTML. Nothing else. No explanation.
"""

    print("  → Gemini Pro generating full HTML template (60-90 seconds)...")
    html_content = ask_gemini(html_prompt)

    # Ensure it starts with <!DOCTYPE html>
    if not html_content.startswith("<!"):
        html_content = "<!DOCTYPE html>\n" + html_content

    (output_dir / "index.html").write_text(html_content)
    print(f"  ✅ index.html — {len(html_content):,} characters")

    # ── Generate README.md ──────────────────────────────────
    readme_prompt = f"""
Write a professional README.md for this Gumroad template product.

Product: {bp['template_name']}
Tagline: {bp['tagline']}
Tech: {bp['tech_stack']}
Features: {json.dumps(bp['must_have_features'])}
Differentiators: {json.dumps(bp['differentiators'])}
Price: ${bp['price_usd']}

Include:
- Eye-catching header with emoji badges
- Short powerful description (2 sentences)
- ✨ Features list with emojis
- 🚀 Quick Start (3 steps max)
- 🎨 Customization (how to change colors via CSS variables)
- 📁 File structure
- 🌐 Deploy to Netlify in 1 click (free hosting tip)
- 📄 MIT License section
- 💬 Support section

Make it look premium and professional. Return ONLY the markdown.
"""

    readme = ask_gemini(readme_prompt)
    if readme.startswith("```"):
        readme = "\n".join(readme.split("\n")[1:-1])
    (output_dir / "README.md").write_text(readme.strip())
    print("  ✅ README.md generated")

    # ── Generate CUSTOMIZATION.md ───────────────────────────
    custom_prompt = f"""
Write a friendly CUSTOMIZATION.md guide for: {bp['template_name']}

Cover:
1. How to change colors (CSS variables at :root)
2. How to change fonts (Google Fonts swap)
3. How to edit sections (which HTML blocks to modify)
4. How to add/remove sections
5. How to deploy FREE on Netlify (drag and drop zip)
6. How to deploy FREE on GitHub Pages
7. Code examples for common customizations

Be clear and beginner-friendly. Use code blocks. Return ONLY markdown.
"""

    custom = ask_gemini(custom_prompt)
    if custom.startswith("```"):
        custom = "\n".join(custom.split("\n")[1:-1])
    (output_dir / "CUSTOMIZATION.md").write_text(custom.strip())
    print("  ✅ CUSTOMIZATION.md generated")

    # ── Write LICENSE ───────────────────────────────────────
    license_text = f"""MIT License

Copyright (c) {datetime.now().year} AutoBusiness Templates

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
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
    (output_dir / "LICENSE").write_text(license_text)
    print("  ✅ LICENSE generated")

    # Save template path
    (KNOWLEDGE / f"template_path_{TODAY}.json").write_text(json.dumps({
        "template_dir": str(output_dir),
        "slug": slug,
        "files": ["index.html", "README.md", "CUSTOMIZATION.md", "LICENSE"],
        "html_size": len(html_content)
    }, indent=2))

    (LOGS / f"agent03_{TODAY}.json").write_text(json.dumps({
        "agent": "03_generate_template", "date": TODAY, "status": "success",
        "api": "gemini-1.5-pro (FREE)",
        "template_name": bp["template_name"],
        "html_chars": len(html_content),
        "files_created": 4
    }, indent=2))

    print(f"✅ Agent 03 complete. Template at: {output_dir}\n")

if __name__ == "__main__":
    run_generation()
