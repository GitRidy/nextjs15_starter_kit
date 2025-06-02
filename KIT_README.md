**File Purpose****: Overview of starter kit structure and usage. To be deleted after kit is installed to new project.

See https://github.com/GitRidy/next_js_starter_kit/


# Project Purpose & Approach

A lightweight project template for guiding development of small Next.js web apps with LLM assistance. Typically for small projects that might be developed with Roo Code, deployed on Vercel, and serve 10s to 100s of users.

- Provides design development helper files, docs, PM helper files, and dev helper scripts.
- Does not provide folders created by Next.js


# Phase A - Setup

## Initialize Project
_Assuming Next.js 15, Typescript, Tailwind CSS_

1. Create new `project_root` folder
2. Open terminal in `project_root`
3. Scaffold Next.js project:

```bash
npx create-next-app@latest . --ts --eslint --tailwind --src-dir --app --use-pnpm --import-alias "@/*"
```

4. pnpm dev


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
	docs/
		api/
		docs.next.js.15.md
		docs.next.js.15.standards.md
		docs.next.js.15.mistakes.md
	pm/
		design/
			ref_examples/
			ui_flow/		
			wireframes/
			architecture.md
			components-guide.md
			design-brief.md
			design-tokens.json
		guides/
			guide.do-tasks.md
			guide.list-tasks.md
			guide.make-prd.md
			guide.ux.md
		prompts/
		tasks/
		app-prd.md
		app-tech-spec.md
		app-vision.md
		plan.md
	.env.example
	.env.local
	.gitignore
	concat_files.py
	concat_files.README.md
	KIT_README.md
	package.kit-extra.json
	project_tree.txt
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
- [[app-prd]]: Product requirements document defining features and specifications
- [[app-tech-spec]]: Technical specifications and architecture documentation
- [[app-vision]]: Project vision, goals, and success criteria

#### pm/design/

- **ref_examples/**: Reference examples from other applications for design inspiration
- **ui_flow/**: Diagrams illustrating user journey through the application
- **wireframes/**: Low-fidelity designs showing layout and user flow
- [[architecture]]: Defines high-level architectural structure and key components
- [[components-guide]]: Catalog of UI components with descriptions and usage guidelines
- [[design-brief.md]]: High-level brief to set out aesthetic vision and principles to guide design
- [[design-tokens.json]]: Design tokens for colors, typography, spacing, and other visual elements

#### docs/
- **api/**: API-specific docs
- [[docs.next.js.15.md]]: High level coding guide for Next.js 15 framework
- [[docs.next.js.15.mistakes.md]]: Common Next.js coding mistakes from Vercel
- [[docs.next.js.15.standards.md]]: Next.js coding standards from Instruct AI

#### pm/guides/

- [[guide.do-tasks.md]]: Guide to LLMs for executing feature development tasks
- [[guide.list-tasks.md]]: Guide to LLMs for listing tasks based on feature PRD
- [[guide.make-prd.md]]: Guide to LLMs for creating a feature-specific PRD
- [[guide.ux.md]]: Defines standards for creating responsive, accessible, and performant user experiences across all interaction touchpoints.

#### pm/tasks/

- Files for tracking development tasks by feature


## Credits

- Ryan Carson's AI coding workflow: https://github.com/snarktank/ai-dev-tasks/blob/main/README.md