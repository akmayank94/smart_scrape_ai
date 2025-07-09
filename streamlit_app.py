"""
Main Streamlit control panel UI
- Webpage which will be visible to users 
- include taking url/htmlfile as an input 
- AI promptbox for processing that data based on user needs
- chunksize selection if data is huge 
- mode
"""
import streamlit as st
import os

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

# Scrape button
if st.button("🚀 Start Scraping & AI Processing"):

    # Validate user input
    if not url and not uploaded_html:
        st.warning("⚠️ Please provide a website URL or upload an HTML file.")
    elif not prompt.strip():
        st.warning("⚠️ Please provide a prompt for the AI to understand what to do.")
    else:
        st.success("✅ Input received! Starting the scraping and cleaning pipeline...")
        st.info("🚧 Functionality coming next: This button will trigger the backend pipeline (scraper → parser → batcher → AI → export)")
        # 🚧 This is where you will integrate the backend logic in later stages


# Output Preview (Placeholder)
with st.expander("📄 Output Preview (Coming Soon)"):
    st.write("Once data is processed, it will appear here with options to compare raw vs cleaned data and export final CSV.")
