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

> **Shadowing rule (very common interview / bug question)**
>
> - If an instance has `self.name`, that value **shadows** `User.name` on the
>   class when you access `obj.name`.
> - There is **no conflict**: they live in different places (`obj.__dict__`
>   vs `User.__dict__`). Python just looks on the instance first, then falls
>   back to the class.
>
> Small demo: `oops/classes/class_vs_instance_name_shadowing.py`.

<augment_code_snippet path="oops/classes/class_vs_instance_name_shadowing.py" mode="EXCERPT">
````python
class User:
    name: str = "class-default"  # class attribute

    def __init__(self, name: str) -> None:
        self.name = name          # instance attribute
````
</augment_code_snippet>

After `u1 = User("Alice")` and `u2 = User("Bob")`:

- `u1.name` → `"Alice"` (instance attribute)
- `u2.name` → `"Bob"` (instance attribute)
- `User.name` → `"class-default"` (class attribute)

If you *did not* assign `self.name` in `__init__`, then `u1.name` would fall
back to the class variable `User.name`.

### 2.3. Instance, class, and static methods

You will often see three method types in real code:

- **Instance methods** (most common): operate on one object (`self`).
- **Class methods**: constructors or helpers that belong to the *class*.
- **Static methods**: utility functions grouped for convenience.

> **Cheat sheet – when to use which**
>
> - Use an **instance method** when the logic depends on `self` (per-object
>   state).
> - Use a **classmethod** when the logic depends on the **class**, shared
>   configuration, or is an **alternate constructor** (`from_dict`, `from_env`,
>   etc.). No instance should be required.
> - Use a **staticmethod** for a small utility/validator that does not need
>   either `self` or `cls`, but you want it grouped with the class for
>   organization.

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

#### 2.3.1. When to use `@classmethod` instead of an instance method

Example file: `oops/classes/classmethod_examples.py`.

A simplified version of the first part:

<augment_code_snippet path="oops/classes/classmethod_examples.py" mode="EXCERPT">
````python
class CounterInstanceStyle:
    class_count: int = 0

    def print_class_count(self) -> None:
        print(f"[instance] class_count = {CounterInstanceStyle.class_count}")
````
</augment_code_snippet>

<augment_code_snippet path="oops/classes/classmethod_examples.py" mode="EXCERPT">
````python
class CounterClassMethod:
    class_count: int = 0

    @classmethod
    def print_class_count(cls) -> None:
        print(f"[classmethod] {cls.__name__}.class_count = {cls.class_count}")
````
</augment_code_snippet>

Key takeaways:

- If a method **does not use `self`** and only works with **class-level state**
  like `class_count` or shared configuration, make it a `@classmethod`.
- With an instance method you must create an object you **do not actually
  need**, just to call the method; with `@classmethod` you can call
  `MyClass.method()` directly.
- `@classmethod` expresses intent: *"this behavior belongs to the class, not a
  particular object"*. This is clearer than `obj.method()` when the logic is
  really about the class.
- Classmethods work naturally with **inheritance**: in
  `SubCounter(CounterClassMethod)`, calling `SubCounter.print_class_count()`
  uses `SubCounter.class_count`, because `cls` is the subclass.
- In real code, `@classmethod` is heavily used for **alternate constructors**
  such as `User.from_dict(...)`, `Config.from_env()`, or `Job.from_row(db_row)`.
- A classmethod **does not require `__init__` at all**: you can have utility
  classes that are never instantiated but still expose useful
  `@classmethod` APIs (for example `Config.load(path)` or
  `Registry.register_default()`). The example file also includes
  `UserWithAltConstructor.from_first_last(...)` to show this pattern.

#### 2.3.2 Alternate constructors with `@classmethod`

In many projects you will see classmethods used as **alternate constructors**:

- They are often named `from_first_last`, `from_dict`, `from_env`, `default`,
  etc.
