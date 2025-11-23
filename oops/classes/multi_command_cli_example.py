from dataclasses import dataclass
from pathlib import Path


@dataclass
class CleanConfig:
    """Configuration for the 'clean' command."""

    root: Path
    dry_run: bool = False


@dataclass
class BuildConfig:
    """Configuration for the 'build' command."""

    root: Path
    target: str = "dev"


class Command:
    """Base class for CLI commands.

    Real tools often use a pattern like this so all commands share a common
    interface (`run()` returning an int exit code).
    """

    def run(self) -> int:  # pragma: no cover - interface only
        raise NotImplementedError


class CleanCommand(Command):
    def __init__(self, config: CleanConfig) -> None:
        self.config = config

    def run(self) -> int:
        print(f"[CLEAN] root={self.config.root} dry_run={self.config.dry_run}")
        print(f"DRY-RUN delete: {self.config.root}/file1.tmp")
        print(f"DRY-RUN delete: {self.config.root}/file2.tmp")
        print("[CLEAN] done")
        return 0


class BuildCommand(Command):
    def __init__(self, config: BuildConfig) -> None:
        self.config = config

    def run(self) -> int:
        print(f"[BUILD] root={self.config.root} target={self.config.target}")
        print("Compiling sources...")
        print("Packaging artifacts...")
        print("[BUILD] done")
        return 0


def run_command(command_name: str) -> int:
    """Very small command dispatcher.

    In a real tool, this might look at sys.argv and then select the
    appropriate command class.
    """

    if command_name == "clean":
        config = CleanConfig(root=Path("/tmp/myproject"), dry_run=True)
        cmd: Command = CleanCommand(config)
    elif command_name == "build":
        config = BuildConfig(root=Path("/tmp/myproject"), target="prod")
        cmd = BuildCommand(config)
    else:
        print(f"Unknown command: {command_name}")
        return 1

    print(f"[DISPATCH] running '{command_name}'")
    return cmd.run()


if __name__ == "__main__":  # pragma: no cover - manual run example
    for name in ["clean", "build", "deploy"]:
        exit_code = run_command(name)
        print("exit_code:", exit_code)


# Captured output from running: python3 multi_command_cli_example.py
output = """[DISPATCH] running 'clean'
[CLEAN] root=/tmp/myproject dry_run=True
DRY-RUN delete: /tmp/myproject/file1.tmp
DRY-RUN delete: /tmp/myproject/file2.tmp
[CLEAN] done
exit_code: 0
[DISPATCH] running 'build'
[BUILD] root=/tmp/myproject target=prod
Compiling sources...
Packaging artifacts...
[BUILD] done
exit_code: 0
Unknown command: deploy
exit_code: 1
"""

