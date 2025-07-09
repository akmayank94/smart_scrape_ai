"""
Main Streamlit control panel UI
- Webpage which will be visible to users 
- include taking url/htmlfile as an input 
- AI promptbox for processing that data based on user needs
- chunksize selection if data is huge 
- mode
"""
import streamlit as st
import pandas as pd
from io import BytesIO
import os

from scraper.scrape_engine import scrape_website
from parser.html_parser import extract_tables_from_html
from llm.batch_manager import process_table_with_ai


st.set_page_config(page_title="Smart Scraper", page_icon="🕷️")

st.title("🕷️ Smart Scraper 🔄")
st.markdown("""
            
It's an intelligent, customizable web scraping assistant tool with AI integration.
This tool allows you to extract data from most of the websites in structured format and process it using a powerful AI model (LLaMA 3.1).

**Start by entering a website URL or uploading an HTML file.**
""")

# Model Display (locked to local LLaMA model)
st.info("**Using AI Model**: LLaMA 3.1 via Ollama (runs locally)")
# TODO: In future, add optional model selector for GPT-4 or others

url = st.text_input("🔗 Enter website URL to scrape:", placeholder="https://smartscrape.com")

# Optional HTML file Uploading option
uploaded_html = st.file_uploader("📁 Or upload a saved HTML file", type=["html", "htm"])

prompt = st.text_area("💬 Enter your instruction for the AI to process the data", height=120, placeholder="e.g., Clean missing values, normalize column names, drop duplicates etc...")

chunk_size = st.slider("📦 Max rows per batch for LLM", min_value=100, max_value=2000, step=100, value=500)

captcha_mode = st.checkbox("🔐 Enable CAPTCHA mode (manual solve for protected sites)", value=False)

# hardcoded for now
model_name = "LLaMA 3.1 (local via Ollama)"

# Scrape button (updated)
if st.button("🚀 Start Scraping & AI Processing"):

    if not url and not uploaded_html:
        st.warning("⚠️ Please provide a website URL or upload an HTML file.")
    elif not prompt.strip():
        st.warning("⚠️ Please enter an instruction for the AI.")
    else:
        with st.spinner("🔄 Scraping and processing... please wait..."):

            # Step 1: SCRAPE
            if url:
                html_path = scrape_website(url, headless=True, captcha_mode=captcha_mode)
            elif uploaded_html:
                # Save uploaded file
                html_path = "data/raw/uploaded_page.html"
                with open(html_path, "wb") as f:
                    f.write(uploaded_html.read())

            if not html_path or not os.path.exists(html_path):
                st.error("❌ Failed to scrape or load the webpage.")
            else:
                # Step 2: PARSE TABLES
                tables = extract_tables_from_html(html_path)

                if not tables:
                    st.warning("⚠️ No tables found on the webpage.")
                else:
                    final_dfs = []
                    for i, df in enumerate(tables):
                        st.info(f"🔎 Processing Table {i+1} ({df.shape[0]} rows)...")
                        cleaned_df = process_table_with_ai(df, prompt, chunk_size=chunk_size)
                        final_dfs.append(cleaned_df)

                    # Merge cleaned tables
                    final_df = pd.concat(final_dfs, ignore_index=True)

                    # Show preview
                    st.success("✅ Processing Complete!")
                    st.dataframe(final_df.head(100))

                    # Download buttons
                    st.download_button("📥 Download CSV", data=final_df.to_csv(index=False), file_name="smart_scraped.csv", mime="text/csv")

                    excel_buffer = BytesIO()
                    final_df.to_excel(excel_buffer, index=False)
                    st.download_button("📥 Download Excel", data=excel_buffer.getvalue(), file_name="smart_scraped.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


# Output Preview (Placeholder)
with st.expander("📄 Output Preview (Coming Soon)"):
    st.write("Once data is processed, it will appear here with options to compare raw vs cleaned data and export final CSV.")
