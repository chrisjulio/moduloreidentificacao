#!/usr/bin/env python3
"""PreToolUse guard: reject PowerShell-only syntax sent to the Bash tool.

On this Windows machine the Bash tool runs Git Bash (``/usr/bin/bash``), a
shell *separate* from PowerShell. PowerShell here-strings and cmdlets routed
to it fail with errors like ``=: command not found`` or
``syntax error near unexpected token '('`` — a recurring, wasteful mistake.

This guard inspects the command a Bash tool call is about to run and denies it
when it carries unambiguous PowerShell signals, pointing the agent to the
PowerShell tool instead. It is a heuristic safety net, not a shell parser:
when in doubt it stays out of the way (any parsing failure → allow).

Wired in ``.claude/settings.json`` as a ``PreToolUse`` hook matching ``Bash``.
Reads the tool payload as JSON on stdin and, on a match, prints a
``permissionDecision: deny`` decision (the documented preferred form).
"""

import json
import re
import sys

# Signals that essentially never appear in legitimate POSIX / Git Bash usage
# in this repository, but are hallmarks of PowerShell. Each entry is
# (compiled-or-raw pattern, human-readable label for the deny message).
_POWERSHELL_SIGNALS: list[tuple[str, str]] = [
    (r"@['\"]", "here-string (@'...'@ or @\"...\"@)"),
    (r"\$env:", "$env: variable reference"),
    (r"\[System\.", "[System.*] .NET type reference"),
    (r"-Encoding\s+utf-?8", "-Encoding parameter"),
    (
        r"\b(?:Set-Content|Get-Content|Add-Content|Out-File|New-Item|"
        r"Get-ChildItem|Remove-Item|Select-Object|Where-Object|"
        r"ForEach-Object|Write-Output|Write-Host|ConvertFrom-Json|"
        r"ConvertTo-Json|Get-Command|Test-Path|Set-Location)\b",
        "PowerShell Verb-Noun cmdlet",
    ),
]


def find_signal(command: str) -> str | None:
    """Return the label of the first PowerShell signal found, else None."""
    for pattern, label in _POWERSHELL_SIGNALS:
        if re.search(pattern, command):
            return label
    return None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        # Unparseable payload: never interfere with the tool call.
        return 0

    command = payload.get("tool_input", {}).get("command", "") or ""
    label = find_signal(command)
    if label is None:
        # No PowerShell signal: emit no decision, normal permission flow applies.
        return 0

    reason = (
        f"This command contains PowerShell-only syntax ({label}). On this "
        "Windows machine the Bash tool runs Git Bash, not PowerShell, so it "
        "will fail. Re-issue the command through the PowerShell tool instead."
    )
    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": reason,
            }
        },
        sys.stdout,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
