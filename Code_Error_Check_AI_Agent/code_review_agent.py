"""
AI-Powered Code Review Agent - Web Application
==============================================

A comprehensive code review system with multi-agent architecture,
security analysis, code quality metrics, and AI-powered suggestions.

Run with: python code_review_agent.py
Access at: http://localhost:5000
"""

import os
import sys
import ast
import re
import json
import hashlib
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod
import warnings
warnings.filterwarnings('ignore')

# Flask for web server
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS

# Try to import Google Generative AI
try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    print("⚠️ google-generativeai not installed. Run: pip install google-generativeai")

# ============================================================
# ENUMS AND CONSTANTS
# ============================================================

class Severity(Enum):
    """Issue severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

class IssueCategory(Enum):
    """Categories of code issues"""
    SECURITY = "security"
    PERFORMANCE = "performance"
    STYLE = "style"
    COMPLEXITY = "complexity"
    DOCUMENTATION = "documentation"
    SYNTAX = "syntax"
    BEST_PRACTICE = "best_practice"
    MAINTAINABILITY = "maintainability"

class Language(Enum):
    """Supported programming languages"""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    JAVA = "java"
    GO = "go"
    UNKNOWN = "unknown"

# Severity colors for display
SEVERITY_COLORS = {
    Severity.CRITICAL: "🔴",
    Severity.HIGH: "🟠",
    Severity.MEDIUM: "🟡",
    Severity.LOW: "🔵",
    Severity.INFO: "⚪"
}

SEVERITY_CSS = {
    Severity.CRITICAL: "critical",
    Severity.HIGH: "high",
    Severity.MEDIUM: "medium",
    Severity.LOW: "low",
    Severity.INFO: "info"
}

# Security patterns to detect
SECURITY_PATTERNS = {
    "python": {
        r"eval\s*\(": ("Use of eval()", Severity.CRITICAL),
        r"exec\s*\(": ("Use of exec()", Severity.CRITICAL),
        r"os\.system\s*\(": ("Use of os.system()", Severity.HIGH),
        r"subprocess\.call\s*\(.*shell\s*=\s*True": ("Shell injection risk", Severity.CRITICAL),
        r"pickle\.loads?": ("Unsafe deserialization with pickle", Severity.HIGH),
        r"yaml\.load\s*\([^)]*\)(?!.*Loader)": ("Unsafe YAML loading", Severity.HIGH),
        r"__import__\s*\(": ("Dynamic import", Severity.MEDIUM),
        r"input\s*\(": ("User input without validation", Severity.LOW),
        r"password\s*=\s*[\"'][^\"']+[\"']": ("Hardcoded password", Severity.CRITICAL),
        r"api_key\s*=\s*[\"'][^\"']+[\"']": ("Hardcoded API key", Severity.CRITICAL),
        r"secret\s*=\s*[\"'][^\"']+[\"']": ("Hardcoded secret", Severity.CRITICAL),
    },
    "javascript": {
        r"eval\s*\(": ("Use of eval()", Severity.CRITICAL),
        r"innerHTML\s*=": ("XSS vulnerability via innerHTML", Severity.HIGH),
        r"document\.write\s*\(": ("Use of document.write()", Severity.MEDIUM),
        r"\$\(.*\)\.html\s*\(": ("Potential XSS in jQuery", Severity.HIGH),
    }
}

# ============================================================
# DATA CLASSES
# ============================================================

@dataclass
class CodeIssue:
    """Represents a single code issue"""
    message: str
    severity: Severity
    category: IssueCategory
    line_number: Optional[int] = None
    column: Optional[int] = None
    suggestion: Optional[str] = None
    code_snippet: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return {
            "message": self.message,
            "severity": self.severity.value,
            "severity_class": SEVERITY_CSS[self.severity],
            "category": self.category.value,
            "line_number": self.line_number,
            "column": self.column,
            "suggestion": self.suggestion,
            "code_snippet": self.code_snippet,
            "icon": SEVERITY_COLORS[self.severity]
        }

@dataclass
class CodeMetrics:
    """Code quality metrics"""
    lines_of_code: int = 0
    blank_lines: int = 0
    comment_lines: int = 0
    cyclomatic_complexity: int = 1
    cognitive_complexity: int = 0
    maintainability_index: float = 100.0
    function_count: int = 0
    class_count: int = 0
    avg_function_length: float = 0.0
    max_function_length: int = 0
    nesting_depth: int = 0
    
    def to_dict(self) -> Dict:
        return {
            "lines_of_code": self.lines_of_code,
            "blank_lines": self.blank_lines,
            "comment_lines": self.comment_lines,
            "cyclomatic_complexity": self.cyclomatic_complexity,
            "cognitive_complexity": self.cognitive_complexity,
            "maintainability_index": round(self.maintainability_index, 2),
            "function_count": self.function_count,
            "class_count": self.class_count,
            "avg_function_length": round(self.avg_function_length, 2),
            "max_function_length": self.max_function_length,
            "nesting_depth": self.nesting_depth,
            "grade": self.get_grade()
        }
    
    def get_grade(self) -> str:
        """Get letter grade based on maintainability index"""
        if self.maintainability_index >= 80:
            return "A"
        elif self.maintainability_index >= 60:
            return "B"
        elif self.maintainability_index >= 40:
            return "C"
        elif self.maintainability_index >= 20:
            return "D"
        else:
            return "F"

@dataclass
class ReviewResult:
    """Complete code review result"""
    code_hash: str
    language: Language
    timestamp: str
    issues: List[CodeIssue] = field(default_factory=list)
    metrics: CodeMetrics = field(default_factory=CodeMetrics)
    ai_suggestions: Optional[str] = None
    execution_time: float = 0.0
    
    def to_dict(self) -> Dict:
        summary = self.get_summary()
        return {
            "code_hash": self.code_hash,
            "language": self.language.value,
            "timestamp": self.timestamp,
            "issues": [i.to_dict() for i in self.issues],
            "metrics": self.metrics.to_dict(),
            "ai_suggestions": self.ai_suggestions,
            "execution_time": round(self.execution_time, 3),
            "summary": summary
        }
    
    def get_summary(self) -> Dict:
        """Get summary statistics"""
        severity_counts = {s.value: 0 for s in Severity}
        category_counts = {c.value: 0 for c in IssueCategory}
        
        for issue in self.issues:
            severity_counts[issue.severity.value] += 1
            category_counts[issue.category.value] += 1
        
        return {
            "total_issues": len(self.issues),
            "by_severity": severity_counts,
            "by_category": category_counts,
            "quality_grade": self.metrics.get_grade(),
            "risk_level": self._calculate_risk_level()
        }
    
    def _calculate_risk_level(self) -> str:
        """Calculate overall risk level"""
        critical_count = sum(1 for i in self.issues if i.severity == Severity.CRITICAL)
        high_count = sum(1 for i in self.issues if i.severity == Severity.HIGH)
        
        if critical_count > 0:
            return "CRITICAL"
        elif high_count > 2:
            return "HIGH"
        elif high_count > 0:
            return "MEDIUM"
        else:
            return "LOW"

# ============================================================
# LANGUAGE DETECTION
# ============================================================

class LanguageDetector:
    """Detect programming language from code"""
    
    PATTERNS = {
        Language.PYTHON: [
            r'^\s*def\s+\w+\s*\(',
            r'^\s*class\s+\w+',
            r'^\s*import\s+\w+',
            r'^\s*from\s+\w+\s+import',
            r':\s*$',
            r'^\s*@\w+',
        ],
        Language.JAVASCRIPT: [
            r'^\s*function\s+\w+\s*\(',
            r'^\s*const\s+\w+\s*=',
            r'^\s*let\s+\w+\s*=',
            r'^\s*var\s+\w+\s*=',
            r'=>',
            r'console\.log',
        ],
        Language.TYPESCRIPT: [
            r':\s*(string|number|boolean|any)\s*[;=)]',
            r'interface\s+\w+',
            r'type\s+\w+\s*=',
            r'<\w+>',
        ],
        Language.JAVA: [
            r'public\s+class\s+\w+',
            r'private\s+\w+\s+\w+',
            r'System\.out\.println',
            r'public\s+static\s+void\s+main',
        ],
        Language.GO: [
            r'^package\s+\w+',
            r'^func\s+\w+\s*\(',
            r'fmt\.Println',
            r':=',
        ]
    }
    
    @classmethod
    def detect(cls, code: str) -> Language:
        """Detect the programming language of the code"""
        scores = {lang: 0 for lang in Language}
        
        for lang, patterns in cls.PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, code, re.MULTILINE):
                    scores[lang] += 1
        
        best_lang = max(scores, key=scores.get)
        if scores[best_lang] > 0:
            return best_lang
        return Language.UNKNOWN

# ============================================================
# CODE UTILITIES
# ============================================================

class CodeUtils:
    """Utility functions for code analysis"""
    
    @staticmethod
    def compute_hash(code: str) -> str:
        """Compute a hash of the code for identification"""
        return hashlib.md5(code.encode()).hexdigest()[:12]
    
    @staticmethod
    def count_lines(code: str) -> Tuple[int, int, int]:
        """Count total, blank, and comment lines"""
        lines = code.split('\n')
        total = len(lines)
        blank = sum(1 for line in lines if not line.strip())
        comment = sum(1 for line in lines if line.strip().startswith('#') or line.strip().startswith('//'))
        return total, blank, comment

# ============================================================
# CODE ANALYSIS TOOLS
# ============================================================

class CodeAnalysisTools:
    """Comprehensive code analysis tools"""
    
    @staticmethod
    def analyze_ast(code: str) -> Dict:
        """Analyze code using AST"""
        try:
            tree = ast.parse(code)
            
            functions = []
            classes = []
            imports = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append({
                        'name': node.name,
                        'line': node.lineno,
                        'args_count': len(node.args.args),
                        'has_docstring': (isinstance(node.body[0], ast.Expr) and 
                                         isinstance(node.body[0].value, ast.Constant) and
                                         isinstance(node.body[0].value.value, str)) if node.body else False
                    })
                elif isinstance(node, ast.ClassDef):
                    classes.append({
                        'name': node.name,
                        'line': node.lineno,
                        'methods_count': sum(1 for n in node.body if isinstance(n, ast.FunctionDef))
                    })
                elif isinstance(node, ast.Import):
                    imports.extend([alias.name for alias in node.names])
                elif isinstance(node, ast.ImportFrom):
                    imports.append(f"{node.module}.{', '.join(alias.name for alias in node.names)}")
            
            return {
                'valid': True,
                'functions': functions,
                'classes': classes,
                'imports': imports
            }
        except SyntaxError as e:
            return {
                'valid': False,
                'error': str(e),
                'line': e.lineno,
                'offset': e.offset
            }
    
    @staticmethod
    def calculate_complexity(code: str) -> Dict:
        """Calculate cyclomatic and cognitive complexity"""
        try:
            tree = ast.parse(code)
            
            cyclomatic = 1
            cognitive = 0
            max_nesting = 0
            
            def analyze_node(node, depth=0):
                nonlocal cyclomatic, cognitive, max_nesting
                
                if isinstance(node, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                    cyclomatic += 1
                    cognitive += 1 + depth
                elif isinstance(node, ast.BoolOp):
                    cyclomatic += len(node.values) - 1
                    cognitive += len(node.values) - 1
                
                new_depth = depth
                if isinstance(node, (ast.If, ast.While, ast.For, ast.With, ast.Try)):
                    new_depth = depth + 1
                    max_nesting = max(max_nesting, new_depth)
                
                for child in ast.iter_child_nodes(node):
                    analyze_node(child, new_depth)
            
            analyze_node(tree)
            
            return {
                'cyclomatic': cyclomatic,
                'cognitive': cognitive,
                'max_nesting': max_nesting
            }
        except:
            return {'cyclomatic': 0, 'cognitive': 0, 'max_nesting': 0}
    
    @staticmethod
    def calculate_maintainability_index(code: str, complexity: int) -> float:
        """Calculate maintainability index (0-100)"""
        lines = code.split('\n')
        loc = len([l for l in lines if l.strip() and not l.strip().startswith('#')])
        
        if loc == 0:
            return 100.0
        
        operators = len(re.findall(r'[+\-*/=<>!&|^~%]', code))
        operands = len(re.findall(r'\b\w+\b', code))
        volume = (operators + operands) * (1 + (operators + operands) / 10) if operators + operands > 0 else 1
        
        mi = 171 - 5.2 * (volume ** 0.23) - 0.23 * complexity - 16.2 * (loc ** 0.25)
        
        return max(0, min(100, mi))
    
    @staticmethod
    def check_security(code: str, language: Language = Language.PYTHON) -> List[CodeIssue]:
        """Check for security vulnerabilities"""
        issues = []
        lang_key = language.value if language.value in SECURITY_PATTERNS else "python"
        patterns = SECURITY_PATTERNS.get(lang_key, {})
        
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            for pattern, (message, severity) in patterns.items():
                if re.search(pattern, line, re.IGNORECASE):
                    issues.append(CodeIssue(
                        message=message,
                        severity=severity,
                        category=IssueCategory.SECURITY,
                        line_number=i,
                        code_snippet=line.strip()[:50]
                    ))
        
        return issues
    
    @staticmethod
    def check_style(code: str, max_line_length: int = 88) -> List[CodeIssue]:
        """Check code style issues"""
        issues = []
        lines = code.split('\n')
        
        import_section_ended = False
        
        for i, line in enumerate(lines, 1):
            if len(line) > max_line_length:
                issues.append(CodeIssue(
                    message=f"Line too long ({len(line)} > {max_line_length})",
                    severity=Severity.LOW,
                    category=IssueCategory.STYLE,
                    line_number=i,
                    suggestion=f"Break line into multiple lines"
                ))
            
            if line.endswith(' ') or line.endswith('\t'):
                issues.append(CodeIssue(
                    message="Trailing whitespace",
                    severity=Severity.INFO,
                    category=IssueCategory.STYLE,
                    line_number=i
                ))
            
            stripped = line.strip()
            if stripped and not stripped.startswith('#') and not stripped.startswith('import') and not stripped.startswith('from'):
                import_section_ended = True
            
            if import_section_ended and (stripped.startswith('import ') or stripped.startswith('from ')):
                issues.append(CodeIssue(
                    message="Import not at top of file",
                    severity=Severity.LOW,
                    category=IssueCategory.STYLE,
                    line_number=i,
                    suggestion="Move imports to the top of the file"
                ))
            
            if ';' in line and not line.strip().startswith('#'):
                issues.append(CodeIssue(
                    message="Multiple statements on one line",
                    severity=Severity.LOW,
                    category=IssueCategory.STYLE,
                    line_number=i,
                    suggestion="Split into separate lines"
                ))
        
        return issues
    
    @staticmethod
    def check_documentation(code: str) -> List[CodeIssue]:
        """Check documentation issues"""
        issues = []
        
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    has_docstring = (node.body and 
                                    isinstance(node.body[0], ast.Expr) and
                                    isinstance(node.body[0].value, ast.Constant) and
                                    isinstance(node.body[0].value.value, str))
                    
                    if not has_docstring and not node.name.startswith('_'):
                        issues.append(CodeIssue(
                            message=f"Function '{node.name}' missing docstring",
                            severity=Severity.LOW,
                            category=IssueCategory.DOCUMENTATION,
                            line_number=node.lineno,
                            suggestion="Add a docstring describing the function's purpose"
                        ))
                
                elif isinstance(node, ast.ClassDef):
                    has_docstring = (node.body and 
                                    isinstance(node.body[0], ast.Expr) and
                                    isinstance(node.body[0].value, ast.Constant) and
                                    isinstance(node.body[0].value.value, str))
                    
                    if not has_docstring:
                        issues.append(CodeIssue(
                            message=f"Class '{node.name}' missing docstring",
                            severity=Severity.LOW,
                            category=IssueCategory.DOCUMENTATION,
                            line_number=node.lineno,
                            suggestion="Add a docstring describing the class"
                        ))
        except SyntaxError:
            pass
        
        return issues
    
    @staticmethod
    def check_best_practices(code: str) -> List[CodeIssue]:
        """Check for best practice violations"""
        issues = []
        
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ExceptHandler) and node.type is None:
                    issues.append(CodeIssue(
                        message="Bare 'except:' clause",
                        severity=Severity.MEDIUM,
                        category=IssueCategory.BEST_PRACTICE,
                        line_number=node.lineno,
                        suggestion="Specify exception type, e.g., 'except Exception:'"
                    ))
                
                if isinstance(node, ast.FunctionDef):
                    for default in node.args.defaults:
                        if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                            issues.append(CodeIssue(
                                message=f"Mutable default argument in '{node.name}'",
                                severity=Severity.MEDIUM,
                                category=IssueCategory.BEST_PRACTICE,
                                line_number=node.lineno,
                                suggestion="Use None as default and initialize inside function"
                            ))
                
                if isinstance(node, ast.Global):
                    issues.append(CodeIssue(
                        message=f"Use of 'global' statement",
                        severity=Severity.LOW,
                        category=IssueCategory.BEST_PRACTICE,
                        line_number=node.lineno,
                        suggestion="Consider passing values as parameters instead"
                    ))
                
                if isinstance(node, ast.ImportFrom) and any(alias.name == '*' for alias in node.names):
                    issues.append(CodeIssue(
                        message=f"Star import from '{node.module}'",
                        severity=Severity.MEDIUM,
                        category=IssueCategory.BEST_PRACTICE,
                        line_number=node.lineno,
                        suggestion="Import specific names instead of using *"
                    ))
        except SyntaxError:
            pass
        
        return issues

# ============================================================
# AGENTS
# ============================================================

class BaseAgent(ABC):
    """Abstract base class for all agents"""
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def analyze(self, code: str, language: Language) -> List[CodeIssue]:
        """Analyze code and return issues"""
        pass

class SyntaxAnalyzerAgent(BaseAgent):
    """Agent for syntax and AST analysis"""
    
    def __init__(self):
        super().__init__("SyntaxAnalyzer")
        self.tools = CodeAnalysisTools()
    
    def analyze(self, code: str, language: Language) -> List[CodeIssue]:
        issues = []
        
        if language == Language.PYTHON:
            ast_result = self.tools.analyze_ast(code)
            
            if not ast_result.get('valid'):
                issues.append(CodeIssue(
                    message=f"Syntax Error: {ast_result.get('error')}",
                    severity=Severity.CRITICAL,
                    category=IssueCategory.SYNTAX,
                    line_number=ast_result.get('line'),
                    column=ast_result.get('offset')
                ))
        
        return issues

class SecurityAgent(BaseAgent):
    """Agent for security vulnerability detection"""
    
    def __init__(self):
        super().__init__("SecurityAgent")
        self.tools = CodeAnalysisTools()
    
    def analyze(self, code: str, language: Language) -> List[CodeIssue]:
        return self.tools.check_security(code, language)

class StyleAgent(BaseAgent):
    """Agent for code style checking"""
    
    def __init__(self, max_line_length: int = 88):
        super().__init__("StyleAgent")
        self.max_line_length = max_line_length
        self.tools = CodeAnalysisTools()
    
    def analyze(self, code: str, language: Language) -> List[CodeIssue]:
        return self.tools.check_style(code, self.max_line_length)

class ComplexityAgent(BaseAgent):
    """Agent for complexity analysis"""
    
    def __init__(self, max_complexity: int = 10):
        super().__init__("ComplexityAgent")
        self.max_complexity = max_complexity
        self.tools = CodeAnalysisTools()
    
    def analyze(self, code: str, language: Language) -> List[CodeIssue]:
        issues = []
        
        if language == Language.PYTHON:
            complexity = self.tools.calculate_complexity(code)
            
            if complexity['cyclomatic'] > self.max_complexity:
                issues.append(CodeIssue(
                    message=f"High cyclomatic complexity: {complexity['cyclomatic']} (max: {self.max_complexity})",
                    severity=Severity.MEDIUM,
                    category=IssueCategory.COMPLEXITY,
                    suggestion="Consider breaking down into smaller functions"
                ))
            
            if complexity['max_nesting'] > 4:
                issues.append(CodeIssue(
                    message=f"Deep nesting detected: {complexity['max_nesting']} levels",
                    severity=Severity.MEDIUM,
                    category=IssueCategory.COMPLEXITY,
                    suggestion="Reduce nesting by using early returns or extracting functions"
                ))
        
        return issues

class DocumentationAgent(BaseAgent):
    """Agent for documentation checking"""
    
    def __init__(self):
        super().__init__("DocumentationAgent")
        self.tools = CodeAnalysisTools()
    
    def analyze(self, code: str, language: Language) -> List[CodeIssue]:
        if language == Language.PYTHON:
            return self.tools.check_documentation(code)
        return []

class BestPracticesAgent(BaseAgent):
    """Agent for best practices checking"""
    
    def __init__(self):
        super().__init__("BestPracticesAgent")
        self.tools = CodeAnalysisTools()
    
    def analyze(self, code: str, language: Language) -> List[CodeIssue]:
        if language == Language.PYTHON:
            return self.tools.check_best_practices(code)
        return []

# ============================================================
# ORCHESTRATOR
# ============================================================

class CodeReviewOrchestrator:
    """Orchestrates all agents for comprehensive code review"""
    
    def __init__(self):
        self.tools = CodeAnalysisTools()
        self.agents = [
            SyntaxAnalyzerAgent(),
            SecurityAgent(),
            StyleAgent(),
            ComplexityAgent(),
            DocumentationAgent(),
            BestPracticesAgent()
        ]
    
    def review_code(self, code: str, language: Language = None) -> ReviewResult:
        """Perform comprehensive code review"""
        start_time = time.time()
        
        if language is None:
            language = LanguageDetector.detect(code)
        
        code_hash = CodeUtils.compute_hash(code)
        
        all_issues: List[CodeIssue] = []
        for agent in self.agents:
            try:
                issues = agent.analyze(code, language)
                all_issues.extend(issues)
            except Exception as e:
                print(f"Error in {agent.name}: {e}")
        
        metrics = self._calculate_metrics(code, language)
        
        execution_time = time.time() - start_time
        result = ReviewResult(
            code_hash=code_hash,
            language=language,
            timestamp=datetime.now().isoformat(),
            issues=all_issues,
            metrics=metrics,
            execution_time=execution_time
        )
        
        return result
    
    def _calculate_metrics(self, code: str, language: Language) -> CodeMetrics:
        """Calculate code metrics"""
        total, blank, comment = CodeUtils.count_lines(code)
        
        metrics = CodeMetrics(
            lines_of_code=total - blank - comment,
            blank_lines=blank,
            comment_lines=comment
        )
        
        if language == Language.PYTHON:
            complexity = self.tools.calculate_complexity(code)
            metrics.cyclomatic_complexity = complexity['cyclomatic']
            metrics.cognitive_complexity = complexity['cognitive']
            metrics.nesting_depth = complexity['max_nesting']
            metrics.maintainability_index = self.tools.calculate_maintainability_index(
                code, complexity['cyclomatic']
            )
            
            ast_result = self.tools.analyze_ast(code)
            if ast_result.get('valid'):
                metrics.function_count = len(ast_result.get('functions', []))
                metrics.class_count = len(ast_result.get('classes', []))
        
        return metrics

# ============================================================
# GEMINI AI INTEGRATION
# ============================================================

class GeminiCodeReviewer:
    """Gemini AI-powered code reviewer"""
    
    def __init__(self, api_key: str = None):
        self.model = None
        self.available = False
        
        if GENAI_AVAILABLE:
            key = api_key or os.environ.get('GOOGLE_API_KEY')
            if key:
                try:
                    genai.configure(api_key=key)
                    self.model = genai.GenerativeModel('gemini-2.0-flash')
                    self.available = True
                except Exception as e:
                    print(f"Failed to initialize Gemini: {e}")
    
    def get_suggestions(self, code: str, issues: List[CodeIssue], 
                        language: Language = Language.PYTHON) -> Optional[str]:
        """Get AI-powered suggestions"""
        if not self.available:
            return None
        
        issues_text = "\n".join([
            f"{i+1}. [{issue.severity.value.upper()}] {issue.message}" + 
            (f" (Line {issue.line_number})" if issue.line_number else "")
            for i, issue in enumerate(issues[:10])
        ])
        
        prompt = f"""You are an expert {language.value} code reviewer. Analyze this code and provide specific fixes.

