# 🚀 Intelligent CI/CD Documentation System (v2.0)

> **Automated documentation, visualization, breaking change detection, and team notifications powered by AI**

A comprehensive GitHub Actions-based system that automatically generates documentation, visualizes architecture, detects breaking changes, generates static documentation sites, and notifies your team across multiple platforms—all powered by LLM intelligence.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF)](https://github.com/features/actions)
[![Powered by Groq](https://img.shields.io/badge/Powered%20by-Groq-orange)](https://groq.com)

---

## 📋 Table of Contents

- [Overview](#overview)
- [New in v2.0](#new-in-v20)
- [Key Features](#key-features)
- [Quick Start](#quick-start)
- [Detailed Features](#detailed-features)
- [Setup Guide](#setup-guide)
- [Configuration](#configuration)
- [CLI Tool](#cli-tool)
- [Usage Examples](#usage-examples)
- [Architecture](#architecture)
- [Contributing](#contributing)

---

## 💡 Why Intelligent CI/CD?

**"Documentation is the code."** — *Everyone says it, but nobody actually searches the code.*

In reality, documentation rots the moment it's written. Developers hate writing it, and teams struggle to maintain it. The cost? Slower onboarding, silent breaking changes, and critical knowledge locked in people's heads.

**This system aims to eliminate documentation debt entirely.**

By treating your CI pipeline as an **Autonomous Knowledge Engine**, this tool ensures that:
1.  **Docs never drift**: If the code changes, the docs update. Instantly.
2.  **Architecture is visible**: Hidden dependencies are visualized automatically.
3.  **Safety is enforced**: Breaking changes are caught *before* they merge.

It allows your team to focus on **building features**, while the Agent handles the **explanation**.

---

## 🎯 Overview

This system revolutionizes code documentation by automatically:
- **Analyzing** every code change with AST-based precision
- **Visualizing** class hierarchies and dependencies with Mermaid.js
- **Generating** comprehensive documentation and static websites
- **Detecting** breaking changes and API modifications
- **Notifying** your team across Discord, Slack, and Pushbullet
- **Assisting** with PR reviews through an Agentic Bot (now with safe Search/Replace)

**No manual documentation updates. No outdated docs. Just intelligent automation.**

---

## 🌟 New in v2.0

We've massively upgraded the system to be faster, safer, and more visual:

- **🏗️ Automated Architecture Diagrams**: Now auto-generates [Mermaid.js](https://mermaid.js.org/) class diagrams to visualize your code structure.
- **🌐 Documentation Portal**: Auto-generates a **searchable static HTML website** with dark mode (deployment ready).
- **🛠️ Unified CLI**: A new `cicd-cli.py` tool to run analysis, docs, and site generation locally.
- **⚡ Diff-Aware Processing**: Optimized LLM usage ensures we only process changed code (faster & cheaper).
- **🛡️ Safer Agentic Bot**: The PR bot now uses a safe `SEARCH/REPLACE` strategy to prevent accidental overwrites.
- **⚙️ Externalized Config**: All language patterns and rules are now in `.github/config/languages.json`.
- **🐍 AST Parsing**: Switched to robust AST parsing for Python (goodbye regex fragility!).

---

## ✨ Key Features

### 🔍 **Automated Code Analysis**
- **Breaking Change Detection** - Identifies signature changes, removed exports, and API modifications
- **Cross-File Impact Analysis** - Detects how changes in one file affect others
- **AST-Based Quality Scoring** - 0-100 score based on real code structure (complexity, maintainability)
- **Security Scanning** - Detects hardcoded secrets, SQL injection, XSS, etc.

### 📚 **Intelligent Documentation & Visualization**
- **AI-Generated Docs** - LLM creates comprehensive documentation from your code
- **Architecture Diagrams** - Visualizes class inheritance and dependencies automatically
- **Documentation Portal** - Generates a static site (`docs-site/`) for easy browsing
- **Changelog Automation** - Auto-updates CHANGELOG.md with categorized changes

### 💬 **PR Enhancement & Agentic Bot**
- **Smart PR Comments** - Detailed analysis posted on every pull request
- **Agentic Bot** - Make code changes via comments (`[auto] add tests`)
- **Safe Edits** - Uses `SEARCH/REPLACE` blocks to ensure data integrity

### 🔔 **Multi-Platform Notifications**
- **Discord** - Rich embeds with color-coded alerts
- **Slack** - Professional blocks with action buttons
- **Pushbullet** - Mobile/desktop push notifications

---

## 🚀 Quick Start

### Prerequisites
- GitHub repository
- [Groq API key](https://console.groq.com) (free tier available)
- Python 3.11+ (for local CLI)

### 5-Minute Setup

```bash
# 1. Clone this repo
git clone https://github.com/Kynlos/CI-CD-Monitor-Test.git
cd CI-CD-Monitor-Test

# 2. Copy workflows to your repo
cp -r .github <your-repo>/

# 3. Add required secret in GitHub Settings > Secrets > Actions
# GROQ_API_KEY = <your-groq-api-key>

# 4. Push a code change and watch the magic! ✨
git add .
git commit -m "feat: Enable intelligent documentation"
git push
```

---

## 🛠️ CLI Tool (Local Usage)

The new **Unified CLI** allows you to run the pipeline locally without pushing to GitHub.

```bash
# Install dependencies
pip install requests markdown

# Run full pipeline (Analysis -> Docs -> Site)
python cicd-cli.py full-run

# Run individual steps
python cicd-cli.py analyze <file>
python cicd-cli.py gen-docs <file>
python cicd-cli.py build-site
```

The generated site will be in `docs-site/index.html`.

---

## ⚙️ Configuration

### Language Rules (`.github/config/languages.json`) // NEW
All parsing rules, security patterns, and complexity keywords are now centralized here. You can easily add support for new languages by editing this file.

```json
"python": {
    "extensions": [".py"],
    "type": "ast",  // Uses AST parser
    "complexity": ["if", "elif", "for", "while"]
},
"javascript": {
    "extensions": [".js", ".ts"],
    "type": "regex", // Uses Regex fallbacks
    "function_pattern": "..."
}
```

### LLM Model
Edit `.github/scripts/generate-docs.py`:
```python
MODEL = 'openai/gpt-oss-20b' # or 'llama-3.1-70b-versatile'
```

---

## 📖 Usage Examples

### Example 1: Agentic Bot (Safety First)
To modify code securely, comment on a PR:
```
[auto] add a docstring to the LoginController class
```
The bot will:
1. Fetch the file content.
2. Locate the specific class using `SEARCH` blocks.
3. Apply the `REPLACE` block with the new docstring.
4. Commit the change automatically.

### Example 2: Breaking Change Detection
Modify a function signature:
```python
# Before
def process(data): ...

# After
def process(data, force=False): ...
```
**Result:**
- 🚨 **Breaking Change**: Signature modified.
- 🏷️ PR labeled `breaking-change`.
- 🔔 Urgent notification sent to Discord.

---

## 🎨 Documentation Portal
The system now builds a static site in the `docs-site` directory.
- **Sidebar Navigation**: Browse all modules.
- **Dark Mode**: Built-in.
- **Diagrams**: Renders Mermaid.js charts inline.

---

## 🏗️ Architecture

1. **Trigger**: GitHub Action (`auto-docs.yml`) triggers on Push/PR.
2. **Analysis**: `code-analyzer.py` parses code (AST/Regex) and scores quality.
3. **Documentation**: `generate-docs.py` uses LLM to write docs & `diagram_generator.py` to draw charts.
4. **Site Gen**: `site_generator.py` builds the HTML portal.
5. **Notification**: `send-notifications.py` alerts external platforms.
6. **Commit**: The Action commits all artifacts (`docs/`, `docs-site/`, `CHANGELOG.md`) back to the repo.

---
*Built with ❤️ by the CI/CD Intelligence Team*
