# Instruction file with four deliberate route defects.

# ghost-skill
- **ghost-skill** (`~/.claude/skills/definitely-not-a-real-skill-xyz/SKILL.md`) - does nothing.
When the user types `/ghost-skill`, invoke the Skill tool with `skill: "ghost-skill"` before doing anything else.

# wrong-root
- **wrong-root** (`totally/made/up/path/SKILL.md`) - declared relative to nothing.

# real-trigger-no-path
When the user types `/another-missing-skill-abc`, invoke the Skill tool before doing anything else.

# a route that DOES resolve, so the fixture is not uniformly broken
- **eli5** (`~/.claude/skills/eli5/SKILL.md`) - explain simply.
When the user types `/eli5`, invoke the Skill tool with `skill: "eli5"` before doing anything else.
