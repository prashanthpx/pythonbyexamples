# Python OOP Guide: Classes from Beginner to Advanced

This guide is about **how classes are actually used in real projects**, with
examples biased toward:

- CLI tools / automation scripts
- Web APIs (FastAPI / Django‑style patterns, but framework‑agnostic examples)

We’ll build this in **phases**, from core syntax to patterns you see in
production code.

---

## 1. Why classes in real projects?

Before syntax, it’s important to know *why* teams use classes at all.

- **Structure & organization**: instead of one huge script, we group related
  data + behavior together.
- **Reusability**: the same class can be reused by multiple scripts or
  endpoints.
- **Testability**: it’s easier to test a class with clear methods than a big
  `if __name__ == "__main__"` script.
- **Abstractions & boundaries**: classes let you hide implementation details
  behind a simple interface (e.g. `GitClient`, `PaymentClient`).

You will most often see classes used for:

- **Domain models**: `Order`, `User`, `Invoice`, `Task` …
- **Services**: `EmailService`, `ReportGenerator`, `PaymentService` …
- **Clients/wrappers**: `S3Client`, `GitClient`, `PaymentGatewayClient` …
- **Configuration / data containers**: `AppConfig`, `JobConfig` …

The rest of this guide focuses on these *practical* uses.

---

## 2. Core building blocks (beginner)

### 2.1. Defining and instantiating a class

The smallest useful class groups some data and operations together.

<augment_code_snippet path="practice/oops/classes/oops.md" mode="EXCERPT">
````python
class TodoItem:
    def __init__(self, title: str, done: bool = False) -> None:
        self.title = title
        self.done = done

    def mark_done(self) -> None:
        self.done = True
````
</augment_code_snippet>

Usage:

- `item = TodoItem("Write docs")`
- `item.mark_done()`

Key ideas:

- `__init__` runs when you create an instance: `TodoItem(...)`.
- `self` is a reference to *this* instance.
- Attributes like `self.title` and `self.done` hold state.

### 2.2. Instance vs class attributes

Classes can have attributes shared by all instances (**class attributes**) and
attributes unique to each instance (**instance attributes**).

<augment_code_snippet path="practice/oops/classes/oops.md" mode="EXCERPT">
````python
class Config:
    # Class attribute: shared default
    DEFAULT_TIMEOUT = 5

    def __init__(self, timeout: int | None = None) -> None:
        # Instance attribute: specific to this Config
        self.timeout = timeout if timeout is not None else self.DEFAULT_TIMEOUT
````
</augment_code_snippet>

- `Config.DEFAULT_TIMEOUT` is on the class.
- `config.timeout` is on the instance.

In real projects, class attributes are often used for **constants or defaults**.

### 2.3. Instance, class, and static methods

You will often see three method types in real code:

- **Instance methods** (most common): operate on one object (`self`).
- **Class methods**: constructors or helpers that belong to the *class*.
- **Static methods**: utility functions grouped for convenience.

<augment_code_snippet path="practice/oops/classes/oops.md" mode="EXCERPT">
````python
class User:
    def __init__(self, email: str, active: bool = True) -> None:
        self.email = email
        self.active = active

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        """Alternate constructor used when parsing JSON or DB rows."""
        return cls(email=data["email"], active=data.get("active", True))

    @staticmethod
    def is_valid_email(email: str) -> bool:
        return "@" in email and "." in email
````
</augment_code_snippet>

Where this shows up in projects:

- `from_dict` / `from_row` / `from_env` constructors are very common.
- `@staticmethod` methods are often simple validators or formatters.

### 2.4. Encapsulation and conventions

Python doesn’t enforce access modifiers, but teams use naming conventions:

- `name` – public API, safe to use.
- `_name` – “internal”, may change; treated as private by convention.
- `__name` – name-mangled; rarely needed, used to avoid attribute clashes.

In your own projects, use `_name` to signal “this is an implementation detail”.

---

## 3. Classes as data containers (`@dataclass`)

In many real projects, simple classes are mainly used to carry data around:
configuration, small domain objects, results from functions, etc.

Instead of writing `__init__` by hand every time, Python offers `@dataclass`.

### 3.1. Configuration and results as dataclasses

Here is a small example taken from a CLI/automation context.

We define:

- `JobConfig` – configuration for a backup/cleanup job.
- `JobResult` – what happened when we ran the job.

The code lives in: `practice/oops/classes/dataclass_config_example.py`.

<augment_code_snippet path="practice/oops/classes/dataclass_config_example.py" mode="EXCERPT">
````python
from dataclasses import dataclass, field


