"""
Main scraping logic that:
- Loads webpage via Selenium
- Scrolls for dynamic content
- Captures full page HTML
- Saves to /data/raw/scraped_page.html
"""

import os
import time
from scraper.stealth_driver import get_stealth_driver

# Where to save the scraped HTML
RAW_HTML_PATH = os.path.join("data", "raw", "scraped_page.html")

def scroll_to_bottom(driver, max_scrolls=20, delay=1.5):
    """
    Scrolls to the bottom of the page to load all lazy-loaded content.

    Args:
        driver (webdriver): Selenium driver
        max_scrolls (int): How many times to scroll
        delay (float): Seconds to wait between scrolls
    """
    last_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(max_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  # Reached the end
        last_height = new_height

def scrape_website(url: str, headless=True, captcha_mode=False) -> str:
    """
    Loads a website and saves its full HTML content.

    Args:
        url (str): Website URL to scrape
        headless (bool): Whether to run in headless mode
        captcha_mode (bool): If True, waits for user to manually solve CAPTCHA

    Returns:
        str: Path to the saved HTML file
    """
    driver = get_stealth_driver(headless=headless)

    try:
        print(f"🌐 Opening URL: {url}")
        driver.get(url)

        # If CAPTCHA mode, let user solve it manually
        if captcha_mode:
            input("🔐 CAPTCHA detected. Please solve it in the browser and press Enter to continue...")

        # Wait for initial content to load
        time.sleep(3)

        # Scroll to load more content
        scroll_to_bottom(driver)

        # Get the full rendered HTML
        html = driver.page_source

        # Save to file
        os.makedirs(os.path.dirname(RAW_HTML_PATH), exist_ok=True)
        with open(RAW_HTML_PATH, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"✅ HTML saved to {RAW_HTML_PATH}")
        return RAW_HTML_PATH

    except Exception as e:
        print(f"❌ Error during scraping: {e}")
        return None

    finally:
        driver.quit()
