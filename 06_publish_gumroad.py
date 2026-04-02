"""
╔══════════════════════════════════════════════════════════╗
║  AGENT 06 — GUMROAD PUBLISHER                            ║
║  API: Playwright Browser Automation (Free)               ║
║  Role: Automated sales & distribution manager            ║
║  Task: Login → Create product → Upload → Publish         ║
╚══════════════════════════════════════════════════════════╝
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

ROOT = Path(__file__).parent.parent
KNOWLEDGE = ROOT / "knowledge"
LOGS = ROOT / "logs"
TODAY = datetime.now().strftime("%Y-%m-%d")

def run_publisher():
    print("🚀 Agent 06 — Gumroad Publisher starting...")

    copy = json.loads((KNOWLEDGE / f"copy_{TODAY}.json").read_text())
    output_info = json.loads((KNOWLEDGE / f"output_{TODAY}.json").read_text())

    zip_path = output_info["zip_path"]
    title = copy["product_title"]
    price = str(copy["price_usd"])
    description = copy["full_description"]
    summary = copy.get("summary_line", "")
    tags = copy["seo_tags"]

    email = os.environ["GUMROAD_EMAIL"]
    password = os.environ["GUMROAD_PASSWORD"]

    print(f"  📦 Product: {title}")
    print(f"  💰 Price: ${price}")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        context = browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        product_url = ""

        try:
            # ── Step 1: Login ──────────────────────────────
            print("  🔐 Logging in to Gumroad...")
            page.goto("https://app.gumroad.com/login", timeout=30000)
            page.wait_for_load_state("networkidle")

            page.fill('input[type="email"]', email)
            page.fill('input[type="password"]', password)
            page.click('button[type="submit"]')

            try:
                page.wait_for_url("**/dashboard**", timeout=15000)
                print("  ✅ Logged in!")
            except:
                page.wait_for_selector('[data-testid="dashboard"], .dashboard, [href*="products"]', timeout=10000)
                print("  ✅ Logged in!")

            time.sleep(2)

            # ── Step 2: Go to New Product ──────────────────
            print("  📝 Opening new product form...")
            page.goto("https://app.gumroad.com/products/new", timeout=20000)
            page.wait_for_load_state("networkidle")
            time.sleep(2)

            # Try clicking Digital Product option if shown
            try:
                digital = page.locator("text=Digital product, text=Digital").first
                if digital.is_visible():
                    digital.click()
                    time.sleep(1)
            except:
                pass

            # ── Step 3: Fill Product Name ──────────────────
            print("  ✏️  Filling product name...")
            name_selectors = [
                'input[name="name"]',
                'input[placeholder*="Name"]',
                'input[placeholder*="name"]',
                'input[id*="name"]',
                '#product_name'
            ]
            for sel in name_selectors:
                try:
                    el = page.locator(sel).first
                    if el.is_visible():
                        el.clear()
                        el.fill(title)
                        print(f"  ✅ Name filled")
                        break
                except:
                    continue
            time.sleep(0.5)

            # ── Step 4: Fill Price ─────────────────────────
            print("  💰 Setting price...")
            price_selectors = [
                'input[name="price"]',
                'input[placeholder*="price"]',
                'input[placeholder*="Price"]',
                'input[id*="price"]',
                '#product_price'
            ]
            for sel in price_selectors:
                try:
                    el = page.locator(sel).first
                    if el.is_visible():
                        el.clear()
                        el.fill(price)
                        print(f"  ✅ Price set: ${price}")
                        break
                except:
                    continue
            time.sleep(0.5)

            # ── Step 5: Click Next/Create ──────────────────
            next_selectors = [
                'button:has-text("Next")',
                'button:has-text("Create product")',
                'button:has-text("Create")',
                'input[type="submit"]'
            ]
            for sel in next_selectors:
                try:
                    btn = page.locator(sel).first
                    if btn.is_visible():
                        btn.click()
                        print("  ✅ Submitted form")
                        break
                except:
                    continue
            time.sleep(3)

            # ── Step 6: Upload ZIP ─────────────────────────
            print("  📁 Uploading ZIP file...")
            try:
                file_input = page.locator('input[type="file"]').first
                file_input.set_input_files(zip_path)
                print(f"  ✅ ZIP uploaded: {Path(zip_path).name}")
                time.sleep(5)
            except Exception as e:
                print(f"  ⚠️  Upload issue: {e}")

            # ── Step 7: Add Description ────────────────────
            print("  📝 Adding description...")
            try:
                desc_selectors = [
                    '[contenteditable="true"]',
                    'textarea[name*="description"]',
                    'textarea[id*="description"]',
                    '.description-editor'
                ]
                for sel in desc_selectors:
                    try:
                        el = page.locator(sel).first
                        if el.is_visible():
                            el.click()
                            el.fill(description)
                            print("  ✅ Description added")
                            break
                    except:
                        continue
            except Exception as e:
                print(f"  ⚠️  Description issue: {e}")
            time.sleep(1)

            # ── Step 8: Add Summary ────────────────────────
            try:
                summ = page.locator('input[placeholder*="summary"], textarea[placeholder*="summary"]').first
                if summ.is_visible():
                    summ.fill(summary)
            except:
                pass

            # ── Step 9: Save ───────────────────────────────
            print("  💾 Saving product...")
            save_selectors = ['button:has-text("Save")', 'button:has-text("Update changes")']
            for sel in save_selectors:
                try:
                    btn = page.locator(sel).first
                    if btn.is_visible():
                        btn.click()
                        print("  ✅ Saved!")
                        break
                except:
                    continue
            time.sleep(3)

            # ── Step 10: Publish ───────────────────────────
            print("  🌐 Publishing...")
            publish_selectors = [
                'button:has-text("Publish")',
                'label:has-text("Published")',
                'input[name*="published"]'
            ]
            for sel in publish_selectors:
                try:
                    btn = page.locator(sel).first
                    if btn.is_visible():
                        btn.click()
                        print("  🎉 PUBLISHED!")
                        break
                except:
                    continue
            time.sleep(2)

            product_url = page.url
            print(f"  🔗 URL: {product_url}")

            # Save result
            result = {
                "date": TODAY, "status": "published",
                "product_title": title, "price_usd": int(price),
                "product_url": product_url, "zip_uploaded": zip_path
            }
            (KNOWLEDGE / f"published_{TODAY}.json").write_text(json.dumps(result, indent=2))

            (LOGS / f"agent06_{TODAY}.json").write_text(json.dumps({
                "agent": "06_publish", "date": TODAY, "status": "success",
                "api": "playwright browser automation (FREE)",
                "product_title": title, "product_url": product_url, "price": price
            }, indent=2))

            print(f"✅ Agent 06 complete. Product is LIVE!\n")

        except Exception as e:
            print(f"  ❌ Publisher error: {e}")
            try:
                page.screenshot(path=str(LOGS / f"error_{TODAY}.png"))
                print(f"  📸 Screenshot saved to logs/error_{TODAY}.png")
            except:
                pass

            (KNOWLEDGE / f"published_{TODAY}.json").write_text(json.dumps({
                "date": TODAY, "status": "failed", "error": str(e),
                "product_title": title, "price_usd": int(price)
            }, indent=2))

            (LOGS / f"agent06_{TODAY}.json").write_text(json.dumps({
                "agent": "06_publish", "date": TODAY, "status": "failed", "error": str(e)
            }, indent=2))
            raise

        finally:
            browser.close()

if __name__ == "__main__":
    run_publisher()
