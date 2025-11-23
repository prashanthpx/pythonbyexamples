from dataclasses import dataclass
from pathlib import Path


@dataclass
class CleanConfig:
    """Configuration for a simple 'clean temp files' CLI command.

    In a real tool this might be populated from argparse arguments.
    """

    root: Path
    dry_run: bool = False


class CleanCommand:
    """Command object representing 'clean temp files' in a CLI.

    This pattern scales to multi-command CLIs (build, clean, deploy, ...).
    """

    def __init__(self, config: CleanConfig) -> None:
        self.config = config

    def run(self) -> int:
        """Execute the command.

        Returns a process-like exit code: 0 for success, non-zero for failure.
        """

        print(f"[CLEAN] root={self.config.root} dry_run={self.config.dry_run}")

        # In a real tool, we'd walk the filesystem. Here we just simulate work.
        temp_files = [
            self.config.root / "file1.tmp",
            self.config.root / "file2.tmp",
        ]

        for path in temp_files:
            if self.config.dry_run:
                print(f"DRY-RUN delete: {path}")
            else:
                print(f"Deleting: {path}")

        print("[CLEAN] done")
        return 0


if __name__ == "__main__":  # pragma: no cover - manual run example
    config = CleanConfig(root=Path("/tmp/myproject"), dry_run=True)
    cmd = CleanCommand(config)
    exit_code = cmd.run()
    print("exit_code:", exit_code)


# Captured output from running: python3 cli_runner_example.py
output = """[CLEAN] root=/tmp/myproject dry_run=True
DRY-RUN delete: /tmp/myproject/file1.tmp
DRY-RUN delete: /tmp/myproject/file2.tmp
[CLEAN] done
exit_code: 0
"""

