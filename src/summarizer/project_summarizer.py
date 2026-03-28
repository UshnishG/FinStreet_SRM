"""
Project Summarizer for Resume.

Analyzes the repository structure, README, requirements, and source code
to generate a concise, resume-ready project description.
"""

import ast
import re
from pathlib import Path
from typing import Dict, List, Optional


# Mapping from package names to display-friendly names
_PACKAGE_DISPLAY_NAMES: Dict[str, str] = {
    "fyers-apiv3": "Fyers API v3",
    "pandas": "Pandas",
    "pandas_ta": "pandas-ta",
    "scikit-learn": "scikit-learn (Random Forest)",
    "python-dotenv": "python-dotenv",
}


class ProjectSummarizer:
    """Analyses a Python project and generates a resume-friendly summary."""

    def __init__(self, project_root: Optional[str] = None) -> None:
        if project_root is None:
            # Default to two levels above this file (repo root)
            self.project_root = Path(__file__).resolve().parent.parent.parent
        else:
            self.project_root = Path(project_root).resolve()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_project_name(self) -> str:
        """Return the project name from the README title or directory name."""
        readme = self._read_readme()
        if readme:
            match = re.search(r"^#\s+(.+)$", readme, re.MULTILINE)
            if match:
                # Strip emoji and leading/trailing whitespace
                title = re.sub(r"[^\w\s\-:/()]", "", match.group(1)).strip()
                return title
        return self.project_root.name

    def get_tech_stack(self) -> List[str]:
        """Return a list of technologies inferred from requirements.txt."""
        req_file = self.project_root / "requirements.txt"
        techs: List[str] = ["Python 3"]
        if req_file.exists():
            for raw_line in req_file.read_text().splitlines():
                line = raw_line.strip()
                if not line or line.startswith("#"):
                    continue
                # Strip version specifiers
                pkg = re.split(r"[=<>!;\[]", line)[0].strip()
                display = _PACKAGE_DISPLAY_NAMES.get(pkg, pkg)
                techs.append(display)
        return techs

    def get_module_descriptions(self) -> Dict[str, str]:
        """
        Return a mapping of module directory → one-line description
        extracted from the module's docstrings or README feature sections.
        """
        descriptions: Dict[str, str] = {}
        src_dir = self.project_root / "src"
        if not src_dir.exists():
            return descriptions

        for module_dir in sorted(src_dir.iterdir()):
            if not module_dir.is_dir() or module_dir.name.startswith("_"):
                continue
            desc = self._describe_module(module_dir)
            if desc:
                descriptions[module_dir.name] = desc
        return descriptions

    def get_quantitative_metrics(self) -> List[str]:
        """
        Return quantitative achievements scraped from the README
        (output example section) and source code constants.
        """
        metrics: List[str] = []
        readme = self._read_readme()
        if readme:
            # Scrape the output example block for numeric results
            example_match = re.search(
                r"Output Example.*?```(.*?)```", readme, re.DOTALL | re.IGNORECASE
            )
            if example_match:
                block = example_match.group(1)
                for pattern, label in [
                    (r"Model Accuracy:\s*([\d.]+%)", "Model Accuracy: {}"),
                    (r"Net Profit:\s*[₹]?([\d.]+)", "Net Profit: ₹{}"),
                    (r"Total Return:\s*([\d.]+%)", "Total Return: {}"),
                    (r"Sharpe Ratio:\s*([\d.]+)", "Sharpe Ratio: {}"),
                ]:
                    m = re.search(pattern, block)
                    if m:
                        metrics.append(label.format(m.group(1)))

        # Search all Python files in the project for initial_capital constants
        for py_file in self.project_root.rglob("*.py"):
            try:
                src = py_file.read_text(encoding="utf-8")
                cap_match = re.search(r"initial_capital\s*=\s*(\d+)", src)
                if cap_match:
                    val = int(cap_match.group(1))
                    metrics.append(f"Simulated on ₹{val:,} initial capital")
                    break  # Use the first match found
            except OSError:
                continue

        return metrics

    def get_resume_bullets(self) -> List[str]:
        """
        Return a list of action-oriented bullet points suitable for a resume.

        For known module names, curated action-oriented descriptions are used.
        For any additional modules not in the known set, a description is
        derived from module docstrings instead.
        """
        _known_bullets: Dict[str, str] = {
            "api": "Integrated Fyers APIv3 for OAuth2 authentication and live intraday order execution",
            "data": "Built a data-loading pipeline that fetches, cleans, and indexes OHLCV candlestick data",
            "features": "Engineered technical features (SMA-10, SMA-20, RSI-14) using pandas-ta for ML input",
            "models": "Trained and deployed a Random Forest Classifier (100 estimators) for next-day price-movement prediction",
            "strategy": "Designed a signal-generation strategy with a tuned confidence threshold (>30.5%) for Buy/Sell decisions",
            "backtest": "Implemented backtesting engine computing ROI, Sharpe Ratio, and model accuracy over historical data",
        }

        bullets: List[str] = []
        src_dir = self.project_root / "src"
        if not src_dir.exists():
            return bullets

        for module_dir in sorted(src_dir.iterdir()):
            name = module_dir.name
            if not module_dir.is_dir() or name.startswith("_"):
                continue
            if name in _known_bullets:
                # Use the curated action-oriented description for known modules
                bullets.append(_known_bullets[name])
            else:
                # For new/unknown modules derive description from docstrings
                doc_desc = self._describe_module(module_dir)
                if doc_desc:
                    bullets.append(doc_desc)

        return bullets

    def generate_summary(self) -> Dict:
        """Return the full structured summary as a dictionary."""
        return {
            "name": self.get_project_name(),
            "tech_stack": self.get_tech_stack(),
            "module_descriptions": self.get_module_descriptions(),
            "quantitative_metrics": self.get_quantitative_metrics(),
            "resume_bullets": self.get_resume_bullets(),
        }

    def format_plain_text(self) -> str:
        """Return a plain-text resume block."""
        s = self.generate_summary()
        lines: List[str] = []

        lines.append(s["name"])
        lines.append("-" * len(s["name"]))
        lines.append("")

        lines.append("Responsibilities / Achievements:")
        for bullet in s["resume_bullets"]:
            lines.append(f"  • {bullet}")
        lines.append("")

        if s["quantitative_metrics"]:
            lines.append("Key Metrics:")
            for metric in s["quantitative_metrics"]:
                lines.append(f"  • {metric}")
            lines.append("")

        lines.append("Technologies: " + ", ".join(s["tech_stack"]))

        return "\n".join(lines)

    def format_markdown(self) -> str:
        """Return a Markdown-formatted resume block."""
        s = self.generate_summary()
        lines: List[str] = []

        lines.append(f"### {s['name']}")
        lines.append("")

        lines.append("**Responsibilities / Achievements:**")
        for bullet in s["resume_bullets"]:
            lines.append(f"- {bullet}")
        lines.append("")

        if s["quantitative_metrics"]:
            lines.append("**Key Metrics:**")
            for metric in s["quantitative_metrics"]:
                lines.append(f"- {metric}")
            lines.append("")

        lines.append("**Technologies:** " + ", ".join(s["tech_stack"]))

        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _read_readme(self) -> Optional[str]:
        for name in ("README.md", "README.rst", "README.txt", "README"):
            path = self.project_root / name
            if path.exists():
                return path.read_text(encoding="utf-8")
        return None

    def _describe_module(self, module_dir: Path) -> Optional[str]:
        """
        Return a one-line description for a module directory by inspecting
        the docstring of the first Python file found inside it.
        """
        for py_file in sorted(module_dir.glob("*.py")):
            desc = self._first_docstring_line(py_file)
            if desc:
                return desc
        return None

    def _first_docstring_line(self, filepath: Path) -> Optional[str]:
        """Parse a Python file and return the first line of its module docstring."""
        try:
            tree = ast.parse(filepath.read_text(encoding="utf-8"))
            docstring = ast.get_docstring(tree)
            if docstring:
                first_line = docstring.strip().splitlines()[0].strip()
                if len(first_line) > 5:
                    return first_line
        except (SyntaxError, ValueError, OSError):
            pass
        return None
