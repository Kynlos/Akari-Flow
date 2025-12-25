---
title: Agentic Pr Bot
layout: default
---

# agentic-bot.py

*Auto-generated from `.github/scripts/agentic-bot.py`*

# Agentic PR Bot – API Documentation

> **File**: `.github/scripts/agentic-bot.py`  
> **Purpose**: A GitHub‑Actions‑friendly bot that reads a PR comment, classifies the intent, generates safe *SEARCH/REPLACE* code edits with an LLM, applies them, commits, pushes, and writes a human‑readable response.

> **Key Features**
> * Authorisation checks (PR author or assignees)
> * Intent classification (CLEAR_ACTION / POSSIBLE_ACTION / QUESTION_ONLY)
> * LLM‑driven code‑editing with a strict SEARCH/REPLACE format
> * Safe application of edits (exact match, no fuzzy logic)
> * Automatic Git commit & push
> * Generates `bot_response.md` for PR comment

---

## 1. Overview

The script is designed to be triggered by a PR comment that
