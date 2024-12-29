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

### License Terms
The IES Ontology family is released under the MIT License, chosen for its permissive terms and broad compatibility. This allows:
- Commercial use
- Modification and distribution
- Private use
- Sublicensing

### Copyright
- UK Crown Copyright applies to all ontology files, code, and documentation.

## 1.4. Project Management

### Version Control
- Semantic versioning (MAJOR.MINOR.PATCH)
- Version tracked in VERSION file
- Changes documented in CHANGELOG.md
- Git tags for release versions

### Change Management
The CHANGELOG.md file tracks:
- Added features and concepts
- Modified relationships and properties
- Deprecated terms
- Breaking changes
- Bug fixes

### Dependencies
Managed through:
- catalog.xml for ontology imports
- imports/dependencies.txt for explicit dependency listing
- Git submodules for IES Core integration

### Project Tracking
Each repository includes:
- GitHub Project board for issue/PR tracking
- Milestone management (in Jira)
- Label system for categorization of issues and PRs
- Automated workflow integration

This infrastructure ensures consistent development practices and maintains high quality across the entire ontology family while enabling efficient collaboration among team members.

# 2. GitHub Organization Setup

## 2.1. IES-Org Configuration

### Team Structure
The IES organization consists of a single team with the following roles:
- 4 Ontology Developers
- 1 Project Manager
- 2 Reviewers
- 2 Customer/Client Representative

### Permission Requirements
- Team members require read/write access to:
  - Repository contents
  - Issues
  - Pull requests
  - Project boards

### GitHub Plan Requirements
A GitHub Team plan is required for:
- Supporting the organization's collaborator count
- Enabling Organization PAT usage on private repositories
- Managing private repositories for the ontology family

## 2.2. Access Management

### Personal Access Tokens (PATs)
- The `ACME-ONTOLOGIES-PAT` is the primary token for automation
- It must be configured as an organization-level secret with the following permissions:
  - `repository access` (read/write access to all repositories owned by the organization)
  - `organization` (Read and Write access to organization actions variables, organization projects, and organization secrets)
  - `repository permissions`
    - `read` (Read access to all repository metadata)
    - `read/write` (Read and Write access to actions, actions variables, administration, code, pull requests, and workflows)

### Organization Secrets
Required organization-level secrets:
- `ACME-ONTOLOGIES-PAT`: Used for cross-repository operations and automation workflows

### Repository Configuration
New repositories are created from the [IES Ontology Repository Template][ont-template] using the [create-ontology-repo.yml][create-ontology]. Each repository is configured with:
- standardised repo labels for issue tracking
- A set of GitHub workflows for common development tasks
- IES Tools for local development and automation
- IES Core ontology as a Git submodule
- A dedicated GitHub Project for issue and PR tracking
- `PROJECT_ID` configured as a repository-level variable
- Additional repository-specific secrets may be added as needed

### Environment Variables
Currently, no environment-specific variables are required beyond the repository-level configurations.

## 2.3. Repository Template

### Template Customization
Repository setup is primarily automated through:
1. The [create-ontology-repo.yml][create-ontology] workflow
2. The `poetry run gh-tools setup-repo` command, which initializes the repository with standard configurations and checks for required CLI tools
3. Manual updates required:
   - Repository README.md to reflect domain ontology name
   - Any domain-specific documentation

### Branch Configuration
- Default branch: `main`
- Release Candidate branch: `rc`
- Development branch: `develop`
- Feature branches: `feature/*`
- Bugfix branches: `bugfix/*`
- Hotfix branches: `hotfix/*`
- Branch protection rules and validation checks are yet to be developed

![IES Branch Flows](../build/docs/diagrams/branch-flows.svg)

### Development Flow
#### Feature and Regular Bugfix Flow
1. All feature development and regular bug fixes occur in `feature/*` and `bugfix/*` branches
2. Ontology developer pull requests target the `develop` branch
3. QA reviewers approve PRs before merging to `develop`
4. QA Reviewer pull requests target the `rc` branch
5. QA Reviewer approves PRs before merging to `rc`
6. Customer/client reviews the release candidate and approves PR to `main`
7. IES TGG reviews and approves release PRs before final merge to `main`
8. Changes are backported to `develop` after merging to `main`

#### Hotfix Flow
1. Critical fixes that can't wait for the regular release cycle are created in `hotfix/*` branches
2. Hotfix pull requests target the `main` branch directly
3. Customer/client must review and approve hotfix PRs
4. IES TGG performs final review before merging to `main`
5. After merge to `main`, changes should be backported to `develop` to maintain consistency

### Repository Policies
- No organization-wide policies are currently implemented
- Repository-specific policies and rules will be developed as needed
- Future considerations may include:
  - Branch protection rules
  - Required status checks
  - Required review processes
  - Automated validation requirements

