# 🤖 capstone_project_Code_Error_Check_AI_Agent

An intelligent, multi-agent code review system powered by Google Gemini AI. This tool performs comprehensive code analysis including security vulnerability detection, code quality metrics, style checking, and provides AI-powered fix suggestions.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Features

### Multi-Agent Architecture
- **SyntaxAnalyzer Agent**: Validates code syntax using AST parsing
- **SecurityAgent**: Detects security vulnerabilities and dangerous patterns
- **StyleAgent**: Checks code style (PEP 8 compliance)
- **ComplexityAgent**: Analyzes cyclomatic and cognitive complexity
- **DocumentationAgent**: Checks for missing docstrings
- **BestPracticesAgent**: Identifies anti-patterns and code smells

### Code Quality Metrics
- Lines of Code (LOC)
- Cyclomatic Complexity
- Cognitive Complexity
- Maintainability Index (0-100 with letter grades A-F)
- Function and Class counts
- Maximum Nesting Depth

### Security Analysis
Detects common vulnerabilities including:
- 🔴 `eval()` and `exec()` usage (Critical)
- 🔴 Hardcoded passwords/API keys (Critical)
- 🟠 `os.system()` usage (High)
- 🟠 Unsafe pickle deserialization (High)
- 🟠 Shell injection risks (High)
- 🟡 Star imports (Medium)
- 🔵 User input without validation (Low)

### AI-Powered Suggestions
- Integrates with Google Gemini AI
- Provides intelligent fix recommendations
- Explains issues in detail
- Suggests best practices

## 📁 Project Structure

```
Code_Error_Check_AI_Agent/
├── code_review_agent.py    # Main Flask application
├── templates/
│   └── index.html          # Web UI template
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Google API Key (optional, for AI suggestions)

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd Code_Error_Check_AI_Agent
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install manually:
   ```bash
   pip install flask flask-cors google-generativeai
   ```

3. **Set up Google API Key (optional, for AI features):**
   ```bash
   # Windows
   set GOOGLE_API_KEY=your_api_key_here
   
   # Linux/Mac
   export GOOGLE_API_KEY=your_api_key_here
   ```

### Running the Application

```bash
# Windows Command Prompt (CMD)
set PYTHONIOENCODING=utf-8 && python code_review_agent.py

# Windows PowerShell
$env:PYTHONIOENCODING="utf-8"; python code_review_agent.py

# Or simply (works on all platforms)
python code_review_agent.py

# Linux/Mac
python code_review_agent.py
```

The server will start at `http://localhost:5000`

## 🖥️ Web Interface

### Main Features
- **Code Input Panel**: Paste your code for analysis
- **Language Selection**: Auto-detect or manually select (Python, JavaScript, TypeScript, Java, Go)
- **Review Code**: Perform static analysis
- **Review with AI**: Get AI-powered suggestions (requires API key)
- **Load Sample**: Load example code with various issues
- **Results Panel**: View issues, metrics, and AI suggestions

### Tabs
1. **Issues**: List of detected problems with severity levels
2. **Metrics**: Code quality metrics and statistics
3. **AI Suggestions**: Intelligent fix recommendations (when available)

## 🔌 API Reference

### POST `/api/review`

Analyze code and return review results.

**Request Body:**
```json
{
  "code": "your code here",
  "language": "python",  // optional, auto-detected if null
  "include_ai": true     // optional, include AI suggestions
}
```

**Response:**
```json
{
  "code_hash": "abc123def456",
  "language": "python",
  "timestamp": "2024-01-15T10:30:00",
  "execution_time": 0.015,
  "issues": [
    {
      "message": "Use of eval()",
      "severity": "critical",
      "category": "security",
      "line_number": 5,
      "suggestion": "Avoid using eval() as it can execute arbitrary code"
    }
  ],
  "metrics": {
    "lines_of_code": 25,
    "cyclomatic_complexity": 5,
    "cognitive_complexity": 8,
    "maintainability_index": 75.5,
    "function_count": 3,
    "class_count": 1,
    "nesting_depth": 2,
    "grade": "B"
  },
  "summary": {
    "total_issues": 5,
    "by_severity": {
      "critical": 1,
      "high": 2,
      "medium": 1,
      "low": 1,
      "info": 0
    },
    "quality_grade": "B",
    "risk_level": "HIGH"
  },
  "ai_suggestions": "..."  // if include_ai was true
}
```

### GET `/api/health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "gemini_available": true,
  "agents": ["SyntaxAnalyzer", "SecurityAgent", "StyleAgent", ...]
}
```

## 📊 Severity Levels

| Level | Icon | Description |
|-------|------|-------------|
| Critical | 🔴 | Must fix immediately (security vulnerabilities) |
| High | 🟠 | Should fix soon (potential bugs) |
| Medium | 🟡 | Recommended to fix (code quality) |
| Low | 🔵 | Nice to fix (style issues) |
| Info | ⚪ | Informational only |

## 📈 Quality Grades

| Grade | Maintainability Index | Description |
|-------|----------------------|-------------|
| A | 80-100 | Excellent, highly maintainable |
| B | 60-79 | Good, maintainable |
| C | 40-59 | Moderate, needs improvement |
| D | 20-39 | Poor, difficult to maintain |
| F | 0-19 | Very poor, needs refactoring |

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | Google Gemini API key for AI features | None |
| `PYTHONIOENCODING` | Character encoding (set to `utf-8` for Windows) | System default |

### Customization

You can customize the analysis by modifying the agent parameters in `code_review_agent.py`:

```python
# Adjust max line length for style checking
StyleAgent(max_line_length=120)

# Adjust complexity threshold
ComplexityAgent(max_complexity=15)
```

## 🧪 Example Usage

### Sample Code with Issues

```python
import os
import pickle

def run_command(cmd):
    os.system(cmd)  # Security issue!
    return True

def load_data(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)  # Unsafe deserialization

password = "super_secret_123"  # Hardcoded password!

def process_input():
    user_input = input("Enter command: ")
    eval(user_input)  # Critical security issue!
```

### Expected Results
- **Total Issues**: 13
- **Critical**: 2 (eval, hardcoded password)
- **High**: 2 (os.system, pickle)
- **Quality Grade**: A (based on maintainability index)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- [Google Gemini AI](https://ai.google.dev/) for AI-powered suggestions
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [Python AST](https://docs.python.org/3/library/ast.html) for code analysis

## 📧 Contact

For questions or feedback, please open an issue on the repository.








