# IES Tools

## Important
These common tools are maintained in the [IES Ontology Template](http://github.com/Acme-Ontologies/ies-ontology-template) repository. The tools are automatically updated daily in the domain ontology repositories using the `sync-tools.yml` GitHub workflow.

**DO NOT MODIFY THE TOOLS IN THIS REPOSITORY DIRECTLY. RATHER MAKE CHANGES IN [IES Ontology Template](https://github.com/Acme-Ontologies/ies-ontology-template)**

## Overview
A collection of automation tools for IES projects. Currently, includes:

- a Python script for automating GitHub CLI (`gh`) commands
- A Just script for automating common tasks

## Directory Structure
```ascii
.
├── ies-tools/
│   └── src/
│       └── github-tools/     # GitHub automation tools
│           └── github.py     # CLI for managing GitHub issues and workflows
│           └── README.md     # Specific README for the GitHub tools script
├── tests/                    # Test directory
│   ├── integration/
│   └── unit/
├── README.md                 # This README file
```

## Usage
### GitHub Tools
The github-tools package provides a CLI for managing GitHub issues and workflows:
    
```bash
# Create a new feature request
poetry run gh-tools create-feature

# Create a pull request
poetry run gh-tools create-pr

# Sync your local repo with the remote
poetry run gh-tools sync
```
Run `poetry run gh-tool --help` to see all available commands.

### Justfile
The Justfile provides a set of common tasks for IES projects. To see all available tasks, run:

```bash
just --list
```

## Contributing
  1. Make changes in [IES Ontology Template repository](https://github.com/Acme-Ontologies/ies-ontology-template)
  2. Add tests for new features
  3. Test in a "consumer" domain ontology repository craeted from the template
  4. Once verified, create a PR on the `main` branch. The updated IES tools will be automatically synced to all domain ontology repositories.
