# Setup & Usage Instructions

## Quick Start

### Option 1: Using the run script (Recommended)
```bash
cd first_execution
./run.sh
```

### Option 2: Manual setup
```bash
cd first_execution
source venv/bin/activate
python __main__.py
```

## First Time Setup

If the venv doesn't exist or you want to recreate it:

```bash
cd first_execution
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python __main__.py
```

## System Requirements

- Python 3.10+
- ~500MB disk space for dependencies

## Features

- **Chat Interface**: Talk to the AI agent in a terminal UI
- **Model Management**: Add and switch between different LLM models (Ctrl+M)
- **Persistent Config**: Your model configuration is saved automatically
- **Real-time Execution**: Watch the agent execute functions in real-time

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+M` | Open model configuration |
| `Ctrl+N` | Clear chat history |
| `Ctrl+Q` | Quit application |
| `Enter` | Send message (in chat) |

## First Run

1. Start the application with `./run.sh`
2. Press `Ctrl+M` to open model configuration
3. Add a model:
   - **Name**: Give it a friendly name (e.g., "Gemini Flash")
   - **Provider**: Select "GEMINI"
   - **Model ID**: Enter the model ID (e.g., "gemini-2.0-flash-lite")
   - **API Key**: Paste your Google Gemini API key
4. Click "Set Active" to activate the model
5. Return to chat screen and start typing!

## Example Query

Try asking the agent to do something with files:
```
List all files in the current directory
```

The agent will use its tools to explore the filesystem and report back.

## Troubleshooting

### Module not found errors
Make sure you've activated the venv:
```bash
source venv/bin/activate
```

### API key rejected
Ensure your Google Gemini API key is valid and has appropriate permissions.

### Port already in use
Textual should handle this automatically. If you get a port error, try running again.

## Project Structure

```
first_execution/
├── config/              # Configuration management
├── agent/               # AI agent core logic
├── ui/                  # Terminal UI components
├── functions/           # File/code operations
├── venv/                # Python virtual environment
├── requirements.txt     # Python dependencies
├── run.sh              # Quick start script
└── __main__.py         # Application entry point
```

## Next Steps

After verifying it works, you can:
1. Add more custom functions in `functions/`
2. Extend the UI with additional screens
3. Add support for more LLM providers
4. Implement conversation history persistence
