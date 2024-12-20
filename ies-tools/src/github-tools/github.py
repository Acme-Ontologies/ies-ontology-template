import json
import re
import subprocess
from typing import Optional, Tuple

import click


@click.group()
def cli():
    """CLI for managing GitHub issues and workflows"""
    pass


def create_issue(title: str, body: str, labels: list[str]) -> str:
    """Create an issue and return its number"""
    try:
        # First create the issue without requesting JSON output
        result = subprocess.run(
            [
                "gh",
                "issue",
                "create",
                "--title",
                title,
                "--body",
                body,
                *sum(
                    [["-l", label] for label in labels], []
                ),  # Flatten label args
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        # Extract issue number from the URL in the output
        # Output is typically in the format: https://github.com/owner/repo/issues/123
        issue_url = result.stdout.strip()
        issue_number = issue_url.split("/")[-1]

        return issue_number

    except subprocess.CalledProcessError as e:
        click.echo(f"Error creating issue: {e.stderr}", err=True)
        if "could not create issue" in str(e.stderr):
            click.echo(
                "Please check that you're authenticated with 'gh auth status'"
            )
        raise


def create_branch(branch_type: str, issue_number: str, title: str) -> str:
    """Create and checkout a new branch with standardized naming"""
    safe_title = title.lower().replace(" ", "-")
    branch_name = f"{branch_type}/issue-{issue_number}-{safe_title}"

    subprocess.run(["git", "checkout", "-b", branch_name], check=True)
    return branch_name


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
    type=click.Choice(["low", "medium", "high"], case_sensitive=False),
    prompt="Priority level",
    help="Priority level of the feature",
)
def create_feature(
    title: str, description: str, acceptance: str, priority: str
):
    """Create a new feature request"""
    body = f"""## Feature Request

### Description
{description}

### Acceptance Criteria
{acceptance}

### Priority
{priority.upper()}
"""

    try:
        # Verify gh CLI is available and authenticated
        try:
            subprocess.run(["gh", "--version"], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            click.echo(
                "Error: GitHub CLI (gh) not found. Please install it first.",
                err=True,
            )
            return
        except FileNotFoundError:
            click.echo(
                "Error: GitHub CLI (gh) not found. Please install it first.",
                err=True,
            )
            return

        # Verify authentication
        try:
            subprocess.run(
                ["gh", "auth", "status"], check=True, capture_output=True
            )
        except subprocess.CalledProcessError:
            click.echo(
                "Error: Not authenticated with GitHub. Please run 'gh auth login' first.",
                err=True,
            )
            return

        # Create issue and get its number
        try:
            issue_number = create_issue(
                title=f"[FEATURE] {title}",
                body=body,
                labels=["enhancement", f"priority-{priority}"],
            )
            click.echo(
                f"✨ Feature request '{title}' created as issue #{issue_number}"
            )

            # Create feature branch
            branch_name = create_branch("feature", issue_number, title)
            click.echo(f"🌿 Created and switched to branch '{branch_name}'")

        except subprocess.CalledProcessError as e:
            if "could not create issue" in str(e.stderr):
                click.echo("Error: Could not create issue. Please check:")
                click.echo("1. You have write access to the repository")
                click.echo(
                    "2. The repository exists and is properly configured"
                )
                click.echo("3. Required labels exist in the repository")
            else:
                click.echo(f"Error creating issue: {e.stderr}", err=True)
            return

    except Exception as e:
        click.echo(f"Unexpected error: {str(e)}", err=True)
        return


@cli.command()
@click.option(
    "--title", "-t", prompt="Bug title", help="Title of the bug report"
)
@click.option(
    "--description",
    "-d",
    prompt="Bug description",
    help="Description of the bug",
)
@click.option(
    "--steps",
    "-s",
    prompt="Steps to reproduce",
    help="Steps to reproduce the bug",
)
@click.option(
    "--priority",
    "-p",
    type=click.Choice(["low", "medium", "high"], case_sensitive=False),
    prompt="Priority level",
    help="Priority level of the bug",
)
def create_bug(title: str, description: str, steps: str, priority: str):
    """Create a new bug report"""
    body = f"""## Bug Report

### Description
{description}

### Steps to Reproduce
{steps}

### Priority
{priority.upper()}
"""

    try:
        # Create issue and get its number
        issue_number = create_issue(
            title=f"[BUG] {title}",
            body=body,
            labels=["bug", f"priority-{priority}"],
        )
        click.echo(f"🐛 Bug report '{title}' created as issue #{issue_number}")

        # Create bugfix branch
        branch_name = create_branch("bugfix", issue_number, title)
        click.echo(f"🌿 Created and switched to branch '{branch_name}'")
    except subprocess.CalledProcessError as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.option(
    "--title",
    "-t",
    prompt="Documentation title",
    help="Title of the documentation task",
)
@click.option(
    "--description",
    "-d",
    prompt="What needs to be documented?",
    help="Description of what needs to be documented",
)
@click.option(
    "--files",
    "-f",
    prompt="Files to Update",
    help="Which files need updating (comma-separated)",
)
@click.option(
    "--type",
    "-y",
    type=click.Choice(
        ["new", "update", "fix", "clarity"], case_sensitive=False
    ),
    prompt="Type of Documentation (comma-separated: new,update,fix,clarity)",
    help="Type of documentation work needed",
)
@click.option(
    "--priority",
    "-p",
    type=click.Choice(["low", "medium", "high"], case_sensitive=False),
    prompt="Priority",
    help="Priority level",
)
def create_docs_task(
    title: str, description: str, files: str, type: str, priority: str
):
    """Create a new documentation task"""
    # Convert comma-separated files into a formatted list
    file_list = [f.strip() for f in files.split(",")]
    files_formatted = "\n".join([f"- `{f}`" for f in file_list])

    # Convert comma-separated types into a list
    doc_types_selected = [t.strip().lower() for t in type.split(",")]

    # Format documentation types as checkboxes
    doc_types = {
        "new": "New documentation",
        "update": "Update existing documentation",
        "fix": "Fix errors/typos",
        "clarity": "Improve clarity",
    }
    type_checkboxes = "\n".join(
        [
            f"- [{'x' if t in doc_types_selected else ' '}] {doc_types[t]}"
            for t in doc_types.keys()
        ]
    )

    body = f"""## Documentation Task

### Description
{description}

### Files to Update
{files_formatted}

### Type of Documentation
{type_checkboxes}

### Priority
{priority.upper()}

### Checklist
{'\n'.join([f'- [ ] Update {f}' for f in file_list])}
"""

    try:
        # Create issue with all labels
        labels = ["documentation", f"priority-{priority}"]
        labels.extend([f"docs-{t}" for t in doc_types_selected])

        issue_number = create_issue(
            title=f"[DOCS] {title}", body=body, labels=labels
        )
        click.echo(
            f"📚 Documentation task '{title}' created as issue #{issue_number}"
        )

        # Create documentation branch
        branch_name = create_branch("docs", issue_number, title)
        click.echo(f"🌿 Created and switched to branch '{branch_name}'")
    except subprocess.CalledProcessError as e:
        click.echo(f"Error: {e}", err=True)


def extract_issue_info(branch_name: str) -> Tuple[Optional[str], Optional[str]]:
    """Extract issue type and number from branch name"""
    # Updated pattern to match our new branch naming convention
    pattern = r"(feature|bugfix|docs)/issue-(\d+)-.*"
    match = re.match(pattern, branch_name)

    if match:
        return match.group(1), match.group(2)
    return None, None


@cli.command()
@click.option(
    "--title",
    "-t",
    help="PR title (defaults to issue title)",
)
@click.option(
    "--body",
    "-b",
    help="PR description (default: auto-generated from branch)",
)
@click.option("--draft/--no-draft", default=False, help="Create as draft PR")
@click.option(
    "--auto-merge/--no-auto-merge",
    default=False,
    help="Enable auto-merge after approval",
)
def create_pr(
    title: Optional[str], body: Optional[str], draft: bool, auto_merge: bool
):
    """Create a pull request for the current branch"""
    try:
        # Get current branch name
        current_branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True
        ).strip()

        # Extract branch type and issue number
        branch_type, issue_number = extract_issue_info(current_branch)

        if not branch_type or not issue_number:
            click.echo(
                "⚠️  Warning: Current branch doesn't follow the standard naming convention"
            )
            if click.confirm("Do you want to continue anyway?", default=False):
                issue_number = None
            else:
                return

        # If no title provided, try to get it from the issue
        if not title and issue_number:
            try:
                issue_data = subprocess.run(
                    ["gh", "issue", "view", issue_number, "--json", "title"],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                title = json.loads(issue_data.stdout)["title"]
            except subprocess.CalledProcessError:
                # Fall back to last commit message if issue not found
                title = subprocess.check_output(
                    ["git", "log", "-1", "--pretty=%B"], text=True
                ).strip()
        elif not title:
            # No issue number and no title provided
            title = subprocess.check_output(
                ["git", "log", "-1", "--pretty=%B"], text=True
            ).strip()

        # Generate PR body if not provided
        if not body:
            body = "## Changes\n\n"
            if branch_type == "feature":
                body += "This PR implements a new feature.\n\n"
            elif branch_type == "bugfix":
                body += "This PR fixes a bug.\n\n"
            elif branch_type == "docs":
                body += "This PR updates documentation.\n\n"

            # Add link to related issue if found
            if issue_number:
                body += f"Resolves #{issue_number}\n\n"

            # Add modified files section
            try:
                files_changed = subprocess.check_output(
                    ["git", "diff", "--name-only", "main..."], text=True
                ).strip()
                if files_changed:
                    body += "## Modified Files\n"
                    body += "\n".join(
                        [f"- `{f}`" for f in files_changed.split("\n")]
                    )
                    body += "\n\n"
            except subprocess.CalledProcessError:
                pass

            body += "## Checklist\n\n"
            body += "- [ ] Code follows the project's coding style\n"
            body += "- [ ] Tests added/updated (if applicable)\n"
            body += "- [ ] Documentation updated (if applicable)\n"
            body += "- [ ] All tests passing\n"

        # Build the PR creation command
        cmd = [
            "gh",
            "pr",
            "create",
            "--title",
            str(title or ""),  # Convert potential None to empty string
            "--body",
            str(body or ""),  # Convert potential None to empty string
            "--base",
            "main",
        ]

        if draft:
            cmd.append("--draft")

        # Create the PR
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        pr_url = result.stdout.strip()
        click.echo("🎉 Pull request created successfully!")
        click.echo(f"   {pr_url}")

        # Enable auto-merge if requested
        if auto_merge:
            subprocess.run(
                ["gh", "pr", "merge", "--auto", "--merge"], check=True
            )
            click.echo("🤖 Auto-merge enabled")

        # Add labels based on branch type
        try:
            labels = []
            if branch_type == "feature":
                labels.append("enhancement")
            elif branch_type == "bugfix":
                labels.append("bug")
            elif branch_type == "docs":
                labels.append("documentation")

            if issue_number:
                labels.append("has-issue")

            if labels:
                subprocess.run(
                    [
                        "gh",
                        "pr",
                        "edit",
                        *sum([["-l", label] for label in labels], []),
                    ],
                    check=True,
                )
        except subprocess.CalledProcessError:
            # Don't fail if labels don't exist
            pass

    except subprocess.CalledProcessError as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.argument("pr_number", type=str, required=False)
def review_pr(pr_number: Optional[str]):
    """Review the current branch's PR or a specific PR"""
    try:
        if not pr_number:
            # Get PR number for current branch
            pr_data = subprocess.check_output(
                ["gh", "pr", "view", "--json", "number"], text=True
            )
            pr_number = pr_data.strip()

        # Ensure pr_number is a string
        pr_number_str = str(pr_number)

        # Show PR diff
        subprocess.run(["gh", "pr", "diff", pr_number_str], check=True)

        # Show the list of changed files
        click.echo("\nChanged files:")
        subprocess.run(["gh", "pr", "view", "--files"], check=True)

        # Prompt for review decision
        decision = click.prompt(
            "\nReview decision",
            type=click.Choice(["approve", "comment", "request-changes"]),
            default="comment",
        )

        comment = click.prompt("Review comment", default="")

        # Submit review
        subprocess.run(
            [
                "gh",
                "pr",
                "review",
                pr_number_str,
                f"--{decision}",
                "--body",
                str(comment),  # Ensure comment is a string
            ],
            check=True,
        )

        click.echo("✅ Review submitted successfully!")

    except subprocess.CalledProcessError as e:
        click.echo(f"Error: {e}", err=True)


if __name__ == "__main__":
    cli()
