# Domo AI Vibe Rules

> **Make AI coding assistants understand Domo** — so you can build custom apps faster.

---

## What is this?

When you use AI coding tools like [Cursor](https://cursor.sh/), they don't know anything about Domo's APIs. This repo gives them that knowledge.

**The problem:** You prototype an app in Google AI Studio or Lovable, then move it to your local machine to continue development. But now your AI assistant doesn't know how to:
- Connect to Domo datasets
- Use AppDB for storage
- Call Code Engine functions
- Trigger workflows
- ...or any other Domo-specific stuff

**The solution:** Copy these rules files into your project. Your AI assistant will now understand Domo.

---

## Who is this for?

This is for anyone who hasn't yet started crafting their own Cursor rules. It's a solid starting point that makes it much more likely the AI will generate code that correctly integrates with Domo's APIs — saving you time debugging and fixing hallucinated code.

> **Note:** Instructions below are for **Cursor** only. If you're using Claude Code, just use the `CLAUDE.md` file.

---

## 🚀 Quick Start (Cursor)

### Step 1: Download the rules

Download these files from this repo:
- `.cursorrules` — The main rules file (or copy content into a `.mdc` file)
- Any API-specific files you need (like `domo-data-api.md`)

### Step 2: Add to your project

**Option A: Simple approach**

Put `.cursorrules` in your project's **root folder**:

```
my-domo-app/
├── .cursorrules     ← Put it here
├── public/
├── src/
└── ...
```

**Option B: Using Cursor's rules folder (recommended)**

Create a `.cursor/rules/` folder and add rules as `.mdc` files:

```
my-domo-app/
├── .cursor/
│   └── rules/
│       ├── domo-app-platform.mdc    ← Main rules (set to "Always")
│       ├── domo-data-api.mdc        ← Set to "Agent-decided"
│       ├── domo-appdb.mdc           ← Set to "Agent-decided"
│       └── ...
├── public/
├── src/
└── ...
```

### Step 3: Configure when rules apply

This is important for keeping AI responses accurate:

| Rule | Setting | Why |
|:-----|:--------|:----|
| **Main rules** (domo-app-platform) | **Always** | Core Domo knowledge should always be available |
| **API-specific rules** (data, appdb, etc.) | **Agent-decided** | Only inject when relevant to avoid context pollution |

> **Why does this matter?** If you inject AppDB documentation into context when your app doesn't use AppDB, you're adding irrelevant information. This ambiguity is when AI starts to hallucinate — it might suggest using AppDB when you don't need it.

### Step 4: Start coding!

Open your project in Cursor and start chatting with the AI. It will now understand Domo.

---

## 📁 What's in this repo?

### Main Rules Files

| File | What it's for |
|:-----|:--------------|
| **`.cursorrules`** | Copy this to your project for Cursor |
| **`CLAUDE.md`** | Copy this to your project for Claude Code |

### API Reference Files

Copy the content from these into your main rules file if you need that specific API:

| File | When you need it |
|:-----|:-----------------|
| `domo-data-api.md` | Querying Domo datasets |
| `domo-appdb.md` | Storing data in collections |
| `domo-ai-endpoints.md` | AI text generation, image-to-text |
| `domo-code-engine.md` | Running server-side code |
| `domo-workflow.md` | Triggering Domo workflows |

### Other Files

| File | What it's for |
|:-----|:--------------|
| `google-ai-studio-to-domo.md` | Migrating a Google AI Studio project to Domo |

---

## ⚠️ Important Note About Cursor

Cursor's rules system has changed several times in the past year. As of now:

- **`.cursorrules`** — Still works, but may be deprecated in the future
- **`.cursor/rules/`** — Newer approach using `.mdc` files
- **`AGENTS.md`** — Another alternative

**Our recommendation:** Start with `.cursorrules` — it's the simplest. If it stops working, check [Cursor's official docs](https://cursor.com/docs/context/rules) for the latest approach.

---

## 📚 Official Domo Documentation

### Getting Started

👉 **[Local Development with Domo CLI](https://developer.domo.com/portal/c8adeafafc236-local-development-with-domo-cli)** — Start here! Quick guide to local custom app development.

### App Framework API Docs

These are the official docs for each API (as of January 2025):

| API | Documentation Link |
|:----|:-------------------|
| AI Service Layer | [View Docs](https://developer.domo.com/portal/wjqiqhsvpadon-ai-service-layer-api-ai-pro-assets-images-pro-png) |
| AppDB | [View Docs](https://developer.domo.com/portal/1l1fm2g0sfm69-app-db-api) |
| Code Engine | [View Docs](https://developer.domo.com/portal/p48phjy7wwtw8-code-engine-api) |
| Data API | [View Docs](https://developer.domo.com/portal/8s3y9eldnjq8d-data-api) |
| File Set (Beta) | [View Docs](https://developer.domo.com/portal/7e8654dedb1c8-file-set-api-beta) |
| Groups | [View Docs](https://developer.domo.com/portal/2hwa98wx7kdm4-groups-api) |
| Task Center | [View Docs](https://developer.domo.com/portal/k2vv2vir3c8ry-task-center-api) |
| User | [View Docs](https://developer.domo.com/portal/n7f7swo7h29wg-user-api) |
| Workflows | [View Docs](https://developer.domo.com/portal/1ay1akbc787jg-workflows-api) |

---

## 💡 Tips for Success

1. **Start simple** — Just copy `.cursorrules` to start. Add API-specific rules only when you need them.

2. **Add project-specific notes** — There's a section at the bottom of the rules file for your own notes. Use it!

3. **Keep the AI focused** — If the AI suggests using a "Domo SDK" or "Domo npm package" that doesn't exist, remind it to use `ryuu.js` and the APIs in your rules.

4. **Don't forget `thumbnail.png`** — Every Domo app needs a `thumbnail.png` file alongside the `manifest.json`.

---

## 🤝 Contributing

Found an error? Have improvements? PRs welcome!

---

<p align="center">
  <i>Built to help Domo developers move faster.</i>
</p>
