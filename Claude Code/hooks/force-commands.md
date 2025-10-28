### 🧩 1. Create or edit your config

Add this snippet to your project’s **`.claude/settings.json`** (or global `~/.claude/settings.json`):

```json
{
  "hooks": {
    "PreToolUse": "jq -e '.args | tostring | test(\"force\")' <<< \"$CLAUDE_EVENT\" && exit 1 || exit 0"
  }
}
```

---

### 🧪 2. Verify syntax

Run this in your terminal to confirm the JSON is valid:

```bash
cat .claude/settings.json | jq .
```

If it prints nicely formatted output, your syntax is good.


### ⚙️ 3. Simulate the hook manually

You can test it outside Claude Code by emulating a `$CLAUDE_EVENT`:

```bash
CLAUDE_EVENT='{"tool":"exampleTool","args":{"force":true}}' \
bash -c 'jq -e ".args | tostring | test(\"force\")" <<< "$CLAUDE_EVENT" && echo "Blocked" || echo "Allowed"'
```

Expected output → `Blocked` ✅
Now try without `"force"`:

```bash
CLAUDE_EVENT='{"tool":"exampleTool","args":{"file":"data.txt"}}' \
bash -c 'jq -e ".args | tostring | test(\"force\")" <<< "$CLAUDE_EVENT" && echo "Blocked" || echo "Allowed"'
```

Expected output → `Allowed` ✅