@dataclass
class JobConfig:
    """Configuration for a simple backup/cleanup job."""

    name: str
    dry_run: bool = False
    retries: int = 3
    tags: list[str] = field(default_factory=list)
````
</augment_code_snippet>

`JobResult` is another dataclass that groups the outcome:

<augment_code_snippet path="practice/oops/classes/dataclass_config_example.py" mode="EXCERPT">
````python
@dataclass
class JobResult:
    """Result of running a job."""

    config: JobConfig
    files_processed: int
    ok: bool
    error: "str | None" = None
````
</augment_code_snippet>

The `run_job` function returns a `JobResult` and prints some information:

<augment_code_snippet path="practice/oops/classes/dataclass_config_example.py" mode="EXCERPT">
````python
def run_job(config: JobConfig) -> JobResult:
    print(f"Running job '{config.name}' (dry_run={config.dry_run})")

    # Imagine some real work here...
    files_processed = 42
    ok = True
    error = None

    return JobResult(config=config, files_processed=files_processed, ok=ok, error=error)
````
</augment_code_snippet>

And in the `__main__` block we construct a config, run the job, and print both:

<augment_code_snippet path="practice/oops/classes/dataclass_config_example.py" mode="EXCERPT">
````python
if __name__ == "__main__":
    config = JobConfig(name="daily-backup", dry_run=True, tags=["test", "backup"])
    result = run_job(config)

    print("Config:", config)
    print("Result:", result)
````
</augment_code_snippet>

### 3.2. Real output from running the example

From inside `practice/oops/classes`:

```bash
python3 dataclass_config_example.py
```

Captured output (stored in the `output` variable in that file):

<augment_code_snippet path="practice/oops/classes/dataclass_config_example.py" mode="EXCERPT">
````text
Running job 'daily-backup' (dry_run=True)
Config: JobConfig(name='daily-backup', dry_run=True, retries=3, tags=['test', 'backup'])
Result: JobResult(config=JobConfig(name='daily-backup', dry_run=True, retries=3, tags=['test', 'backup']), files_processed=42, ok=True, error=None)
````
</augment_code_snippet>

This is a realistic pattern you will see in many codebases:

- Take parsed CLI args or environment variables.
- Put them into a configuration dataclass.
- Return another dataclass from your core logic so it is easy to log, test, or
  send over the network.


---

## 4. Classes in CLI tools & automation scripts

One of the most common real uses of classes is to structure CLI tools:

- A **config** object that holds parsed arguments.
- A **command** class whose `run()` method does the work and returns an exit code.

### 4.1. A simple `clean` command as a class

Example file: `practice/oops/classes/cli_runner_example.py`

We start with a small configuration dataclass:

<augment_code_snippet path="practice/oops/classes/cli_runner_example.py" mode="EXCERPT">
````python
from dataclasses import dataclass
from pathlib import Path


@dataclass
class CleanConfig:
    """Configuration for a simple 'clean temp files' CLI command."""

    root: Path
    dry_run: bool = False
````
</augment_code_snippet>

Then we define a `CleanCommand` class whose `run()` method implements the logic:

<augment_code_snippet path="practice/oops/classes/cli_runner_example.py" mode="EXCERPT">
````python
class CleanCommand:
    """Command object representing 'clean temp files' in a CLI."""

    def __init__(self, config: CleanConfig) -> None:
        self.config = config

    def run(self) -> int:
        print(f"[CLEAN] root={self.config.root} dry_run={self.config.dry_run}")

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
````
</augment_code_snippet>

In the `__main__` block we wire it up like a real CLI entry point:

<augment_code_snippet path="practice/oops/classes/cli_runner_example.py" mode="EXCERPT">
````python
if __name__ == "__main__":
    config = CleanConfig(root=Path("/tmp/myproject"), dry_run=True)
    cmd = CleanCommand(config)
    exit_code = cmd.run()
    print("exit_code:", exit_code)
````
</augment_code_snippet>

### 4.2. Real output from running the CLI example

From inside `practice/oops/classes`:

```bash
python3 cli_runner_example.py
```

Actual output (also stored in the `output` variable in that file):

<augment_code_snippet path="practice/oops/classes/cli_runner_example.py" mode="EXCERPT">
````text
[CLEAN] root=/tmp/myproject dry_run=True
DRY-RUN delete: /tmp/myproject/file1.tmp
DRY-RUN delete: /tmp/myproject/file2.tmp
[CLEAN] done
exit_code: 0
````
</augment_code_snippet>

