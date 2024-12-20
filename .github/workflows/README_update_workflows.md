# GitHub Configuration Sync Workflow

This workflow automatically synchronizes GitHub configuration files (everything in `.github/` directory) from a central configuration repository to consuming repositories.

## Overview

The workflow:
1. Runs daily at midnight
2. Can be manually triggered
3. Creates a PR when changes are detected
4. Preserves the sync workflow file itself in consuming repos

## Prerequisites

1. Central config repository (`ies-github-workflows`) containing the master `.github/` configuration
2. Personal Access Token (PAT) with:
   - `contents:write`
   - `workflows:write`
   permissions for both repositories

## Setup

1. Create a PAT:
   - Go to your GitHub Settings → Developer settings → Personal access tokens → Fine-grained tokens
   - Create new token with:
     * Repository access: Selected repositories (`ies-github-workflows` and consuming repos)
     * Repository permissions:
       - Contents: Write
       - Workflows: Write

2. Add the PAT as a repository secret:
   - Go to consuming repository Settings → Secrets and variables → Actions
   - Create new repository secret:
     * Name: `WORKFLOW_SYNC_TOKEN`
     * Value: Your PAT

3. Add the workflow file:
   - Create `.github/workflows/sync-config.yaml` in your consuming repository
   - Copy the workflow code

## How It Works

1. Checks central repository for `.github/` contents
2. Downloads all files and directories
3. Compares with local `.github/` directory
4. If changes detected:
   - Creates new branch
   - Updates files (preserving sync workflow)
   - Creates PR with detailed changes
   - PR requires review and approval

## Special Handling

- The `sync-config.yaml` workflow file is preserved during sync
- Changes to workflow files require special permissions (hence the PAT requirement)
- The sync process is atomic - all changes are made in a single PR

## Debugging

The workflow includes debug steps that show:
- API access status
- Repository contents
- File change detection
- PR creation process

Check the workflow run logs for detailed information about each step.

## Manual Trigger

To manually trigger the sync:
1. Go to the Actions tab in your repository
2. Select "Sync GitHub Configuration"
3. Click "Run workflow"
4. Select branch (usually 'main')
5. Click "Run workflow"

## Troubleshooting

1. Permission errors:
   - Verify PAT has correct permissions
   - Ensure PAT is added as `WORKFLOW_SYNC_TOKEN`
   - Check PAT hasn't expired

2. 404 errors:
   - Verify repository paths
   - Check repository access permissions
   - Ensure `.github` directory exists in central repo

3. Push/PR failures:
   - Ensure branch protection rules allow GitHub Actions
   - Verify PR creation permissions
