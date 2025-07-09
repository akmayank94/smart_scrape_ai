"""
Handles batching of large tables and sending each chunk to the LLM.

Used by: LLM engine (ollama_client) and Streamlit pipeline
"""

import pandas as pd
from io import StringIO
from llm.ollama_client import call_llm_with_prompt

def split_dataframe(df: pd.DataFrame, chunk_size: int) -> list:
    """
    Splits a DataFrame into smaller row-wise chunks

    Args:
        df (DataFrame): The full table
        chunk_size (int): Max number of rows per chunk

    Returns:
        List of DataFrames
    """
    return [df.iloc[i:i + chunk_size] for i in range(0, len(df), chunk_size)]

def process_table_with_ai(df: pd.DataFrame, prompt: str, chunk_size: int = 500) -> pd.DataFrame:
    """
    Processes a large DataFrame in chunks using an LLM.

    Args:
        df (DataFrame): Raw table
        prompt (str): User instruction for transformation
        chunk_size (int): Max rows per batch to send to LLM

    Returns:
        DataFrame: Combined, transformed table
    """
    all_chunks = split_dataframe(df, chunk_size)
    processed_chunks = []

    for i, chunk in enumerate(all_chunks):
        print(f"📦 Sending chunk {i+1}/{len(all_chunks)} to LLM...")

        # Convert DataFrame to markdown table string
        markdown_table = chunk.to_markdown(index=False)

        # Construct final prompt ( now updated after creating prompt_formater.py)
        from llm.prompt_formatter import create_cleaning_prompt
        final_prompt = create_cleaning_prompt(chunk, prompt)

        # Send to LLM (Ollama backend)
        result_md = call_llm_with_prompt(final_prompt)

        # Parse back from markdown to DataFrame
        try:
            # cleaned_df = pd.read_table(pd.compat.StringIO(result_md), sep="|", engine="python", skiprows=1)
            cleaned_df = pd.read_table(StringIO(result_md), sep="|", engine="python", skiprows=1)
            cleaned_df = cleaned_df.loc[:, ~cleaned_df.columns.str.contains('^Unnamed')]  # Remove empty cols
            processed_chunks.append(cleaned_df)
        except Exception as e:
            print(f"❌ Failed to parse AI output for chunk {i+1}: {e}")

    # Merge all cleaned chunks
    if processed_chunks:
        final_df = pd.concat(processed_chunks, ignore_index=True)
        return final_df
    else:
        print("⚠️ No valid output from AI")
        return pd.DataFrame()
