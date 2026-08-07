import shutil
import tempfile
from pathlib import Path

from invoke import Context, task

EXTENSION_ID = "ulauncher-theme-synchronizer"
EXTENSIONS_DIRECTORY = Path.home() / ".local" / "share" / "ulauncher" / "extensions"

ARTIFACT_DIRECTORIES = ("__pycache__", ".pytest_cache", ".ruff_cache", "htmlcov")
ARTIFACT_FILES = (".coverage",)
EXCLUDED_DIRECTORIES = (".git", ".venv")

FILE_LOGGING_VARIABLE = "ULAUNCHER_THEME_SYNCHRONIZER_FILE_LOG"
LOG_FILE_PATH = Path(tempfile.gettempdir()) / f"{EXTENSION_ID}.log"


@task(aliases=["i"])
def install(c: Context) -> None:
    """Install the development dependencies"""
    c.run("pip install -r requirements-dev.txt")


@task(default=True)
def test(c: Context) -> None:
    """Run the test suite"""
    c.run("pytest")


@task
def cov(c: Context) -> None:
    """Run the test suite with a coverage report"""
    c.run("pytest --cov")


@task
def lint(c: Context) -> None:
    """Check the code for errors"""
    c.run("ruff check .")


@task
def types(c: Context) -> None:
    """Check the code for type errors"""
    c.run("pyright")


@task(aliases=["f"])
def fix(c: Context) -> None:
    """Format the code and automatically fix errors"""
    c.run("ruff format .")
    c.run("ruff check --fix .")


@task(aliases=["l"])
def link(c: Context) -> None:
    """Symlink the extension into the Ulauncher extensions directory"""
    EXTENSIONS_DIRECTORY.mkdir(parents=True, exist_ok=True)
    destination = EXTENSIONS_DIRECTORY / EXTENSION_ID

    if destination.is_symlink() or destination.exists():
        print(f"Already linked: {destination}")
        return

    destination.symlink_to(Path.cwd(), target_is_directory=True)
    print(f"Linked: {destination} -> {Path.cwd()}")


@task
def unlink(c: Context) -> None:
    """Remove the extension symlink from the Ulauncher extensions directory"""
    destination = EXTENSIONS_DIRECTORY / EXTENSION_ID

    if not destination.is_symlink():
        print(f"Not linked: {destination}")
        return

    destination.unlink()
    print(f"Unlinked: {destination}")


@task(help={"file_log": f"Write logs to {LOG_FILE_PATH}"})
def dev(c: Context, file_log: bool = False) -> None:
    """Run Ulauncher in development mode"""
    environment = {FILE_LOGGING_VARIABLE: "1"} if file_log else {}
    c.run("ulauncher --dev --verbose", env=environment, disown=True, echo=True)


@task
def logs(c: Context) -> None:
    """Tail the extension log file"""
    c.run(f"tail -F {LOG_FILE_PATH}", pty=True)


@task
def restart(c: Context) -> None:
    """Restart Ulauncher process"""
    c.run("pkill -x ulauncher", warn=True)
    c.run("sleep 1 && ulauncher --hide-window", disown=True)
    print("Restarted Ulauncher")


@task(aliases=["k"])
def kill(c: Context) -> None:
    """Kill Ulauncher process"""
    c.run("pkill -x ulauncher", warn=True)
    print("Pkill-ed Ulauncher")


@task
def clean(c: Context) -> None:
    """Clean up the compiled files and caches"""
    for path in _walk_artifacts(ARTIFACT_DIRECTORIES):
        shutil.rmtree(path, ignore_errors=True)

    for path in _walk_artifacts(ARTIFACT_FILES):
        path.unlink(missing_ok=True)

    print("Cleaned up the compiled files and caches")


def _walk_artifacts(names: tuple[str, ...]) -> list[Path]:
    return [
        path
        for name in names
        for path in Path().rglob(name)
        if not any(part in EXCLUDED_DIRECTORIES for part in path.parts)
    ]