- They **return a new instance** of the class (usually by calling `cls(...)`).
- They can be called **without an existing object**: `User.from_dict(data)`.

Typical patterns:

- **Different input shape** – e.g. `User.from_first_last(first, last)` builds
  the full name inside the class instead of every caller writing
  `User(first + " " + last)`.
- **Parsing external data** – e.g. `User.from_dict(payload)` when data comes
  from JSON/DB rows, not positional arguments.
- **Loading configuration** – e.g. `Config.from_env()` that reads environment
  variables and returns a ready-to-use `Config` instance.
- **Preset defaults** – e.g. `RetryPolicy.default()` that returns a commonly
  used configuration object.

One small example from `oops/classes/classmethod_examples.py`:

<augment_code_snippet path="oops/classes/classmethod_examples.py" mode="EXCERPT">
````python
class UserWithAltConstructor:
    def __init__(self, full_name: str) -> None:
        self.full_name = full_name

    @classmethod
    def from_first_last(cls, first: str, last: str) -> "UserWithAltConstructor":
        return cls(f"{first} {last}")
````
</augment_code_snippet>

The key idea: the **class** owns the object-creation details; callers just pick
the right constructor name based on where their data comes from.

Another example file: `oops/classes/retry_policy_examples.py` compares two
designs:

- `RetryPolicyRigid` – hard-codes defaults in `__init__`, so every instance is
  identical (no flexibility).
- `RetryPolicy` – keeps `__init__` general and offers presets via
  `default()`, `fast()`, `slow()` classmethods.

<augment_code_snippet path="oops/classes/retry_policy_examples.py" mode="EXCERPT">
````python
class RetryPolicy:
    def __init__(self, attempts: int, delay: float) -> None:
        self.attempts = attempts
        self.delay = delay

    @classmethod
    def default(cls) -> "RetryPolicy":
        return cls(attempts=3, delay=1.0)
````
</augment_code_snippet>

Key differences:

- Hard-coding values in `__init__` gives you **only one** configuration.
- Using classmethods as alternate constructors lets you keep
  `__init__` **flexible** (`RetryPolicy(7, 2.5)`) and still provide
  **named presets** (`RetryPolicy.default()`, `RetryPolicy.fast()`, ...).
- Because classmethods receive `cls`, calling `CustomRetryPolicy.default()`
  returns a `CustomRetryPolicy` instance, which is hard to achieve if everything
  is baked into `__init__`.

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

#### Polymorphism vs `@override`

It is easy to confuse **polymorphism** with the `@override` decorator sometimes
seen in type-checked Python code:

- **Polymorphism** is the *runtime* behaviour you just saw: different
  subclasses provide their own `handle()` implementation, and Python picks the
  right one based on the actual object.
- **`@override`** (from `typing` / `typing_extensions`) is just a *static
  check* that you really are overriding a method from the base class. It does
  not change how method calls behave.

For example, with shapes:

<augment_code_snippet mode="EXCERPT">
````python
from typing import override


class Shape:
    def area(self) -> float:
        ...


class Square(Shape):
    @override
    def area(self) -> float:  # type checkers verify this really overrides
        return 4 * 4
````
</augment_code_snippet>

If you accidentally wrote `def areaaaa(self)` by mistake, `@override` would let
type checkers warn you that you are *not* actually overriding anything. The
runtime polymorphism (`shape.area()`) is the same with or without
`@override`.

Example file: `oops/classes/override_typo_example.py` shows a common bug:

- You intend to override `language()` from a base class.
- In the subclass you accidentally write `languag()` with a typo and decorate
  it with `@override`.
- At **runtime**, Python happily runs and still calls the base `language()`
  method; `@override` is ignored.
- A **static type checker** (mypy, pyright, PyCharm, VS Code) would instead
  flag an error like "Method `languag` does not override any method in
  superclass".

So in practice:

- Use polymorphism for behaviour (`obj.method()` dispatching to different
  implementations).
