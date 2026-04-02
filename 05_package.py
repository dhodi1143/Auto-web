"""
╔══════════════════════════════════════════════════════════╗
║  AGENT 05 — PRODUCT PACKAGER                             ║
║  API: None (Pure Python — always free)                   ║
║  Role: Quality assurance + delivery engineer             ║
║  Task: Validate, quality check, and ZIP the template     ║
╚══════════════════════════════════════════════════════════╝
"""

import json
import os
import zipfile
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
KNOWLEDGE = ROOT / "knowledge"
OUTPUTS = ROOT / "outputs"
LOGS = ROOT / "logs"
OUTPUTS.mkdir(exist_ok=True)
TODAY = datetime.now().strftime("%Y-%m-%d")

def run_packaging():
    print("📦 Agent 05 — Product Packager running quality checks...")

    template_info = json.loads((KNOWLEDGE / f"template_path_{TODAY}.json").read_text())
    copy = json.loads((KNOWLEDGE / f"copy_{TODAY}.json").read_text())
    template_dir = Path(template_info["template_dir"])
    slug = template_info["slug"]

    # ── Quality Checks ──────────────────────────────────────
    html_path = template_dir / "index.html"
    html = html_path.read_text() if html_path.exists() else ""

    checks = {
        "index.html exists": html_path.exists(),
        "README.md exists": (template_dir / "README.md").exists(),
        "LICENSE exists": (template_dir / "LICENSE").exists(),
        "CUSTOMIZATION.md exists": (template_dir / "CUSTOMIZATION.md").exists(),
        "Has DOCTYPE": "<!DOCTYPE" in html.upper(),
        "Has viewport meta": "viewport" in html,
        "Has title tag": "<title>" in html.lower(),
        "Has style tag": "<style>" in html.lower(),
        "Has script tag": "<script>" in html.lower(),
        "Has nav section": "<nav" in html.lower(),
        "Has footer": "<footer" in html.lower(),
        "Minimum size (5KB)": len(html) > 5000,
        "No lorem ipsum": "lorem ipsum" not in html.lower()
    }

    passed = sum(checks.values())
    total = len(checks)
    score = round(passed / total * 10, 1)

    print(f"\n  📋 Quality Report ({passed}/{total} checks passed — Score: {score}/10):")
    for check, result in checks.items():
        print(f"    {'✅' if result else '❌'} {check}")

    if passed < total * 0.75:
        raise ValueError(f"❌ Quality too low ({passed}/{total}). Aborting packaging.")

    # ── Create ZIP ──────────────────────────────────────────
    zip_name = f"{slug}_{TODAY}.zip"
    zip_path = OUTPUTS / zip_name

    print(f"\n  📦 Creating ZIP: {zip_name}")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in sorted(template_dir.iterdir()):
            zf.write(file, arcname=file.name)
            size_kb = file.stat().st_size / 1024
            print(f"    📄 {file.name} ({size_kb:.1f} KB)")

    zip_size_kb = zip_path.stat().st_size / 1024
    print(f"\n  ✅ ZIP ready: {zip_name} ({zip_size_kb:.1f} KB)")

    # Save output info
    output_info = {
        "zip_path": str(zip_path),
        "zip_name": zip_name,
        "zip_size_kb": round(zip_size_kb, 1),
        "product_title": copy["product_title"],
        "price_usd": copy["price_usd"],
        "quality_score": score,
        "checks_passed": f"{passed}/{total}"
    }
    (KNOWLEDGE / f"output_{TODAY}.json").write_text(json.dumps(output_info, indent=2))

    (LOGS / f"agent05_{TODAY}.json").write_text(json.dumps({
        "agent": "05_package", "date": TODAY, "status": "success",
        "api": "none (pure python)",
        "zip_path": str(zip_path),
        "quality_score": score,
        "zip_size_kb": round(zip_size_kb, 1)
    }, indent=2))

    print(f"✅ Agent 05 complete. ZIP ready to sell!\n")

if __name__ == "__main__":
    run_packaging()
