# IES Ontology Family - Design and Development Guide

## ToDo

- [ ] Add DOCUMENT_ID and DOCUMENT_DRAFT_STATUS_ID to project secrets
- [ ] Note to add the `ACME-ONTOLOGIES-PAT` token as a repo secret for each domain ontology repo
- [ ] Add ies-core as submodule to all domain ontologies; can it be done automatically? Or using a one-off workflow or just script (yes, use a just script to add the submodule)
- [ ] Make issue-feature work in a domain ontology repo
- [ ] Make issue-bug work in a domain ontology repo
- [ ] Make issue-doc work in a domain ontology repo
- [ ] Make ontology-qa-review work in a domain ontology repo
- [ ] Make ontology-release-candidate work in a domain ontology repo
- [ ] Make ontology-validation work in a domain ontology repo
- [ ] Add a CONTRIBUTING.md file to the domain ontology repo
- [ ] Create the CHANGELOG.md file, as example
- [ ] Add Crown copyright notice to the LICENSE file
- [ ] Wrap feature commits and issue comments together in a workflow
- [ ] TBD

# 1. Overview

## 1.1. Introduction to IES Ontologies

The IES Ontology family is a collection of interconnected ontologies designed to model and represent knowledge across various industrial and enterprise system domains. At its foundation is the IES Core ontology, which provides common concepts, patterns, and relationships that are extended by domain-specific ontologies.

### Architecture Overview

#### Visual Overview

The following diagram illustrates the core architecture of the IES Ontology family, showing the relationship between IES Core concepts and domain-specific extensions:

![IES Ontology Overview](../build/docs/diagrams/ontology-overview.svg)

Key elements in the diagram:
- Blue boxes represent core concepts from IES Core
- Green boxes represent domain-specific extensions
- Pink diamonds represent object properties (relations between entities)
- Yellow diamonds represent data properties (entity attributes)
- Arrows show inheritance and property relationships

The diagram demonstrates how domain ontologies extend core concepts while maintaining a clear separation of concerns.

The ontology family follows a modular architecture:

1. **IES Core Ontology**
- Serves as the upper ontology for the entire family
- Defines fundamental concepts and relationships
- Establishes common patterns for domain extensions
- Provides base classes and properties for reuse
- Maintains consistency across all domain ontologies

2. **Domain Ontologies**
- IES Building: Models building structures, spaces, and systems
- IES Infrastructure: Represents infrastructure assets and networks
- IES Security: Defines security concepts and controls
- IES People: Models organizational structures and roles
- IES Transport: Represents transportation systems and networks

Each domain ontology imports IES Core as a Git submodule, ensuring consistency in the base concepts while allowing domain-specific extensions and specializations.

### Design Philosophy

The IES Ontology family adheres to these core principles:
- Modularity: Clear separation between core and domain concepts
- Reusability: Common patterns defined in IES Core
- Consistency: Standardized development and maintenance processes
- Quality: Rigorous testing and validation requirements
- Maintainability: Automated tooling and standardized workflows

## 1.2. Ontology Structure

### 1.2.1. IES Core

IES Core serves as the foundation for all domain ontologies. It provides:
- Basic entity types and relationships
- Common design patterns
- Reusable property definitions
- Extension points for domain specialization
- Validation rules and constraints

Key features:
- Maintained in a dedicated repository
- Versioned independently of domain ontologies
- Imported by all domain ontologies as a Git submodule
- Changes managed through a strict review process

### 1.2.2. Domain Ontologies

Each domain ontology extends IES Core with specialized concepts and relationships. Domain ontologies:
- Import IES Core as a Git submodule
- Define domain-specific classes and properties
- Implement domain patterns and rules
- Maintain their own versioning
- Follow standardized development processes

## 1.3. Licensing and Copyright

### Licence Terms
The IES Ontology family is released under the MIT License, chosen for its permissive terms and broad compatibility. This allows:
- Commercial use
- Modification and distribution
- Private use
- Sublicensing

### Copyright
- UK Crown Copyright applies to all ontology files, code, and documentation.

## 1.4. Project Management

### 1.4.1 Version Control
- Semantic versioning (MAJOR.MINOR.PATCH)
- Version tracked in VERSION file
- Changes documented in CHANGELOG.md
- Git tags for release versions

