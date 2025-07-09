"""
prompt_formatter.py
-------------------
Creates clean and standardized prompts for the LLM.

Used by: batch_manager.py (and future AI modes)
"""

import pandas as pd

def create_cleaning_prompt(dataframe_chunk: pd.DataFrame, user_instruction: str) -> str:
    """
    Generates a markdown-formatted prompt for the LLM.

    Args:
        dataframe_chunk (pd.DataFrame): A portion of the full table
        user_instruction (str): What the user wants the AI to do

    Returns:
        str: Full LLM prompt with table + instructions
    """

    markdown_table = dataframe_chunk.to_markdown(index=False)

    prompt = f"""
You are a helpful data assistant.

Below is a table in markdown format:

{markdown_table}

Your task is:  
{user_instruction}

Please return ONLY the cleaned table in markdown format.
Do NOT include any extra commentary or headers outside the table.
    """

    return prompt.strip()
