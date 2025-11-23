from dataclasses import dataclass, field


@dataclass
class JobConfig:
    """Configuration for a simple backup/cleanup job.

    In real CLI tools this might come from argparse or environment variables.
    """

    name: str
    dry_run: bool = False
    retries: int = 3
    tags: list[str] = field(default_factory=list)


@dataclass
class JobResult:
    """Result of running a job.

    Keeping this as a dataclass makes it easy to log, return, or test.
    """

    config: JobConfig
    files_processed: int
    ok: bool
    error: "str | None" = None  # type: ignore[assignment]


def run_job(config: JobConfig) -> JobResult:
    """Fake implementation of a file-processing job.

    In a real script this might walk a directory, upload files, etc.
    Here we just pretend and return a fixed result.
    """

    print(f"Running job '{config.name}' (dry_run={config.dry_run})")

    # Imagine some real work here...
    files_processed = 42
    ok = True
    error = None

    return JobResult(config=config, files_processed=files_processed, ok=ok, error=error)


if __name__ == "__main__":  # pragma: no cover - manual run example
    config = JobConfig(name="daily-backup", dry_run=True, tags=["test", "backup"])
    result = run_job(config)

    print("Config:", config)
    print("Result:", result)


# The variable below will be filled with real output by running this file
# once and pasting the result. This mirrors the pattern used in the pytest
# mini-project tests.
output = """Running job 'daily-backup' (dry_run=True)
Config: JobConfig(name='daily-backup', dry_run=True, retries=3, tags=['test', 'backup'])
Result: JobResult(config=JobConfig(name='daily-backup', dry_run=True, retries=3, tags=['test', 'backup']), files_processed=42, ok=True, error=None)
"""

