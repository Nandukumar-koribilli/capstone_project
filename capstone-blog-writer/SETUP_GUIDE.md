# Automated Blog Writer Agent - Complete Setup Guide

This is a complete step-by-step guide to install, set up, and run the **Automated Blog Writer Agent** on your machine. This multi-agent system automates the entire blog writing process using Google's Gemini AI model.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation Steps](#installation-steps)
3. [API Key Setup](#api-key-setup)
4. [Running the Agent](#running-the-agent)
5. [Using the Agent](#using-the-agent)
6. [Troubleshooting](#troubleshooting)
7. [Project Structure](#project-structure)

---

## Prerequisites

Before you begin, ensure you have:

- **Python 3.10 or higher** installed on your machine
- **Windows, macOS, or Linux** operating system
- **Git** (for cloning the repository)
- **Administrator access** (for some Windows installations)
- A **Google Gemini API key** (free from [Google AI Studio](https://aistudio.google.com))

### Check Python Version

Open a terminal/PowerShell and run:

```powershell
python --version
```

If this command doesn't work, [install Python](https://www.python.org/downloads/). Make sure to check "Add Python to PATH" during installation.

---

## Installation Steps

### Step 1: Clone or Download the Project

```powershell
# Clone from Git (if available)
git clone <repository-url>
cd capstone-blog-writer
```

Or download and extract the project folder manually.

### Step 2: Install `uv` (Dependency Manager)

The project uses `uv` for fast, reliable dependency management. Install it:

```powershell
pip install uv
```

Verify installation:

```powershell
uv --version
```

### Step 3: Install Project Dependencies

From the project root directory, run:

```powershell
cd capstone-blog-writer
uv pip install -r requirements.txt
```

This command will:
- Create a virtual environment (`.venv`)
- Install all required Python packages
- Set up the Google ADK framework

**Wait for the installation to complete** (this may take 2-5 minutes depending on your internet speed).

### Step 4: Verify Installation

Test that everything installed correctly:

```powershell
uv run python -c "import google.adk; print('ADK installed successfully')"
```

You should see: `ADK installed successfully`

---

## API Key Setup

### Get Your Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com)
2. Click **"Get API Key"** in the left sidebar
3. Click **"Create new secret key"**
4. Copy the API key (it starts with `AIza...`)
5. **Keep this key private** — never share it or commit it to git

### Add Your API Key to the Project

The project uses a `.env` file to store your API key securely (the file is in `.gitignore` and won't be committed).

#### Option A: Using the `.env` File (Recommended)

1. Open the `.env` file in the project root with a text editor:
   ```
   .env
   ```

2. Replace `<YOUR_API_KEY_HERE>` with your actual Gemini API key:
   ```
   GOOGLE_GENAI_USE_VERTEXAI=False
   GOOGLE_API_KEY=AIzaSyCKXY6XAOUcd67_Ly3-IZwikj3_8RV_udc
   ```

3. Save the file.

#### Option B: Using Environment Variables (Per-Session)

If you prefer not to use a file, set the environment variables in your PowerShell session:

```powershell
$env:GOOGLE_GENAI_USE_VERTEXAI = "False"
$env:GOOGLE_API_KEY = "YOUR_ACTUAL_API_KEY_HERE"
```

### ⚠️ Security Note

- **Never commit `.env` to git** — it's already in `.gitignore`
- **Never paste your API key in chat or shared documents**
- If you accidentally exposed your key, regenerate it in [Google AI Studio](https://aistudio.google.com)

---

## Running the Agent

Choose one of the following methods:

### Method 1: Web User Interface (Interactive Playground) — Recommended

The web UI provides a visual chat interface to interact with your agent.

#### Start the Server

```powershell
cd C:\Users\YOUR_USERNAME\path\to\capstone-blog-writer
uv run python start_web.py
```

**Expected output:**
```
[INFO] Graphviz mock module injected
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

#### Access the Web UI

Open your browser and go to:

```
http://127.0.0.1:8000
```

#### Using the Web UI

1. The page will load and show available agents
2. Select **`blogger_agent`** from the list
3. Click **"Create New Session"**
4. Start chatting with your agent in the message box
5. Type your message and press Enter to send

**Example conversation:**
```
You: I want to write a blog about AI agents
Agent: I can help you create a technical blog post about AI agents...
```

#### Stop the Server

Press `Ctrl+C` in the terminal, or run:

```powershell
taskkill /F /PID <PID_NUMBER>
```

---

### Method 2: Command-Line Interface (CLI)

The CLI runs directly in your terminal with no browser needed.

#### Start the Agent

```powershell
cd C:\Users\YOUR_USERNAME\path\to\capstone-blog-writer
$env:GOOGLE_GENAI_USE_VERTEXAI = "False"
$env:GOOGLE_API_KEY = "YOUR_ACTUAL_API_KEY_HERE"
uv run adk run blogger_agent
```

**Expected output:**
```
Running agent interactive_blogger_agent, type exit to exit.
[user]:
```

#### Using the CLI

Type your messages at the `[user]:` prompt:

```
[user]: I want to write a blog about Gemini 2.5
[interactive_blogger_agent]: I can help you create a blog post about Gemini 2.5. Let me start by generating an outline...
[user]: yes, that looks good
[interactive_blogger_agent]: Great! Now I'll write the full blog post...
```

#### Exit the Agent

Type `exit` and press Enter:

```
[user]: exit
```

---

## Using the Agent

### Workflow Overview

The agent follows this workflow:

1. **Provide a Topic** — Tell the agent what blog post you want to write about
2. **Codebase Analysis (Optional)** — If relevant, provide a directory for the agent to analyze
3. **Outline Approval** — Review and approve the blog outline
4. **Content Visuals** — Choose how to include images/visuals
5. **Blog Writing** — The agent writes the full blog post
6. **Editing & Feedback** — Review and request revisions
7. **Social Media Posts (Optional)** — Generate social media content
8. **Export** — Save the final blog post as a markdown file

### Example: Write a Blog About Python

**Web UI:**
```
You: I want to write a blog post about Python programming best practices

Agent: Great! I'll create an outline for a blog about Python best practices.

Here's the outline:
1. Introduction to Python Best Practices
2. Code Style and PEP 8
3. Documentation Standards
...

You: looks good, write it

Agent: Writing the blog post now...
```

**CLI:**
```
[user]: I want to write a blog post about Python programming best practices
[interactive_blogger_agent]: I'll create an outline for you...
[user]: looks good, write it
[interactive_blogger_agent]: Now writing the full blog post...
```

---

## Troubleshooting

### Issue: "python is not recognized"

**Solution:** Python is not in your system PATH.
- [Reinstall Python](https://www.python.org/downloads/) and check "Add Python to PATH"
- Or use the full path: `C:\Users\YOUR_USERNAME\AppData\Local\Programs\Python\Python311\python.exe`

### Issue: "uv is not recognized"

**Solution:** `uv` is not installed or not in PATH.

```powershell
pip install --upgrade uv
```

Or use Python module:
```powershell
python -m uv --version
```

### Issue: "GOOGLE_API_KEY not found" or authentication error

**Solution:** Your API key is not set correctly.

1. Verify the `.env` file exists and has your actual API key
2. Or set the environment variable explicitly:
   ```powershell
   $env:GOOGLE_API_KEY = "YOUR_ACTUAL_KEY"
   ```
3. Check that your key is not truncated or has extra spaces

### Issue: "Port 8000 already in use"

**Solution:** Another process is using port 8000.

```powershell
netstat -ano | findstr :8000
taskkill /F /PID <PID_NUMBER>
```

Then restart the server.

### Issue: Web server starts but chat doesn't work

**Solution:** Refresh the browser (Ctrl+F5) or clear browser cache.

If still not working, try the CLI method instead.

### Issue: "No module named 'blogger_agent'"

**Solution:** You're not in the project directory or environment not activated.

```powershell
cd C:\Users\YOUR_USERNAME\path\to\capstone-blog-writer
uv run adk run blogger_agent
```

---

## Project Structure

```
capstone-blog-writer/
├── .env                          # Your Gemini API key (DO NOT COMMIT)
├── .env.example                  # Example .env template
├── .gitignore                    # Ignores .env and other files
├── start_web.py                  # Start web server with graphviz mock
├── fix_graphviz.py               # Graphviz mock module
├── run_web.ps1                   # PowerShell script to run web server
├── requirements.txt              # Python dependencies
├── pyproject.toml                # Project metadata
├── README.md                     # Original README
│
├── blogger_agent/
│   ├── __init__.py
│   ├── agent.py                  # Main agent orchestrator
│   ├── config.py                 # Agent configuration & Gemini models
│   ├── tools.py                  # Custom tools (file saving, codebase analysis)
│   ├── agent_utils.py
│   ├── validation_checkers.py
│   │
│   └── sub_agents/               # Specialized sub-agents
│       ├── blog_planner.py       # Generates blog outline
│       ├── blog_writer.py        # Writes the full blog post
│       ├── blog_editor.py        # Edits based on feedback
│       └── social_media_writer.py# Generates social media posts
│
├── tests/
│   ├── test_agent.py             # Integration tests
│   └── README.md
│
└── eval/
    ├── test_eval.py              # Evaluation tests
    └── data/
        ├── blog_eval.test.json
        └── test_config.json
```

---

## Key Features

✅ **Multi-Agent System** — Specialized agents for planning, writing, editing, and social media  
✅ **AI-Powered Research** — Uses Google Search to find relevant information  
✅ **Interactive Chat** — Web UI and CLI interfaces  
✅ **Iterative Editing** — Get feedback and refine the blog post  
✅ **File Export** — Save posts as markdown files  
✅ **Session Management** — Maintains conversation history  

---

## Next Steps

1. ✅ Install and run the agent
2. 📝 Write your first blog post
3. 📊 Review generated content
4. 🔄 Iterate and refine
5. 💾 Export and publish

---

## Support & Resources

- **Google ADK Documentation:** https://cloud.google.com/docs/agents
- **Gemini API Documentation:** https://ai.google.dev
- **Project Issues:** Check the project repository

---

## License

This project is licensed under the Apache License 2.0. See `LICENSE` file for details.

---

**Happy blogging! 🚀**
