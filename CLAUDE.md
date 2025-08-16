# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python script that fetches podcast highlights from Readwise, processes them using an LLM via OpenRouter to clean and structure the text, and updates the highlights back in Readwise. The script specifically targets highlights that contain transcripts from podcasts and cleans them for better readability.

## Environment Setup

Required environment variables in `.env`:
- `READWISE_API_KEY`: Your Readwise API key
- `OPENROUTER_API_KEY`: Your OpenRouter API key  
- `OPENROUTER_MODEL`: The LLM model to use (e.g., "google/gemini-2.5-flash-preview")

## Development Commands

```bash
# Setup virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the script
python main.py

# Debugging commands
python main.py --dry-run          # Process without updating Readwise
python main.py --limit 5           # Process only first 5 highlights
python main.py --dry-run --limit 5 # Combine flags for testing
```

## Code Architecture

The codebase consists of a single main.py file with the following key functions:

- **API Integration**: Uses the Readwise API v2 for fetching/updating highlights and OpenRouter API for LLM processing
- **Filtering Logic**: Identifies podcast highlights by checking book category and presence of "Transcript:" in text
- **LLM Processing**: Sends highlights to OpenRouter with specific cleaning instructions to remove transcription artifacts, format paragraphs, and improve readability
- **Command-line Interface**: Uses argparse for --dry-run and --limit flags to support testing

The script processes highlights in batches with pagination support (1000 items per page) and includes rate limiting delays between API calls.