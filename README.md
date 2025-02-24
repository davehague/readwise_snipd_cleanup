# Readwise Podcast Highlight Cleaner

This script fetches highlights from Readwise that are categorized as "podcasts," processes them using an LLM via OpenRouter to clean and structure the text, and updates them back to Readwise.

## Features
- Fetches all books from Readwise and filters for those categorized as "podcasts."
- Retrieves all highlights from Readwise with pagination.
- Filters highlights that contain a standalone `Transcript:` line.
- Sends highlights to OpenRouter (Claude 3.5 Sonnet) for cleaning and structuring.
- Updates the cleaned highlights back to Readwise.

## Requirements
- Python 3.12+ (untested below that, but could work)
- Readwise API Key
- OpenRouter API Key

## Setup

1. **Clone the repository**
   ```sh
   git clone https://github.com/yourusername/readwise-podcast-cleaner.git
   cd readwise-podcast-cleaner
   ```

2. **Create a virtual environment and install dependencies**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. **Create a `.env` file in the root directory and add:**
   ```ini
   READWISE_API_KEY=your_readwise_api_key_here
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   ```

4. **Run the script**
   ```sh
   python main.py
   ```

## Configuration
- The script currently uses the OpenRouter model `anthropic/claude-3.5-sonnet`.
- A 1-second delay is included between API calls to avoid rate limits.

## Contributing
Feel free to open issues or submit pull requests to improve this project!

## License
[MIT](LICENSE)

