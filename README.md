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
- OPENROUTER_MODEL environment variable

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
   OPENROUTER_MODEL="google/gemini-2.5-flash-preview"
   ```

4. **Run the script**
   ```sh
   python main.py
   ```

## Debugging and Testing

You can use command-line arguments to control the script's behavior for testing and debugging:

- `--dry-run`: Process highlights and print the cleaned text to the console without updating the highlights in Readwise.
- `--limit <number>`: Limit the number of highlights processed to the specified number.

Example: Run a dry run on the first 5 highlights:

```sh
python main.py --dry-run --limit 5
```

## Configuration

- The script uses the OpenRouter model specified by the `OPENROUTER_MODEL` environment variable in your `.env` file. The script will exit if this variable is not set.
- A 1-second delay is included between API calls to avoid rate limits.

## Contributing

Feel free to open issues or submit pull requests to improve this project!

## License

[MIT](LICENSE)

## Links

[Readwise API](https://readwise.io/api_deets)
[OpenRouter Docs](https://openrouter.ai/docs/quickstart)