- Use `@override` to let tools catch mistakes in your overrides; it only has an
  effect when you run a type checker.

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


### 5.4. Abstract base classes (`ABC`) and `@abstractmethod`

Sometimes you want a base class that is **only a blueprint**, not something
you ever instantiate directly. In Python you model this with an **abstract base
class** (ABC).

Example file: `oops/classes/abc_shape_example.py`.

<augment_code_snippet path="oops/classes/abc_shape_example.py" mode="EXCERPT">
````python
from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        ...  # subclasses must implement this


class Square(Shape):
    def __init__(self, side: float) -> None:
        self.side = side

    def area(self) -> float:
        return self.side * self.side
````
</augment_code_snippet>

Key ideas:

- `ABC` stands for **Abstract Base Class**.
  - A class inheriting from `ABC` is meant to be a **blueprint**.
  - You cannot instantiate it if it has unimplemented `@abstractmethod`s.
- `@abstractmethod` marks methods that **must be implemented** by subclasses.
- A subclass that implements all abstract methods becomes a **concrete class**
  and can be instantiated.

The file also contains a `BadShape` example that forgets to implement
`area()`:

<augment_code_snippet path="oops/classes/abc_shape_example.py" mode="EXCERPT">
````python
class BadShape(Shape):
    # No area() implementation here on purpose.
    pass


bad = BadShape()  # TypeError: Can't instantiate abstract class BadShape
````
</augment_code_snippet>

Contrast this with a plain base class **without** `ABC` / `@abstractmethod`:

<augment_code_snippet mode="EXCERPT">
````python
class Shape:
    def area(self) -> float:
        # Placeholder implementation
        return 0.0


s = Shape()  # This succeeds, even though area() is not meaningful
````
</augment_code_snippet>

Using `ABC` + `@abstractmethod` tells Python (and your team):

- "This class is not meant to be instantiated directly."
- "Subclasses must provide real implementations for these methods."

Paired with polymorphism, this gives you a clear, enforced contract: code can
depend on the abstract `Shape` interface, while concrete subclasses (`Square`,
`Circle`, ...) provide the actual behaviour.


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
  This is how real projects add encapsulation without breaking their API.

Another small example file, `oops/classes/property_use_cases.py`, shows other
common patterns:

- **Computed values** – `Rectangle.area` is a property that calculates
  `width * height` but is used like `rect.area` (no `get_area()` method).
- **Hiding implementation details** – `UserFullName.full_name` joins
  `first` and `last`, but callers just use `user.full_name`.
- **Lazy loading / caching** – `Data.expensive_result` runs a heavy operation
  only on first access, then returns the cached value.
- **Validation on assignment** – `UserEmail.email` validates the address in a
  property setter while callers keep writing `user.email = "alice@example.com"`.

#### Tiny before/after: evolving a public attribute into a property

Often you really do start with a plain public attribute and later realise you
need validation or other logic. Properties let you **upgrade** the
implementation without changing how callers use it.

Example file: `oops/classes/property_evolution_example.py`.

"Before" – simple public attribute:

<augment_code_snippet path="oops/classes/property_evolution_example.py" mode="EXCERPT">
````python
class UserV1:
    def __init__(self, age: int) -> None:
        self.age = age  # direct public attribute
````
</augment_code_snippet>

"After" – same idea, but `age` is now a property with validation. Callers still
write `user.age` and `user.age = value`:

<augment_code_snippet path="oops/classes/property_evolution_example.py" mode="EXCERPT">
````python
class UserV2:
    def __init__(self, age: int) -> None:
        self._age = 0
        self.age = age  # goes through the setter

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, value: int) -> None:
        if value < 0:
            raise ValueError("Age cannot be negative")
        self._age = value
````
</augment_code_snippet>

In a real project you would just evolve the original `User` implementation, but
the idea is the same: callers keep using `user.age` while you add
encapsulation, validation, logging, caching, etc. behind the scenes.
