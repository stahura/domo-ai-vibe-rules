# Add DA CLI Documentation and Lovable/v0 Conversion Guide

## Summary

This PR adds comprehensive documentation for the `@domoinc/da` CLI tool and a guide for converting Lovable/v0 (or similar LLM-generated) apps to functioning Domo apps.

## What's Added

1. **DA CLI Documentation**
   - Purpose and capabilities of the DA CLI
   - Installation and setup
   - Code generation commands (components, reducers)
   - Manifest management for multiple environments
   - Project structure overview

2. **Converting Generated Apps Guide**
   - Step-by-step process for converting Lovable/v0 apps to Domo
   - Recommended pattern using DA CLI as reference
   - Common incompatibilities and how to fix them
   - Data fetching migration patterns
   - Routing and build configuration updates

## Why This Matters

Many developers use AI tools like Lovable or v0 to generate app prototypes, but these tools create Next.js/Remix apps with server-side rendering that are incompatible with Domo's client-side-only architecture. This guide provides a clear path for conversion.

## Key Highlights

- **DA CLI Purpose**: Explains that DA CLI is a scaffolding tool, not a conversion tool, but can be used as a reference structure
- **Conversion Pattern**: Step-by-step guide for manually porting components and logic
- **SSR Detection**: Reinforces the importance of detecting and removing server-side code
- **API Migration**: Clear patterns for replacing backend calls with Domo APIs

## Location

Added after the "Build & Deploy Workflow" section, before "Base Path Configuration".