### Template Maintenance
- Template repository serves as the source of truth for the ontolofy repo structure, IES tools and automation workflows
- Changes to template structure should be managed through:
  - Pull requests to template repository
  - [Synchronization workflow][sync-tools] to propagate workflow and tool changes to ontology repositories
  - Version control of template components

Clearly, some changes to the template structure, workflows, or GitHub configurations may be required as the ontology family evolves. These changes should be managed through the template repository, but may need to be manually propagated to ontology repos to avoid overwriting local customisations.

## 3. Development Infrastructure
### 3.1 Repository Creation and Setup
#### 3.1.1 Create Ontology Repository Workflow
The [create-ontology-repo.yml][create-ont] workflow automates the initialization of new ontology repositories, ensuring consistency across the family of ontologies. This workflow:

1. Creates a new repository from the template
2. Configures basic repository settings
3. Sets up the initial directory structure
4. Establishes required GitHub configurations, including a project board

**Key Configuration Steps:**
- Repository naming convention enforcement
- Basic metadata setup (description, topics, visibility)
- Initial branch creation and protection
- Documentation template population
- IES Tools installation and setup

#### 3.1.2 Jira and GitHub Project Boards
Overall ontology development is managed in jira that is integrated with GitHub project boards (TBD - see below):
- Jira project setup
- Sprint planning board
- Backlog management
- Release tracking
- Bug tracking

Additionally, each repository maintains a GitHub project board structure that integrates with the organizational workflow:

- Issue creation
- Pull Request (PR) management
- Release tracking and versioning
- Bug tracking

#### 3.1.3 Ontology repository set-up
After creation from the template, each ontology repository is configured with the following standard settings:
- Standard labels are automatically configured for:
- Issue types (bug, feature, enhancement)
- Priority levels
- Development stages
- Release tracking
- Documentation needs

This is applied using the `poetry run gh-tools setup-repo` command, which also checks for required CLI tools and sets up the repository for development (see the repository [README.md][repo-readme].

#### 3.1.4 Branch Protection Rules
TBD - The following branch protection rules are implemented:

- Main branch:
  - Requires pull request reviews by a customer or IES TGG member
  - Requires status checks to pass
  - No direct pushes allowed (other than approved `Hotfix/*` branches)
  
- Release candidate (rc) branch:
  - Similar protections to main
  - Additional deployment checks
  
- Develop branch:
  - Requires QA review
  - Automated tests must pass

### 3.2. GitHub Projects Integration
- Project board structure
- Issue tracking
- PR management
- Automation rules

### 3.3. Common Tools and Workflows
- ies-tools overview
- GitHub workflow automation
- Tool synchronization process
- Local development setup

## 4. Development Process
### 4.1. Branch Flow Strategy
- Branch types and purposes
- Branch naming conventions
- Branch lifetime management
- Branch protection rules

### 4.2. Development Workflow
- Feature development process
- Bug fix process
- Hotfix process
- Code review requirements
- Testing requirements

### 4.3. Quality Assurance
- QA review process
- Validation requirements
- Testing guidelines
- Documentation requirements

### 4.4. Release Management
- Release candidate process
- Version tagging
- Release notes
- Distribution process

## 5. Repository Structure
### 5.1. Source Directory (src/)
- Ontology file organization
- Competency queries
- Sample data
- Delta tracking

### 5.2. Build Directory (build/)
- Build process
- Output formats
- Documentation generation
- Release artifacts

### 5.3. Test Directory (tests/)
- Test organization
- Test types
- Test data management
- Validation framework

### 5.4. Documentation Directory (docs/)
- Documentation structure
- Required documentation
- Diagram guidelines
- Documentation formats

### 5.5. Import Management
- Catalog.xml configuration
- Dependency management
- Git submodule usage
- Version compatibility

## 6. Tools and Automation
### 6.1. Common Workflows
- Workflow types
- Trigger events
- Configuration options
- Error handling

### 6.2. Tool Maintenance
- Update process
- Synchronization workflow
- Version management
- Backward compatibility

### 6.3. Local Development Tools
- Required software
- Configuration
- Usage guidelines
- Troubleshooting

## 7. Best Practices and Guidelines
### 7.1. Development Standards
- Coding conventions
- Documentation requirements
- Testing requirements
- Review process

### 7.2. Quality Control
- Validation checks
- Review checklists
- Common pitfalls
- Resolution procedures

### 7.3. Maintenance
- Regular maintenance tasks
- Update procedures
- Deprecation process
- Migration guidelines

## Appendices
### A. Glossary
### B. Reference Configurations
### C. Workflow Examples
### D. Troubleshooting Guide
### E. Quick Reference Guides

[ont-template]: https://github.com/IES-Org/ies-ontology-template
[create-ontology]: https://github.com/Acme-Ontologies/ies-ontology-template/actions/workflows/create-ontology-repo.yml
[repo-readme]: ../README.md
[sync-tools]: ../.github/workflows/sync-ies-tools.yml