### 1.4.2 Change Management
The CHANGELOG.md file tracks:
- Added features and concepts
- Modified relationships and properties
- Deprecated terms
- Breaking changes
- Bug fixes

### 1.4.3 Dependencies
Managed through:
- catalog.xml for ontology imports
- imports/dependencies.txt for explicit dependency listing
- Git submodules for IES Core integration

### 1.4.4 Project Tracking
Each repository includes:
- GitHub Project board for issue/PR tracking
- Milestone management (in Jira)
- Label system for categorization of issues and PRs
- Automated workflow integration

This infrastructure ensures consistent development practices and maintains high quality across the entire ontology family while enabling efficient collaboration among team members.

# 2. GitHub Organization Setup

## 2.1. IES-Org Configuration

### 2.1.1 Team Structure
The IES organization consists of a single team with the following roles:
- 4 Ontology Developers
- 1 Project Manager
- 2 Reviewers
- 2 Customer/Client Representative

### 2.1.2 Permission Requirements
- Team members require read/write access to:
  - Repository contents
  - Issues
  - Pull requests
  - Project boards

### 2.1.3 GitHub Plan Requirements
A GitHub Team plan is required for:
- Supporting the organization's collaborator count
- Enabling Organization PAT usage on private repositories
- Managing private repositories for the ontology family

## 2.2 Access Management

### 2.2.1 Personal Access Tokens (PATs)
- The `ACME-ONTOLOGIES-PAT` is the primary token for automation
- It must be configured as an organization-level secret with the following permissions:
  - `repository access` (read/write access to all repositories owned by the organization)
  - `organization` (Read and Write access to organization actions variables, organization projects, and organization secrets)
  - `repository permissions`
    - `read` (Read access to all repository metadata)
    - `read/write` (Read and Write access to actions, actions variables, administration, code, pull requests, and workflows)

### 2.2.2 Organization Secrets
Required organization-level secrets:
- `ACME-ONTOLOGIES-PAT`: Used for cross-repository operations and automation workflows

### 2.2.3 Repository Configuration
New repositories are created from the [IES Ontology Repository Template][ont-template] using the [create-ontology-repo.yml][create-ontology]. Each repository is configured with:
- standardised repo labels for issue tracking
- A set of GitHub workflows for common development tasks
- IES Tools for local development and automation
- IES Core ontology as a Git submodule
- A dedicated GitHub Project for issue and PR tracking
- `PROJECT_ID` configured as a repository-level variable
- Additional repository-specific secrets may be added as needed

### 2.2.4 Environment Variables
Currently, no environment-specific variables are required beyond the repository-level configurations.

## 2.3 Repository Template

### 2.3.1 Template Customization
Repository setup is primarily automated through:
1. The [create-ontology-repo.yml][create-ontology] workflow
2. The `poetry run gh-tools setup-repo` command, which initializes the repository with standard configurations and checks for required CLI tools
3. Manual updates required:
   - Repository README.md to reflect domain ontology name
   - Any domain-specific documentation

### 2.3.2 Branch Configuration
- Default branch: `main`
- Release Candidate branch: `rc`
- Development branch: `develop`
- Feature branches: `feature/*`
- Bugfix branches: `bugfix/*`
- Hotfix branches: `hotfix/*`
- Branch protection rules and validation checks are yet to be developed

![IES Branch Flows](../build/docs/diagrams/branch-flows.svg)

### 2.3.3 Development Flow
#### 2.3.3.1 Feature and Regular Bugfix Flow
1. All feature development and regular bug fixes occur in `feature/*` and `bugfix/*` branches
2. Ontology developer pull requests target the `develop` branch
3. QA reviewers approve PRs before merging to `develop`
4. QA Reviewer pull requests target the `rc` branch
5. QA Reviewer approves PRs before merging to `rc`
6. Customer/client reviews the release candidate and approves PR to `main`
7. IES TGG reviews and approves release PRs before final merge to `main`
8. Changes are backported to `develop` after merging to `main`

