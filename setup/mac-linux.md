# Mac / Linux Setup Notes

### Palace path format

Use forward slashes:

```json
"args": ["--palace", "/home/yourname/claude-memory"]
```

Mac recommended path: `~/claude-memory` → `/Users/yourname/claude-memory`

### settings.json location

```
~/.claude/settings.json
```

### Merging settings (if file already exists)

Don't overwrite your existing settings. Instead, manually add the `mcpServers` and `hooks` sections, or use:

```bash
# Install jq first: brew install jq (Mac) or apt install jq (Linux)
jq -s '.[0] * .[1]' ~/.claude/settings.json settings.json.template > /tmp/merged.json
mv /tmp/merged.json ~/.claude/settings.json
```

### Mempalace PATH

After `npm install -g mempalace-mcp`, confirm it's available:

```bash
which mempalace
mempalace --version
```

If not found, add npm global bin to PATH:

```bash
# Add to ~/.bashrc or ~/.zshrc
export PATH="$PATH:$(npm bin -g)"
```
