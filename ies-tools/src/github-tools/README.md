# GitHub Tools

A command-line tool for managing GitHub issues, project boards, and development workflows. This tool integrates with your GitHub repository to automate common development tasks.

## Features

- Create feature requests with standardized templates
- Automatically add issues to GitHub project boards
- Create and manage feature branches
- Synchronize local and remote branches
- Create pull requests linked to issues

## Prerequisites

- Python 3.8 or higher
- Poetry for dependency management
- GitHub CLI (`gh`) installed and authenticated
- Git configured with your repository

### GitHub CLI Setup

1. Install the GitHub CLI:
   ```bash
   # macOS
   brew install gh

   # Windows
   winget install --id GitHub.cli

   # Linux
   type -p curl >/dev/null || apt install curl -y
   curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
   && chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
   && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
   && apt update \
   && apt install gh -y
   ```

2. Authenticate with GitHub:
   ```bash
   gh auth login
   ```

3. Ensure you have the required scopes:
   ```bash
   gh auth refresh --scopes "repo,project"
   ```

### Repository Setup

1. Set your PROJECT_ID as a repository variable:
   ```bash
   gh variable set PROJECT_ID --body "PVT_xxx..."
   ```

2. Required repository labels:
   - `enhancement`
   - `priority:high`, `priority:medium`, `priority:low`
   - `size:xs`, `size:s`, `size:m`, `size:l`, `size:xl`

## Installation

The tool is installed as part of the repository's Python package:

```bash
# Clone the repository
git clone <repository-url>
cd <repository>

# Install dependencies
poetry install
```

## Usage

### Creating a Feature Request

Creates a new feature issue and sets up a development branch:

```bash
poetry run gh-tools create-feature
```

Or with direct arguments:
```bash
poetry run gh-tools create-feature \
  --title "My New Feature" \
  --description "Feature description" \
  --acceptance "Done when..." \
  --priority medium \
  --size m
```

This will:
1. Create a new issue with the [Feature] prefix
2. Add it to your project board
3. Create a feature branch
4. Set up initial development files
5. Push the branch to remote

### Syncing Branches

Synchronize your local branch with remote changes:

```bash
# Sync current branch
poetry run gh-tools sync

# Sync specific branch
poetry run gh-tools sync feature/issue-123-my-feature

# Force sync (stashing local changes)
poetry run gh-tools sync --force
```

### Creating Pull Requests

Create a pull request from your current feature branch:

```bash
# Create PR to develop branch
poetry run gh-tools create-pr

# Create as draft PR
poetry run gh-tools create-pr --draft

# Target different base branch
poetry run gh-tools create-pr --base main
```

## Branch Strategy

The tool supports the following branch structure:
- `main` - Production branch
- `rc` - Release candidate branch
- `develop` - Integration branch
- `feature/*` - Feature development branches
- `hotfix/*` - Production hotfix branches
- `bugfix/*` - Non-urgent bug fixes

## Project Integration

The tool integrates with GitHub Projects V2. To set this up:

1. Get your Project ID from the project URL or settings
2. Set it as a repository variable:
   ```bash
   gh variable set PROJECT_ID --body "PVT_xxx..."
   ```

The tool will automatically:
- Add new issues to the project board
- Track development status
- Link issues and pull requests

## Troubleshooting

### Authentication Issues

If you see permission errors:
1. Check your authentication status:
   ```bash
   gh auth status
   ```
2. Refresh token with required scopes:
   ```bash
   gh auth refresh --scopes "repo,project"
   ```

### Project Board Issues

If issues aren't being added to your project:
1. Verify your PROJECT_ID:
   ```bash
   gh variable list
   ```
2. Ensure you have project write permissions
3. Check your token has the `project` scope

### Branch Sync Issues

If branch sync fails:
1. Check for local changes:
   ```bash
   git status
   ```
2. Use `--force` to stash local changes:
   ```bash
   poetry run gh-tools sync --force
   ```

## Contributing

1. Create a feature branch:
   ```bash
   poetry run gh-tools create-feature
   ```
2. Make your changes
3. Create a pull request:
   ```bash
   poetry run gh-tools create-pr
   ```

## License
These scripts are licensed under the MIT License. See [LICENSE](LICENSE) for details.
