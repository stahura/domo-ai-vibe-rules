# Domo AI Vibe Rules

Rules files for [Cursor](https://cursor.sh/) and [Claude Code](https://claude.ai/code) to help developers build Domo App Platform custom apps.

## Purpose

This repo provides AI coding assistant rules that make local development easier for less technical users (SEs, Business Analysts, etc.) who are building Domo custom apps. These rules give AI assistants the context they need about Domo's App Framework APIs, manifest.json configuration, and deployment workflow.

**Common use case:** You prototype an app in Google AI Studio or Lovable, then move it local to work on in Cursor or Claude Code. The Domo-specific APIs (Data API, AppDB, AI endpoints, Code Engine, Workflows, etc.) require extra knowledge to set up correctly - these rules provide that knowledge to your AI assistant.

## Quick Start

1. Copy `.cursorrules` (for Cursor) or `CLAUDE.md` (for Claude Code) to your project root
2. Add any API-specific rules you need (e.g., `domo-data-api.md` content)
3. Add your project-specific instructions at the bottom of the rules file
4. Start coding with AI assistance that understands Domo!

## Files

| File | Purpose |
|------|---------|
| `.cursorrules` | Main rules file for Cursor |
| `CLAUDE.md` | Main rules file for Claude Code |
| `domo-data-api.md` | Data API and SQL API reference |
| `domo-appdb.md` | AppDB (Collections) CRUD operations |
| `domo-ai-endpoints.md` | AI text generation and image-to-text |
| `domo-code-engine.md` | Code Engine server-side functions |
| `domo-workflow.md` | Workflow triggering and status |
| `google-ai-studio-to-domo.md` | Migration guide from Google AI Studio |

## Official Documentation

**Getting Started:**
- [Local Development with Domo CLI](https://developer.domo.com/portal/c8adeafafc236-local-development-with-domo-cli) - Quick guide to local custom app development

**App Framework API Documentation (as of 1/20/26):**
- [AI Service Layer API](https://developer.domo.com/portal/wjqiqhsvpadon-ai-service-layer-api-ai-pro-assets-images-pro-png)
- [AppDB API](https://developer.domo.com/portal/1l1fm2g0sfm69-app-db-api)
- [Code Engine API](https://developer.domo.com/portal/p48phjy7wwtw8-code-engine-api)
- [Data API](https://developer.domo.com/portal/8s3y9eldnjq8d-data-api)
- [File Set API (Beta)](https://developer.domo.com/portal/7e8654dedb1c8-file-set-api-beta)
- [Groups API](https://developer.domo.com/portal/2hwa98wx7kdm4-groups-api)
- [Task Center API](https://developer.domo.com/portal/k2vv2vir3c8ry-task-center-api)
- [User API](https://developer.domo.com/portal/n7f7swo7h29wg-user-api)
- [Workflows API](https://developer.domo.com/portal/1ay1akbc787jg-workflows-api)

## Contributing

Found an error or have improvements? PRs welcome!
