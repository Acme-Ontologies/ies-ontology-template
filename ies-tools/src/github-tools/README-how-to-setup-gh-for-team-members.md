# Team Member Setup Guide

This guide explains how to set up team members to use the GitHub tools script in an organizational context.

## Organization Admin Setup

The organization admin needs to configure several settings to ensure team members have the correct permissions.

### 1. Organization Member Privileges

Go to `Organization Settings -> Member privileges`:

- Set Base permissions to `Write`
- Repository creation:
  - [x] Allow members to create public repositories
  - [x] Allow members to create private repositories
- Repository forking:
  - [ ] Disable forking (unchecked)
- Repository discussions:
  - [x] Allow members to enable/disable discussions (checked)
- Projects base permissions: `Write`

### 2. Project Access Settings

For each project that team members need to access:

1. Go to `Project -> Settings -> Manage access`
2. Under "Base Role", ensure "Organization members" is set to `Write`
3. This provides the baseline access needed for the script to work

## Team Member Setup

Each team member needs to perform these steps to use the script:

### 1. Install Prerequisites

```bash
# Install GitHub CLI
# macOS
brew install gh

# Windows
winget install --id GitHub.cli

# Linux (Ubuntu/Debian)
type -p curl >/dev/null || sudo apt install curl -y
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
&& sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
&& echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
&& sudo apt update \
&& sudo apt install gh -y
```

### 2. Configure GitHub CLI

1. Log out of any existing authentication:
   ```bash
   gh auth logout
   ```

2. Login with required scopes:
   ```bash
   gh auth login
   ```
   - Select "GitHub.com"
   - Select "HTTPS"
   - Select "Login with a web browser"
   - Complete the web authentication process

3. Add required scopes:
   ```bash
   gh auth refresh --scopes "repo,project"
   ```

4. Verify setup:
   ```bash
   gh auth status
   ```
   You should see scopes including 'repo' and 'project'

### 3. Verify Access

Test your setup by:

1. Clone the repository:
   ```bash
   git clone <repository-url>, e.g. https://github.com/Acme-Ontologies/ies-building
   cd <repository-name>, e.g. ies-building
   ```

2. Install dependencies:
   ```bash
   poetry install
   ```

3. Try creating a feature:
   ```bash
   poetry run gh-tools create-feature
   ```

## Troubleshooting

### Permission Errors

If you see permission errors:

1. Check your authentication status:
   ```bash
   gh auth status
   ```

2. Ensure you have the correct scopes:
   ```bash
   gh auth refresh --scopes "repo,project"
   ```

3. Verify organization membership:
   ```bash
   gh org list
   ```

### Project Access Issues

If issues aren't being added to projects:

1. Ask your organization admin to verify:
   - Your organization membership is active
   - The project's base role is set to `Write` for organization members
   - You have `Write` access to the repository

2. Try refreshing your token with additional scopes:
   ```bash
   gh auth refresh --scopes "repo,project,write:org"
   ```

## Need Help?

If you encounter issues:
1. Confirm your organization membership status
2. Verify your local gh CLI configuration
3. Contact your organization admin if permission issues persist

Contact [insert-support-contact] for additional assistance.