# termExplain 🔍

**AI-powered CLI error explainer using Gemini**

`termExplain` is a Python-based command-line tool that takes terminal errors and explains them using Google's Gemini AI. It provides clear, actionable explanations of what went wrong, why it happened, and how to fix it.

## How to Use

### Setup
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set your Gemini API key:**
   ```bash
   export GEMINI_API_KEY="your-api-key-here"
   ```

### Usage Examples

```bash
# Explain an error directly
python3 main.py "ModuleNotFoundError: No module named 'requests'"

# Pipe error from a file
cat error.log | python3 main.py

# Interactive mode
python3 main.py

# With caching
python3 main.py --save "Permission denied"
```



### Shell Integration
Add to your shell profile (`.bashrc`, `.zshrc`, etc.):
```bash
source /path/to/termExplain/explain.sh
```

Then use anywhere:
```bash
explain "command not found: docker"

explain --file <test_file.py>
``` 