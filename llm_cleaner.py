"""Shared LLM text cleaning functionality."""

import requests
import json

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def clean_text_with_llm(text, model, api_key):
    """
    Send text to OpenRouter for cleaning and return the response.
    
    Args:
        text: The text to clean
        model: The OpenRouter model to use
        api_key: The OpenRouter API key
    
    Returns:
        Cleaned text from the LLM
    """
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "Only perform the action the user specifies. Do not add a greeting, preface, or summary of your work.",
            },
            {
                "role": "user",
                "content": f"I need your help cleaning up some book notes from Readwise. These passages are too long and need to be broken into readable chunks. When you see three dots (...) that means there was a concatenation from the book, so it's a good place to make a new paragraph (please remove the 3 dots). If there are no dots, look for a logical place to start a new paragraph. Don't give an explanation of your work. If the last part of the text looks like '(Author Name, Book Title)' that's the source - don't include it in your results. Also, don't include any leading or trailing quotation marks in your response. I'll post the passages one at a time for you to clean up. Remove meta information as well such as the word 'Transcript' and the 'Speaker 1', 'Speaker 2' annotations.\n* Remove filler words and phrases like 'you know' and 'kind of' to make the text more concise.\n* Keep paragraphs relatively short, with each focusing on a single main idea or point.\n* Remove redundant information or repetitive phrases but keep the tone of the speaker.\n* If there is a title, keep it\n* Use bullet points for structured processes or lists.\n* Transform streams of questions into bullet points when they form a coherent list\nHighlight is as follows:\n\n{text}",
            },
        ],
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    response = requests.post(OPENROUTER_URL, data=json.dumps(payload), headers=headers)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]