This pattern scales directly to larger tools:

- One **config** dataclass per command.
- One **command class** with a `run()` method per command (build, clean, deploy).
- A thin `if __name__ == "__main__"` block that:
  - parses CLI arguments (e.g. with `argparse` or `typer`),
  - builds the config object,
  - constructs the command class and calls `run()`.


### 4.3. Multi-command CLI pattern with a base Command class

The previous example had only one command. Real CLIs usually support multiple
subcommands (e.g. `clean`, `build`, `deploy`). A common pattern is:

- One **base** `Command` class with a `run()` method.
- One subclass per concrete command, e.g. `CleanCommand`, `BuildCommand`.
- A **dispatcher** function that picks the right command class.

Example file: `practice/oops/classes/multi_command_cli_example.py`

We define configurations for each command:

<augment_code_snippet path="practice/oops/classes/multi_command_cli_example.py" mode="EXCERPT">
````python
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
````
</augment_code_snippet>

Then a small `Command` base class and two concrete commands:

<augment_code_snippet path="practice/oops/classes/multi_command_cli_example.py" mode="EXCERPT">
````python
class Command:
    """Base class for CLI commands."""

    def run(self) -> int:
        raise NotImplementedError


class CleanCommand(Command):
    def __init__(self, config: CleanConfig) -> None:
        self.config = config

    def run(self) -> int:
        print(f"[CLEAN] root={self.config.root} dry_run={self.config.dry_run}")
        # ...
        return 0
````
</augment_code_snippet>

The dispatcher chooses which command to run based on a name:

<augment_code_snippet path="practice/oops/classes/multi_command_cli_example.py" mode="EXCERPT">
````python
def run_command(command_name: str) -> int:
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
````
</augment_code_snippet>

### 4.4. Real output from the multi-command example

From inside `practice/oops/classes`:

```bash
python3 multi_command_cli_example.py
```

Output (also captured in the `output` variable in that file):

<augment_code_snippet path="practice/oops/classes/multi_command_cli_example.py" mode="EXCERPT">
````text
[DISPATCH] running 'clean'
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
````
</augment_code_snippet>

This mirrors how tools like `git`, `kubectl`, or custom internal CLIs are
structured:

- A **dispatcher** decides which command class to instantiate.
- Each command class holds its own config and `run()` logic.
- Adding a new command is usually just:
  - create a new `XxxConfig` dataclass,
  - create a new `XxxCommand` subclass,
  - extend the dispatcher.



---

## 5. Inheritance and polymorphism (simple, real-world style)

So far you’ve already used inheritance and polymorphism without naming them
explicitly:

- In the CLI section, `Command` is a base class and `CleanCommand` /
  `BuildCommand` are subclasses.
- The dispatcher works with `Command` but actually calls the overridden `run()`
  on each specific subclass.

This section makes those ideas explicit with a small automation example.

### 5.1. Base class and subclasses

Example file: `practice/oops/classes/inheritance_polymorphism_example.py`

We start with a simple `Task` dataclass and a base `TaskHandler`:

<augment_code_snippet path="practice/oops/classes/inheritance_polymorphism_example.py" mode="EXCERPT">
````python
@dataclass
class Task:
    """A simple task in an automation system."""

    id: int
    description: str


class TaskHandler:
    """Base class for handling tasks."""

    def handle(self, task: Task) -> None:
        raise NotImplementedError
````
</augment_code_snippet>

Then we create two concrete handlers that **inherit** from `TaskHandler` and
**override** `handle()`:

<augment_code_snippet path="practice/oops/classes/inheritance_polymorphism_example.py" mode="EXCERPT">
````python
class EmailTaskHandler(TaskHandler):
    def __init__(self, email: str) -> None:
        self._email = email  # internal detail

    def handle(self, task: Task) -> None:
        print(f"[EMAIL] Sending '{task.description}' to {self._email}")


class SlackTaskHandler(TaskHandler):
    def __init__(self, channel: str) -> None:
        self._channel = channel

    def handle(self, task: Task) -> None:
        print(f"[SLACK] Posting '{task.description}' to channel {self._channel}")
````
</augment_code_snippet>

### 5.2. Polymorphism in action

Now we write a function that accepts a list of `TaskHandler` objects and calls
`handle()` on each one. It does **not** care whether it got an
`EmailTaskHandler` or `SlackTaskHandler`.

<augment_code_snippet path="practice/oops/classes/inheritance_polymorphism_example.py" mode="EXCERPT">
````python
def process_task_with_all_handlers(handlers: List[TaskHandler], task: Task) -> None:
    for handler in handlers:
        handler.handle(task)
