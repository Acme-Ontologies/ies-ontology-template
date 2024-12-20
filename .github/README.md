# GitHub Workflows and Issue Templates

This ontology template repository includes definitions for common GitHub workflows and issue templates used across multiple (domain) ontology development projects.

## Contents
```ascii
.
├── .github
│   ├── CODEOWNERS
│   ├── ISSUE_TEMPLATE
│   │   ├── issue-bug.yml
│   │   ├── issue-doc.yml
│   │   └── issue-feature.yml
│   └── workflows
│       ├── README_update_workflows.md
│       ├── issue-bug.yml
│       ├── issue-doc.yml
│       ├── issue-feature.yml
│       ├── ontology-qa-review.yml
│       ├── ontology-release-candidate.yml
│       └── ontology-validation.yml
└── README.md
```

## Usage

This template repository is used to create a new (domain) ontology repository on GitHub.com for development. [Use this template](https://github.com/Acme-Ontologies/ies-ontology-template/generate) page to create a new repository.

This will create a new ontology development repository with the workflows and issue templates from this template repository.

To keep the GitHub workflows and IES tools in sync, the `sync-tools.yaml` workflow is scheduled to run every day. If there are updates to the workflows or IES tools, a PR is created in the domain ontology repository. This enables the updated tools to be merged into the repository.

The GitHub workflows and IES tools can be used as they would be in any other repository.

## Contents
### Workflows
  - sync-tools.yml - Syncs workflows and IES tools from the [ies-ontology-template](https://github.com/Acme-Ontologies/ies-ontology-template) repository to the domain ontology repository
  - issue-feature.yml - Handles feature request automation
  - issue-bug.yml - Handles bug report automation
  - issue-doc.yml - Handles documentation task automation
  - ontology-qa-review.yml - Workflow for ontology QA review
  - ontology-release-candidate.yml - Workflow for ontology release candidates
  - ontology-validation.yml - Workflow for ontology validation

### Issue Templates
  - issue-feature.yml - GitHub workflow Template for new feature requests
  - issue-bug.yml - Template for bug reports
  - issue-doc.yml - Template for documentation tasks

## Contributing
When making changes to workflows or templates:

  1. Make changes in this repository in a `dev` branch
  2. Validate in a test consumer repository
  3. Once confirmed working, merge changes into `main`
4. All 'consuming' (domain) ontology development repositories will receive the updates via the `sync-tools` workflow, which is scheduled to run daily
