# IES [INSERT NAME] Ontology

![IES Logo](assets/images/ies-logo.png)

## Update This README
Modify this README to reflect the domain ontology project. As a minimum:

  - Replace `[INSERT NAME]` with the name of the ontology project
  - Update the `Overview` section with a brief description of the ontology project
  - (Optional) update the `Repository Structure` section with the structure of the ontology project

## Overview
This repository contains the development artifacts for an IES ontology project. It follows the standard IES ontology development repository structure and incorporates shared IES tools and GitHub workflows.

## Repository Structure
The repository follows the IES standardized structure for ontology development:

* `.github/` - GitHub workflows and issue templates
* `assets/` - Project assets like images and logos
* `build/` - Build artifacts and outputs
* `docs/` - Project documentation
  * `diagrams/` - Ontology diagrams and visualizations
  * `exemplars/` - Example usage and patterns
  * `specifications/` - Formal specifications
* `imports/` - Imported ontologies and dependencies
* `src/` - Source files
  * `competencies/` - Competency questions in SPARQL
  * `data/` - Source data files
  * `ontology/` - Ontology source files
* `tests/` - Test suites
  * `integration/` - Integration tests
  * `unit/` - Unit tests
  * `validation/` - Validation tests and shapes
* `ies-tools/` - Development tools

## Initial Setup
See the [.gitHub README.md](.github/README.md) for detailed information about available workflows and templates.

After creating a new repository from the template, follow these steps to complete set up:

1. Create the `development` branch from `main`. `feature/*` branches should be created from `development`. Push `development` to the remote repository.
+
```bash
git branch develop
git push -u origin develop
```

2. Set up poetry / Python environment for ies-tools:
+
```bash
# Install poetry
# On macOS
brew install poetry
# On Ubuntu
sudo apt-get install poetry
# On Windows
TBD

# Install and update project dependencies
poetry install
poetry update
```
3. Verify poetry setup:
+
```bash
poetry run gh-tools --help
```
If all is well, you should see the help output for the `gh-tools` command, including several available workflows.

4. Commit and push `poetry.lock` to the repository.
```bash
git add .
git commit -m "chore(project): Add poetry.lock"
git push origin main
```

5. Run project set-up script to initialise the repository.
```bash
poetry run gh-tools setup-repo

5. If necessary, install GitHub CLI, `gh`
+
```bash
# On macOS
brew install gh

# On Ubuntu
sudo apt-get install gh

# On Windows
TBD
```

6. Authenticate `gh`
```bash
gh auth login
```

7. Check repo labels
```bash
gh label list
```

## Development GitHub Workflows

### Creating Issues

#### Alternative 1
Use the provided tools to create issues, PRs, and sync changes:

```bash
# Create a new feature request and set up development branch
poetry run gh-tools create-feature

# Create a pull request for the current branch
poetry run gh-tools create-pr

# Sync local repository with remote changes
poetry run gh-tools sync
```

#### Alternative 2
```bash
# Create a feature request
gh workflow run feature-request.yml \
  -f title="My New Feature" \
  -f problem="Description of the problem" \
  -f solution="Proposed solution" \
  -f priority="priority:medium" \
  -f size="size:m" \
  -f type="Core Functionality" \
  -f acceptance="- [ ] Feature works as expected"
```
The workflow creates the feature issue and a feature branch for development. Update your local clone and switch to the new feature branch to start development.
```bash
git fetch origin
git switch feature/[feature-name]-[issue-number]
```

### Updating GitHub workflows and IES Tools
The special GitHub workflow `sync-tools.yml` is scheduled to run daily to update the common IES workflows and tools from the [IES Ontology Template](https://github.com/Acme-Ontologies/ies-ontology-template).
When updates are available, a PR will be created ready to be reviewed and merged into the local repository.

Alternatively, the workflow can be triggered manually by running the following commands:

```bash
# Fetch latest tool changes from the IES Ontology Template
poetry run sync-tools
```

If there are updates, review the new PR and merge it into the local repository.

## Contributing
Please see [Contributing Guide](docs/CONTRIBUTING) for guidelines on how to contribute to this ontology project.

## License
This ontology repository is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Changelog
See [CHANGELOG](CHANGELOG) for a list of changes in each release.

## Version
Current version information is maintained in the [VERSION](VERSION) file.