#### 2.3.3.2 Hotfix Flow
1. Critical fixes that can't wait for the regular release cycle are created in `hotfix/*` branches
2. Hotfix pull requests target the `main` branch directly
3. Customer/client must review and approve hotfix PRs
4. IES TGG performs final review before merging to `main`
5. After merge to `main`, changes should be backported to `develop` to maintain consistency

### 2.3.4 Repository Policies
- No organization-wide policies are currently implemented
- Repository-specific policies and rules will be developed as needed
- Future considerations may include:
  - Branch protection rules
  - Required status checks
  - Required review processes
  - Automated validation requirements

### 2.3.5 Template Maintenance
- Template repository serves as the source of truth for the ontolofy repo structure, IES tools and automation workflows
- Changes to template structure should be managed through:
  - Pull requests to template repository
  - [Synchronization workflow][sync-tools] to propagate workflow and tool changes to ontology repositories
  - Version control of template components

Clearly, some changes to the template structure, workflows, or GitHub configurations may be required as the ontology family evolves. These changes should be managed through the template repository, but may need to be manually propagated to ontology repos to avoid overwriting local customisations.

# 3 Development Infrastructure

## 3.1 Repository Creation and Setup

### 3.1.1 Create Ontology Repository Workflow

The `create-ontology-repo.yml` workflow automates the initialization of new ontology repositories, ensuring consistency across the family of ontologies. This workflow:

1. Creates a new repository from the template
2. Configures basic repository settings
3. Sets up the initial directory structure
4. Establishes required GitHub configurations

#### 3.1.1.1 Key Configuration Steps:

- Repository naming convention enforcement
- Basic metadata setup (description, topics, visibility)
- Initial branch creation and protection
- Documentation template population

### 3.1.2 Project Board Configuration

Each repository maintains a standardized project board structure that integrates with the organizational workflow:

- Sprint planning board
- Backlog management
- Release tracking
- Bug tracking

### 3.1.3 Label Management

Standard labels are automatically configured for:

- Issue types (bug, feature, enhancement)
- Priority levels
- Development stages
- Release tracking
- Documentation needs

### 3.1.4 Branch Protection Rules

The following branch protection rules are implemented:

- Main branch:
  - Requires pull request reviews
  - Requires status checks to pass
  - No direct pushes allowed
  
- Release candidate (rc) branch:
  - Similar protections to main
  - Additional deployment checks
  
- Develop branch:
  - Requires basic review
  - Automated tests must pass

### 3.2 Jira and GitHub Projects Integration

#### 3.2.1 Jira Integration (TBD)
The following Jira integration features are planned for implementation:
- Project structure and hierarchy
- Sprint management and agile workflow
- Integration with GitHub repositories
- Automated issue synchronization
- (Optional) custom fields for ontology-specific metadata

#### 3.2.2 GitHub Project Board Structure
Each ontology repository maintains a standardized project board that:
- Provides visibility into active development
- Tracks issues and pull requests
- Manages releases and versions
- Facilitates bug tracking and resolution

The board includes the following views:
**Development Pipeline**
- New Issues
- In Progress
- Ready for Review
- Done

**Release Planning**
- Upcoming Features
- Completed Items

#### 3.2.3 Issue and PR Management
Issues and Pull Requests follow a standardized workflow:
**Creation and Triage**
- Issue templates ensure consistent information capture
- Labels applied for categorization
- Priority assignment 
**Development Tracking**
- Branch creation
- Work progress updates
- Review assignments
**Completion and Closure**
- Review approval
- Merge process
- Issue closure

#### 3.2.4 Pull Request Automation
The [Pull Request checks Workflow][pr-checks] automates PR management across IES repositories through several key features:

**Branch Flow Validation:**
- Enforces established branch flow rules:
- `feature/*` → `develop`: Feature development
- `bugfix/*` → `develop`: Bug fixes in development
- `hotfix/*` → `main`: Critical production fixes
- `develop` → `rc`: Release candidate preparation
- `rc` → `main`: Production release
- `sync-ies-tools-*` → `main`: Tool synchronization

**Label Management:**
- Automatically applies and manages labels:
  - Process labels: `needs-review`, `needs-link`, `invalid-target`
  - Type labels: `enhancement`, `bug`, `hotfix`, `release-candidate`, `production-release`
  - Inherited from linked issues: `priority:*`, `size:*`, `documentation`
