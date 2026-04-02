"""
╔══════════════════════════════════════════════════════════╗
║  AGENT 05 — PRODUCT PACKAGER                             ║
║  Role: Quality assurance + delivery engineer             ║
║  Task: Package, validate, and zip the template           ║
╚══════════════════════════════════════════════════════════╝
"""

import json
import os
import zipfile
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
KNOWLEDGE = ROOT / "knowledge"
OUTPUTS = ROOT / "outputs"
LOGS = ROOT / "logs"
OUTPUTS.mkdir(exist_ok=True)
TODAY = datetime.now().strftime("%Y-%m-%d")

def run_packaging():
    # Load paths
    template_path_file = KNOWLEDGE / f"template_path_{TODAY}.json"
    template_info = json.loads(template_path_file.read_text())
    template_dir = Path(template_info["template_dir"])
    slug = template_info["slug"]

    strategy = json.loads((KNOWLEDGE / f"strategy_{TODAY}.json").read_text())
    copy = json.loads((KNOWLEDGE / f"copy_{TODAY}.json").read_text())

    print(f"📦 Packaging template: {template_dir.name}")

    # ── Quality Checks ──────────────────────────────────────
    required_files = ["index.html", "README.md", "LICENSE", "CUSTOMIZATION.md"]
    missing = [f for f in required_files if not (template_dir / f).exists()]

    if missing:
        raise FileNotFoundError(f"❌ Missing required files: {missing}")

    html_content = (template_dir / "index.html").read_text()

    checks = {
        "has_html_tag": "<html" in html_content,
        "has_head_tag": "<head" in html_content,
        "has_body_tag": "<body" in html_content,
        "has_responsive_meta": "viewport" in html_content,
        "has_title_tag": "<title>" in html_content,
        "has_css": "<style>" in html_content or "stylesheet" in html_content,
        "has_js": "<script>" in html_content,
        "min_size_chars": len(html_content) > 5000,
        "no_placeholder_text": "lorem ipsum" not in html_content.lower()[:500]
    }

    passed = sum(checks.values())
    total = len(checks)
    print(f"  🔎 Quality checks: {passed}/{total} passed")

    for check, result in checks.items():
        status = "✅" if result else "⚠️"
        print(f"    {status} {check}")

    if passed < total * 0.8:
        raise ValueError(f"❌ Template failed quality checks ({passed}/{total})")

    # ── Create ZIP ──────────────────────────────────────────
    zip_name = f"{slug}_{TODAY}.zip"
    zip_path = OUTPUTS / zip_name

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in template_dir.iterdir():
            zf.write(file, arcname=file.name)
            print(f"  📄 Added: {file.name} ({file.stat().st_size:,} bytes)")

    zip_size = zip_path.stat().st_size
    print(f"\n  📦 ZIP created: {zip_name} ({zip_size:,} bytes)")

    # ── Save output info ────────────────────────────────────
    output_info = {
        "zip_path": str(zip_path),
        "zip_name": zip_name,
        "zip_size_bytes": zip_size,
        "product_title": copy["product_title"],
        "price_usd": copy["price_usd"],
        "files_included": required_files,
        "quality_score": passed / total
    }
    (KNOWLEDGE / f"output_{TODAY}.json").write_text(json.dumps(output_info, indent=2))

    log = {
        "agent": "05_package",
        "date": TODAY,
        "status": "success",
        "zip_path": str(zip_path),
        "quality_score": passed / total,
        "zip_size_bytes": zip_size
    }
    (LOGS / f"agent05_{TODAY}.json").write_text(json.dumps(log, indent=2))

    print(f"✅ Agent 05 done. ZIP ready: {zip_path}")

if __name__ == "__main__":
    run_packaging()