## Code:
```{language.value}
{code}
```

## Issues Detected:
{issues_text}

## Your Task:
1. Explain each issue briefly (1-2 sentences)
2. Provide corrected code snippets
3. Give best practice recommendations

Keep your response concise and actionable. Use markdown formatting.
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error getting AI suggestions: {str(e)}"

# ============================================================
# FLASK WEB APPLICATION
# ============================================================

app = Flask(__name__)
CORS(app)

# Initialize components
orchestrator = CodeReviewOrchestrator()
gemini_reviewer = GeminiCodeReviewer()

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/review', methods=['POST'])
def api_review():
    """API endpoint for code review"""
    try:
        data = request.get_json()
        code = data.get('code', '')
        language_str = data.get('language')
        include_ai = data.get('include_ai', False)
        
        if not code.strip():
            return jsonify({'error': 'No code provided'}), 400
        
        # Detect or parse language
        language = None
        if language_str:
            try:
                language = Language(language_str)
            except ValueError:
                language = None
        
        # Perform review
        result = orchestrator.review_code(code, language)
        
        # Get AI suggestions if requested
        if include_ai and result.issues:
            ai_suggestions = gemini_reviewer.get_suggestions(
                code, result.issues, result.language
            )
            result.ai_suggestions = ai_suggestions
        
        return jsonify(result.to_dict())
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'gemini_available': gemini_reviewer.available,
        'agents': [a.name for a in orchestrator.agents]
    })

# ============================================================
# MAIN
# ============================================================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("AI CODE REVIEW AGENT - WEB APPLICATION")
    print("="*60)
    print(f"\nGemini AI Available: {gemini_reviewer.available}")
    print(f"Agents Loaded: {len(orchestrator.agents)}")
    for agent in orchestrator.agents:
        print(f"   - {agent.name}")
    print("\nStarting web server...")
    print("Access at: http://localhost:5000")
    print("\n" + "="*60 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)