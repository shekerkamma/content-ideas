# Worker brief and manifest

Each Codex dispatch is stateless and sees only its brief.

```text
You are Codex worker <ID> completing ONE independent subtask.

SUBTASK: <atomic goal>
IN SCOPE:
- <included work>
OUT OF SCOPE:
- <excluded work>
INPUTS:
<complete minimal context>

ACCEPTANCE CRITERIA:
1. [<ID>-C1] <observable criterion>
2. [<ID>-C2] <observable criterion>
3. [<ID>-C3] <observable criterion>

REQUIRED OUTPUT FORMAT:
<schema, headings, JSON shape, or unified diff>

ARTIFACT MANIFEST:
- logical_name: <name>
- intended_target: <path or NONE>
- direct_write_allowed: false

VERIFICATION CONTRACT:
- <criterion> -> <check the host will run>

Do only this subtask. Do not modify the user's project or credentials. Label
unsupported claims UNVERIFIED. If required input is absent, begin with
INPUT GAP. Return only the requested output.
```

Redispatch only with the exact failed criterion, observed evidence, and required correction.

Manifest schema:

```json
{
  "default_model": "gpt-5.6-sol",
  "concurrency": 3,
  "timeout_seconds": 600,
  "max_brief_bytes": 100000,
  "workers": [
    {"id": "W1", "brief_file": "briefs/W1.txt", "output_file": "results/W1.txt"},
    {"id": "W2", "model": "gpt-5.6-terra", "brief_file": "briefs/W2.txt", "output_file": "results/W2.txt"}
  ]
}
```

Omit model fields to inherit the authenticated Codex CLI default. Confirm explicit model IDs with a real completion before relying on them.