- Cleans up process labels after PR merge

**Issue Linkage:**
- Enforces issue linking for feature, bugfix, and hotfix branches
- Validates issue references in PR description
- Inherits relevant labels from linked issues
- Adds warning comments for unlinked PRs

**Future Enhancements (Planned):**
- Approval requirements based on target branch
- Code coverage requirements per target
- Automated changelog generation
- Reviewer assignments based on PR type
- Conventional commit message enforcement
- Enhanced branch protection rules

### 3.3 Common Tools and Workflows

#### 3.3.1 IES Tools Overview
The `ies-tools/` directory contains shared tooling and utilities that can be used across all ontology repositories:

**Core Components:**
- Command-line interface (CLI) tools for repository management
- Shared GitHub workflow definitions
- Common configuration files
- Development environment setup scripts
- Quality assurance and validation tools

**Key Features:**
- Standardized development environment
- Consistent tooling across repositories
- Automated repository setup and maintenance
- Shared quality control mechanisms

#### 3.3.2 GitHub Workflow Automation
The repositories utilize several automated workflows defined in `.github/workflows/`:

1. Repository Management
   - Repository creation and setup
   - Label and project board configuration
   - Branch protection rules implementation

2. Development Workflows
   - Pull request validation and management
   - Issue tracking and linking
   - Release process automation

3. Quality Control
   - Automated testing
   - Documentation build
   - Style and consistency checks

#### 3.3.3 Tool Synchronization Process
The `sync-ies-tools.yml` workflow maintains consistency across repositories and is scheduled to run daily.

**Synchronization Process:**
1. Detects updates in the template repository
2. Creates synchronization branches in each repository
3. Updates common tooling and workflows
4. Generates pull requests for review
5. Applies changes after approval

**Synchronized Components:**
- GitHub workflow definitions
- IES Tools scripts

#### 3.3.4 Local Development Setup
Developers need to configure their local environment with - see the main [README.md][repo-readme] for details.

**Required Tools:**
- Python 3.9 or higher
- Poetry for dependency management
- Git with LFS support `git`
- GitHub CLI `gh`
- `node` and `npm`
- `just` CLI for task automation

**Development Guidelines:**
- Use provided CLI tools for common tasks
- Follow branch naming conventions
- Commit often and with meaningful messages (see [commitizen README][commitizen])
- Ensure all tests pass locally before pushing
- Keep tools and dependencies updated

## 4. Repository Structure

### 4.1 Project Files
Each ontology repository contains standard project files that define its configuration and behavior:

**General Project Files:**
- `README.md`: Project overview, setup instructions, and usage guidelines
- `pyproject.toml`: Python project configuration and dependencies
- `poetry.toml`: Poetry-specific configurations
- `CHANGELOG.md`: Version history and release notes
- `VERSIONING`: Version numbering and release guidelines
- `.gitignore`: Git ignore patterns for build artifacts and local files
- `justfile`: Command runner for common development tasks
- `LICENCE`: Project licence information (MIT))

### 4.2 Source Directory (src/)
The `src/` directory contains the primary ontology content:

```asciidoc
├── src
│   ├── README.md
│   ├── competencies
│   │   └── competency.sparql
│   ├── data
│   │   └── data.ttl
│   └── ontology
│       ├── ontology.trig
│       └── ontology.ttl
```
**Note: the template provides example files for demonstration purposes.**

**Competencies**
Contains SPARQL queries that define competency questions for the ontology.

**Ontology**
Contains the primary ontology files in Turtle and TriG formats. It is recommended that ontology files are defined using the turtle format. If needed, other RDF formats can be generated and stored in the `build/` directory.

**Data**
Includes sample data files that can be used for testing and demonstration purposes. Again, data samples should use the turtle format.

### 4.3 Build Directory (build/)

The `build/` directory contains build outputs and artifacts:

#### 4.3.1 Build Components

The `build/` directory is intended to be used as a staging area for build artifacts and outputs suitable for packaging a release of the ontology and its documentation.

- **Documentation**: Generated documentation files in various formats (e.g., HTML, PDF, Markdown).
- **Diagrams**: Ontology diagrams and visualizations in SVG and PNG formats.
- **Ontology Files**: Ontology files in RDF/Turtle format.

