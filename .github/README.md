# GitHub Workflows and Issue Templates

This ontology template repository includes definitions for common GitHub workflows and issue templates used across multiple (domain) ontology development projects.

## Contents
```ascii
.
├── CODEOWNERS
├── ISSUE_TEMPLATE
│   ├── feature-request.yml
│   ├── issue-bug.yml
│   └── issue-doc.yml
├── README.md
├── sstructure.txt
└── workflows
    ├── README-create-ontology-repo.md
    ├── README-feature-workflows.md
    ├── README-sync-ies-tools.md
    ├── create-ontology-repo.yml
    ├── feature-development.yml
    ├── feature-request.yml
    ├── issue-bug.yml
    ├── issue-doc.yml
    ├── ontology-qa-review.yml
    ├── ontology-release-candidate.yml
    ├── ontology-validation.yml
    ├── setup-labels.yml
    └── sync-ies-tools.yml

3 directories, 19 files
```

## Usage

This template repository is used to create a new (domain) ontology repository on GitHub.com for development. [Use this template](https://github.com/Acme-Ontologies/ies-ontology-template/generate) page to create a new repository, or run the `create-ontology-repo.yml` workflow.

This will create a new ontology development repository with the workflows and issue templates from this template repository.

To keep the GitHub workflows and IES tools in sync, the `sync-tools.yaml` workflow is scheduled to run every day. If there are updates to the workflows or IES tools, a PR is created in the domain ontology repository. This enables the updated tools to be merged into the repository.

The GitHub workflows and IES tools can be used as they would be in any other repository.

## Contents
### Workflows
  - `sync-ies-tools.yml` - Syncs workflows and IES tools from the [ies-ontology-template](https://github.com/Acme-Ontologies/ies-ontology-template) repository to the domain ontology repository
  - `setup-labels.yml` - Sets up standard repository labels for issue tracking
  - `create-ontology-repo.yml` - Workflow to create a new ontology repository from this template
  - `feature-request.yml` - Handles opening a new feature issue
  - `feature-development.yml` - Automated workflow for feature development
  - `issue-bug.yml` - Handles bug report automation
  - `issue-doc.yml` - Handles documentation task automation
  - `ontology-qa-review.yml` - Workflow for ontology QA review
  - `ontology-release-candidate.yml` - Workflow for ontology release candidates
  - `ontology-validation.yml` - Workflow for ontology validation

### Issue Templates
  - `feature-request.yml` - GitHub workflow to open a new feature issue
  - `issue-bug.yml` - GitHub workflow to open a new bug issue
  - `issue-doc.yml` - GitHub workflow to open a new documentation issue

## Contributing
When making changes to workflows or templates:

  1. Make changes in this repository in a `dev` branch
  2. Validate in a test consumer repository
  3. Once confirmed working, merge changes into `main`
4. All 'consuming' (domain) ontology development repositories will receive the updates via the `sync-tools` workflow, which is scheduled to run daily
