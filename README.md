# termExplain 🔍

**AI-powered CLI error explainer using Gemini**

`termExplain` is a Python-based command-line tool that takes terminal errors and explains them using Google's Gemini AI. It provides clear, actionable explanations of what went wrong, why it happened, and how to fix it.



## Installation

### Via Homebrew (Recommended)

```bash
# Add the tap
brew tap smundhra-git/explain

# Install termExplain
brew install termexplain
```

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/smundhra-git/termExplain.git
cd termExplain

# Install in development mode
pip install -e .
```

## Setup

1. **Get a Gemini API Key**:
   - Visit [Google AI Studio](https://aistudio.google.com/)
   - Create a free account and get your API key

2. **Set your API key**:
   ```bash
   export GEMINI_API_KEY="your-api-key-here"
   ```

3. **Add to your shell profile** (optional):
   ```bash
   echo 'export GEMINI_API_KEY="your-api-key-here"' >> ~/.zshrc
   source ~/.zshrc
   ```

## Usage

### Explain an error directly:
```bash
explain "ModuleNotFoundError: No module named 'requests'"
```

### Run a file and explain any errors:
```bash
explain --file my_script.py
explain --file app.js
```

### Interactive mode:
```bash
explain
# Then enter your error when prompted
```

### Get help:
```bash
explain --help
explain --version
```

## Examples

```bash
# Explain a Python import error
explain "ModuleNotFoundError: No module named 'pandas'"

# Explain a JavaScript error
explain "ReferenceError: x is not defined"

# Run a Python file and explain any errors
explain --file my_script.py

# Cache an explanation for future use
explain --save "Permission denied"
```

## Requirements

- Python 3.8 or higher
- Gemini API key
- Internet connection for AI explanations

## Dependencies

- `google-generativeai`: Google Gemini AI client
- `click`: Command-line interface creation kit
- `rich`: Rich text and beautiful formatting
- `colorama`: Cross-platform colored terminal text
- `python-dotenv`: Environment variable management
- `requests`: HTTP library

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any issues, please report them on the [GitHub issues page](https://github.com/smundhra-git/termExplain/issues). 