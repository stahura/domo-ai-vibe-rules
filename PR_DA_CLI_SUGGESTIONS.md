# PR Suggestions: DA CLI Documentation and Conversion Guide

## Overview

This PR adds documentation for the `@domoinc/da` CLI tool and a comprehensive guide for converting Lovable/v0 (or similar LLM-generated) apps to functioning Domo custom apps.

## Rationale

### DA CLI Documentation Gap

The current `.cursorrules` file mentions DA CLI briefly but doesn't explain:
- What DA CLI is and why it exists
- Its full capabilities (code generation, manifest management)
- How it differs from other setup methods
- When to use it vs. manual setup

### Conversion Guide Need

Many developers use AI tools (Lovable, v0, etc.) to generate app prototypes, but these tools create:
- Next.js apps with SSR (incompatible with Domo)
- API routes (no backend in Domo)
- Framework-specific patterns (need Domo equivalents)

There's currently no guidance on how to convert these apps. This PR fills that gap.

## Impact Assessment

**High Value Addition:**
- **DA CLI docs** - Helps developers understand the recommended tooling
- **Conversion guide** - Saves hours of trial-and-error for developers with generated apps
- **Pattern guidance** - Provides clear migration path from common frameworks

**Developer Benefits:**
- Understand when and how to use DA CLI
- Clear process for converting generated apps
- Avoid common pitfalls (SSR, API routes, routing)
- Know what DA CLI can and cannot do

## Proposed Addition Location

Insert after the "Build & Deploy Workflow" section and before "Base Path Configuration". This placement makes sense because:
1. It's about project setup and workflow
2. Conversion is part of the development process
3. It comes before technical configuration details

## Content Structure

The addition includes:

### 1. DA CLI - Purpose and Capabilities
- What DA CLI is (scaffolding and code generation tool)
- Installation and basic usage
- Code generation commands
- Manifest management
- Project structure it creates

### 2. Converting Generated Apps to Domo
- The conversion challenge (SSR, API routes, etc.)
- Recommended conversion pattern
- Step-by-step process:
  1. Use DA CLI to generate reference structure
  2. Detect and remove SSR code
  3. Replace data fetching with Domo APIs
  4. Update routing (HashRouter)
  5. Fix build configuration
- What DA CLI helps with (reference structure, component generation)
- What DA CLI doesn't do (no automatic conversion)

## Key Highlights

### Critical Information Included:
- **DA CLI is not a conversion tool** - Important clarification
- **Use DA CLI as reference** - Recommended pattern for conversion
- **SSR detection** - Reinforces existing warning about server-side code
- **API migration patterns** - Clear examples of replacing backend calls
- **Step-by-step process** - Actionable conversion workflow

### Code Examples:
- DA CLI installation and usage
- Component generation examples
- Manifest management for environments
- Conversion pattern examples
- Data fetching migration (Next.js → Domo APIs)

## Testing Notes

This documentation is based on:
- Official DA CLI documentation patterns
- Common conversion scenarios from Lovable/v0 apps
- Best practices for Domo app architecture
- Integration with existing SSR detection warnings

## Files to Update

- `.cursorrules` - Add DA CLI section and conversion guide
