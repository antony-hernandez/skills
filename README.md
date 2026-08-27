# skills

Process skills packaged as a **Claude Code plugin marketplace** so they install and update through the native mechanism — no hand-copied files.

Also usable from Cursor by syncing this repo (see local install notes below).

| Plugin | Version | What it does |
|---|---|---|
| [`spec`](plugins/spec) | 0.9.0 | Refines the Technical Changes section of a Confluence Spec against its FRD, the real project, and the repo’s viable tech stack |

## Install (Claude Code)

```
/plugin marketplace add antony-hernandez/skills
/plugin install spec@antony-skills
```

The first line registers the marketplace; the second installs the plugin. After install, the skill triggers when the conversation is about refining technical changes, or via `/spec <SPEC_URL> [<FRD_URL>]`.

## How updates work

Claude Code compares each plugin’s resolved `version` string. Same version → keep the cache; different → download the new one. That string comes from `version` in `plugin.json` (it wins over any other source).

Refresh marketplaces in the background via settings, or on demand:

```
/plugin marketplace update antony-skills
/plugin update spec@antony-skills
```

Use the marketplace-qualified name: `claude plugin update spec` alone fails with `Plugin "spec" not found`. After an update, reload the session or run `/reload-plugins` so hooks/servers pick up the new path.

**Publishing rule:** pushing commits is not enough. If `version` does not change, nobody receives the update. CI fails when plugin files change without a version bump — see `scripts/validate.py`.

## Cursor

Cursor does not auto-update personal skills the same way. Keep a clone of this repo and point `~/.cursor/skills/spec` at `plugins/spec/skills/spec` (symlink), then pull on session start. Team Marketplace + Auto Refresh is the native alternative once `.cursor-plugin/` manifests exist.

## Publish a version

1. Edit the skill in `plugins/<plugin>/skills/<skill>/SKILL.md`.
2. Bump `version` in `plugins/<plugin>/.claude-plugin/plugin.json` (semver: patch = wording, minor = behavior/output, major = breaking output contract).
3. Record the change in `plugins/<plugin>/CHANGELOG.md`.
4. Commit, PR, merge to `main`.
5. Tag: `git tag <plugin>-v<version> && git push origin <plugin>-v<version>`.

Do not put `version` on the marketplace entry: Claude Code uses `plugin.json` only; a second copy goes stale and confuses.

## Add a plugin

```
plugins/<name>/
├── .claude-plugin/plugin.json     # name, version, description, author
├── skills/<name>/SKILL.md         # frontmatter with name + description
└── CHANGELOG.md
```

Add an entry in `.claude-plugin/marketplace.json` with `"source": "./plugins/<name>"`. Each plugin has its own version and installs separately.

Validate before committing:

```
python3 scripts/validate.py
```

## Author

Antony Hernandez — antony.hernandez@atomchat.io

## License

MIT — see [LICENSE](LICENSE).
