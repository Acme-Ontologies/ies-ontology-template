"""Build tools for generating documentation and ontology release files."""

import logging
import os
import subprocess
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Optional

import click

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DiagramType(str, Enum):
    """Supported diagram types."""
    MERMAID = "mermaid"
    GRAPHVIZ = "graphviz"
    UNKNOWN = "unknown"


@dataclass
class DiagramFile:
    """Represents a diagram file with source and output information."""
    source: Path
    type: DiagramType
    name: str


class DiagramBuilder:
    """Handles the generation of diagrams from source files."""

    EXTENSIONS = {
        '.mmd': DiagramType.MERMAID,
        '.mermaid': DiagramType.MERMAID,
        '.dot': DiagramType.GRAPHVIZ
    }
    OUTPUT_FORMATS = ['.svg', '.png']

    def __init__(self, root_dir: Path):
        """Initialize with project root directory."""
        self.root_dir = Path(root_dir)
        self.docs_diagrams = self.root_dir / 'docs' / 'diagrams'
        self.build_diagrams = self.root_dir / 'build' / 'docs' / 'diagrams'

    def verify_tools(self) -> None:
        """Verify required tools are available."""
        # Check Mermaid CLI
        try:
            subprocess.run(['mmdc', '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.warning("mermaid-cli not found. Install with: npm install -g @mermaid-js/mermaid-cli")

        # Check Graphviz
        try:
            subprocess.run(['dot', '-V'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.warning("Graphviz not found. Install with package manager (apt/brew install graphviz)")

    def setup_build_directory(self) -> None:
        """Create build directory if it doesn't exist."""
        try:
            self.build_diagrams.mkdir(parents=True, exist_ok=True)
            logger.info(f"Build directory ensured at {self.build_diagrams}")
        except Exception as e:
            raise click.ClickException(f"Failed to create build directory: {e}")

    def find_diagram_files(self) -> List[DiagramFile]:
        """Find all diagram source files in docs/diagrams directory."""
        if not self.docs_diagrams.exists():
            logger.warning(f"Diagrams directory not found: {self.docs_diagrams}")
            return []

        diagram_files = []
        for source in self.docs_diagrams.iterdir():
            if source.suffix in self.EXTENSIONS:
                diagram_files.append(
                    DiagramFile(
                        source=source,
                        type=self.EXTENSIONS[source.suffix],
                        name=source.stem
                    )
                )

        logger.info(f"Found {len(diagram_files)} diagram source files")
        return diagram_files

    def generate_mermaid_diagram(self, source: Path, output: Path) -> bool:
        """Generate diagram from Mermaid source file."""
        try:
            result = subprocess.run(
                [
                    'mmdc',
                    '-i', str(source),
                    '-o', str(output),
                    '-b', 'transparent'
                ],
                capture_output=True,
                check=True
            )
            logger.info(f"Generated {output} from {source}")
            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to generate Mermaid diagram: {e.stderr}")
            return False

    def generate_graphviz_diagram(self, source: Path, output: Path) -> bool:
        """Generate diagram from Graphviz source file."""
        try:
            fmt = output.suffix[1:]  # Remove the dot
            result = subprocess.run(
                [
                    'dot',
                    '-T', fmt,
                    '-o', str(output),
                    str(source)
                ],
                capture_output=True,
                check=True
            )
            logger.info(f"Generated {output} from {source}")
            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to generate Graphviz diagram: {e.stderr}")
            return False

    def generate_all_diagrams(self) -> None:
        """Generate all diagrams in specified output formats from docs/diagrams/."""
        try:
            self.verify_tools()
            self.setup_build_directory()

            source_files = self.find_diagram_files()
            if not source_files:
                logger.warning("No diagram files found to process")
                return

            success_count = 0
            total_files = len(source_files) * len(self.OUTPUT_FORMATS)

            for diagram in source_files:
                for output_ext in self.OUTPUT_FORMATS:
                    output = self.build_diagrams / f"{diagram.name}{output_ext}"

                    if diagram.type == DiagramType.MERMAID:
                        if self.generate_mermaid_diagram(diagram.source, output):
                            success_count += 1
                    elif diagram.type == DiagramType.GRAPHVIZ:
                        if self.generate_graphviz_diagram(diagram.source, output):
                            success_count += 1

            if success_count < total_files:
                logger.warning(
                    f"Generated {success_count} out of {total_files} diagram files"
                )
            else:
                logger.info(f"Successfully generated all {total_files} diagram files")

        except Exception as e:
            raise click.ClickException(f"Diagram generation failed: {e}")


@click.group()
def cli():
    """Build tools for documentation and ontology generation."""
    pass


@cli.command()
@click.option(
    '--docs-dir',
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    default=Path('docs'),
    help="Path to the docs directory containing diagrams/ subdirectory"
)
def build_diagrams(docs_dir: Path):
    """Generate diagrams from source files in docs/diagrams/."""
    try:
        # Check for diagrams subdirectory
        diagrams_dir = docs_dir / 'diagrams'
        if not diagrams_dir.exists():
            raise click.ClickException(
                f"Diagrams directory not found at {diagrams_dir}. "
                "Ensure you have a docs/diagrams/ directory with source files."
            )

        click.echo("🎨 Starting diagram generation...")
        builder = DiagramBuilder(docs_dir.parent)
        builder.generate_all_diagrams()
        click.echo("✨ Diagram generation completed")

    except click.ClickException as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        raise click.Abort()


if __name__ == "__main__":
    cli()
