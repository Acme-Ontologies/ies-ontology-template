# This is a common justfile shared across all IES projects
# It provides equivalent functionality to the github.py script

# Set shell for commands
set shell := ["bash", "-c"]

# Default recipe to show help
default:
    @just --list

# Check required tools are installed
check-tools:
    #!/usr/bin/env bash
    echo "🔧 Checking required tools..."

    # Check gh CLI
    if ! command -v gh &> /dev/null; then
        echo "❌ GitHub CLI (gh) is not installed"
        echo "Please install it from: https://cli.github.com/"
        exit 1
    else
        echo "✓ GitHub CLI is installed"
    fi

    # Check gh auth status
    if ! gh auth status &> /dev/null; then
        echo "❌ Not authenticated with GitHub"
        echo "Please run 'gh auth login' first"
        exit 1
    else
        echo "✓ GitHub CLI authenticated"
    fi

# Setup repository with required configuration
setup-repo: check-tools
    #!/usr/bin/env bash
    echo "🔧 Setting up repository..."

    # Setup submodules
    if [[ "$(basename $(git rev-parse --show-toplevel))" != "ies-core" ]]; then
        echo "🔗 Setting up submodules..."
        git submodule add https://github.com/Acme-Ontologies/ies-core.git core || true
        git submodule update --init --recursive
    else
        echo "ℹ️ Skipping submodule setup in ies-core repository"
    fi

    # Setup branches
    echo "🌱 Setting up branches..."
    DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef --jq .defaultBranchRef.name)

    # Create develop branch if it doesn't exist
    if ! git rev-parse --verify develop &> /dev/null; then
        git checkout -b develop origin/${DEFAULT_BRANCH} || git checkout -b develop
        git push -u origin develop
    fi

    # Create rc branch if it doesn't exist
    if ! git rev-parse --verify rc &> /dev/null; then
        git checkout ${DEFAULT_BRANCH}
        git checkout -b rc
        git push -u origin rc
    fi

    # Return to develop branch
    git checkout develop

    # Setup labels
    echo "🏷️ Setting up labels..."
    gh workflow run setup-labels.yml

    echo "✨ Repository setup completed"

# Create a new feature request
feature *args:
    #!/usr/bin/env bash
    echo "📝 Creating new feature request..."

    # Check for clean working directory
    if [[ -n $(git status --porcelain) ]]; then
        read -p "Working directory has uncommitted changes. Continue? [y/N] " response
        if [[ ! "$response" =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi

    # Prompt for feature details
    read -p "Feature title: " title
    read -p "Feature description: " description
    read -p "Acceptance criteria: " acceptance
    read -p "Priority (low/medium/high): " priority
    read -p "Size (xs/s/m/l/xl): " size

    # Create issue with labels
    issue_data=$(gh issue create \
        --title "[FEATURE] $title" \
        --body "## Problem Statement
$description

## Acceptance Criteria
$acceptance

## Priority
${priority^^}

## Size
${size^^}

## Development
🔄 Development branch will be created after issue creation." \
        --label "enhancement" \
        --label "priority:$priority" \
        --label "size:$size" \
        --json number,url)

    # Extract issue number and create branch
    issue_number=$(echo $issue_data | jq -r .number)
    branch_name="feature/issue-$issue_number-$(echo $title | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd '[:alnum:]-')"

    # Create and switch to feature branch
    git checkout develop
    git checkout -b "$branch_name"
    git push -u origin "$branch_name"

    echo "✨ Feature created: Issue #$issue_number"
    echo "🌿 Branch created: $branch_name"

# Create a pull request
create-pr base="develop" draft="false":
    #!/usr/bin/env bash
    echo "📝 Creating pull request..."

    # Get current branch
    current_branch=$(git rev-parse --abbrev-ref HEAD)

    # Extract issue number from branch name
    if [[ ! "$current_branch" =~ ^(feature|bugfix|docs)/issue-([0-9]+) ]]; then
        echo "❌ Current branch doesn't follow the naming convention"
        exit 1
    fi
    issue_number="${BASH_REMATCH[2]}"

    # Get issue details
    issue_title=$(gh issue view $issue_number --json title --jq .title)

    # Create PR
    draft_flag=""
    if [[ "$draft" == "true" ]]; then
        draft_flag="--draft"
    fi

    gh pr create \
        --base "$base" \
        --title "$issue_title" \
        --body "Closes #$issue_number" \
        $draft_flag

# Sync current branch with remote
sync branch="" force="false":
    #!/usr/bin/env bash
    echo "🔄 Syncing with remote..."

    # Use current branch if none specified
    if [[ -z "$branch" ]]; then
        branch=$(git rev-parse --abbrev-ref HEAD)
    fi

    # Fetch latest changes
    git fetch origin

    # Check if branch exists remotely
    if ! git ls-remote --heads origin "$branch" | grep -q "$branch"; then
        echo "❌ Branch $branch does not exist on remote"
        exit 1
    fi

    # Handle local changes
    if [[ -n $(git status --porcelain) ]]; then
        if [[ "$force" == "true" ]]; then
            echo "⚠️ Stashing local changes..."
            git stash
        else
            echo "❌ You have local changes. Commit, stash, or use --force to proceed"
            exit 1
        fi
    fi

    # Sync branch
    git checkout -B "$branch" "origin/$branch"

    # Restore stashed changes if necessary
    if [[ "$force" == "true" ]] && [[ -n $(git stash list) ]]; then
        echo "📝 Reapplying local changes..."
        git stash pop
    fi

    echo "✨ Branch synchronized successfully"

# Validate ontology files
# ToDo Implement the workflow file for ontology validation, `ontology-validation.yml`
validate:
    @echo "Validating ontology files..."
    gh workflow run ontology-validation.yml

# Run all tests
# ToDo - write the workflow file for tests, `tests.yml`
test: validate
    @echo "Running tests..."
    gh workflow run tests.yml

# Build documentation
# ToDo - write the workflow file for documentation, `doc-build.yml`
docs:
    @echo "Building documentation..."
    gh workflow run doc-build.yml
