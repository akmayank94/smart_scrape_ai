"""
Parses saved HTML pages and extracts <table> elements as structured data.
Used by: Streamlit UI & LLM Pipeline
"""

from bs4 import BeautifulSoup
import pandas as pd
import os

def extract_tables_from_html(html_path: str) -> list:
    """
    Parses HTML and extracts all <table> elements into Pandas DataFrames.

    Args:
        html_path (str): Path to the saved HTML file

    Returns:
        List of Pandas DataFrames, one for each table found
    """
    tables = []

    # Check if file exists
    if not os.path.exists(html_path):
        print(f"❌ HTML file not found: {html_path}")
        return tables

    # Load the HTML content
    with open(html_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "lxml")

    # Find all <table> elements
    raw_tables = soup.find_all("table")
    print(f"🔍 Found {len(raw_tables)} table(s) in HTML")

    # Loop through each <table> and convert to DataFrame
    for i, table in enumerate(raw_tables):
        df = pd.read_html(str(table), flavor="lxml")[0]
        tables.append(df)
        print(f"✅ Table {i+1} extracted: {df.shape[0]} rows × {df.shape[1]} columns")

    return tables

# Optional: preview helper
def print_table_sample(tables: list):
    """
    Prints the first few rows of all extracted tables for debugging
    """
    for i, df in enumerate(tables):
        print(f"\n📊 Table {i+1}")
        print(df.head())