#### 4.3.2 Build Validation

**ToDo - implement validation checks tool and tests**

Before compiling an ontology build, the ontology tests and validation checks should be successfully completed. This includes:

- Syntax validation of ontology files
- Consistency checks
- Competency SPARQL query validation
- Data sample validation
- SHAPES validation
- IES Core compliance and consistency checks

#### 4.3.3 Build Compilation

As a minimum, an ontology build should contain:

- The ontology definitions in turtle format (`.ttl`) and any additional formats required for distribution or consumption.
- The ontology documentation in MarkDown format (`.md`) or other formats as needed (e.g. HTML, PDF).
- Ontology diagrams are generated from the `doc/diagrams/` directory and stored in the `build/docs/diagrams/` directory.

A build can be produced using the `ies-build` tool:
```bash
# Build the project diagrams in `.svg` and `.png` formats
poetry run ies-build build-diagrams

# Build the project documentation in MarkDown (.`md`) format
poetry run ies-build build-docs

# Build the project ontology in Turtle (`.ttl`) format
poetry run ies-build build-ontology

# Update the ontology metadata and version information
poetry run ies-build build-metadata
```

**Diagrams**

Diagrams are generated in `.svg` and `.png` formats in `build/docs/diagrams/` from the source files in `docs/diagrams/`. These can be referenced in documentation source files.

**Documentation**

Documentation is generated in MarkDown format (`.md`) and can be converted to other formats as needed, including HTML, PDF, and MS Word.

**Ontology Files**

Ontology files must be represented in RDF/Turtle format. Additionally, other formats such as RDF/XML, JSON-LD, and N-Triples can be generated as needed.

### 4.4 Test Directory (tests/)
**TBD - the test framework is not yet implemented**

The `tests/` directory contains the testing framework:

#### 4.4.1 Test Structure
**TBD** - The test directory structure includes:
- `unit/` - Ontology unit tests
- `integration/` - Ontology integration tests
- `validation/` - Ontology validation and consistency checks
- `test-data/` - Sample data files for testing

#### 4.4.2 Unit Tests
**TBD** - Unit tests are used to validate individual ontology components, such as class hierarchies, properties, and terms. These tests are typically written in SPARQL and can be executed using a test runner.

Key test areas include:
- Class hierarchy validation
- Property domain/range constraints
- Term definitions and annotations
- Individual assertions

#### 4.4.3 Integration Tests
Integration tests validate the interaction between ontology components, including class relationships, property usage, and query results. These tests are more comprehensive and may involve multiple ontology components as well as integration with IES Core.

Test coverage includes:
- IES Core compatibility
- Cross-module dependencies
- Import chain validation
- (Optional) query performance

#### 4.4.4 Validation Tests
**TBD** - Validation tests ensure the ontology adheres to defined standards and best practices:

1. Structural Validation
   - Syntax correctness
   - URI conventions
   - Naming patterns
   - Annotation completeness

2. Semantic Validation
   - Logical consistency
   - Classification results
   - Subsumption hierarchies
   - Property restrictions

3. Documentation Validation
   - Required annotations
   - Term definitions
   - Usage examples
   - Version metadata

#### 4.4.5 Test Data Management
**TBD** - Test data is used to validate ontology queries and ensure consistent results. This data can be stored in the `tests/test-data/` directory.

Data organization:
- Sample instances
- Query test cases
- Validation scenarios
- Performance benchmarks

Best practices:
- Version control test data
- Document data generation methods
- Maintain data-ontology alignment
- Regular data refresh cycles

#### 4.4.6 Validation Framework
**TBD** - The ontology validation framework will include:

Planned components:
- Automated test runners
- Continuous integration hooks
- Coverage reporting
- Performance metrics
- Quality assurance tools

Future enhancements:
- Automated regression testing
- Cross-repository validation
- Semantic diff tools
- Impact analysis

### 4.5 Documentation Directory (docs/)
The `docs/` directory maintains all project documentation using Markdown as the primary source format:

#### 4.5.1 Documentation Structure
- `getting-started/` - Setup and initial usage guides
- `user-guides/` - Detailed usage documentation
- `reference/` - API and term reference documentation
- `diagrams/` - Source files for documentation diagrams
- `examples/` - Code examples and usage patterns
- `releases/` - Release notes and version history

