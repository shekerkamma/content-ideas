"""Structural contract for the content-ideas skill: files present, frontmatter
valid, template wired to the generator, and the Claude Code + Codex packaging
manifests agreeing. No third-party deps."""

import json
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SKILL = REPO / "skills" / "content-ideas"
PIPELINE_SKILL = REPO / "skills" / "pipeline-runner"
PACKAGED_SKILLS = (
    "content-ideas",
    "pipeline-runner",
    "second-brain",
    "plaid",
    "karpathy-guidelines",
)


def _json(rel):
    return json.loads((REPO / rel).read_text(encoding="utf-8"))


def _skill_version():
    fm = (SKILL / "SKILL.md").read_text(encoding="utf-8").split("\n---\n", 1)[0]
    match = re.search(r'(?m)^version:\s*"([^"]+)"\s*$', fm)
    assert match, "SKILL.md version frontmatter not found"
    return match.group(1)


def _pyproject_version():
    text = (REPO / "pyproject.toml").read_text(encoding="utf-8")
    match = re.search(r'(?m)^version\s*=\s*"([^"]+)"', text)
    assert match, "pyproject.toml version not found"
    return match.group(1)


class SkillFilesTests(unittest.TestCase):
    def test_expected_files_exist(self):
        for rel in [
            "SKILL.md",
            "references/content-strategy.md",
            "assets/for-you-template.html",
            "scripts/scrape.py",
            "scripts/generate_feed.py",
            "scripts/gbrain_tool.py",
            "scripts/pipeline_runner.py",
            "scripts/lib/__init__.py",
            "scripts/lib/gbrain.py",
            "scripts/lib/strategy_pipeline.py",
            "scripts/lib/pipeline.py",
        ]:
            self.assertTrue((SKILL / rel).exists(), f"missing {rel}")

    def test_pipeline_runner_files_exist(self):
        self.assertTrue((PIPELINE_SKILL / "SKILL.md").exists(), "missing pipeline-runner/SKILL.md")
        self.assertTrue((REPO / "commands" / "pipeline-runner.md").exists(), "missing commands/pipeline-runner.md")


class FrontmatterTests(unittest.TestCase):
    def setUp(self):
        self.text = (SKILL / "SKILL.md").read_text()

    def test_has_yaml_frontmatter(self):
        self.assertTrue(self.text.startswith("---\n"))
        self.assertGreaterEqual(self.text.count("\n---\n"), 1)

    def test_has_name_and_description(self):
        fm = self.text.split("\n---\n", 1)[0]
        self.assertRegex(fm, r"(?m)^name:\s*content-ideas\s*$")
        self.assertRegex(fm, r"(?m)^description:")

    def test_user_invocable(self):
        fm = self.text.split("\n---\n", 1)[0]
        self.assertRegex(fm, r"(?m)^user-invocable:\s*true\s*$")

    def test_taste_uses_memory_not_learnings_file(self):
        # Taste was migrated from brand/learnings.md to auto-memory.
        self.assertNotIn("brand/learnings.md", self.text)
        self.assertIn("memory", self.text.lower())


class ReferenceDocTests(unittest.TestCase):
    def test_content_strategy_has_no_learnings_file_refs(self):
        cs = (SKILL / "references" / "content-strategy.md").read_text()
        self.assertNotIn("brand/learnings.md", cs)


