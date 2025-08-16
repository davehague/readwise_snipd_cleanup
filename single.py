import os
import sys
from dotenv import load_dotenv
import argparse
from llm_cleaner import clean_text_with_llm

# Load API keys from .env
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL")

# Setup argument parser
parser = argparse.ArgumentParser(
    description="Clean a single text snippet or file using an LLM.",
    epilog="For multi-line text, using --file is recommended over --text"
)
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument(
    "--text", 
    type=str, 
    help="Text snippet to clean (for short, single-line text)"
)
group.add_argument(
    "--file", 
    type=str, 
    help="Path to text file to clean (recommended for multi-line text)"
)
parser.add_argument(
    "--model", 
    type=str, 
    help="Override the OpenRouter model specified in .env"
)
parser.add_argument(
    "--output",
    type=str,
    help="Optional output file path to save the cleaned text"
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
    sys.exit(1)

# Check for API key
if not OPENROUTER_API_KEY:
    print("Error: OPENROUTER_API_KEY not found in .env file")
    sys.exit(1)




def main():
    # Get input text
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                input_text = f.read()
            print(f"Read {len(input_text)} characters from {args.file}")
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found")
            sys.exit(1)
        except Exception as e:
            print(f"Error reading file: {e}")
            sys.exit(1)
    else:
        input_text = args.text
        print(f"Processing {len(input_text)} characters from command line")
    
    # Clean the text
    print("Sending to LLM for cleaning...")
    try:
        cleaned_text = clean_text_with_llm(input_text, OPENROUTER_MODEL, OPENROUTER_API_KEY)
    except Exception as e:
        print(f"Error processing text with LLM: {e}")
        sys.exit(1)
    
    # Output results
    print("\n--- Cleaned Text ---")
    print(cleaned_text)
    print("-------------------\n")
    
    # Save to file if requested
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(cleaned_text)
            print(f"Cleaned text saved to: {args.output}")
        except Exception as e:
            print(f"Error saving to file: {e}")
            sys.exit(1)
    
    return cleaned_text


if __name__ == "__main__":
    main()