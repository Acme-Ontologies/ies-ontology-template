# IES [INSERT NAME] Ontology

![IES Logo](assets/images/ies-logo.png)

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
Follow these steps to set up a new ontology repository:

1. Create a new (domain) ontology development repository from the IES Ontology template [IES Ontology Template](https://github.com/Acme-Ontologies/ies-ontology-template/generate). See the [.gitHub README.md](.github/README.md) for detailed information about available workflows and templates.

2. Set up poetry / Python environment for ies-tools:
   ```bash
   poetry install
   ```

3. Verify poetry setup:
   ```bash
   poetry run gh-tool --help
   ```

If all is well, you should see the help output for the `gh-tool` command.

## Development GitHub Workflows

### Creating Issues
Use the provided tools to create standardized issues:

```bash
# Create a feature request
poetry run gh-tool create-feature

# Create a bug report
poetry run gh-tool create-bug

# Create a documentation task
poetry run gh-tool create-docs-task
```

### Pull Requests
Create pull requests using the provided tool:

```bash
poetry run gh-tool create-pr
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
Please see [Contributing Guide](docs/CONTRIBUTING.adoc) for guidelines on how to contribute to this ontology project.

## License
This ontology repository is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Changelog
See [CHANGELOG](CHANGELOG.adoc) for a list of changes in each release.

## Version
Current version information is maintained in the [VERSION](VERSION) file.