class TemplateContractTests(unittest.TestCase):
    def setUp(self):
        self.html = (SKILL / "assets" / "for-you-template.html").read_text()

    def test_has_embed_placeholder(self):
        self.assertIn("/*__EMBEDDED_DATA__*/", self.html)

    def test_no_stale_external_data_script(self):
        # The old `<script src="feed-data.js">` handoff must be gone.
        self.assertNotIn('src="feed-data.js"', self.html)

    def test_renderer_reads_feed_data_global(self):
        self.assertIn("FEED_DATA", self.html)

    def test_feedback_layer_present(self):
        self.assertIn("__initFeedback", self.html)
        self.assertIn("FEEDBACK_MODE", self.html)

    def test_merged_posts_tab(self):
        # Posts + Ideas tabs, single posts list, sort/filter controls.
        self.assertIn('data-tab="posts"', self.html)
        self.assertIn('data-tab="ideas"', self.html)
        self.assertIn('id="posts-list"', self.html)
        self.assertIn("renderControlBar", self.html)
        self.assertIn("setupPostControls", self.html)
        self.assertIn('data-sort="popular"', self.html)
        self.assertIn('data-sort="recent"', self.html)
        self.assertIn("outlier-toggle", self.html)

    def test_old_three_tab_structure_gone(self):
        # The separate Competitors / Top Performers tabs were merged away.
        self.assertNotIn('data-tab="competitors"', self.html)
        self.assertNotIn('data-tab="top"', self.html)
        self.assertNotIn("renderCompetitors", self.html)
        self.assertNotIn("renderTopPerformers", self.html)


