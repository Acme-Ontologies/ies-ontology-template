# IES Build Tools

This package provides build tools for IES Ontology development, including diagram generation and documentation building. It's part of the `ies-tools` package and integrates with the existing development workflow.

## Features

- Automatic diagram generation from source files
  - Mermaid (.mmd, .mermaid) diagrams
  - Graphviz (.dot) diagrams
  - Multiple output formats (SVG, PNG)
- Build directory management
- Comprehensive error handling and logging
- Integration with poetry and project workflow

## Prerequisites

The build tools require the following dependencies:

1. Python 3.9 or higher
2. Poetry for package management
3. Node.js and NPM:
   ```bash
   # Ubuntu/Debian
   curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
   sudo apt-get install -y nodejs

   # macOS
   brew install node

   # Windows
   winget install OpenJS.NodeJS
   # or
   choco install nodejs
   ```

4. Mermaid CLI (requires Node.js/NPM):
   ```bash
   npm install -g @mermaid-js/mermaid-cli
   ```

   To verify installation:
   ```bash
   node --version
   npm --version
   mmdc --version
   ```
4. Graphviz for DOT diagrams:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install graphviz

   # macOS
   brew install graphviz

   # Windows
   winget install graphviz
   # or
   choco install graphviz
   ```

## Installation

The build tools are part of the `ies-tools` package and are installed via poetry using the `pyproject.toml` configuration:

```bash
# In your ontology repository root directory
poetry install
```

This installs the `ies-build` command along with other `ies-tools` commands defined in `pyproject.toml`.

## Usage

### Command Line Interface

The build tools provide a CLI interface that should be run using poetry:

```bash
# Generate all diagrams from docs/diagrams/
poetry run ies-build build-diagrams

# Specify custom docs directory location
poetry run ies-build build-diagrams --docs-dir /path/to/docs

Note: The tool expects to find diagram source files in a 'diagrams/' subdirectory 
under the specified docs directory.
```

Note: All `ies-tools` commands must be run using `poetry run` to ensure they execute in the correct environment with all dependencies available.

### Directory Structure

The build tools expect the following directory structure:

```
ontology-repo/
├── docs/
│   └── diagrams/           # Source diagram files
│       ├── diagram1.mmd    # Mermaid diagram
│       └── diagram2.dot    # Graphviz diagram
└── build/
    └── docs/
        └── diagrams/       # Generated diagram files
            ├── diagram1.svg
            ├── diagram1.png
            ├── diagram2.svg
            └── diagram2.png
```

### Diagram Generation

1. **Mermaid Diagrams**
   - Place your Mermaid diagram files in `docs/diagrams/` with `.mmd` or `.mermaid` extension
   - Example Mermaid file:
     ```mermaid
     graph TD
         A[Start] --> B[Process]
         B --> C[End]
     ```

2. **Graphviz Diagrams**
   - Place your Graphviz DOT files in `docs/diagrams/` with `.dot` extension
   - Example DOT file:
     ```dot
     digraph G {
         rankdir=LR;
         A -> B;
         B -> C;
     }
     ```

The build process will:
1. Create the build directory if it doesn't exist
2. Generate both SVG and PNG versions of each diagram
3. Maintain the original filename with new extensions
4. Provide detailed logging of the process

### Error Handling

The build tools include comprehensive error handling:

- Missing dependencies are reported with installation instructions
- File access issues are reported with clear error messages
- Failed diagram generation is logged but doesn't stop the build process
- Summary of successful and failed generations is provided

## Development

### Adding New Build Features

To add new build features:

1. Create a new class in `build.py` for the feature
2. Add a new Click command to the CLI group
3. Update tests and documentation
4. Update `pyproject.toml` if new dependencies are required

### Running Tests

```bash
poetry run pytest tests/unit/test_build.py
```

## Troubleshooting

Common issues and solutions:

1. **Mermaid CLI not found**
   ```bash
   npm install -g @mermaid-js/mermaid-cli
   ```

2. **Graphviz not found**
   - Install using your system's package manager
   - Ensure `dot` command is available in your PATH

3. **Permission Issues**
   - Ensure you have write permissions in the build directory
   - Run with elevated privileges if necessary

4. **Build Directory Issues**
   - Check that the directory structure matches the expected layout
   - Ensure no processes have locked the output files

## Contributing

1. Navigate to the [GitHub IES Core repository][ies-core-repo]
2. Follow the standard development workflow
2. Add tests for new features
3. Update documentation as needed
4. Submit a PR for review

## License

This project is licensed under MIT - see the [LICENCE][LICENCE] file for details.

[ies-core-repo]: https://github.com/Acme-Ontologies/ies-core
[LICENCE]: ../../LICENSE
