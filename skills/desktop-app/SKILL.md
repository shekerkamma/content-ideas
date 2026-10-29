---
name: desktop-app
description: Use when asked to build or package a desktop application, create an Electron app, or prepare a Windows or Linux desktop build from an existing web app.
---

# Desktop application build workflow

Canonical skill: `skills/desktop-app/`. Reuse the target project's existing engine first. For a new desktop app with no selected engine, this host has Electron 44.5.1 and electron-builder 26.15.3 installed under `/home/sheke/.local/share/codex-tools/desktop-app` with WSL Node 24.18.1.

## Workflow

1. Use PLAID/product docs to identify target operating systems, local storage, permissions, login and acceptance checks. Preserve any explicitly requested engine or platform.
2. For new Electron projects, declare pinned Electron/build dependencies in that project's package manifest rather than relying on the host cache as a portable dependency. Keep renderer code separate from main/preload; default nodeIntegration=false and contextIsolation=true. Use explicit IPC interfaces for required desktop features.
3. Run the app visibly and test opening, core actions, local persistence and error handling. Use the project's tests and browser tools for renderer logic. A version check alone does not verify an app launch.
4. Use electron-builder with an explicit target and output directory. WSL's host runtime validates Linux builds. Native Windows/macOS package signing and platform-specific packaging require the corresponding build environment and credentials; do not claim a Linux launch proves them.
5. Keep source, editable assets, build commands and verification reports together. Show the concrete build and report unsupported targets before delivery.

## iOS boundary

Use the canonical ios-design-review/ios-qa workflows for design and existing project checks when applicable. Native iOS compilation and signing require macOS/Xcode or an authorized remote Mac/CI service. This Windows/WSL setup cannot install Xcode; adding unrelated Windows tools does not resolve it. No paid build service is created by this skill.

## Gotchas

A desktop wrapper does not make a web app production-ready. Test native integration and packaging separately. Keep auth secrets out of renderer code and skill files. Do not publish/sign a release as a setup smoke test. Host binaries are conveniences, not project source.

## Skill Relationships

Category: Scaffolding & Templates. PLAID is upstream for app scope. karpathy-guidelines is the coding overlay. Existing browser QA validates web renderer flows. Blender may supply exported 3D assets. No new presentation route is introduced.

## Host Compatibility

Claude Code, Codex CLI and Desktop execute Linux tooling through WSL and Node 24. Windows/macOS/iOS artifact targets require their target-specific environment. Desktop discovery is a thin adapter to this canonical bundle.
