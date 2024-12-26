# ToDo - replace [domain] with the actual domain name
# Contributing to IES [Domain] Ontology

## Getting Started
1. Clone locally from `main` branch of https://github.com/Acm-Ontologies/ies-[domain]-ontology
2. Install dependencies: `poetry install`
3. Setup repository: `poetry run gh-tools setup-repo`

## Development Workflow
- Create branch from `develop`:
  - `feature/*` for new features
  - `bugfix/*` for fixes
  - `hotfix/*` for urgent production fixes
- Write tests
- Update documentation
- Submit PR

## Branch Strategy
- `main`: Production
- `develop`: Integration from `feature/*` and `bugfix/*` branches
- `rc`: Release candidates following QA review od `develop` branch
- Feature branches: New development
- Bugfix branches: Issue fixes
- Hotfix branches: Urgent fixes that can / should be deployed immediately to `main` branch

## Commits
- Use conventional commits
- Reference issues
- Keep atomic

## Pull Requests
- Link issues
- Update tests
- Include documentation
- Add to CHANGELOG.md

## Testing
- Run tests: `just test`
- Add new test cases
- Ensure 100% coverage

## Documentation
- Update relevant docs
- Follow markdown style
- Keep diagrams current

## Release Process

### Feature Development
1. Create `feature/*` or `bugfix/*` branch from `develop`
2. Run validation suite
3. Create PR to merge into `develop`
4. QA review and merge (or iterate from step 1)
5. Update VERSION and CHANGELOG.md
6. Delete feature/bugfix branch
7. Tag release candidate

### Release
1. Create PR to merge `develop` into `rc`
2. IES TG review and merge (or iterate remedial actions)
3. Create PR to merge `rc` into `main`
4. IES TG review and merge
5. Update VERSION and CHANGELOG.md
6. Create GitHub release

## Questions?
Open an issue or contact maintainers
