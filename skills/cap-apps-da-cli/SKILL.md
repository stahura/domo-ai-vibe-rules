---
name: cap-apps-da-cli
description: Advanced DA CLI usage for scaffolding, generation, and manifest instances.
---

# @domoinc/da CLI - App Scaffolding and Code Generation

The DA CLI (`@domoinc/da`) is a command-line tool for scaffolding Domo custom apps and generating boilerplate code. It's the **recommended way** to create new Domo apps and generate components.

## Purpose

DA CLI provides:
- **Project scaffolding** - Creates new Domo apps with correct structure (Vite + React 18 + TypeScript)
- **Code generation** - Generates components, reducers, and other boilerplate with proper Domo patterns
- **Manifest management** - Manages environment-specific manifest configurations
- **Best practices** - Ensures projects follow Domo conventions from the start

## Installation

```bash
# Install globally
pnpm add -g @domoinc/da

# Or with npm
npm install -g @domoinc/da
```

## Creating a New App

```bash
# Create new Domo app (recommended - Vite + React 18 + TypeScript)
da new my-app-name
cd my-app-name

# With custom template
da new my-app --template @myorg/custom-template
da new my-app --template github.com/user/repo
da new my-app --template ./local-template
```

**Project Structure Created:**
```
my-app/
├── public/
│   ├── manifest.json      # Domo app configuration
│   └── thumbnail.png      # App icon in Domo
├── src/
│   ├── components/        # React components
│   ├── reducers/          # Redux slices (if using)
│   ├── services/          # API service layers
│   ├── types/             # TypeScript definitions
│   └── index.tsx          # App entry point
├── package.json
└── vite.config.ts
```

## Code Generation

```bash
# Generate component with styles, tests, and Storybook
da generate component MyComponent
# Creates:
#   src/components/MyComponent/MyComponent.tsx
#   src/components/MyComponent/MyComponent.module.scss
#   src/components/MyComponent/MyComponent.test.tsx
#   src/components/MyComponent/MyComponent.stories.tsx

# Shorthand
da g component MyComponent

# Generate Redux slice (auto-imports to store)
da generate reducer myFeature
# Creates: src/reducers/myFeature/slice.ts

# Shorthand
da g reducer myFeature
```

## Manifest Management

DA CLI helps manage multiple Domo environments (dev, staging, prod):

```bash
# Create environment-specific manifest overrides
da manifest instance.prod "Production on customer.domo.com"
da manifest instance.dev "Development on dev.domo.com"

# Apply an override before publishing
da apply-manifest instance.prod
yarn upload
```

**Override file structure:**
```json
{
  "instance.prod": {
    "description": "Production environment",
    "manifest": {
      "id": "prod-app-design-id",
      "proxyId": "prod-card-id"
    }
  }
}
```



## Converting Generated Apps?

For converting Lovable/v0/Google AI Studio apps to Domo, use the dedicated workflow skills:
- `wf-apps-migrate-lovable` — Full step-by-step SSR-to-Domo conversion
- `wf-apps-migrate-googleai` — Google AI Studio project conversion

DA CLI can scaffold a reference project (`da new my-app`) to compare against, but it is not a conversion tool.