#### 4.5.2 Required Documentation
Each ontology repository must maintain:

1. Core Documentation
   - Installation and setup guide
   - Basic usage documentation
   - Term definitions and examples
   - Contributing guidelines
   - Licence information

2. Technical Documentation
   - Query examples
   - Integration patterns
   - Extension guidelines

3. Release Documentation
   - Version history
   - Migration guides
   - Breaking changes
   - Deprecation notices

#### 4.5.3 Diagram Guidelines
Diagrams are managed using source files that are version controlled:

1. Mermaid Diagrams (`.mmd`)
   - Class hierarchies
   - Flow diagrams
   - Sequence diagrams
   - State diagrams

2. GraphViz Diagrams (`.dot`)
   - Ontology structure visualization
   - Dependency graphs
   - Relationship networks

3. Build Process
   ```bash
   # Generate SVG and PNG files from diagram sources
   poetry run ies-build build-diagrams
   ```
   - Source files committed to version control
   - Generated files stored in `build/docs/diagrams/`

#### 4.5.4 Documentation Formats
Documentation is generally maintained in MarkDown format supporting multiple output types:

1. Source Format
   - Markdown (`.md`) as primary format
   - Plain text when appropriate
   - Diagram source files (`.mmd`, `.dot`)

2. Generated Formats
   - HTML (`.html`) for web viewing
   - PDF (`.pdf`) for distribution
   - Word (`.docx`) when required
   - AsciiDoc (`.adoc`) for specific use cases

3. Build Process
   ```bash
   # Generate documentation in all required formats
   poetry run ies-build build-docs
   ```
   - Documentation built for reviews and releases
   - Format conversion automated
   - Consistent styling maintained
   - Version numbers included

## 5 Import Management
Management of ontology imports and dependencies:

### 5.1 Import Components (`imports/`)
1. Catalog.xml Configuration
- Import mappings
- URI resolution
- Local references
- Cache configuration

2. Dependency Management
- Version constraints
- Compatibility checks
- Update procedures
- Conflict resolution

### 5.2 Git Submodule Usage
The IES Core ontology is included in each domain ontology as a Git submodule, appearing as `core/`. This ensures consistency and version control across the ontology family. 

To update the submodule (e.g., after a new release of IES Core):
```bash
# Update the submodule to the latest version
git submodule update --remote
```

## Appendices
### A. Glossary

**Branch Protection Rules**  
Settings that enforce certain conditions before changes can be merged into specified branches, such as requiring review approvals or passing status checks.

**Catalog.xml**  
A configuration file that manages ontology import mappings and URI resolutions for local and remote ontology references.

**Competency Questions**  
SPARQL queries that define what questions the ontology should be able to answer, used to validate ontology functionality and coverage.

**Domain Ontology**  
An ontology that models concepts, relationships, and constraints specific to a particular field or area of knowledge (e.g., IES Building, IES Security).

**Feature Branch**  
A temporary branch (`feature/*`) created to develop new functionality isolated from the main ontology base.

**GitHub Project Board**  
A project management tool that organizes and tracks issues, pull requests, and other work items using customizable views and automation.

**IES Core**  
The foundational upper ontology that provides common concepts, patterns, and relationships used across all IES domain ontologies.

**IES Tools**  
A collection of command-line utilities and scripts for managing ontology development, testing, and deployment tasks.

**Integration Tests**  
Tests that verify the correct interaction between different ontology components and their integration with IES Core.

**Organization PAT**  
Personal Access Token configured at the organization level, used for automated workflows and cross-repository operations.

**Pull Request (PR)**  
A proposed set of changes to an ontology repository that follows defined workflows and requires review before merging.

**Release Candidate (RC)**  
A version of the ontology that is potentially ready for release and undergoes final testing and validation.

**SPARQL**  
A semantic query language used to retrieve and manipulate data stored in ontology formats.

**Submodule**  
A Git feature used to include IES Core within domain ontology repositories, allowing version control of the dependency.

**Unit Tests**  
Tests that validate individual ontology components such as class hierarchies, properties, and terms.

