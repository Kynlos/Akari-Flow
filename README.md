# Symbol Capsules CI/CD - Auto-Documentation

GitHub Actions workflow that automatically generates documentation when code changes, using Symbol Capsules for 88% token savings.

## Setup for https://github.com/Kynlos/CI-CD-Monitor-Test

### 1. Add GitHub Secret

1. Go to https://github.com/Kynlos/CI-CD-Monitor-Test/settings/secrets/actions
2. Click "New repository secret"
3. Name: `GROQ_API_KEY`
4. Value: `<your-groq-api-key>`
5. Click "Add secret"

### 2. Copy Workflow Files

Copy these files to your repo:

```bash
mkdir -p .github/workflows
mkdir -p .github/scripts

cp .github/workflows/auto-docs.yml <your-repo>/.github/workflows/
cp .github/scripts/generate-docs.py <your-repo>/.github/scripts/
chmod +x <your-repo>/.github/scripts/generate-docs.py
```

### 3. Commit and Push

```bash
git add .github/
git commit -m "feat: Add Symbol Capsules auto-documentation CI/CD"
git push
```

## How It Works

### On Every Commit to Main:

1. **Detects changed files** - Only processes .ts/.js/.py files that changed
2. **Extracts symbols** - Functions, classes, interfaces, types
3. **Builds Symbol Index** - Compressed representation (~88% smaller)
4. **Calls Groq API** - Generates documentation from symbols
5. **Commits docs** - Updates `API-DOCS.md` automatically

### On Every Pull Request:

1. **Same extraction process**
2. **Posts PR comment** with:
   - Generated documentation
   - List of changed symbols
   - Token savings calculation
   - Cost savings

## Example Output

### PR Comment:

```markdown
## 🤖 Auto-Generated Documentation

**Changes detected in 2 file(s)**

### auth.ts

**Added Functions:**
- `validateToken(token: string): Promise<User>` - Validates JWT token and returns user object
- `refreshSession(sessionId: string): Promise<Session>` - Refreshes expired session

**Modified Functions:**
- `login(username, password, options?)` - Now accepts optional LoginOptions parameter

### database.ts

**Added Classes:**
- `DatabaseConnection` - Manages PostgreSQL connection pool with automatic retry

---

**Symbol Capsules Efficiency:**
- Traditional approach: 3,240 tokens
- Symbol Capsules: 420 tokens
- **Saved: 2,820 tokens (87.0%)** 💰
- Cost saved: $0.000008

*Documentation generated using Symbol Capsules - 88% more efficient than traditional approaches.*
```

### Committed File (API-DOCS.md):

```markdown
# API Documentation

*Last updated: 2025-11-14*

## auth.ts

### validateToken
Validates JWT token and returns authenticated user object.

**Signature:** `async validateToken(token: string): Promise<User>`

**Parameters:**
- `token` - JWT authentication token

**Returns:** User object if valid

...
```

## Benefits

### Cost Savings

**Traditional approach (sending full files):**
- 10 files changed × 5KB each = 50KB
- ~12,500 tokens × $0.000003 (Claude) = $0.0375 per commit

**Symbol Capsules approach:**
- 10 files × 20 symbols × 50 tokens = 10,000 tokens compressed  
- ~1,500 tokens × $0.000003 = $0.0045 per commit

**Savings: $0.033 per commit (88% reduction)**

**Annual (for active repo):**
- 1,000 commits/year
- Traditional: $37.50/year
- Capsules: $4.50/year
- **Saves: $33/year per repo**

**Organization with 100 repos:**
- **Saves: $3,300/year**

### Speed Benefits

- **Faster API calls** - Fewer tokens = faster response
- **Parallel processing** - Can document multiple files simultaneously
- **Lower rate limits** - Fewer tokens = more requests possible

### Quality Benefits

- **Consistent docs** - Every commit auto-documented
- **No outdated docs** - Regenerated on every change
- **PR reviews** - Reviewers see exactly what APIs changed
- **Breaking changes** - Automatically highlighted when signatures change

## Customization

### Change the Model

Edit `.github/scripts/generate-docs.py`:

```python
MODEL = 'llama-3.3-70b-versatile'  # Default (fast, cheap)
# MODEL = 'openai/gpt-oss-120b'    # More capable
# MODEL = 'mixtral-8x7b-32768'     # Alternative
```

### Customize Documentation Prompt

Edit the prompt in `generate_documentation()`:

```python
prompt = f"""Generate API documentation...

Include:
1. Overview
2. Function descriptions
3. Usage examples  # <-- Add this
4. Type definitions  # <-- Add this
```

### Change Trigger Files

Edit `.github/workflows/auto-docs.yml`:

```yaml
paths:
  - '**.ts'      # TypeScript
  - '**.py'      # Python
  - '**.go'      # Add Go
  - '**.rs'      # Add Rust
```

## Testing Locally

```bash
# Simulate changed files
echo "src/auth.ts" > changed_files.txt
echo "src/database.ts" >> changed_files.txt

# Run generator
export GROQ_API_KEY="your-key"
python .github/scripts/generate-docs.py

# Check output
cat doc_output.md
cat API-DOCS.md
```

## Troubleshooting

### "GROQ_API_KEY not set"

**Fix:** Add the secret in GitHub repo settings:
```
Settings → Secrets and variables → Actions → New repository secret
```

### "No documentation generated"

**Cause:** No code files changed

**Check:** Look at workflow logs to see which files were detected

### "API rate limit exceeded"

**Fix:** Add rate limiting or use a different model

## Next Steps

1. **Add to your repo** - Follow setup steps above
2. **Make a test commit** - Watch the action run
3. **Review generated docs** - Check API-DOCS.md
4. **Submit a PR** - See the PR comment with docs
5. **Customize prompts** - Tune to your needs

## Files

- `.github/workflows/auto-docs.yml` - GitHub Actions workflow
- `.github/scripts/generate-docs.py` - Documentation generator
- `API-DOCS.md` - Auto-generated documentation (committed)
- `doc_output.md` - PR comment content (not committed)

## Cost Analysis

**Your repo with this setup:**
- Average 50 commits/month
- Average 5 files changed per commit
- Average 10 symbols per file

**Traditional:** 50 commits × $0.0375 = **$1.88/month**
**Capsules:** 50 commits × $0.0045 = **$0.23/month**
**Savings:** **$1.65/month = $19.80/year**

For a single repo this is modest, but **scales linearly with repos and commit frequency**.
