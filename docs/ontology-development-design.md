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

### Copyright Management
- Copyright notices maintained in each ontology file
- Clear attribution requirements
- Year and copyright holder information
- Contribution guidelines

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
- Milestone management
- Label system for categorization
- Automated workflow integration

This infrastructure ensures consistent development practices and maintains high quality across the entire ontology family while enabling efficient collaboration among team members.

## 2. GitHub Organization Setup
### 2.1. IES-Org Configuration
- Organization structure
- Teams and roles
- Permission levels
- Required GitHub plan features

### 2.2. Access Management
- PAT configuration (IES-ORG-PAT)
- Organization secrets
- Repository secrets
- Environment variables

### 2.3. Repository Template
- Standard repository structure
- Directory organization
- Configuration files
- Required files and their purposes

## 3. Development Infrastructure
### 3.1. Repository Creation and Setup
- Using create-ontology-repo.yml
- Repository initialization process
- Project board setup
- Label configuration
- Branch protection rules

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