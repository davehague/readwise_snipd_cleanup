# Readwise Podcast Highlight Cleaner

This project includes two scripts:
1. `main.py` - Fetches highlights from Readwise that are categorized as "podcasts," processes them using an LLM via OpenRouter to clean and structure the text, and updates them back to Readwise.
2. `single.py` - Processes a single text snippet or file using the same LLM cleaning logic.

## Features

### Main Script (main.py)
- Fetches all books from Readwise and filters for those categorized as "podcasts"
- Retrieves all highlights from Readwise with pagination support
- Filters highlights that contain "Transcript:" text
- Sends highlights to OpenRouter for cleaning and structuring using your chosen LLM model
- Updates the cleaned highlights back to Readwise

### Single Text Processor (single.py)
- Processes individual text snippets or files without Readwise integration
- Supports both command-line text input and file input
- Uses the same LLM cleaning logic as the main script
- Can save cleaned output to a file

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

### Main Script (main.py)

You can use command-line arguments to control the script's behavior for testing and debugging:

- `--dry-run`: Process highlights and print the cleaned text to the console without updating the highlights in Readwise.
- `--limit <number>`: Limit the number of highlights processed to the specified number.
- `--model <model_name>`: Override the OpenRouter model specified in the `.env` file.

Examples:

```sh
python main.py --dry-run --limit 5
python main.py --model "openai/gpt-4o-mini"  # Override model from .env
python main.py --dry-run --limit 1 --model "openai/gpt-4o-mini"  # Combine all flags
```

### Single Text Processing (single.py)

Process individual text snippets or files without connecting to Readwise:

- `--text <snippet>`: Process a text snippet directly from the command line (good for short, single-line text)
- `--file <path>`: Process text from a file (recommended for multi-line text)
- `--model <model_name>`: Override the OpenRouter model specified in the `.env` file
- `--output <path>`: Save the cleaned text to a file

Examples:

```sh
# Process a short text snippet
python single.py --text "Your text snippet here"

# Process text from a file (recommended for multi-line text)
python single.py --file input.txt

# Override the model
python single.py --file input.txt --model "openai/gpt-4o"

# Save output to a file
python single.py --file input.txt --output cleaned.txt

# Combine options
python single.py --file input.txt --model "openai/gpt-4o-mini" --output cleaned.txt
```

**Note**: For multi-line text, using `--file` is strongly recommended as command-line arguments can be problematic with line breaks and special characters.

## Configuration

- The script uses the OpenRouter model specified by the `OPENROUTER_MODEL` environment variable in your `.env` file, or you can override it using the `--model` command-line flag.
- If no model is specified (neither in `.env` nor via `--model`), the script will exit with an error.
- A 1-second delay is included between API calls to avoid rate limits.

## Contributing

Feel free to open issues or submit pull requests to improve this project!

## License

[MIT](LICENSE)

## Links

[Readwise API](https://readwise.io/api_deets)
[OpenRouter Docs](https://openrouter.ai/docs/quickstart)
