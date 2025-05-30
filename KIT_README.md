**File Purpose****: Overview of starter kit structure and usage. To be deleted after kit is installed to new project.

See https://github.com/GitRidy/next_js_starter_kit/


# Project Purpose & Approach

A lightweight project template for guiding development of small Next.js web apps with LLM assistance. Typically for small projects that might be developed with Roo Code, deployed on Vercel, and serve 10s to 100s of users.

- Provides design development helper files, docs, PM helper files, and dev helper scripts.
- Does not provide folders created by Next.js


# Phase A - Setup

## Initialize Project

1. Create new `project_root` folder
2. Open terminal in `project_root`
3. Scaffold Next.js project:

```bash
npx create-next-app@14.2.0 . --ts --eslint --tailwind --src-dir --app --use-pnpm
```

## Copy Starter Kit

1. Copy kit files to project (via temp folder):

```bash
git clone https://github.com/GitRidy/next_js_starter_kit.git temp_kit
cp -r temp_kit/* .
cp temp_kit/.* . 2>/dev/null || true
rm -rf temp_kit
rm -rf .git
```

    _Note: degit expects public repo

2. Merge scripts from `package.kit-extra.json` into `package.json`

## Git Setup

1. In VS Code terminal, initialize git and commit

```bash
git init
git add .
git commit -m "Initial commit with starter kit"
```

2. Create new GitHub repo (GitRidy/repo_name)
3. Connect local repo to GitHub and push:

```bash
git remote add origin https://github.com/GitRidy/repo_name.git
git branch -M main
git push -u origin main
```

## Save VS Code Workspace

1. Make .vscode folder

```bash
mkdir .vscode
```

2. Save workspace there

## Phase B - Planning

See `plan.md`


# Reference

## Project Structure

```structure
PROJECT_ROOT/
	.vscode/
	pm/
		design/
			ref_examples/
			ui_flow/		
			wireframes/
			architecture.md
			components_guide.md
			design_brief.md
			design_tokens.json
		docs/
			api/
			docs.react.18.3.1.md
			docs.next.js.14.2.0.md
		guides/
			guide.next.js.14.2.0.md
			guide.qa.md
			guide.react.18.3.1.md
			guide.tasks.md
			guide.ux.md
		prompts/
		plan.md
		prd.md
		tasks.md
		tech_spec.md
		vision.md
	.env.example
	.env.local
	.gitignore
	concat_files.py
	concat_files.README.md
	KIT_README.md
	package.kit-extra.json
	README.md
```


## Key Folders & Files

### Project Root

- **.vscode/**: IDE workspace and settings
- **pm/**: Project management documents and planning materials
- **.env.example**: Template for environment variables needed by the application
- **.env.local**: Non-source controlled secrets, such as API keys
- **.gitignore**: List of file intentionally untracked by git
- **concat_files.py**: Script to combine docs into a single file (for giving to LLMs)
- **concat_files.README.md**: Help file for concat_files.py script
- **KIT_README.md**: Overview of starter kit structure and usage. To be deleted after kit is installed to new project.
- **README.md**: Project overview, setup instructions, and links to essential documentation
- **package.kit-extra.json**: Project scripts to add to `package.json` (including concat-docs and project-tree utilities)

### pm/

- **design/**: Design assets, wireframes, and visual documentation
- **docs/**: Markdown docs specific to the framework used (e.g., Next.js, React)
- **docs/api/**: Markdown docs for external APIs used in the project
- **guides/**: Guidelines for developers working on the project
- **prompts/**: Collection of LLM coding prompts in markdown
- [[plan.md]]: Project phases, milestones, and timeline
- [[prd.md]]: Product requirements document defining features and specifications
- [[tasks.md]]: Summary of current and planned development tasks
- [[tech_spec.md]]: Technical specifications and architecture documentation
- [[vision.md]]: Project vision, goals, and success criteria

#### pm/design/

- **ref_examples/**: Reference examples from other applications for design inspiration
- **ui_flow/**: Diagrams illustrating user journey through the application
- **wireframes/**: Low-fidelity designs showing layout and user flow
- [[architecture.md]]: Defines high-level architectural structure and key components
- [[components_guide.md]]: Catalog of UI components with descriptions and usage guidelines
- [[design_brief.md]]: High-level brief to set out aesthetic vision and principles to guide design
- [[design_tokens.json]]: Design tokens for colors, typography, spacing, and other visual elements

#### pm/guides/

- [[guide.next.js.14.2.0.md]]: Developer guide for Next.js framework.
- [[guide.qa.md]]: Outlines testing strategies, error handling protocols, and quality monitoring practices to ensure reliable, production-ready code.
- [[guide.react.18.3.1.md]]: Developer guide for React library
- [[guide.tasks.md]]: General sequence for all sprints to follow
- [[guide.ux.md]]: Defines standards for creating responsive, accessible, and performant user experiences across all interaction touchpoints.
