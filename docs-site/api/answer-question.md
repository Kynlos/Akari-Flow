---
title: Answer Question
layout: default
---

# answer-question.py

*Auto-generated from `.github/scripts/answer-question.py`*

# `answer-question.py` – Interactive PR Bot

> **What this module does**  
> The script is a lightweight GitHub Actions helper that answers questions asked in pull‑request comments.  
> It reads the comment text, determines if the bot should reply, builds a code context from the changed files, sends a prompt to a LLM (Groq by default), and writes the bot’s reply to `bot_response.md`.

---

## Exports

| Export | Type | Description |
|--------|------|-------------|
| `should_respond(comment_text: str) -> bool` | Function | Heuristic that decides whether a comment is a question for the bot. |
| `load_changed_files() -> List[str]` | Function | Reads `pr_files.txt` and returns a list of changed file paths. |
| `build_code_context(files: Iterable[str]) -> str` | Function | Builds a Markdown‑formatted code context from the provided file list. |
| `answer_question(question: str, code_context: str) -> str` | Function | Sends a prompt to the LLM and returns the generated answer. |
| `main() -> None` | Function | CLI entry point – orchestrates the whole workflow. |

> **Note**: The module also defines a few module‑level constants (`GROQ_API_KEY`, `COMMENT_BODY`, `COMMENT_USER`, `MODEL`) that are read from environment variables.

---

## Usage Examples

> These examples assume the script is executed in a GitHub Actions environment where the required environment variables are set.

### 1. `should_respond`

```python
from answer_question import should_respond

comment = "Hey @bot, can you explain why this change is needed?"
if should_respond(comment):
    print("Bot will reply.")
else:
    print("No reply needed.")
```

### 2. `load_changed_files`

```python
from answer_question import load_changed_files

changed = load_changed_files()
print(f"Changed files: {changed}")
```

> The function expects a file named `pr_files.txt` in the current working directory. Each line should contain a relative path to a changed file.

### 3. `build_code_context`

```python
from answer_question import build_code_context

files = ['src/main.py', 'src/utils/helpers.ts']
context = build_code_context(files)
print(context)
```

> The returned string is Markdown‑formatted and can be embedded in a prompt.

### 4. `answer_question`

```python
from answer_question import answer_question

question = "Why did we rename the function `foo` to `bar`?"
code_context = build_code_context(['src/main.py'])
reply = answer_question(question, code_context)
print(reply)
```

### 5. Running the script

```bash
# In a GitHub Action step
- name: Answer PR question
  run: python .github/scripts/answer-question.py
  env:
    GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
    COMMENT_BODY: ${{ github.event.comment.body }}
    COMMENT_USER: ${{ github.event.comment.user.login }}
    LLM_MODEL: openai/gpt-oss-20b
```

After execution, the bot’s reply will be available in `bot_response.md`.

---

## Function Details

### `should_respond(comment_text: str) -> bool`

| Parameter | Type | Description |
|-----------|------|-------------|
| `comment_text` | `str` | The raw comment body. |

| Return | Description |
|--------|-------------|
| `bool` | `True` if the comment looks like a question for the bot; otherwise `False`. |

> **Implementation notes**  
> * Ignores comments that start with `## 🤖` (the bot’s own replies).  
> * Looks for question indicators such as `?`, `@bot`, `explain`, `what`, `how`, `why`, `show me`, `tell me`.  
> * Case‑insensitive search.

---

### `load_changed_files() -> List[str]`

| Parameter | Type | Description |
|-----------|------|-------------|
| None | | |

| Return | Description |
|--------|-------------|
| `List[str]` | Paths of changed files listed in `pr_files.txt`. Empty list if the file does not exist or is empty. |

> **Implementation notes**  
> * Reads `pr_files.txt` line‑by‑line, stripping whitespace.  
> * Skips blank lines.

---

### `build_code_context(files: Iterable[str]) -> str`

| Parameter | Type | Description |
|-----------|------|-------------|
| `files` | `Iterable[str]` | Iterable of file paths to include in the context. |

| Return | Description |
|--------|-------------|
| `str` | Markdown string that contains the code snippets of the provided files. |

> **Implementation notes**  
> * Supports `.ts`, `.js`, `.tsx`, `.jsx`, `.py`.  
> * Skips non‑code files or missing files.  
> * Truncates files larger than 10 000 characters to the first 200 lines and appends `... (file truncated)`.  
> * Each file is wrapped in a Markdown code block with the appropriate language hint.

---

### `answer_question(question: str, code_context: str) -> str`

| Parameter | Type | Description |
|-----------|------|-------------|
| `question` | `str` | The question extracted from the PR comment. |
| `code_context` | `str` | Markdown context built from the changed files. |

| Return | Description |
|--------|-------------|
| `str` | The LLM’s answer or an error message. |

> **Implementation notes**  
> * Requires `GROQ_API_KEY` to be set; otherwise returns an error string.  
> * Constructs a prompt that includes the code context and the question.  
> * Calls `get_client().call_chat` with `model=MODEL` (default `openai/gpt-oss-20b`).  
> * Uses `temperature=0.3`, `max_tokens=1500`.  
> * If the LLM returns a falsy value, returns a generic error string.  
> * Catches exceptions and returns an error string prefixed with ❌.

---

### `main() -> None`

| Parameter | Type | Description |
|-----------|------|-------------|
| None | | |

| Return | Description |
|--------|-------------|
| `None` | Prints progress to stdout and writes the bot’s reply to `bot_response.md`. |

> **Workflow**  
> 1. Prints header.  
> 2. Calls `should_respond` on `COMMENT_BODY`. Exits if `False`.  
> 3. Loads changed files via `load_changed_files`. Exits if none.  
> 4. Builds code context with `build_code_context`.  
> 5. Generates answer with `answer_question`.  
> 6. Formats a Markdown reply and writes it to `bot_response.md`.  
> 7. Prints a success banner.

---

## Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `GROQ_API_KEY` | API key for the LLM provider. | **Required** |
| `COMMENT_BODY` | The raw comment text that triggered the action. | **Required** |
| `COMMENT_USER` | GitHub username of the commenter. | `user` |
| `LLM_MODEL` | LLM model name. | `openai/gpt-oss-20b` |

> **Tip**: In a GitHub Action, set these via `env:` or `secrets:`.

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `llm` | Provides `get_client()` which abstracts the LLM API call. |
| `requests` | Used indirectly by the `llm` client.
