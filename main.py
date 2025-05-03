import os
import time
import requests
import json
from dotenv import load_dotenv
import argparse  # Import argparse

# Load API keys from .env
load_dotenv()
READWISE_API_KEY = os.getenv("READWISE_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL")
BASE_URL = "https://readwise.io/api/v2"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {"Authorization": f"Token {READWISE_API_KEY}"}

if not OPENROUTER_MODEL:
    print("Error: OPENROUTER_MODEL environment variable not set.")
    exit(1)

# Setup argument parser
parser = argparse.ArgumentParser(
    description="Clean Readwise podcast highlights using an LLM."
)
parser.add_argument(
    "--dry-run",
    action="store_true",
    help="Process highlights and print cleaned text without updating Readwise.",
)
parser.add_argument(
    "--limit", type=int, help="Limit the number of highlights to process."
)
args = parser.parse_args()


def get_all_books():
    """Fetch all books with a max page size of 1000."""
    url = f"{BASE_URL}/books/?page_size=1000"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json().get("results", [])


def get_all_highlights():
    """Fetch all highlights with a max page size of 1000, paginating as needed."""
    highlights = []
    page = 1
    while True:
        url = f"{BASE_URL}/highlights/?page={page}&page_size=1000"
        print(f"Getting highlights, page {page}...")
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        batch = data.get("results", [])

        if not batch:
            break

        highlights.extend(batch)
        if not data.get("next"):
            break

        page += 1
        time.sleep(1)  # Delay to prevent hitting rate limits

    return highlights


def filter_podcast_highlights(books, highlights):
    """Find highlights that belong to books categorized as 'podcasts' and contain 'Transcript:'"""
    podcast_book_ids = {
        book["id"] for book in books if book.get("category") == "podcasts"
    }
    return [
        h
        for h in highlights
        if h["book_id"] in podcast_book_ids and "Transcript:" in h["text"]
    ]


def clean_highlight_with_llm(text):
    """Send highlight text to OpenRouter for cleaning and return the response."""
    payload = {
        "model": OPENROUTER_MODEL,
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
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    response = requests.post(OPENROUTER_URL, data=json.dumps(payload), headers=headers)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def update_highlight(highlight_id, cleaned_text):
    """Update a highlight in Readwise with cleaned text."""
    url = f"{BASE_URL}/highlights/{highlight_id}/"
    payload = {"text": cleaned_text}
    response = requests.patch(url, headers=HEADERS, data=payload)
    response.raise_for_status()
    return response.json()


def main():
    books = get_all_books()
    print(f"Found {len(books)} books.")

    highlights = get_all_highlights()
    print(f"Found {len(highlights)} highlights.")

    filtered_highlights = filter_podcast_highlights(books, highlights)
    print(f"Total highlights to process: {len(filtered_highlights)}")

    if args.limit:
        filtered_highlights = filtered_highlights[: args.limit]
        print(f"Processing a limited number of {len(filtered_highlights)} highlights.")

    index = 1
    total = len(filtered_highlights)
    for highlight in filtered_highlights:
        print(f"Processing highlight {index} of {total}")
        index += 1
        cleaned_text = clean_highlight_with_llm(highlight["text"])

        if args.dry_run:
            print("\n--- Cleaned Text (Dry Run) ---")
            print(cleaned_text)
            print("----------------------------\n")
        else:
            update_highlight(highlight["id"], cleaned_text)
            # time.sleep(1)  # Small delay to avoid overwhelming the API

    if args.dry_run:
        print("Dry run complete. No highlights were updated.")
    else:
        print("All highlights updated successfully.")

    return filtered_highlights


if __name__ == "__main__":
    main()
