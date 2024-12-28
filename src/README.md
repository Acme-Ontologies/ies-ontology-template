# Source Directory Documentation

This directory contains the core ontology files and associated resources for the IES Domain Ontologies project.

## Directory Structure

- `./ontology/` - Contains the main ontology files
  - `ontology.ttl` - Primary ontology definition in Turtle format
  - `ontology.trig` - A 'delta' file showing the differences between the current version and the last one (when generated)
- `./competencies/` - SPARQL queries defining competency questions
- `./data/` - Instance data and examples

## Ontology Development Guidelines

### File Organization

1. Keep ontology definitions in `ontology.ttl` and use `data.ttl` for instance data
2. Create new competency questions in the `competencies/` directory using SPARQL
3. Consider creating sub-files for modular ontology development following separation of concerns (e.g., `organization.ttl`, `process.ttl`, `product.ttl`). This helps manage complexity while maintaining semantic cohesion within the domain

### Naming Conventions

- Use CamelCase for class names (e.g., `domain:MyDomainEntity`)
- Use camelCase for property names (e.g., `domain:hasRelation`)
- Prefix all terms with the domain namespace
- Use descriptive labels in English (GB) with appropriate language tags (e.g., `rdfs:label "Manufacturing Process"@en-GB`)
- Form class names using singular nouns or noun phrases that clearly identify the concept (e.g., `domain:ManufacturingProcess`, `domain:QualitySpecification`, `domain:ProductComponent`)

### Best Practices

- Document all terms with `rdfs:label` and `rdfs:comment`
- Include complete metadata for the ontology
- Import the IES Core ontology using `owl:imports`
- Define clear class hierarchies using `rdfs:subClassOf`
- Specify domains and ranges for all properties
- Keep instance data separate from ontology definitions
- Follow the principle of minimal ontological commitment

### Quality Control

1. Test ontology changes against competency questions
2. Validate against shapes in `/tests/validation/shapes/`
3. Ensure all terms align with the IES Core ontology
4. Document significant changes in the root [CHANGELOG.md][CHANGELOG]

### Development Workflow

1. Create a feature branch for new developments
2. Run validation tests before committing
3. Follow the contribution guidelines in [../docs/CONTRIBUTING.md][CONTRIBUTING]
4. Submit pull requests for review

## Additional Resources

- See [../docs/ontology-development-design.md][docs-design] for detailed design principles
- Review [../tests/README.md][tests-readme] for testing procedures
- Check [../docs/requirements/requirements.md][reqs] for domain requirements

[CHANGELOG]: ../CHANGELOG.md
[CONTRIBUTING]: ../docs/CONTRIBUTING.md
[docs-design]: ../docs/ontology-development-design.md
[reqs]: ../docs/requirements/requirements.md
[tests-readme]: ../tests/README.md