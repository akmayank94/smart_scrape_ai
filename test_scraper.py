# This is a simple test script to run the scraper without Streamlit

from scraper.scrape_engine import scrape_website

# Replace with a test website URL that loads fast and has simple structure
test_url = "https://en.wikipedia.org/wiki/2024_Summer_Olympics_medal_table"  # Perfect for scraping practice

# Call the function
html_path = scrape_website(
    url=test_url,
    headless=False,         # Show browser for debugging
    captcha_mode=False      # No CAPTCHA handling in this test
)

print(f"HTML saved at: {html_path}")