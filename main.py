import os
import time
import requests
from dotenv import load_dotenv
import argparse
from llm_cleaner import clean_text_with_llm

# Load API keys from .env
load_dotenv()
READWISE_API_KEY = os.getenv("READWISE_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL")
BASE_URL = "https://readwise.io/api/v2"
HEADERS = {"Authorization": f"Token {READWISE_API_KEY}"}

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
parser.add_argument(
    "--model", type=str, help="Override the OpenRouter model specified in .env"
)
args = parser.parse_args()

# Override model if specified via CLI
if args.model:
    OPENROUTER_MODEL = args.model
    print(f"Using model from CLI: {OPENROUTER_MODEL}")
elif OPENROUTER_MODEL:
    print(f"Using model from .env: {OPENROUTER_MODEL}")
else:
    print("Error: No model specified. Use --model flag or set OPENROUTER_MODEL in .env")
    exit(1)


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
        cleaned_text = clean_text_with_llm(highlight["text"], OPENROUTER_MODEL, OPENROUTER_API_KEY)

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
