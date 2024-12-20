# This is a common justfile shared across all IES projects and is designed to be imported into project-specific justfiles.

# Create a new feature issue and branch
feature:
    #!/usr/bin/env sh
    read -p "Feature title: " title
    issue_number=$(gh issue create -l enhancement --title "[FEATURE] $title" --json number --jq .number)
    branch_name="feature/$issue_number-$(echo $title | tr '[:upper:]' '[:lower:]' | tr ' ' '-')"
    git checkout -b $branch_name
    git push -u origin $branch_name

# Validate ontology files
validate:
    @echo "Validating ontology files..."
    gh workflow run ontology-validation.yml

# Run all tests
# ToDo - this is an example only, implementation needed
test: validate
    @echo "Running SPARQL tests..."
    # Run unit tests
    for file in tests/unit/**/*.sparql; do \
        sparql --data src/ontology/ontology.ttl --query "$file"; \
    done
    # Run integration tests
    for file in tests/integration/**/*.sparql; do \
        sparql --data src/ontology/ontology.ttl --query "$file"; \
    done

# Build documentation
# ToDo - this is an example only, implementation needed
docs:
    @echo "Building documentation..."
    gh workflow run doc-build.yml

# Import dependencies listed in imports/dependencies.txt
# ToDo - this is an example only, implementation needed
import-deps:
    @echo "Importing dependencies..."
    cat imports/dependencies.txt | while read dep; do \
        curl -o "imports/$(basename $dep)" "$dep"; \
    done

# Create a new release
# ToDo - this is an example only, implementation needed
release version:
    @echo "Creating release {{version}}..."
    echo "{{version}}" > VERSION
    git add VERSION
    git commit -m "Release version {{version}}"
    git tag -a v{{version}} -m "Release version {{version}}"
    git push origin v{{version}}

# Clean generated files
# ToDo - this is an example only, implementation needed
clean:
    rm -f imports/catalog-v001.xml
    rm -f **/*.bak