class CrossHostPackagingTests(unittest.TestCase):
    """Codex + Claude Code install from the same repo — the manifests and the
    skill-dir resolution must agree so the skill loads on both hosts."""

    def test_codex_manifest_points_at_skills_tree(self):
        manifest = _json(".codex-plugin/plugin.json")
        self.assertEqual("content-ideas", manifest["name"])
        self.assertEqual("./skills/", manifest["skills"])
        self.assertTrue((SKILL / "SKILL.md").is_file())
        self.assertTrue((SKILL / "scripts" / "scrape.py").is_file())

    def test_repo_marketplace_packages_every_shared_skill(self):
        marketplace = _json(".agents/plugins/marketplace.json")
        plugin_rel = marketplace["plugins"][0]["source"]["path"]
        self.assertTrue(plugin_rel.startswith("./"))
        plugin = REPO / plugin_rel
        manifest = json.loads(
            (plugin / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        self.assertEqual("./skills/", manifest["skills"])

        for name in PACKAGED_SKILLS:
            canonical = REPO / "skills" / name
            packaged = plugin / "skills" / name
            self.assertTrue((packaged / "SKILL.md").is_file(), f"missing packaged {name}")
            canonical_files = {
                path.relative_to(canonical)
                for path in canonical.rglob("*")
                if path.is_file() and "__pycache__" not in path.parts
            }
            packaged_files = {
                path.relative_to(packaged)
                for path in packaged.rglob("*")
                if path.is_file() and "__pycache__" not in path.parts
            }
            self.assertEqual(canonical_files, packaged_files, f"file drift in {name}")
            for rel in canonical_files:
                self.assertEqual(
                    (canonical / rel).read_bytes(),
                    (packaged / rel).read_bytes(),
                    f"content drift in {name}/{rel}",
                )

    def test_plaid_uses_skill_relative_validator(self):
        plaid = (REPO / "skills" / "plaid" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn('"<skill-dir>/scripts/validate-vision.js"', plaid)
        self.assertNotIn("node scripts/validate-vision.js --migrate", plaid)

    def test_cross_host_interaction_fallbacks_are_documented(self):
        content = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        pipeline = (PIPELINE_SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("otherwise ask the", content)
        self.assertIn("normal chat", content)
        self.assertIn("If the skill is unavailable", pipeline)

    def test_versions_match_across_manifests(self):
        version = _pyproject_version()
        self.assertEqual(version, _skill_version())
        self.assertEqual(version, _json(".codex-plugin/plugin.json")["version"])
        self.assertEqual(version, _json(".claude-plugin/plugin.json")["version"])
        self.assertEqual(version, _json("plugin.json")["version"])

        plugins = _json(".claude-plugin/marketplace.json").get("plugins") or []
        self.assertEqual(1, len(plugins))
        self.assertEqual(version, plugins[0]["version"])

    def test_root_manifest_conforms_to_agent_plugins_1_0_0(self):
        # Agent Plugins 1.0.0 uses a closed schema: $schema and name are
        # required, every other key must be one the spec defines, and
        # client-specific data may only live under `extensions`. The Codex
        # `interface` block therefore stays in .codex-plugin/plugin.json --
        # no reverse-domain namespace is registered for any client yet.
        manifest = _json("plugin.json")
        self.assertEqual(
            "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
            manifest["$schema"],
        )
        self.assertEqual("content-ideas", manifest["name"])
        self.assertRegex(manifest["name"], r"^(?!.*(?:--|\.\.))[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$")
        allowed = {
            "$schema",
            "name",
            "version",
            "description",
            "author",
            "homepage",
            "repository",
            "license",
            "keywords",
            "extensions",
        }
        self.assertEqual(set(), set(manifest) - allowed)
        self.assertEqual({"name"}, set(manifest["author"]) - {"email", "url"})

    def test_spec_component_locations_exist(self):
        # Clients discover skills from skills/ and MCP servers from mcp.json.
        # This repo ships no MCP server of its own; a missing mcp.json is
        # explicitly non-fatal per the spec, so only skills/ is required.
        self.assertTrue((REPO / "skills").is_dir())
        for name in PACKAGED_SKILLS:
            self.assertTrue(
                (REPO / "skills" / name / "SKILL.md").is_file(),
                f"skills/{name}/SKILL.md missing",
            )

    def test_agents_md_delegates_to_claude_md(self):
        # Codex reads AGENTS.md; it should re-use the single CLAUDE.md guidance.
        agents = (REPO / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("@CLAUDE.md", agents)
        self.assertIn("OpenHands", agents)
        self.assertIn("github.com/OpenHands/OpenHands", agents)
        self.assertIn("gbrain", agents)
        self.assertIn("GBrain Recall", agents)
        self.assertIn("GBrain Write-back", agents)
        self.assertIn("Read from GBrain first", agents)
        self.assertIn("Write durable findings back to GBrain", agents)
        self.assertIn("embedding-backed semantic retrieval", agents)
        self.assertIn("not the system of record", agents)
        self.assertIn("exa", agents)
        self.assertIn("MCP-connected research server", agents)
        self.assertIn("https://api.exa.ai/search", agents)
        self.assertIn("does not replace", agents)
        self.assertIn("not an exception", agents)
        self.assertIn("BRANDED_PPTX_TEMPLATE", agents)
        self.assertIn("CLIENT_DELIVERY_DIR", agents)
        self.assertIn("reviewed", agents)
        self.assertTrue((REPO / "CLAUDE.md").is_file())

    def test_slash_command_present(self):
        self.assertTrue((REPO / "commands" / "content-ideas.md").is_file())

    def test_pipeline_runner_command_present(self):
        self.assertTrue((REPO / "commands" / "pipeline-runner.md").is_file())

    def test_session_hook_present(self):
        hooks = _json("hooks/hooks.json")
        self.assertIn("SessionStart", hooks["hooks"])
        self.assertTrue((REPO / "hooks" / "scripts" / "check-setup.sh").is_file())

    def test_skill_resolves_for_codex_not_just_claude(self):
        # The resolution block must look beyond CLAUDE_PLUGIN_ROOT so Codex
        # (which never sets it) can still locate the scripts.
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn(".codex/plugins/cache", text)
        self.assertIn(".claude/plugins/cache", text)

    def test_claude_md_mentions_openhands_source_of_truth(self):
        text = (REPO / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertIn("github.com/OpenHands/OpenHands", text)
        self.assertIn("docs.openhands.dev", text)
        self.assertIn("gbrain", text)
        self.assertIn("GBrain Recall", text)
        self.assertIn("GBrain Write-back", text)
        self.assertIn("Read from GBrain first", text)
        self.assertIn("write durable findings back", text)
        self.assertIn("embedding-backed semantic retrieval", text)

    def test_claude_md_requires_branded_pptx_template(self):
        text = (REPO / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertIn("exa", text)
        self.assertIn("MCP-connected research server", text)
        self.assertIn("https://api.exa.ai/search", text)
        self.assertIn("does not replace local file generation", text)
        self.assertIn("not an exception path", text)
        self.assertIn("BRANDED_PPTX_TEMPLATE", text)
        self.assertIn("CLIENT_DELIVERY_DIR", text)
        self.assertIn("SECOND_BRAIN_DIR", text)
        self.assertIn("OBSIDIAN_VAULT_DIR", text)
        self.assertIn("branded-pptx-deck", text)
        self.assertIn("Do not generate", text)
        self.assertIn("structured content", text)
        self.assertIn("PPTX QA is a delivery gate", text)
        self.assertIn("draft", text)
        self.assertIn("reviewed", text)
        self.assertIn("no red overflow boxes", text)


class StrategyChainingContractTests(unittest.TestCase):
    def test_content_ideas_skill_advertises_pipeline_runner_handoff(self):
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn('mode = "strategy"', text)
        self.assertIn("useCases", text)
        self.assertIn("/pipeline-runner", text)
        self.assertIn("gbrain", text)
        self.assertIn("GBrain Recall", text)
        self.assertIn("GBrain Write-back", text)
        self.assertIn("use it by default for cross-session memory and retrieval", text)
        self.assertIn("write durable findings back", text)
        self.assertIn("embedding-backed semantic", text)
        self.assertIn("exa", text)
        self.assertIn("MCP-connected research server", text)
        self.assertIn("https://api.exa.ai/search", text)
        self.assertIn("does **not** replace", text)
        self.assertIn("not an exception", text)
        self.assertIn("/vertical-scorer", text)
        self.assertIn("/presales-deal-prep", text)

    def test_pipeline_runner_skill_describes_stage_chain(self):
        text = (PIPELINE_SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("content-research", text)
        self.assertIn("vertical-scorer", text)
        self.assertIn("ai-strategy-brief", text)
        self.assertIn("research-to-strategy", text)
        self.assertIn("presales-deal-prep", text)
        self.assertIn("feed-data.json", text)
        self.assertIn("gbrain", text)
        self.assertIn("GBrain Recall", text)
        self.assertIn("GBrain Write-back", text)
        self.assertIn("use it by default at the start of", text)
        self.assertIn("write durable findings back to GBrain", text)
        self.assertIn("embedding-backed semantic retrieval", text)
        self.assertIn("github.com/OpenHands/OpenHands", text)
        self.assertIn("exa", text)
        self.assertIn("MCP-connected research server", text)
        self.assertIn("https://api.exa.ai/search", text)
        self.assertIn("does **not** replace", text)
        self.assertIn("not an exception", text)
        self.assertIn("BRANDED_PPTX_TEMPLATE", text)
        self.assertIn("CLIENT_DELIVERY_DIR", text)
        self.assertIn("SECOND_BRAIN_DIR", text)
        self.assertIn("OBSIDIAN_VAULT_DIR", text)
        self.assertIn("Do **not** substitute", text)
        self.assertIn("Every slide in the deck must carry structured content", text)
        self.assertIn("PPTX QA is required before this stage is considered complete", text)
        self.assertIn("Recommended filename convention", text)
        self.assertIn("deck-reviewed.pptx", text)

    def test_pipeline_runner_command_targets_pipeline_skill(self):
        text = (REPO / "commands" / "pipeline-runner.md").read_text(encoding="utf-8")
        self.assertIn("Invoke the `pipeline-runner` skill", text)
        self.assertIn("latest /content-ideas feed", text)
        self.assertIn("GBrain Recall", text)
        self.assertIn("content-research", text)
        self.assertIn("vertical-scorer", text)

    def test_file_schemas_documents_use_case_pass_throughs(self):
        text = (REPO / "FILE-SCHEMAS.md").read_text(encoding="utf-8")
        self.assertIn("useCases", text)
        self.assertIn("verticalName", text)
        self.assertIn("sourceUrls", text)
        self.assertIn("/pipeline-runner", text)


if __name__ == "__main__":
    unittest.main()