````
</augment_code_snippet>

In the `__main__` block we create one `Task` and two handlers:

<augment_code_snippet path="practice/oops/classes/inheritance_polymorphism_example.py" mode="EXCERPT">
````python
if __name__ == "__main__":
    task = Task(id=1, description="Deploy new version")

    handlers: List[TaskHandler] = [
        EmailTaskHandler("dev-team@example.com"),
        SlackTaskHandler("#deployments"),
    ]

    process_task_with_all_handlers(handlers, task)
````
</augment_code_snippet>

This is **runtime polymorphism**:

- The variable `handler` is typed as `TaskHandler`.
- At runtime, `handler` is sometimes an `EmailTaskHandler`, sometimes a
  `SlackTaskHandler`.
- Calling `handler.handle(task)` automatically uses the correct overridden
  method for each subclass.

### 5.3. Real output from the inheritance/polymorphism example

From inside `practice/oops/classes`:

```bash
python3 inheritance_polymorphism_example.py
```

Output (also captured in the `output` variable in that file):

<augment_code_snippet path="practice/oops/classes/inheritance_polymorphism_example.py" mode="EXCERPT">
````text
[EMAIL] Sending 'Deploy new version' to dev-team@example.com
[SLACK] Posting 'Deploy new version' to channel #deployments
````
</augment_code_snippet>

You will see this pattern everywhere in real codebases:

- A base interface-like class (here `TaskHandler`, earlier `Command`).
- Many small subclasses which each implement one concrete behavior.
- High-level code that depends only on the base class, so you can plug in new
  subclasses without changing that high-level logic.


---

## 6. Encapsulation with properties (`@property`)

Earlier we talked about encapsulation using naming conventions (`name`, `_name`).
A common next step in real projects is to use **properties** to control how
important attributes are read and written.

Properties let you:

- keep attribute-style access (`account.balance`),
- but still run code when that value is read or updated.

### 6.1. A small `Account` example

Example file: `practice/oops/classes/encapsulation_property_example.py`

We model a tiny bank account:

- Real value is stored in a "private" attribute `_balance`.
- A `balance` property enforces the rule: balance cannot go negative.

<augment_code_snippet path="practice/oops/classes/encapsulation_property_example.py" mode="EXCERPT">
````python
class Account:
    """A simple bank account with encapsulated balance."""

    def __init__(self, owner: str, balance: int = 0) -> None:
        self.owner = owner
        self._balance = 0
        self.balance = balance
````
</augment_code_snippet>

The `balance` property controls access to `_balance`:

<augment_code_snippet path="practice/oops/classes/encapsulation_property_example.py" mode="EXCERPT">
````python
    @property
    def balance(self) -> int:
        return self._balance

    @balance.setter
    def balance(self, value: int) -> None:
        if value < 0:
            raise ValueError("Balance cannot be negative")
        self._balance = value
````
</augment_code_snippet>

On the outside, code still just does `account.balance` and
`account.balance = 123`, but under the hood we now have a single place to
validate and protect invariants.

### 6.2. Using the `Account` class

In the `__main__` block we create an account, deposit, and try to overdraw:

<augment_code_snippet path="practice/oops/classes/encapsulation_property_example.py" mode="EXCERPT">
````python
if __name__ == "__main__":
    account = Account("alice", balance=100)
    print("Owner:", account.owner)
    print("Initial balance:", account.balance)

    account.deposit(50)
    print("After deposit:", account.balance)

    try:
        account.withdraw(200)
    except ValueError as e:
        print("Withdraw failed:", e)

    print("Balance after failed withdraw:", account.balance)

    account.withdraw(50)
    print("Final balance:", account.balance)
````
</augment_code_snippet>

### 6.3. Real output from the encapsulation example

From inside `practice/oops/classes`:

```bash
python3 encapsulation_property_example.py
```

Output (also captured in the `output` variable in that file):

<augment_code_snippet path="practice/oops/classes/encapsulation_property_example.py" mode="EXCERPT">
````text
Owner: alice
Initial balance: 100
[DEPOSIT] +50
After deposit: 150
[WITHDRAW] -200
Withdraw failed: Balance cannot be negative
Balance after failed withdraw: 150
[WITHDRAW] -50
Final balance: 100
````
</augment_code_snippet>

Properties are a key tool for **evolving** your classes safely:

- You can start with a plain public attribute (e.g. `balance`).
- Later, if you need validation or logging, you can convert it into a property
  without changing existing call sites (`account.balance` still works).