**Upper Ontology**  
An ontology (like IES Core) that describes general concepts that are the same across all domains.

**Validation Framework**  
A set of tools and processes that verify ontology correctness, consistency, and compliance with standards.

**Workflow**  
An automated process defined in GitHub Actions that handles tasks like pull request validation, testing, and deployment.

### B. Workflow Examples
**TBD**

### C. Troubleshooting Guide

#### C.1 Environment Setup Issues

**Problem: Poetry installation fails**
```bash
# Common error message:
ERROR: Poetry command not found
```
Solution:
1. Ensure Python 3.9 or higher is installed: `python --version`
2. Try reinstalling Poetry: `curl -sSL https://install.python-poetry.org | python3 -`
3. Verify PATH includes Poetry's bin directory

**Problem: Git submodule initialization fails**
```bash
# Common error message:
fatal: No url found for submodule path 'core' in .gitmodules
```
Solution:
1. Check `.gitmodules` file exists and contains correct URLs
2. Reinitialize submodules:
   ```bash
   git submodule init
   git submodule update
   ```
3. If problems persist, remove and re-add the submodule

#### C.2 Workflow Issues

**Problem: Pull request targets wrong branch**
```bash
# Error message from PR workflow:
⚠️ Invalid target branch
```
Solution:
1. Check branch naming follows conventions:
   - `feature/*` → `develop`
   - `bugfix/*` → `develop`
   - `hotfix/*` → `main`
2. Close PR and create new one with correct target
3. Or update PR target branch if possible

**Problem: Missing required labels**
Solution:
1. Run repository setup tool: `poetry run gh-tools setup-repo`
2. Verify organization PAT has correct permissions
3. Manually sync labels from template repository

#### C.3 Build Issues

**Problem: Diagram generation fails**
```bash
# Error when running build-diagrams:
ERROR: Could not generate diagram
```
Solution:
1. Verify Mermaid/GraphViz syntax in source files
2. Ensure all required tools are installed:
   ```bash
   npm install -g @mermaid-js/mermaid-cli
   apt-get install graphviz
   ```
3. Check diagram source file permissions

**Problem: Documentation build fails**
```bash
# Error when running build-docs:
ERROR: Could not generate documentation
```
Solution:
1. Check Markdown syntax in source files
2. Verify all referenced files exist
3. Ensure sufficient disk space for build

#### C.4 Testing Issues

**Problem: Test framework initialization fails**
Solution:
1. Verify Python environment: `poetry env info`
2. Check test dependencies are installed
3. Ensure test data files are present

**Problem: SPARQL queries fail**
Solution:
1. Validate query syntax
2. Check ontology file loading
3. Verify test data is properly formatted

#### C.5 Git and GitHub Issues

**Problem: Unable to push changes**
```bash
# Error message:
remote: error: GH006: Protected branch update failed
```
Solution:
1. Verify branch protection rules
2. Check if PR is required
3. Ensure required status checks pass

**Problem: GitHub Actions workflow fails**
Solution:
1. Check workflow logs for specific errors
2. Verify secret availability and permissions
3. Ensure workflow file syntax is correct

#### C.6 Version Control Issues

**Problem: Merge conflicts with IES Core**
Solution:
1. Update submodule to latest version:
   ```bash
   git submodule update --remote
   ```
2. Resolve conflicts in ontology files
3. Run validation tests after resolution

**Problem: Branch out of sync**
Solution:
1. Update branch with latest changes:
   ```bash
   git fetch origin
   git rebase origin/develop
   ```
2. Resolve any conflicts
3. Force push if necessary (only for feature branches)

#### C.7 Getting Help

If you encounter issues not covered here:
1. Check the latest documentation in the template repository
2. Submit an issue in the template repository
3. Contact the IES ontology team for support
4. Include relevant error messages and environment details when reporting issues

[ont-template]: https://github.com/IES-Org/ies-ontology-template
[commitizen]: ../docs/COMMITIZEN.md
[create-ontology]: https://github.com/Acme-Ontologies/ies-ontology-template/actions/workflows/create-ontology-repo.yml
[pr-checks]: ../.github/workflows/pr-checks.yml
[repo-readme]: ../README.md
[sync-tools]: ../.github/workflows/sync-ies-tools.yml
