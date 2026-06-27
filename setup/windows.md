# Windows Setup Notes

### Palace path format

Use backslashes in the JSON (escaped):

```json
"args": ["--palace", "C:\\Users\\yourname\\claude-memory"]
```

### settings.json location

```
%USERPROFILE%\.claude\settings.json
```

i.e. `C:\Users\yourname\.claude\settings.json`

### Hooks — PowerShell vs bash

The `settings.json.template` includes both `command` (bash/WSL) and `commandWindows` (PowerShell) for each hook. Claude Code picks the right one automatically on Windows.

### Mempalace wake-up on Windows

The hook uses:
```powershell
if (Get-Command mempalace -ErrorAction SilentlyContinue) { mempalace --palace "C:\Users\yourname\claude-memory" wake-up }
```

If mempalace isn't on PATH after install, restart your terminal or run:
```powershell
$env:PATH += ";$env:APPDATA\npm"
```
