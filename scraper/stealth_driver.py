"""
Creates a Selenium Chrome driver with stealth settings which helps avoid detection on websites that block bots.

Used by: scrape_engine.py
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Optional: stealth mode (can be expanded)
def get_stealth_driver(headless=True):
    """
    Initializes and returns a Chrome driver with options.

    Args:
        headless (bool): Whether to run Chrome in headless mode (no GUI)

    Returns:
        driver (webdriver.Chrome): A configured Selenium Chrome driver
    """

    chrome_options = Options()

    # Basic settings
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Run in headless mode (invisible browser window)
    if headless:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")

    # Pretend to be a real user (optional tweaks)
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    # Create and return driver using ChromeDriverManager
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Further anti-detection tweaks (if needed)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        """
    })

    return driver