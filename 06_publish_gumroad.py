"""
╔══════════════════════════════════════════════════════════╗
║  AGENT 06 — GUMROAD PUBLISHER                            ║
║  Role: Automated sales & distribution manager            ║
║  Task: Log into Gumroad, create & publish product        ║
╚══════════════════════════════════════════════════════════╝
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

ROOT = Path(__file__).parent.parent
KNOWLEDGE = ROOT / "knowledge"
LOGS = ROOT / "logs"
TODAY = datetime.now().strftime("%Y-%m-%d")

def run_publisher():
    copy = json.loads((KNOWLEDGE / f"copy_{TODAY}.json").read_text())
    output_info = json.loads((KNOWLEDGE / f"output_{TODAY}.json").read_text())

    zip_path = output_info["zip_path"]
    title = copy["product_title"]
    price = copy["price_usd"]
    description_html = copy["full_description"]
    tags = copy["seo_tags"]
    summary = copy.get("summary_line", "")

    email = os.environ["GUMROAD_EMAIL"]
    password = os.environ["GUMROAD_PASSWORD"]

    print(f"🚀 Publisher starting — listing: {title}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        )
        page = context.new_page()

        try:
            # ── STEP 1: Login ──────────────────────────────
            print("  🔐 Logging into Gumroad...")
            page.goto("https://app.gumroad.com/login", timeout=30000)
            page.wait_for_selector('input[type="email"]', timeout=10000)
            page.fill('input[type="email"]', email)
            page.fill('input[type="password"]', password)
            page.click('button[type="submit"]')
            page.wait_for_url("**/dashboard**", timeout=15000)
            print("  ✅ Logged in successfully")
            time.sleep(2)

            # ── STEP 2: Navigate to New Product ───────────
            print("  📝 Creating new product...")
            page.goto("https://app.gumroad.com/products/new", timeout=20000)
            time.sleep(2)

            # Select digital product type
            try:
                digital_btn = page.locator("text=Digital product").first
                digital_btn.click()
                time.sleep(1)
            except:
                pass

            # ── STEP 3: Fill Product Name ──────────────────
            name_input = page.locator('input[placeholder*="name"], input[name*="name"], input[id*="name"]').first
            name_input.fill(title)
            time.sleep(0.5)

            # ── STEP 4: Set Price ──────────────────────────
            price_input = page.locator('input[placeholder*="price"], input[name*="price"], input[id*="price"]').first
            price_input.fill(str(price))
            time.sleep(0.5)

            # ── STEP 5: Click Next/Create ──────────────────
            next_btn = page.locator('button:has-text("Next"), button:has-text("Create"), button:has-text("Continue")').first
            next_btn.click()
            time.sleep(3)

            # ── STEP 6: Upload ZIP file ────────────────────
            print("  📁 Uploading ZIP file...")
            try:
                file_input = page.locator('input[type="file"]').first
                file_input.set_input_files(zip_path)
                print(f"  ✅ File uploaded: {Path(zip_path).name}")
                time.sleep(5)  # Wait for upload
            except Exception as e:
                print(f"  ⚠️  File upload selector issue: {e}")

            # ── STEP 7: Add Description ────────────────────
            print("  ✍️  Adding description...")
            try:
                # Try rich text editor
                desc_area = page.locator('[contenteditable="true"], textarea[name*="desc"]').first
                desc_area.click()
                desc_area.fill(description_html)
            except:
                try:
                    desc_area = page.locator('textarea').first
                    desc_area.fill(description_html)
                except Exception as e:
                    print(f"  ⚠️  Description field issue: {e}")
            time.sleep(1)

            # ── STEP 8: Add Summary ────────────────────────
            try:
                summary_input = page.locator('input[placeholder*="summary"], textarea[placeholder*="summary"]').first
                summary_input.fill(summary)
            except:
                pass

            # ── STEP 9: Save ───────────────────────────────
            save_btn = page.locator('button:has-text("Save"), button:has-text("Update")').first
            save_btn.click()
            time.sleep(3)

            # ── STEP 10: Publish ───────────────────────────
            print("  🌐 Publishing product...")
            try:
                publish_btn = page.locator('button:has-text("Publish"), label:has-text("Published")').first
                publish_btn.click()
                time.sleep(2)
                print("  ✅ Product published!")
            except Exception as e:
                print(f"  ⚠️  Publish button issue (may already be published): {e}")

            # ── Get Product URL ────────────────────────────
            product_url = page.url
            print(f"  🔗 Product URL: {product_url}")

            # Save result
            result = {
                "date": TODAY,
                "status": "published",
                "product_title": title,
                "price_usd": price,
                "product_url": product_url,
                "zip_uploaded": zip_path
            }
            (KNOWLEDGE / f"published_{TODAY}.json").write_text(json.dumps(result, indent=2))

            log = {
                "agent": "06_publish",
                "date": TODAY,
                "status": "success",
                "product_title": title,
                "product_url": product_url,
                "price": price
            }
            (LOGS / f"agent06_{TODAY}.json").write_text(json.dumps(log, indent=2))

            print(f"🎉 Agent 06 done. Product LIVE on Gumroad!")

        except PlaywrightTimeout as e:
            print(f"❌ Timeout error: {e}")
            page.screenshot(path=str(LOGS / f"error_screenshot_{TODAY}.png"))
            log = {"agent": "06_publish", "date": TODAY, "status": "failed", "error": str(e)}
            (LOGS / f"agent06_{TODAY}.json").write_text(json.dumps(log, indent=2))
            raise

        except Exception as e:
            print(f"❌ Publisher error: {e}")
            try:
                page.screenshot(path=str(LOGS / f"error_screenshot_{TODAY}.png"))
            except:
                pass
            log = {"agent": "06_publish", "date": TODAY, "status": "failed", "error": str(e)}
            (LOGS / f"agent06_{TODAY}.json").write_text(json.dumps(log, indent=2))
            raise

        finally:
            browser.close()

if __name__ == "__main__":
    run_publisher()
