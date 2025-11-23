# Vibecoded Agent 2

A small ReAct-style agent that uses Google Gemini (via `google-genai`) together with `yfinance` to fetch and compare stock prices (today vs. yesterday). The agent exposes tools the model can call to retrieve the current price and the previous trading day's close for a ticker symbol, and it coordinates those tool calls to produce a final comparison.

**Contents**
- `vibecoded_agent_2.py` — main agent script (single-file module).
- `pyproject.toml` — basic project metadata and dependencies.
- `requirements.txt` — runtime dependencies for quick installs.

**What it does**
- Uses `google-genai` to interact with a Gemini model in a ReAct loop.
- Provides two tool functions for the model:
  - `get_current_price(ticker)` — fetches the current market price using `yfinance`.
  - `get_yesterday_close(ticker)` — fetches the previous trading day's close using `yfinance`.
- The agent runs the loop, executes model-requested tools, feeds back observations, and returns a final textual answer.

Requirements
- Python 3.10+
- See `requirements.txt` for versions used during development.

Environment
- The agent expects a `GEMINI_API_KEY` environment variable (Google Gemini API key). Locally, create a `.env` file in the repository root with:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

Make sure `.env` is ignored by Git (this repository includes `.env` in `.gitignore`). For local development prefer copying `.env.example` to `.env` and pasting your key.

Setup (recommended)
1. Create and activate a virtual environment (macOS / zsh):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

Running the agent
-----------------
- From the repository root run the module script:

```bash
cd Vibecoded-Agent-2
python vibecoded_agent_2.py
```

This will execute the example `main()` in `vibecoded_agent_2.py`, which runs a sample query comparing current vs. yesterday's prices for example tickers.

Notes and troubleshooting
- `yfinance` depends on network access and can fail if the ticker is invalid or if the Yahoo endpoint is rate-limited. The tool functions handle exceptions and return error dictionaries in those cases.
- If the script raises a `ValueError` about `GEMINI_API_KEY` not being found, confirm you created a `.env` with the key or that the environment variable is set in your shell.
- If you plan to package this project, convert `vibecoded_agent_2.py` into a package directory (`vibecoded_agent_2/__init__.py`) and add a `build-system` table to `pyproject.toml`.

Security
- Do not commit `.env` or secrets to the repository. Use the included `.env.example` as a template and keep real secrets only in local environment variables or a secrets manager.

Contributing
- Small repo: opening issues or PRs for bugfixes, improvements to tool functions, or tests is welcome.

License
- No license file is included in this repo by default — add a `LICENSE` at the repository root if you want to make usage terms explicit.
