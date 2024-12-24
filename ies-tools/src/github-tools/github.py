import os
import sys
import json
import re
import subprocess
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple, List

import click


class PriorityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class IssueType(str, Enum):
    FEATURE = "feature"
    BUG = "bugfix"
    DOCS = "docs"


@dataclass
class IssueMetadata:
    number: str
    title: str
    type: IssueType
    branch_name: str


def verify_gh_cli():
    """Verify GitHub CLI is available and authenticated"""
    try:
        subprocess.run(["gh", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise click.ClickException(
            "GitHub CLI (gh) not found. Please install it first."
        )

    try:
        subprocess.run(["gh", "auth", "status"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        raise click.ClickException(
            "Not authenticated with GitHub. Please run 'gh auth login' first."
        )


def debug_graphql(cmd: List[str], error: subprocess.CalledProcessError):
    """Debug a GraphQL command failure"""
    click.echo("\nDebug Information:")
    click.echo("Command:", " ".join(cmd))
    click.echo("\nError Output:", error.stderr)
    click.echo("\nStandard Output:", error.stdout)

    # Try to get more info about the current state
    try:
        owner = get_repo_owner()
        repo = get_repo_name()
        click.echo(f"\nRepository: {owner}/{repo}")

        # Test basic API access
        test_cmd = ["gh", "api", f"/repos/{owner}/{repo}"]
        result = subprocess.run(test_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            click.echo("\nAPI Access Test Failed:")
            click.echo(result.stderr)
        else:
            click.echo("\nAPI Access Test Succeeded")
    except Exception as e:
        click.echo(f"Could not get repository info: {e}")


def verify_git_clean():
    """Verify git working directory is clean"""
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True,
        check=True,
    )
    if result.stdout.strip():
        if not click.confirm(
                "Working directory has uncommitted changes. Continue anyway?",
                default=False,
        ):
            raise click.Abort()


def get_default_branch() -> str:
    """Get the default branch (usually 'main' or 'develop')"""
    try:
        result = subprocess.run(
            ["gh", "repo", "view", "--json", "defaultBranchRef"],
            capture_output=True,
            text=True,
            check=True,
        )
        data = json.loads(result.stdout)
        return data["defaultBranchRef"]["name"]
    except (subprocess.CalledProcessError, KeyError, json.JSONDecodeError):
        return "develop"  # Fallback to develop


def get_repo_owner() -> str:
    """Get repository owner from git remote"""
    try:
        remote_url = subprocess.check_output(
            ["git", "remote", "get-url", "origin"],
            text=True
        ).strip()
        # Handle both HTTPS and SSH URLs
        if "github.com:" in remote_url:  # SSH
            owner = remote_url.split("github.com:")[1].split("/")[0]
        else:  # HTTPS
            owner = remote_url.split("github.com/")[1].split("/")[0]
        return owner
    except (subprocess.CalledProcessError, IndexError):
        raise click.ClickException("Could not determine repository owner")


def get_repo_name() -> str:
    """Get repository name from git remote"""
    try:
        remote_url = subprocess.check_output(
            ["git", "remote", "get-url", "origin"],
            text=True
        ).strip()
        # Handle both HTTPS and SSH URLs
        name = remote_url.split("/")[-1].replace(".git", "")
        return name
    except (subprocess.CalledProcessError, IndexError):
        raise click.ClickException("Could not determine repository name")


def get_project_id() -> Optional[str]:
    """Get project ID from repository variables"""
    try:
        result = subprocess.run(
            ["gh", "variable", "list", "--json", "name,value"],
            capture_output=True,
            text=True,
            check=True,
        )
        variables = json.loads(result.stdout)
        for var in variables:
            if var["name"] == "PROJECT_ID":
                return var["value"]
        return None
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        return None


def setup_develop_branch() -> bool:
    """Create and push develop branch if it doesn't exist"""
    try:
        # Check if develop branch exists locally
        result = subprocess.run(
            ["git", "branch", "--list", "develop"],
            capture_output=True,
            text=True,
            check=True,
        )

        if not result.stdout.strip():
            click.echo("🌱 Creating develop branch...")
            # Get default branch (usually main)
            default_branch = get_default_branch()

            # Create develop branch from default branch
            subprocess.run(
                ["git", "checkout", "-b", "develop", f"origin/{default_branch}"],
                check=True,
                capture_output=True,
            )

            # Push to remote and set upstream
            click.echo("⬆️  Pushing develop branch to remote...")
            subprocess.run(
                ["git", "push", "-u", "origin", "develop"],
                check=True,
                capture_output=True,
            )
            click.echo("✨ Develop branch created and pushed successfully")
        else:
            click.echo("ℹ️  Develop branch already exists")
        return True

    except subprocess.CalledProcessError as e:
        click.echo(f"❌ Failed to setup develop branch: {e.stderr}", err=True)
        return False


def setup_labels() -> bool:
    """Run the labels setup workflow"""
    try:
        workflow_path = ".github/workflows/setup-labels.yml"

        # Check if workflow file exists
        if not os.path.exists(workflow_path):
            click.echo(f"❌ Workflow file not found: {workflow_path}", err=True)
            return False

        click.echo("🏷️  Running labels setup workflow...")
        subprocess.run(
            ["gh", "workflow", "run", "setup-labels.yml"],
            check=True,
            capture_output=True,
        )
        click.echo("✨ Labels setup workflow triggered successfully")
        return True

    except subprocess.CalledProcessError as e:
        click.echo(f"❌ Failed to run labels workflow: {e.stderr}", err=True)
        return False


def get_platform_type() -> str:
    """Determine the platform type more accurately"""
    system = platform.system().lower()
    if system == "darwin":
        return "macos"
    elif system == "linux":
        return "linux"
    elif system == "windows":
        return "windows"
    else:
        return "unknown"


def check_gh_cli() -> bool:
    """Check if GitHub CLI is installed"""
    try:
        subprocess.run(["gh", "--version"], check=True, capture_output=True)
        click.echo("✓ GitHub CLI is installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        click.echo("❌ GitHub CLI (gh) is not installed", err=True)

        # Provide installation instructions based on platform
        platform_type = get_platform_type()
        if platform_type == "macos":
            click.echo("To install on macOS:")
            click.echo("  brew install gh")
        elif platform_type == "linux":
            click.echo("To install on Linux:")
            click.echo(
                "  curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg")
            click.echo(
                "  echo \"deb [signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main\" | sudo tee /etc/apt/sources.list.d/github-cli.list")
            click.echo("  sudo apt update")
            click.echo("  sudo apt install gh")
        elif platform_type == "windows":
            click.echo("To install on Windows:")
            click.echo("  winget install GitHub.cli")
            click.echo("  # or")
            click.echo("  choco install gh")
        return False


def check_just() -> bool:
    """Check if just is installed"""
    try:
        subprocess.run(["just", "--version"], check=True, capture_output=True)
        click.echo("✓ just is installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        click.echo("❌ just is not installed", err=True)

        # Provide installation instructions based on platform
        platform_type = get_platform_type()
        if platform_type == "macos":
            click.echo("To install on macOS:")
            click.echo("  brew install just")
        elif platform_type == "linux":
            click.echo("To install on Linux:")
            click.echo("  curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s")
        elif platform_type == "windows":
            click.echo("To install on Windows:")
            click.echo("  winget install just")
            click.echo("  # or")
            click.echo("  choco install just")
        else:
            click.echo("Please visit https://just.systems/man/en/chapter_4.html for installation instructions")
        return False


def create_issue(
        title: str, body: str, labels: List[str], issue_type: IssueType
) -> IssueMetadata:
    """Create an issue and return its metadata"""
    try:
        # Create the issue
        result = subprocess.run(
            [
                "gh",
                "issue",
                "create",
                "--title",
                f"[{issue_type.name}] {title}",
                "--body",
                body,
                *sum([["-l", label] for label in labels], []),  # Flatten label args
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        # Extract issue number from the URL in the output
        # Output is typically in the format: https://github.com/owner/repo/issues/123
        issue_url = result.stdout.strip()
        issue_number = issue_url.split("/")[-1]

        # Get the Project ID
        project_id = get_project_id()

        if project_id:
            try:
                # Get issue node ID using REST API
                click.echo("🔍 Getting issue ID...")
                issue_query = subprocess.run(
                    ["gh", "api", f"/repos/{get_repo_owner()}/{get_repo_name()}/issues/{issue_number}"],
                    capture_output=True,
                    text=True,
                    check=True
                )

                issue_data = json.loads(issue_query.stdout)
                issue_id = issue_data["node_id"]  # GitHub's node ID for GraphQL

                # Add to project
                click.echo("📌 Adding to project board...")
                project_mutation_cmd = [
                    "gh", "api", "graphql",
                    "--raw-field",
                    f'query=mutation($projectId: ID!, $contentId: ID!) {{ addProjectV2ItemById(input: {{ projectId: $projectId, contentId: $contentId }}) {{ item {{ id }} }} }}',
                    "--raw-field", f'projectId={project_id}',
                    "--raw-field", f'contentId={issue_id}'
                ]

                project_mutation = subprocess.run(
                    project_mutation_cmd,
                    capture_output=True,
                    text=True,
                    check=True
                )

                if project_mutation.returncode == 0:
                    click.echo("✨ Added issue to project board")

            except subprocess.CalledProcessError as e:
                click.echo(f"Warning: Failed to add issue to project: {e.stderr}")
                # Continue since issue was created successfully
        else:
            click.echo("⚠️  Warning: PROJECT_ID not found. Issue won't be added to project board.")

        # Generate branch name
        safe_title = re.sub(r"[^a-zA-Z0-9-]", "-", title.lower())
        branch_name = f"{issue_type.value}/issue-{issue_number}-{safe_title}"

        return IssueMetadata(
            number=issue_number,
            title=title,
            type=issue_type,
            branch_name=branch_name,
        )

    except subprocess.CalledProcessError as e:
        click.echo(f"Error creating issue: {e.stderr}", err=True)
        if "could not create issue" in str(e.stderr):
            click.echo(
                "Please check that you're authenticated with 'gh auth status'"
            )
        if "graphql" in str(e.cmd[0]):
            debug_graphql(e.cmd, e)
        raise


def setup_development_branch(
        metadata: IssueMetadata, base_branch: str = "develop"
) -> None:
    """Set up development branch locally and remotely"""
    try:
        # Fetch latest changes
        subprocess.run(["git", "fetch", "origin"], check=True)

        # Create branch from base
        subprocess.run(
            ["git", "checkout", "-b", metadata.branch_name, f"origin/{base_branch}"],
            check=True,
        )

        # Create initial commit
        readme_content = f"""# {metadata.type.name.title()} Implementation

## Overview
This branch implements {metadata.type.value} #{metadata.number}.

## Development Status
🚧 In Progress

## Related Issues
- #{metadata.number}
"""
        with open("DEVELOPMENT.md", "w") as f:
            f.write(readme_content)

        # Commit and push
        subprocess.run(["git", "add", "DEVELOPMENT.md"], check=True)
        subprocess.run(
            [
                "git",
                "commit",
                "-m",
                f"{metadata.type.value}: initial commit for #{metadata.number}",
            ],
            check=True,
        )
        subprocess.run(
            ["git", "push", "-u", "origin", metadata.branch_name], check=True
        )

        # Add branch reference comment to issue
        subprocess.run(
            [
                "gh",
                "issue",
                "comment",
                metadata.number,
                "--body",
                f"🔨 Development branch [`{metadata.branch_name}`](../tree/{metadata.branch_name}) has been created from `{base_branch}`.",
            ],
            check=True,
        )

    except subprocess.CalledProcessError as e:
        raise click.ClickException(f"Failed to set up branch: {e}")


def check_branch_status() -> Tuple[bool, bool, bool]:
    """Check branch status returning (has_local_changes, has_unpushed, has_unmerged)"""
    # Check for local changes
    status = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True,
        check=True,
    )
    has_local_changes = bool(status.stdout.strip())

    # Check for unpushed commits
    unpushed = subprocess.run(
        ["git", "log", "@{u}..HEAD", "--oneline"],
        capture_output=True,
        text=True,
        check=True,
    )
    has_unpushed = bool(unpushed.stdout.strip())

    # Check for unmerged changes
    unmerged = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=U"],
        capture_output=True,
        text=True,
        check=True,
    )
    has_unmerged = bool(unmerged.stdout.strip())

    return has_local_changes, has_unpushed, has_unmerged


def sync_remote_branch(branch_name: str, force: bool = False):
    """Sync local branch with remote"""
    try:
        # Fetch the latest from remote
        click.echo("📡 Fetching remote changes...")
        subprocess.run(
            ["git", "fetch", "origin"], check=True, capture_output=True
        )

        # Check if branch exists remotely
        remote_exists = subprocess.run(
            ["git", "ls-remote", "--heads", "origin", branch_name],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()

        if not remote_exists:
            raise click.ClickException(f"Branch {branch_name} does not exist on remote")

        # Check branch status
        has_local_changes, has_unpushed, has_unmerged = check_branch_status()

        # Handle local changes
        if has_local_changes:
            if force:
                click.echo("⚠️ Stashing local changes...")
                subprocess.run(["git", "stash"], check=True)
            else:
                raise click.ClickException(
                    "You have local changes. Commit, stash, or use --force to proceed"
                )

        # Handle unpushed commits
        if has_unpushed:
            if force:
                click.echo("⚠️ Resetting to remote branch...")
                subprocess.run(
                    ["git", "reset", "--hard", f"origin/{branch_name}"],
                    check=True
                )
            else:
                raise click.ClickException(
                    "You have unpushed commits. Push them or use --force to proceed"
                )

        # Handle unmerged changes
        if has_unmerged:
            raise click.ClickException(
                "You have unmerged changes. Resolve conflicts first"
            )

        # Create/update local branch tracking remote
        click.echo("🔄 Updating local branch...")
        subprocess.run(
            ["git", "checkout", "-B", branch_name, f"origin/{branch_name}"],
            check=True,
            capture_output=True,
        )

        # Pop stashed changes if we stashed them
        if force and has_local_changes:
            click.echo("📝 Reapplying local changes...")
            subprocess.run(["git", "stash", "pop"], check=True)

        click.echo("✨ Branch synchronized successfully")

    except subprocess.CalledProcessError as e:
        raise click.ClickException(f"Failed to sync branch: {e}")


@click.group()
def cli():
    """CLI for managing GitHub issues and workflows"""
    pass


@cli.command()
def setup_repo():
    """Set up repository with develop branch and required tools"""
    success_count = 0
    total_steps = 2  # Minimum required steps

    click.echo("🔧 Setting up repository...")

    # Check for gh CLI installation
    check_gh_cli()

    # Verify GitHub CLI authentication
    try:
        verify_gh_cli()
        click.echo("✓ GitHub CLI authenticated")
    except click.ClickException as e:
        click.echo(f"❌ {str(e)}", err=True)
        return

    # Check for just installation
    check_just()

    # Setup develop branch
    if setup_develop_branch():
        success_count += 1

    # Setup labels
    if setup_labels():
        success_count += 1

    # Final status report
    if success_count == total_steps:
        click.echo("🎉 Repository setup completed successfully!")
    else:
        click.echo(f"⚠️  Repository setup completed with {total_steps - success_count} failures")
        click.echo("Please check the logs above and fix any issues manually")


@cli.command()
@click.option(
    "--title", "-t", prompt="Feature title", help="Title of the feature request"
)
@click.option(
    "--description",
    "-d",
    prompt="Feature description",
    help="Detailed description of the feature",
)
@click.option(
    "--acceptance",
    "-a",
    prompt="Acceptance criteria",
    help="What needs to be true for this feature to be complete",
)
@click.option(
    "--priority",
    "-p",
    type=click.Choice([p.value for p in PriorityLevel], case_sensitive=False),
    prompt="Priority level",
    help="Priority level of the feature",
)
@click.option(
    "--size",
    "-s",
    type=click.Choice(["xs", "s", "m", "l", "xl"], case_sensitive=False),
    prompt="Size estimate",
    help="Estimated size of the feature",
)
def create_feature(
        title: str,
        description: str,
        acceptance: str,
        priority: str,
        size: str,
):
    """Create a new feature request and set up development branch"""
    verify_gh_cli()
    verify_git_clean()

    body = f"""## Problem Statement
{description}

## Acceptance Criteria
{acceptance}

## Priority
{priority.upper()}

## Size
{size.upper()}

## Development
🔄 Development branch will be created after issue creation.
"""

    try:
        # Create issue
        metadata = create_issue(
            title=title,
            body=body,
            labels=[
                "enhancement",
                f"priority:{priority}",
                f"size:{size}",
            ],
            issue_type=IssueType.FEATURE,
        )
        click.echo(
            f"✨ Feature request '{title}' created as issue #{metadata.number}"
        )

        # Set up development branch
        setup_development_branch(metadata)
        click.echo(
            f"🌿 Created and switched to branch '{metadata.branch_name}'"
        )

    except click.ClickException as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.option(
    "--base",
    "-b",
    help="Base branch for PR",
    default="develop",
    show_default=True,
)
@click.option("--draft/--no-draft", default=False, help="Create as draft PR")
def create_pr(base: str, draft: bool):
    """Create a pull request for the current branch"""
    verify_gh_cli()

    try:
        # Get current branch name
        current_branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True
        ).strip()

        # Extract issue number from branch name
        match = re.match(r"(?:feature|bugfix|docs)/issue-(\d+)", current_branch)
        if not match:
            raise click.ClickException(
                "Current branch doesn't follow the naming convention"
            )

        issue_number = match.group(1)

        # Get issue details
        issue_data = subprocess.run(
            ["gh", "issue", "view", issue_number, "--json", "title,labels"],
            capture_output=True,
            text=True,
            check=True,
        )
        issue = json.loads(issue_data.stdout)

        # Create PR with reference to issue
        cmd = [
            "gh",
            "pr",
            "create",
            "--base",
            base,
            "--title",
            issue["title"],
            "--body",
            f"Closes #{issue_number}",
        ]

        if draft:
            cmd.append("--draft")

        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        click.echo(f"🎉 Pull request created: {result.stdout.strip()}")

    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.argument("branch_name", required=False)
@click.option(
    "--force",
    "-f",
    is_flag=True,
    help="Force sync, stashing local changes",
)
def sync(branch_name: Optional[str] = None, force: bool = False):
    """Sync local repository with remote changes"""
    verify_gh_cli()

    try:
        if not branch_name:
            # Get current branch
            branch_name = subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                text=True
            ).strip()

        click.echo(f"🔍 Checking branch: {branch_name}")

        # Sync the branch
        sync_remote_branch(branch_name, force)

    except click.ClickException as e:
        click.echo(f"Error: {e}", err=True)


if __name__ == "__main__":
    cli()
