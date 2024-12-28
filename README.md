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
See the [.gitHub README.md][gh-readme] for detailed information about available workflows and templates.

After creating a new repository from the template, follow these steps to complete set up:

1. Set up poetry / Python environment for ies-tools:
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
2. Verify poetry setup:
+
```bash
poetry run gh-tools --help
```
If all is well, you should see the help output for the `gh-tools` command, including several available workflows.

3. Commit and push `poetry.lock` to the repository.
```bash
git add .
git commit -m "chore(project): update poetry dependencies"
git push origin main
```

4. Run project set-up script to initialise the repository. This:
  - Sets up repository labels
  - Creates the `develop` branch from `main` and switches to it
  - Adds IES Core as a Git submodule
  - Checks for `gh` and `just` CLIs

```bash
poetry run gh-tools setup-repo
```

5. If this ontology repository is _not_ `ies-core`, then commit and push the submodule changes.
```bash
# We're in `develop` branch
git add .
git commit -m "chore(project): add IES Core submodule"
git push origin develop
# Merge to `main` branch
git switch main
git merge develop
git push origin main
```

6. If necessary, install GitHub CLI, `gh`
```bash
# On macOS
brew install gh

# On Ubuntu
sudo apt-get install gh

# On Windows
TBD
```

7. Authenticate `gh`
```bash
gh auth login
```

8. If necessary, install `just`
```bash
# On macOS
brew install just

# On Ubuntu
sudo apt-get install just

# On Windows
TBD
```

9. Check repo labels
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
The special GitHub workflow `sync-tools.yml` is scheduled to run daily to update the common IES workflows and tools from the [IES Ontology Template][ont-template]
When updates are available, a PR will be created ready to be reviewed and merged into the local repository.

Alternatively, the workflow can be triggered manually by running the following commands:

```bash
# Fetch latest tool changes from the IES Ontology Template
poetry run sync-tools
```

If there are updates, review the new PR and merge it into the local repository.

## IES Core

**DO NOT CHANGE IES CORE form this repository. Instead, go directly to IES Core repo and use the development workflow to propose changes for PR and review**

This ontology repository uses IES Core as a submodule. To update IES Core, run the following commands:

```bash
# Update IES Core submodule
git submodule update --remote --merge
```

For further details on IES Core, see the [IES Core README.md][ies-core].

## IES Tools

See the [IES Tools README.md][ies-tools] for details on the tools available for ontology development.

## GitHub Workflows

See the [.github README.md][gh-readme] for detailed information about available workflows and templates.

## Commitizen

See the [Commitizen guidance][commit-readme] for details on how we prefer to format Git commits.

## Ontology Narrative Documentation

See the [Narrative Documentation guidance][docs-readme] for details on how to write narrative documentation for the ontology.

## Builds

This repository uses GitHub Actions for CI/CD. The build artifacts are stored in the `build/` directory.

We follow DRY (Don't Repeat Yourself) principles, meaning, for example, that ontology files are always mastered in `.ttl` files, and other RDF formats are generated from these files and stored in `./build/`.

See the [Builds guidance][build-readme] for more details.

## Contributing
Please see [Contributing Guide][docs-contrib] for guidelines on how to contribute to this ontology project.

## Licensing

Unless stated otherwise, the ontology definitions and codebase are released under [the MIT License][mit].
This covers both the [ontology src][src] and any sample code in the [documentation][docs].

The documentation is [© Crown copyright][copyright] and available under the terms
of the [Open Government 3.0][ogl] licence.

### Attribution
When using this ontology, please include the attribution:
> © Crown Copyright 2024, Department for Business and Trade

### Third Party Components
This project includes third party software and tools under different licenses. See individual dependency documentation for details.

## Changelog
See [CHANGELOG][CHANGELOG] for a list of changes in each release.

## Version
Current version information is maintained in the [VERSION][VERSION] file.

## Vulnerability Disclosure

GOV.UK Pay aims to stay secure for everyone. If you are a security researcher and have discovered a security vulnerability in this repository, we appreciate your help in disclosing it to us in a responsible manner. Please refer to our [vulnerability disclosure policy][vul] and our [security.txt][sec] file for details.

[build-readme]: build/README.md
[CHANGELOG]: CHANGELOG.md
[commit-readme]: docs/COMMITIZEN.md
[copyright]: https://www.nationalarchives.gov.uk/information-management/re-using-public-sector-information/uk-government-licensing-framework/crown-copyright/
[docs]: docs/README.md
[docs-contrib]: docs/CONTRIBUTING.md
[docs-readme]: docs/README.md
[gh-readme]: .github/README.md
[ies-core]: core/README.md
[ies-tools]: ies-tools/README.md
[mit]: LICENCE
[ogl]: https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/
[ont-template]: https://github.com/Acme-Ontologies/ies-ontology-template
[sec]: https://vdp.cabinetoffice.gov.uk/.well-known/security.txt
[src]: src/README.md
[VERSION]: VERSION
[vul]: https://www.gov.uk/help/report-vulnerability