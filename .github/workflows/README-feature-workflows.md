# Feature Request Workflow System

This directory contains a set of GitHub Actions workflows that automate the feature request and development process. This ensures consistent handling of feature requests from creation through to completion.

## Overview

There are three main components:
1. Feature request issue, `feature-reuest.yml` (manual trigger)
2. PR checks, `pr-checks.yml` (event-triggered)
3. Setup repo labels, `setup-labels.yml` (manual trigger)

### Branch Strategy

The workflows support the following branch structure:
- `main` - Production branch containing released versions
- `rc` - Release candidate branch for final validation
- `develop` - Integration branch for feature development
- `feature/*` - Feature branches for development work
- `hotfix/*` - For urgent fixes to production
- `bugfix/*` - For non-urgent bug fixes

## Workflows

### 1. Feature Request (`feature-request.yml`)

A manually triggered workflow for creating new feature requests.

**Local repo usage:**
```bash
gh workflow run create-feature.yml
git fetch origin
git branch
```
Switch to the feature branch:
```bash
git switch feature/[feature-name]
```

**GitHub Web Usage:**
1. Go to GitHub.com Actions tab
2. Select "Create Feature Issue"
3. Click "Run workflow"
4. Fill out the form:
   - Feature title
   - Feature description
   - Priority level
   - Size estimate
   - Acceptance criteria

### 2. Automated PR Workflow (`pr-checks.yml`)

Automatically processes issues and pull requests.

**Triggers:**
- Issues: opened, labeled, reopened
- Pull requests: opened, closed, reopened, edited

**Functionality:**
- Adds issues to project board
- Manages labels based on content
- Validates PR target branches
- Links PRs to issues
- Updates status labels

### 3. Label Setup (`setup-labels.yml`)

Manages the repository's labels used by the feature workflow system.

**Usage:**
1. Go to Actions tab
2. Select "Setup Repository Labels"
3. Click "Run workflow"

## Labels

The system uses the following label categories:

### Standard Labels
- `bug` - Something isn't working
- `documentation` - General documentation tasks
- `duplicate` - This issue or pull request already exists
- `enhancement` - New feature or request
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention is needed
- `invalid` - This doesn't seem right
- `question` - Further information is requested
- `wontfix` - This will not be worked on
- `hotfix` - Urgent production fix

### Priority Labels
- `priority:high` - Urgent issues
- `priority:medium` - Important but not urgent
- `priority:low` - Nice to have

### Size Labels
- `size:xs` - Extra small (few hours)
- `size:s` - Small (1-2 days)
- `size:m` - Medium (3-5 days)
- `size:l` - Large (1-2 weeks)
- `size:xl` - Extra large (2+ weeks)

### Process Labels
- `wip` - Work in progress
- `tech-review-needed` - Needs technical review
- `ready-for-review` - Ready for final review
- `has-issue` - PR linked to an issue
- `needs-attention` - Pull request needs attention
- `production-release` - Pull Request is a production release
- `release-candidate` - Pull Request is a release candidate

### Documentation Labels
- `docs-new` - New documentation needed
- `docs-update` - Updates to existing docs
- `docs-fix` - Documentation fixes
- `docs-clarity` - Improvements to documentation clarity

## Development Flow

1. **Creating a Feature Request:**
   - Use the issue template or create-feature workflow
   - Provide required information
   - Issue is automatically labeled and added to project

2. **Starting Development:**
   - Create feature branch from `develop`
   - Branch name should follow `feature/*` pattern
   - Reference issue in commit messages

3. **Pull Request:**
   - Create PR targeting `develop`
   - Link to original issue using "Closes #X"
   - Await review and approval

4. **Review Process:**
   - Automated checks for correct target branch
   - Required reviews from QA team
   - Labels updated automatically based on status

## Required Secrets and Variables

The workflows require the following secrets and variables to be configured:
- `ACME_ONTOLOGIES_PAT` - (secret) GitHub Personal Access Token with repo scope
- `PROJECT_ID` - (variable) ID of the GitHub Project board

## Customization

To modify the workflow behavior:

1. **Issue Template:**
   - Edit `.github/ISSUE_TEMPLATE/create-feature.yml`
   - Update fields, validations, or descriptions

2. **Workflows:**
   - Edit `create-feature.yml` for issue creation behavior
   - Edit `pr-checks.yml` for development workflow
   - Modify other `.yml` files in `.github/workflows/` as needed
   - Update triggers, conditions, or actions

3. **Labels:**
   - Edit the label definitions in `setup-labels.yml`
   - Run the workflow to apply changes

## Troubleshooting

Common issues and solutions:

1. **Wrong Target Branch:**
   - Check branch naming follows conventions
   - Ensure PR targets correct branch
   - Look for "needs-attention" label and comments

2. **Missing Labels:**
   - Run the label setup workflow
   - Check for error messages in workflow logs

3. **Project Board Issues:**
   - Verify the GitHug.com PROJECT_ID variable is correct
   - Ensure the GitHib.com Organization PAT has required permissions