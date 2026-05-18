# AI Agent TUI - Terminal User Interface

A beautiful, interactive terminal UI for interacting with AI agents using Google Gemini or other LLM providers.

## 🎯 Features

- **Interactive Chat Interface**: Talk to AI agents in a rich terminal environment
- **Graphical Model Management**: Add, remove, and switch between LLM models without editing code
- **Real-time Execution**: Watch AI agents execute functions live
- **File Operations**: Let agents read, write, and explore files
- **Python Execution**: Run Python scripts with agent orchestration
- **Persistent Configuration**: Your models and settings are saved automatically
- **Tokyo Night Theme**: Beautiful dark theme optimized for terminal use

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- 500MB disk space

### Installation & Running

**Option 1: Quick start (Linux/Mac)**
```bash
cd first_execution
./run.sh
```

**Option 2: Manual setup**
```bash
cd first_execution
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python __main__.py
```

**Option 3: Verify installation first**
```bash
cd first_execution
source venv/bin/activate
python verify.py
```

## 📋 First Time Setup

1. **Start the application**
   ```bash
   ./run.sh
   ```

2. **Configure a model (Ctrl+M)**
   - Click "Add Model" form
   - Enter:
     - **Name**: "Gemini Flash" (or your preference)
     - **Provider**: Select "GEMINI"
     - **Model ID**: `gemini-2.0-flash-lite` (or another Gemini model)
     - **API Key**: Your Google Gemini API key
   - Click "Add Model"

3. **Set as active**
   - Select the model from the dropdown
   - Click "Set Active"

4. **Start chatting!**
   - Return to chat screen
   - Type your prompt and press Enter

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+M` | Open/close model configuration |
| `Ctrl+N` | Clear chat history |
| `Ctrl+Q` | Quit application |
| `Enter` | Send message (in input field) |
| `Tab` | Navigate between UI elements |

## 🎨 UI Layout

```
┌─────────────────────────────────────────────┐
│ Header - Application Title                  │
├────────────────┬───────────────────────────┤
│  Model Sidebar │   Chat Display            │
│                │   ┌─────────────────────┐ │
│  Active Model  │   │ Message History     │ │
│  Dropdown      │   │                     │ │
│  Set Active    │   │ Function Calls      │ │
│                │   │ Responses           │ │
│                │   └─────────────────────┘ │
│                │                           │
│                │ Input Field (Your prompt)│
├────────────────┴───────────────────────────┤
│ Footer - Keybindings                       │
└─────────────────────────────────────────────┘
```

## 📝 Example Queries

Try these prompts to test the agent:

**List files:**
```
List all files in the current directory and show their sizes
```

**Read a file:**
```
Read the file called lorem.txt and tell me what's in it
```

**Run code:**
```
Run the calculator with the expression "10 + 20 * 3"
```

**Explore:**
```
What files are in the pkg directory?
```

## 🔧 Project Structure

```
first_execution/
├── config/                  # Configuration management
│   ├── settings.py         # Pydantic models
│   ├── models.py           # Model registry
│   └── storage.py          # JSON persistence
├── agent/                   # AI agent logic
│   ├── core.py             # Agentic loop
│   └── models.py           # LLM provider interface
├── ui/                      # Terminal UI
│   ├── app.py              # Main application
│   ├── style.tcss          # Styling
│   ├── screens/            # Screen layouts
│   │   ├── chat_screen.py
│   │   └── model_config_screen.py
│   └── widgets/            # Reusable components
├── functions/               # File/code operations (copied)
├── tests/                   # Test suite
├── .config/                # Configuration storage
├── venv/                   # Python virtual environment
├── requirements.txt        # Dependencies
├── __main__.py             # Entry point
├── run.sh                  # Quick start script
├── verify.py               # Verification script
├── SETUP.md                # Setup instructions
└── README.md               # This file
```

## 🤖 Supported Features

### File Operations
- **List directories**: See all files and folders
- **Read files**: View file contents (max 10KB per read)
- **Write files**: Create or modify files
- **Directory traversal**: Safely explore the filesystem

### Code Execution
- **Run Python files**: Execute Python scripts with arguments
- **Capture output**: See stdout and stderr
- **Error handling**: Graceful error reporting

### Model Management
- **Add models**: Register new LLM APIs
- **Switch models**: Change active model on the fly
- **Save config**: Persistent storage of your setup
- **Supported providers**: GEMINI (OpenAI, Anthropic coming soon)

## 🔐 Security

- **Path sandboxing**: All operations confined to working directory
- **API key handling**: Keys stored locally in config
- **Execution timeout**: Python scripts limited to 30 seconds
- **Validation**: Input sanitization on all operations

## 🐛 Troubleshooting

### "Module not found" errors
Ensure the virtual environment is activated:
```bash
source venv/bin/activate
```

### API key rejected
- Verify your Google Gemini API key is valid
- Check that the key has appropriate permissions
- Ensure there are no extra spaces in the key

### No models appear
- Check that `.config/models.json` exists
- Verify the file has valid JSON format
- Try adding a new model in the UI

### UI looks broken
- Try resizing your terminal window
- Ensure terminal supports 256 colors
- Update Textual: `pip install --upgrade textual`

### Agent doesn't respond
- Check that a model is set as active (Ctrl+M)
- Verify internet connection for API calls
- Check API rate limits

## 📚 Dependencies

- **google-genai**: Google Gemini API client
- **textual**: Terminal UI framework
- **pydantic**: Data validation
- **python-dotenv**: Environment variable management

## 🚀 Advanced Usage

### Using Environment Variables
Create a `.env` file:
```bash
GEMINI_API_KEY=your-api-key-here
```

### Adding Custom Functions
Edit `functions/schemas.py` to define new capabilities, then implement in `functions/`.

### Extending UI Screens
Add new screens to `ui/screens/` and register in `ui/app.py`.

### Supporting New LLM Providers
1. Create a new provider class in `agent/models.py`
2. Update `config/settings.py` with provider enum
3. Implement in `agent/core.py`

## 📖 Documentation

- **SETUP.md**: Installation and first-run guide
- **IMPLEMENTATION_PLAN.md**: Architecture and design decisions
- **PROJECT_SPEC.md**: Complete feature specification

## 🤝 Contributing

This is a learning project! Feel free to:
- Add new functions to the agent
- Improve the UI/UX
- Add support for more LLM providers
- Write tests

## 📄 License

This project is provided as-is for educational purposes.

## 🎓 Learning Resources

This project demonstrates:
- Agentic AI loops (multi-turn conversations)
- LLM function calling
- Terminal UI development with Textual
- Async/await patterns in Python
- Configuration management with Pydantic
- Tool composition and orchestration

## ✨ What's Next?

Phase 5 (Polish & Features) coming soon:
- [ ] Conversation history export
- [ ] Model fine-tuning options
- [ ] Plugin system for custom functions
- [ ] Multi-agent orchestration
- [ ] Response streaming display
- [ ] Token usage analytics

## 🆘 Support

If you encounter issues:
1. Run `python verify.py` to check installation
2. Check the troubleshooting section above
3. Review SETUP.md for detailed instructions
4. Ensure all dependencies are installed with `pip install -r requirements.txt`

---

**Happy Chatting! 🚀**
