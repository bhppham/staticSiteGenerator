# AGENTS.md

## Purpose

This project is a static site generator which turns a raw Markdown files into a static (html + css) website. Specifically, the static site generator would be used to create a portfolio page for Bill Pham.

## Project overview

1. The static site generator (SSG) copies everything from `static/` folder into `public/` folder
2. Then SSG parses `content/index.md`
3. SSG then splits the parsed markdown file into blocknodes
4. Blocknodes then are translated into textnodes
5. Textnodes then are translated into htmlnodes
6. HTML nodes then are assembled into a website using the `template.html`

## Project Structure

staticSiteGenerator
├── AGENTS.md
├── content
├── main.sh
├── public
├── README.md
├── src
│   ├── __pycache__
│   ├── blocknode.py
│   ├── htmlnode.py
│   ├── inline_markdown.py
│   ├── main.py
│   ├── test_blocknode.py
│   ├── test_htmlnode.py
│   ├── test_inline_markdown.py
│   ├── test_textnode.py
│   └── textnode.py
├── static
│   ├── images
│   └── index.css
└── test.sh

## Build and test commands

There is no building for this project
To test the project run the `test.sh` file.

## Code style guidelines

- Avoid using helper functions and complex structures when something can easily be solved with a single function
- When writing functions always use type hints.

## Testing Instrucitons

Tests are wrtitten in the python files with prefix `test_` inside the `src/` folder.
The command to run the tests is:
```bash
./test.sh
```

## Security considerations

- Never ever delete files with `rm` or similar commands
- Never use any git commands at all (unless asked to)

## Current Implementation Snapshot

- Primary code lives in `src/`
- Tests currently pass via `./test.sh`
- Canonical run command for generator tasks: `./main.sh`
- Current repo reality includes:
  - `content/index.md` is currently missing
  - `template.html` is currently missing
  - `public/` currently exists and is empty

## Target Architecture vs Current State

Target architecture (intended):
1. Copy assets from `static/` into `public/`
2. Parse `content/index.md`
3. Convert markdown into block nodes
4. Convert block nodes into text nodes
5. Convert text nodes into HTML nodes
6. Assemble final page with `template.html`
7. Write site output into `public/`

Current state (as of now):
- Project has parsing and node-conversion logic under active development
- End-to-end generation wiring is not yet fully implemented to match intended architecture
- Required input/template files are not yet present in repo

## Input/Output Contract

- Required content input file: `content/index.md`
- Expected template file: `template.html`
- Output directory: `public/`
- Output behavior target: clean rebuild of generated output each run
- Error handling target: fail fast with clear, actionable errors when required inputs are missing

## Supported Markdown Scope (Tested)

Support claims should be limited to behaviors currently covered by tests:

- Paragraphs
- Headings (`#` to `######`)
- Fenced code blocks (triple backticks)
- Block quotes (`>`)
- Unordered lists (`-`)
- Ordered lists (`1.`, `2.`, `3.` style)
- Inline bold (`**text**`)
- Inline italic (`_text_`)
- Inline code (`` `code` ``)
- Links (`[text](url)`)
- Images (`![alt](url)`)

## Operational Defaults

- Python baseline: 3.12+
- Prefer concise milestone logging during generation runs
- Prefer minimal, targeted changes over broad refactors unless explicitly requested
- Treat existing tests as the default behavioral contract

## Quality Gate

- `./test.sh` must pass before considering a task complete

## Known Gaps / Near-Term TODOs

- Complete end-to-end generation path from markdown input to final site output
- Add required content input file at `content/index.md`
- Add required template file at `template.html`
- Wire template-based assembly into generation pipeline
- Ensure `./main.sh` produces expected output in `public/`

## Collaboration Priority

- Preserve existing behavior expected by current tests unless user explicitly requests behavior changes
- Explicit user instructions override AGENTS defaults when conflicts exist
