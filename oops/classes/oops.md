# Python OOP Guide: Classes from Beginner to Advanced

This guide is about **how classes are actually used in real projects**, with
examples biased toward:

- CLI tools / automation scripts
- Web APIs (FastAPI / Django‑style patterns, but framework‑agnostic examples)

We’ll build this in **phases**, from core syntax to patterns you see in
production code.

You can read it straight through, or jump to the part you care about:

- [1. Why classes in real projects?](#1-why-classes-in-real-projects)
- [2. Core building blocks (beginner)](#2-core-building-blocks-beginner)
- [3. Classes as data containers (@dataclass)](#3-classes-as-data-containers-dataclass)
- [4. Classes in CLI tools & automation scripts](#4-classes-in-cli-tools--automation-scripts)
- [5. Inheritance and polymorphism](#5-inheritance-and-polymorphism-simple-real-world-style)
- [6. Encapsulation with properties (@property)](#6-encapsulation-with-properties-property)

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

This section builds a solid mental model of **what a class is** and how
instances are created. By the end you should be comfortable with:

- writing a class and its `__init__` method (the *initializer*),
- the difference between **instance attributes** and **class attributes**,
- when to use **instance**, **class**, and **static** methods,
- what really happens when you call `MyClass(...)` and how `self` is bound.

### 2.1. Defining and instantiating a class

The smallest useful class groups some data and operations together.


````python
class TodoItem:
    def __init__(self, title: str, done: bool = False) -> None:
        self.title = title
        self.done = done

    def mark_done(self) -> None:
        self.done = True
````
 

Usage:

- `item = TodoItem("Write docs")`
- `item.mark_done()`

Key ideas:

- `__init__` runs when you create an instance: `TodoItem(...)`.
- `self` is a reference to *this* instance.
- Attributes like `self.title` and `self.done` hold state.

In many languages you will hear the word **constructor**. In Python, that is
conceptually split into two steps: `__new__` (low-level object allocation) and
`__init__` (initialising the new object). In everyday code you almost always
only implement `__init__`. Section [2.5](#25-how-object-creation-and-self-really-work-__new-__init-and-argument-binding)
shows the full picture, but for now you can think:

- *"Calling `TodoItem(...)` creates a new object and then calls my
  `__init__` to set it up."*

### 2.2. Instance vs class attributes

Classes can have attributes shared by all instances (**class attributes**) and
attributes unique to each instance (**instance attributes**).


````python
class Config:
    # Class attribute: shared default
    DEFAULT_TIMEOUT = 5

    def __init__(self, timeout: int | None = None) -> None:
        # Instance attribute: specific to this Config
        self.timeout = timeout if timeout is not None else self.DEFAULT_TIMEOUT
````

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


````python
class User:
    name: str = "class-default"  # class attribute

    def __init__(self, name: str) -> None:
        self.name = name          # instance attribute
````


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


Where this shows up in projects:

- `from_dict` / `from_row` / `from_env` constructors are very common.
- `@staticmethod` methods are often simple validators or formatters.

#### 2.3.1. When to use `@classmethod` instead of an instance method

Example file: `oops/classes/classmethod_examples.py`.

A simplified version of the first part:


````python
class CounterInstanceStyle:
    class_count: int = 0

    def print_class_count(self) -> None:
        print(f"[instance] class_count = {CounterInstanceStyle.class_count}")
````



````python
class CounterClassMethod:
    class_count: int = 0

    @classmethod
    def print_class_count(cls) -> None:
        print(f"[classmethod] {cls.__name__}.class_count = {cls.class_count}")
````


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


````python
class UserWithAltConstructor:
    def __init__(self, full_name: str) -> None:
        self.full_name = full_name

    @classmethod
    def from_first_last(cls, first: str, last: str) -> "UserWithAltConstructor":
        return cls(f"{first} {last}")
````


The key idea: the **class** owns the object-creation details; callers just pick
the right constructor name based on where their data comes from.

Another example file: `oops/classes/retry_policy_examples.py` compares two
designs:

- `RetryPolicyRigid` – hard-codes defaults in `__init__`, so every instance is
  identical (no flexibility).
- `RetryPolicy` – keeps `__init__` general and offers presets via
  `default()`, `fast()`, `slow()` classmethods.


````python
class RetryPolicy:
    def __init__(self, attempts: int, delay: float) -> None:
        self.attempts = attempts
        self.delay = delay

    @classmethod
    def default(cls) -> "RetryPolicy":
        return cls(attempts=3, delay=1.0)
````


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

#### 2.4.1 Inner helper vs `_make_api` vs static/class helpers

Example file: `oops/classes/method_helper_placement_example.py`.

Sometimes you have a small “helper” operation (like **joining `base_url` and an
endpoint**) and you are not sure **where to put that logic**:

- define an **inner helper function inside a method**,
- make a **private instance method** like `_make_api_url`,
- use a **`@staticmethod`** helper, or
- expose a **`@classmethod`** alternate constructor.

##### A method that defines an inner helper function

In this example, the `fetch_users_with_inner_helper` method defines a local
helper function `make_url` inside itself:


````python
class ApiClient:
    def fetch_users_with_inner_helper(self) -> None:
        def make_url(endpoint: str) -> str:
            return f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        url = make_url("/users")
````


**Topology**: *“a method defines another function inside it”*.

Good for:

- Very small, **one-off helpers** that are used only in this method.
- Keeping the outer method readable by pushing a few lines into the inner
  helper.

Limitations:

- Cannot be reused from other methods or subclasses.
- Harder to test directly (you can only hit it by calling the outer method).

##### Private instance method: `_make_api_url`

Here we move the helper to a **private instance method** so it can be reused:


````python
class ApiClient:
    def _make_api_url(self, endpoint: str) -> str:
        return f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

    def fetch_users_with_private_method(self) -> None:
        url = self._make_api_url("/users")
````


Key points:

- `_make_api_url` is **part of the class**, but the leading `_` says
  “internal detail” (callers should not rely on it).
- Multiple methods can reuse the same helper (see
  `fetch_orders_with_private_method`).
- Subclasses can **override** `_make_api_url` to customize behavior.

This is usually the best default **inside one class hierarchy**: clear, testable
(`client._make_api_url("/users")` in tests), and override-friendly.

##### `@staticmethod` helper: no `self`, no `cls`

If the helper does **not need `self` or `cls` at all**, you can make it a
`@staticmethod`:


````python
class ApiClient:
    @staticmethod
    def _join_url(base_url: str, endpoint: str) -> str:
        return f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"

    def fetch_users_with_static_helper(self) -> None:
        url = self._join_url(self.base_url, "/users")
````


Key ideas:

- `_join_url` is a **pure function**; grouping it on the class is for
  **organization**, not because it needs object state.
- In tests you can call `ApiClient._join_url("https://api", "/users")`
  directly.
- If you later realize it *does* need `self` or `cls`, you can convert it to an
  instance method or classmethod.

You could also make `_join_url` a **module-level** function; whether you use a
`@staticmethod` is mostly a **style / organization** decision.

##### `@classmethod` option: alternate constructors / shared config

Classmethods are most useful when you want an **alternate constructor** or need
to work with **class-level configuration**, not for tiny helpers:


````python
class ApiClient:
    @classmethod
    def from_default(cls) -> "ApiClient":
        default_base = "https://api.example.com"
        return cls(default_base)
````


Here:

- `from_default` hides *how* we decide the default base URL (config, env vars,
  etc.).
- Callers just do `ApiClient.from_default()` to get a ready-to-use client.
- Subclasses get the right type automatically:
  `SpecialClient.from_default()` returns a `SpecialClient` instance because
  `cls` is the subclass.

##### Summary – choosing between them

- **Inner helper** (function inside a method): keep very local details readable;
  use when the helper is truly one-off and tied to that method only.
- **Private instance method** (e.g. `_make_api_url`): best when multiple methods
  in the same class (or subclasses) share behavior that depends on `self`.
- **`@staticmethod`**: use for pure helpers that do not touch `self`/`cls` but
  conceptually “belong” with the class.
- **`@classmethod`**: use when the logic is about the **class itself** (common
  examples: `from_dict`, `from_env`, `from_default`, or building typed
  instances from configuration).

##### When *not* to use inner functions

Even though inner helpers are convenient, they are a bad fit when:

- You **know** the helper will be reused by other methods or subclasses.
- You want to **override** the behavior in a subclass (you cannot override an
  inner function, but you *can* override `_make_api_url`).
- You want to **unit-test** the helper in isolation (private methods and
  staticmethods are much easier to call directly in tests).

In those cases, prefer a private instance method like `_make_api_url` or a
`@staticmethod`/module-level helper. Reserve inner helpers for truly local
details that you do not intend to share or override.

##### Quick comparison table: where to put helper logic

| Helper location              | Needs `self`/`cls`? | Reusable across methods? | Overridable in subclasses? | Easy to unit-test directly? | Typical use case                                      |
|-----------------------------|----------------------|---------------------------|-----------------------------|-----------------------------|-------------------------------------------------------|
| **Inner helper function**   | Yes (via closure)    | No                        | No                          | No                          | One-off local logic inside a single method           |
| **Private instance method** | Yes (`self`)         | Yes                       | Yes                         | Yes (`obj._helper(...)`)    | Shared behavior that depends on instance state       |
| **`@staticmethod`**         | No                   | Yes                       | No (but can be shadowed)    | Yes (`Class.helper(...)`)   | Pure utility that conceptually belongs to the class  |
| **`@classmethod`**          | Yes (`cls`)          | Yes                       | Yes                         | Yes (`Class.helper(...)`)   | Alternate constructors, class-level configuration    |
| **Module-level function**   | No                   | Yes                       | N/A                         | Yes (`helper(...)`)         | Generic utility not tied to any particular class     |

### 2.5. How object creation and `self` really work (`__new__`, `__init__`, and argument binding)

Example file: `oops/classes/object_creation_self_binding_example.py`.

#### 2.5.1 The simple rule when you call a class

When you write:

```python
GatekeeperService(some_argument)
```

Python secretly does **two steps**:

```python
temp_obj = GatekeeperService.__new__(GatekeeperService)
GatekeeperService.__init__(temp_obj, some_argument)
```

So for `__init__`:

- The **first argument** is always the **new object being created** → this is
  what we call `self`.
- Any arguments you write in parentheses go to the **remaining parameters**.

Key idea:

- There is **no magical swapping** of arguments.
- There is **no automatic passing of some “caller object”**.
- Only what you explicitly pass is passed.

#### 2.5.2 Example: `ClusterInstance` passing itself into `Service`

Example file: `oops/classes/object_creation_self_binding_example.py`.

In the example, `ClusterInstance` has a class attribute `PORT` and, inside its
constructor, it creates a `Service` and passes itself in:


````python
class Service:
    def __init__(self, val: "ClusterInstance") -> None:
        print(val.PORT)


class ClusterInstance:
    PORT = 100

    def __init__(self) -> None:
        self.g = Service(self)
````


And then we construct a `ClusterInstance`:

```python
c = ClusterInstance()
```

The program prints:

```text
100
```

Let’s break down **exactly** what happens, step by step.

##### Step 1 – Creating the `ClusterInstance`

This call:

```python
c = ClusterInstance()
```

is conceptually expanded by Python into:

```python
temp_cluster_obj = ClusterInstance.__new__(ClusterInstance)
ClusterInstance.__init__(temp_cluster_obj)
```

So inside `ClusterInstance.__init__`, the name `self` refers to:

- `self` → the **new `ClusterInstance` object** (`temp_cluster_obj`).

##### Step 2 – Calling `Service(self)` from inside `ClusterInstance.__init__`

Inside `ClusterInstance.__init__` we run:

```python
self.g = Service(self)
```

At that moment, `self` is still the `ClusterInstance` object, so you can think
of the call as:

```python
Service(self_cluster_obj)
```

##### Step 3 – Python creates the `Service` object

Just like before, Python conceptually does:

```python
temp_service_obj = Service.__new__(Service)
Service.__init__(temp_service_obj, self_cluster_obj)
```

Now we are **inside** `Service.__init__`, whose signature is:

```python
def __init__(self, val: "ClusterInstance") -> None:
    print(val.PORT)
```

The parameter binding looks like this:

| Name | What it refers to                          |
|------|--------------------------------------------|
| self | the **new `Service` object**               |
| val  | the **`ClusterInstance` object** we passed |

So when `Service.__init__` runs `print(val.PORT)`, it:

- Looks up `PORT` on the `ClusterInstance` object.
- Finds `ClusterInstance.PORT = 100`.
- Prints `100`.

##### Step 4 – Final mental model (very important)

When you write:

```python
Service(self)
```

*inside* `ClusterInstance.__init__`, what happens in `Service.__init__` is:

| In `Service.__init__(self, val)` | What it actually is                       |
|----------------------------------|-------------------------------------------|
| `self`                           | the **new `Service` instance**            |
| `val`                            | the **`ClusterInstance` you passed in**   |

This is **exactly** the same pattern you see in real projects when code does
something like `GatekeeperService(self)` inside another class:

- Class **A** creates an instance of class **B**.
- It passes **itself** (A) into B’s constructor.
- Inside B, that object becomes a normal parameter (often named `owner`,
  `client`, `cluster`, etc.).

Visually:

```text
ClusterInstance ----passes itself----> Service
         ^                                   |
         |-------------- "val" --------------|
```

#### 2.5.3 Why this always works the same way

Python always follows these rules:

- The **first parameter** of an instance method (`self` by convention) refers to
  the object that owns the method.
- Any extra arguments you pass in the call go into the **later parameters**.

So for:

```python
Service(self)
```

Python binds:

- `self` of `Service.__init__` → the **new `Service` object**.
- `val` → the **`ClusterInstance`** you passed in.

There is no special case, no hidden swap, and no hidden reference to the caller
object. The same rules apply to every class and every method.

---

## 3. Classes as data containers (`@dataclass`)

In many real projects, simple classes are mainly used to carry data around:
configuration, small domain objects, results from functions, etc.

Instead of writing `__init__` by hand every time, Python offers `@dataclass`.

### What is `@dataclass`?

`@dataclass` is a Python shortcut for writing simple classes whose main job is
to **store data**.

Think of it as:

> "Python, please write the boring class code for me."

#### Layman explanation

Normally, when you create a class to hold data, you must write:

- an initializer (`__init__`)
- maybe `__repr__` (for printing)
- maybe `__eq__` (for comparisons)

`@dataclass` **auto-generates all of that** from the fields you declare.

#### With `@dataclass` (clean, Pythonic)

```python
from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int
```

That's it.

Python automatically creates:

- `__init__(self, name, age)`
- `__repr__`
- `__eq__`

#### 🔍 What exactly does `@dataclass` generate?

By default:

| Method | Purpose |
|--------|---------|
| `__init__` | Constructor |
| `__repr__` | Pretty printing |
| `__eq__` | Equality comparison |

#### Example usage

```python
u1 = User("Alice", 30)
u2 = User("Alice", 30)

print(u1)
# User(name='Alice', age=30)

print(u1 == u2)
# True
```

#### How to remember `@dataclass`

Think:

> **data + class = dataclass**

Or:

> "Like a struct in C / Go, but Pythonic"

#### What is `@dataclass` — super simple

Think of `@dataclass` as:

> A neat, labeled box to store related values

Instead of remembering:

- "name" means user name
- "age" means user age

You say:

- this thing **has** a name
- this thing **has** an age

### Could you use a dictionary instead?

✅ Yes — but there are trade-offs.

#### Dictionary version

```python
user = {
    "name": "Alice",
    "age": 30
}

print(user["name"])
```

This works.

So why bother with `@dataclass`?

#### What goes wrong with dictionaries (real problems)

##### ❌ Typos are silent

```python
user["naem"]   # KeyError at runtime
```

Dataclass:

```python
u.naem         # IDE/type checker catches this
```

##### ❌ No guarantee what keys exist

```python
def print_user(user):
    print(user["name"])
```

What if someone passes:

```python
{"age": 40}
```

💥 Runtime error.

Dataclass:

```python
def print_user(user: User):
    print(user.name)
```

Now Python tools **know** what a `User` must have.

### What is `__repr__` in plain English?

`__repr__` answers this question:

> "If I print this object, what should it look like?"

#### When is `__repr__` used (without you calling it)?

##### ✅ 1. `print()`

```python
u = User("Alice", 30)
print(u)
```

Output:

```
User(name='Alice', age=30)
```

Without `@dataclass` (and without defining `__repr__` yourself), `print(u)`
would show something unhelpful like:

```
<__main__.User object at 0x7f...>
```

`@dataclass` gives you the nice, readable output for free.

---

### 3.1. Configuration and results as dataclasses

Here is a small example taken from a CLI/automation context.

We define:

- `JobConfig` – configuration for a backup/cleanup job.
- `JobResult` – what happened when we ran the job.

The code lives in: `oops/classes/dataclass_config_example.py`.


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


`JobResult` is another dataclass that groups the outcome:


````python
@dataclass
class JobResult:
    """Result of running a job."""

    config: JobConfig
    files_processed: int
    ok: bool
    error: "str | None" = None
````


The `run_job` function returns a `JobResult` and prints some information:


````python
def run_job(config: JobConfig) -> JobResult:
    print(f"Running job '{config.name}' (dry_run={config.dry_run})")

    # Imagine some real work here...
    files_processed = 42
    ok = True
    error = None

    return JobResult(config=config, files_processed=files_processed, ok=ok, error=error)
````


And in the `__main__` block we construct a config, run the job, and print both:


````python
if __name__ == "__main__":
    config = JobConfig(name="daily-backup", dry_run=True, tags=["test", "backup"])
    result = run_job(config)

    print("Config:", config)
    print("Result:", result)
````


### 3.2. Real output from running the example

From inside `oops/classes`:

```bash
python3 dataclass_config_example.py
```

Captured output (stored in the `output` variable in that file):


````text
Running job 'daily-backup' (dry_run=True)
Config: JobConfig(name='daily-backup', dry_run=True, retries=3, tags=['test', 'backup'])
Result: JobResult(config=JobConfig(name='daily-backup', dry_run=True, retries=3, tags=['test', 'backup']), files_processed=42, ok=True, error=None)
````


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

Example file: `oops/classes/cli_runner_example.py`

We start with a small configuration dataclass:


````python
from dataclasses import dataclass
from pathlib import Path


@dataclass
class CleanConfig:
    """Configuration for a simple 'clean temp files' CLI command."""

    root: Path
    dry_run: bool = False
````


Then we define a `CleanCommand` class whose `run()` method implements the logic:


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


In the `__main__` block we wire it up like a real CLI entry point:


````python
if __name__ == "__main__":
    config = CleanConfig(root=Path("/tmp/myproject"), dry_run=True)
    cmd = CleanCommand(config)
    exit_code = cmd.run()
    print("exit_code:", exit_code)
````


### 4.2. Real output from running the CLI example

From inside `oops/classes`:

```bash
python3 cli_runner_example.py
```

Actual output (also stored in the `output` variable in that file):


````text
[CLEAN] root=/tmp/myproject dry_run=True
DRY-RUN delete: /tmp/myproject/file1.tmp
DRY-RUN delete: /tmp/myproject/file2.tmp
[CLEAN] done
exit_code: 0
````


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

Example file: `oops/classes/multi_command_cli_example.py`

We define configurations for each command:


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


Then a small `Command` base class and two concrete commands:


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


The dispatcher chooses which command to run based on a name:


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


### 4.4. Real output from the multi-command example

From inside `oops/classes`:

```bash
python3 multi_command_cli_example.py
```

Output (also captured in the `output` variable in that file):


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

Example file: `oops/classes/inheritance_polymorphism_example.py`

We start with a simple `Task` dataclass and a base `TaskHandler`:


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


Then we create two concrete handlers that **inherit** from `TaskHandler` and
**override** `handle()`:


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


### 5.2. Polymorphism in action

Now we write a function that accepts a list of `TaskHandler` objects and calls
`handle()` on each one. It does **not** care whether it got an
`EmailTaskHandler` or `SlackTaskHandler`.


````python
def process_task_with_all_handlers(handlers: List[TaskHandler], task: Task) -> None:
    for handler in handlers:
        handler.handle(task)
````


In the `__main__` block we create one `Task` and two handlers:


````python
if __name__ == "__main__":
    task = Task(id=1, description="Deploy new version")

    handlers: List[TaskHandler] = [
        EmailTaskHandler("dev-team@example.com"),
        SlackTaskHandler("#deployments"),
    ]

    process_task_with_all_handlers(handlers, task)
````


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

From inside `oops/classes`:

```bash
python3 inheritance_polymorphism_example.py
```

Output (also captured in the `output` variable in that file):


````text
[EMAIL] Sending 'Deploy new version' to dev-team@example.com
[SLACK] Posting 'Deploy new version' to channel #deployments
````


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


Key ideas:

- `ABC` stands for **Abstract Base Class**.
  - A class inheriting from `ABC` is meant to be a **blueprint**.
  - You cannot instantiate it if it has unimplemented `@abstractmethod`s.
- `@abstractmethod` marks methods that **must be implemented** by subclasses.
- A subclass that implements all abstract methods becomes a **concrete class**
  and can be instantiated.

The file also contains a `BadShape` example that forgets to implement
`area()`:


````python
class BadShape(Shape):
    # No area() implementation here on purpose.
    pass


bad = BadShape()  # TypeError: Can't instantiate abstract class BadShape
````


Contrast this with a plain base class **without** `ABC` / `@abstractmethod`:


````python
class Shape:
    def area(self) -> float:
        # Placeholder implementation
        return 0.0


s = Shape()  # This succeeds, even though area() is not meaningful
````


Using `ABC` + `@abstractmethod` tells Python (and your team):

- "This class is not meant to be instantiated directly."
- "Subclasses must provide real implementations for these methods."

Paired with polymorphism, this gives you a clear, enforced contract: code can
depend on the abstract `Shape` interface, while concrete subclasses (`Square`,
`Circle`, ...) provide the actual behaviour.

### 5.5 Abstract, generic services: `class Service(ABC, Generic[HandleT])`

> **Advanced / optional:** This section is about **type hints and generics**.
> You can safely skip it on a first read if you only care about core OOP
> behaviour. Come back later when you are comfortable with sections 1–4 and the
> earlier parts of 5.

In real projects you will often see classes defined like:

```python
class Service(ABC, Generic[HandleT]):
    ...
```

This means the class:

- Inherits from **`ABC`** → it is an **abstract base class** (a blueprint).
- Inherits from **`Generic[HandleT]`** → it is **generic over a type
  parameter** `HandleT`.

Put differently:

- `ABC` says: *"You cannot instantiate this until all abstract methods are
  implemented by a subclass."*
- `Generic[HandleT]` says: *"This class works with some handle type `HandleT`
  chosen by the subclass (or caller).

#### 5.5.1 Quick recap: `ABC`

From above:

- `ABC` and `@abstractmethod` let you define a **blueprint**.
- Subclasses **must implement** all abstract methods.
- Trying to instantiate the abstract class directly raises `TypeError`.

Tiny standalone example:

```python
from abc import ABC, abstractmethod


class Animal(ABC):
    @abstractmethod
    def speak(self) -> None:
        ...


# a = Animal()  # TypeError: Can't instantiate abstract class Animal
```

#### 5.5.2 Quick recap: generic classes with `TypeVar` and `Generic`

Python's `typing` module lets you write **generic classes** (like generics in
Java, C#, TypeScript):

- `TypeVar("HandleT")` declares a **type variable**.
- `Generic[HandleT]` says *"this class is parameterised by a type called
  `HandleT`"*.

```python
from typing import Generic, TypeVar


HandleT = TypeVar("HandleT")


class Service(ABC, Generic[HandleT]):
    ...
```

Now `Service[...]` becomes a **family of types**:

- `Service[FileHandle]` – a service whose handle type is `FileHandle`.
- `Service[DBConnection]` – a service whose handle type is `DBConnection`.

Type checkers then know that if `start()` returns `HandleT`, `stop()` must take
the **same** type `HandleT`.

#### 5.5.3 Real-world mini framework example

File: `oops/classes/service_generic_example.py`.

We define a generic abstract base class that manages some *resource handle* and
two concrete services that choose different handle types:


````python
HandleT = TypeVar("HandleT")


class Service(ABC, Generic[HandleT]):
    @abstractmethod
    def start(self) -> HandleT: ...

    @abstractmethod
    def stop(self, handle: HandleT) -> None: ...


class FileService(Service[str]):
    ...  # start() returns str, stop() takes str


class DatabaseService(Service[DBConnection]):
    ...  # start() returns DBConnection, stop() takes DBConnection
````


Key ideas:

- `Service` is an **abstract** base: you cannot instantiate `Service()`.
- `Service[HandleT]` is also **generic**: subclasses decide what `HandleT`
  actually is.
- For `FileService(Service[str])`:
  - `HandleT` is `str`.
  - `start()` returns `str` (e.g. a file path or ID).
  - `stop()` must accept a `str`.
- For `DatabaseService(Service[DBConnection])`:
  - `HandleT` is `DBConnection`.
  - `start()` returns a `DBConnection`.
  - `stop()` must accept a `DBConnection`.

Because of the generic parameter, **different subclasses can choose different
handle types**, while sharing the same abstract API (`start` / `stop` /
`restart`). Type checkers will then warn if you accidentally pass the wrong
kind of handle to `stop()`.

Mental model:

- `ABC` → *"This is an abstract blueprint; subclasses must fill in the
  details."*
- `Generic[HandleT]` → *"This blueprint works for any `HandleT`, and subclasses
  get to decide what `HandleT` is."*

#### 5.5.4 Why use `Generic[HandleT]` if it is optional?

Important point: **you do not need** `Generic[HandleT]` for the class to work at
runtime.

This version is perfectly valid Python:


````python
from abc import ABC, abstractmethod


class Service(ABC):
    @abstractmethod
    def start(self):
        ...

    @abstractmethod
    def stop(self, handle):
        ...
````


Python will happily run this. So why bother with generics and type hints?

##### Runtime behaviour vs *meaning*

- `Generic[HandleT]` **does not change runtime behaviour**.
- It changes what the class **means** to humans and to **type checkers / IDEs**.

Without generics:

- What is `handle`? A `str`? A file object? A DB connection? A Kubernetes pod?
- Nothing enforces consistency between what `start()` returns and what
  `stop()` expects.
- You could accidentally write:

  
  ````python
  s.stop(12345)  # maybe completely wrong type, but Python won't complain
  ````
  

With generics, you encode that relationship in the type system:


````python
from typing import Generic, TypeVar


HandleT = TypeVar("HandleT")


class Service(ABC, Generic[HandleT]):
    @abstractmethod
    def start(self) -> HandleT:
        ...

    @abstractmethod
    def stop(self, handle: HandleT) -> None:
        ...
````


Now the class reads as:

> "Whatever type my subclass uses for `HandleT`, `start()` must return it and
>  `stop()` must accept the same type."

When you create concrete subclasses, type checkers can enforce that:


````python
class FileService(Service[str]):
    def start(self) -> str:
        return "/tmp/app.log"

    def stop(self, handle: str) -> None:
        ...


class DBConnection: ...


class DatabaseService(Service[DBConnection]):
    def start(self) -> DBConnection:
        return DBConnection()

    def stop(self, handle: DBConnection) -> None:
        ...
````


If you accidentally make them inconsistent (for example, `start()` returns
`int` but `stop()` takes `str`), a type checker like `mypy` or an IDE will warn
you.

##### Why this is useful in real code

Using `Generic[HandleT]` buys you:

- **Type safety** – helpers like `Service` can be reused across many handle
  types, while keeping them consistent.
- **Better readability** – the API is self-documenting: readers see that
  `start()` and `stop()` are tied via the same `HandleT`.
- **Stronger IDE support** – autocompletion and inline type hints show the
  right handle type for each concrete subclass.
- **Reusable design** – you write `Service` once and specialise it as
  `Service[str]`, `Service[DBConnection]`, `Service[FileHandle]`, etc.

You can think of it like a labelled toolbox:

- Without generics: a box just labelled *"tool"* – you might throw in a
  hammer, a banana, and a USB stick; no one stops you.
- With generics: `Toolbox[Screwdriver]` – now the label says what should go
  inside, and your tools (type checker, IDE) can complain if you try to put the
  wrong thing in.

#### 5.5.5 Naming `TypeVar`s and `Any` vs `TypeVar`

Example file: `oops/classes/typevar_vs_any_example.py`.

##### Naming the `TypeVar`

`HandleT = TypeVar("HandleT")` is **just a convention**. You can call it
anything:


````python
PHandle = TypeVar("PHandle")
ID = TypeVar("ID")
T = TypeVar("T")
MyType = TypeVar("MyType")
````


All of these behave the same. People often choose names like:

- `T` / `U` / `V` – short, generic type parameters.
- `HandleT`, `ItemT` – where the name explains the role (*"handle type"*,
  *"item type"*), and the `T` suffix hints *"this is a type variable"*.

You could even write:


````python
Banana = TypeVar("Banana")
````


It would **work**, but it would be confusing to humans reading the code. Names
are for readability.

##### `Any` vs `TypeVar`: "I don't care" vs "I care, but not here"

Using `Any` and using `TypeVar` look similar in code, but they mean very
different things.

**`Any` turns off type checking**:


````python
class AnyService(ABC):
    @abstractmethod
    def start(self) -> Any:
        ...

    @abstractmethod
    def stop(self, handle: Any) -> None:
        ...
````


Here:

- Type checkers will not warn if `start()` returns the "wrong" type.
- They will not warn if you pass the "wrong" thing into `stop()`.
- Calls like `file_service.stop(12345)` or `file_service.stop(None)` are all
  considered fine.

`Any` effectively means: *"I don't care what the type is."* It trades away
type safety.

**`TypeVar` keeps track of one unknown, consistent type**:


````python
HandleT = TypeVar("HandleT")


class Service(ABC, Generic[HandleT]):
    @abstractmethod
    def start(self) -> HandleT:
        ...

    @abstractmethod
    def stop(self, handle: HandleT) -> None:
        ...
````


Now subclasses **lock in** a specific type for `HandleT`:


````python
class FileService(Service[str]):
    def start(self) -> str:
        return "/tmp/app.log"

    def stop(self, handle: str) -> None:
        ...


class DBConnection: ...


class DatabaseService(Service[DBConnection]):
    def start(self) -> DBConnection:
        return DBConnection()

    def stop(self, handle: DBConnection) -> None:
        ...
````


For `FileService`, `HandleT` is `str`. For `DatabaseService`, `HandleT` is
`DBConnection`. A type checker will then report an error if you try something
like `file_service.stop(123)`.

Another common pattern is a generic container:


````python
ItemT = TypeVar("ItemT")


class Box(Generic[ItemT]):
    def __init__(self) -> None:
        self._item: ItemT | None = None

    def put(self, item: ItemT) -> None:
        self._item = item

    def get(self) -> ItemT | None:
        return self._item
````


If you create `b = Box[int]()` then, conceptually:

- `b.put(10)` is OK.
- `b.put("hi")` is a **type error** (even though Python will run it, your
  type checker / IDE can warn you).

If you instead defined `Box` using `Any` (like `AnyBox` in the example file),
you could put `int`, `str`, lists, or anything else into the same box and the
type checker would never complain. That is the "everything is allowed, no
enforcement" situation described above.

The key idea:

- `Any` → *"I don't care what the type is."*
- `TypeVar` → *"I care that the same type is used consistently, but the
  concrete type will be chosen later (by the subclass or caller)."*

In your `Service` example:

- `start()` returns `HandleT`.
- `stop()` accepts `HandleT`.
- `restart()` returns `HandleT`.

All three methods are tied together by the **same** type variable. That
relationship disappears if you change everything to `Any`. The purpose of the
`TypeVar` here is **not** to "allow any type"; it is to tie several methods
together so they all behave consistently once a concrete type is chosen.

#### 5.5.6 Two type parameters: `Dictionary[K, V]`

Sometimes a class needs **more than one** type parameter. A common pattern is a
mapping type:


````python
from typing import Generic, TypeVar


K = TypeVar("K")
V = TypeVar("V")


class Dictionary(Generic[K, V]):
    def __init__(self) -> None:
        self.data: dict[K, V] = {}

    def add(self, key: K, value: V) -> None:
        self.data[key] = value

    def get(self, key: K) -> V:
        return self.data[key]
````


Example file: `oops/classes/dictionary_generic_example.py`.

What this **does not** mean:

- It does **not** mean "values must be of type `K` **and** type `V`".
- It does **not** mean "keys must match both types".
- It does **not** mean "keys and values are globally restricted to only these
  two types".

What it really means:

- The class has **two separate type parameters**.
- `K` is the type of the **keys**.
- `V` is the type of the **values**.
- When you *use* the class, you decide what `K` and `V` are.

You can think of it as a template:

- `Dictionary[KeyType, ValueType]`

When you instantiate it, you plug in real types:

- `Dictionary[str, int]`  keys are `str`, values are `int`.
- `Dictionary[int, str]`  keys are `int`, values are `str`.
- `Dictionary[str, list[int]]`  keys are `str`, values are `list[int]`.

For example:


````python
d1 = Dictionary[str, int]()
d1.add("age", 25)        # OK
d1.add("height", 180)    # OK
# d1.add("age", "hello")  # type checker error: value must be int

d2 = Dictionary[int, str]()
d2.add(1, "apple")       # OK
# d2.add("one", "apple")  # type checker error: key must be int

d3 = Dictionary[str, list[int]]()
d3.add("scores", [10, 20, 30])      # OK
# d3.add("scores", "not a list")     # type checker error: value must be list[int]
````


So `K` and `V` are **templates**, not concrete types by themselves:

- They do not limit values globally.
- They simply say "for this particular `Dictionary[K, V]`, keys use `K` and
  values use `V`".
- A type checker enforces that consistency for each concrete choice of
  `Dictionary[...]`.

#### 5.5.7 Constrained `TypeVar`s: limiting allowed types

So far, our `TypeVar`s have been **unconstrained**:

- `HandleT = TypeVar("HandleT")`

This means:

- `HandleT` can be **any** type.
- The only rule is *consistency*: every place that uses `HandleT` must use the
  same concrete type (once chosen).

Sometimes you want to say:

> "This class or function only works with **these specific** types, not any
>  possible type."

For that, Python lets you define a **constrained** `TypeVar`:


````python
T = TypeVar("T", A, B)
````


Meaning:

- `T` is allowed to be **only** `A` or `B`.
- In set notation: `T ∈ {A, B}`.
- Nothing else (no `str`, no `float`, etc.).

Applied to your example, you might write (assuming the proper imports):


````python
from subprocess import Popen
from typing import Any
import psutil


HandleT = TypeVar("HandleT", Popen[Any], psutil.Process)
````


This means:

- `HandleT` can be **only one of these** two types:
  - `Popen[Any]`
  - `psutil.Process`
- It is **not** "any type".
- It is **not** "a base class".
- It is **not** "both types at once".

You might then use it in a generic service:


````python
HandleT = TypeVar("HandleT", Popen[Any], psutil.Process)


class ProcessService(Generic[HandleT]):
    def start(self) -> HandleT:
        ...

    def stop(self, handle: HandleT) -> None:
        ...
````


Now subclasses must pick **one of the allowed types**:

- ✅ Works:

  
  ````python
  class PopenService(ProcessService[Popen[Any]]):
      ...


  class PsutilService(ProcessService[psutil.Process]):
      ...
  ````

- ❌ Not allowed (type checker error):

  
  ````python
  class StringService(ProcessService[str]):
      ...  # str is not in {Popen[Any], psutil.Process}
  ````
  

A type checker will complain that `str` is **not** one of the permitted
options.

##### About using quoted types: `"Popen[Any]"`

Sometimes you might see something like:


````python
HandleT = TypeVar("HandleT", "Popen[Any]", psutil.Process)
````


Here `"Popen[Any]"` is a **string**, not the actual type object. In type
annotations, strings are used as **forward references**:

- They refer to a type by name (e.g. "User") before it is defined or imported.
- This is mostly used *inside annotations* to avoid circular imports.

For `TypeVar` constraints, you normally pass the **actual types**, not strings.
So the preferred version is:


````python
HandleT = TypeVar("HandleT", Popen[Any], psutil.Process)
````


##### A small runnable example (without external dependencies)

In this repo we use a similar idea, but with simple stand-in types instead of
real `Popen` / `psutil.Process` so that the example runs everywhere:

Example file: `oops/classes/process_service_constrained_typevar_example.py`.


````python
HandleT = TypeVar("HandleT", PopenHandle, PsutilProcessLike)


class ProcessService(ABC, Generic[HandleT]):
    @abstractmethod
    def start(self) -> HandleT:
        ...

    @abstractmethod
    def stop(self, handle: HandleT) -> None:
        ...
````


Concrete services choose one of the allowed handle types:


````python
class PopenService(ProcessService[PopenHandle]):
    def start(self) -> PopenHandle:
        handle = PopenHandle("sleep 1")
        print("Starting:", handle)
        return handle

    def stop(self, handle: PopenHandle) -> None:
        print("Stopping:", handle)
        handle.terminate()


class PsutilService(ProcessService[PsutilProcessLike]):
    def start(self) -> PsutilProcessLike:
        handle = PsutilProcessLike(1234)
        print("Starting:", handle)
        return handle

    def stop(self, handle: PsutilProcessLike) -> None:
        print("Stopping:", handle)
        handle.kill()
````


Trying to define:


````python
# class StringService(ProcessService[str]):
#     ...  # type checker error: str not allowed here
````


would be rejected by a type checker, because `str` is not in the allowed set
`{PopenHandle, PsutilProcessLike}`.

**TL;DR for constrained `TypeVar`s**

- `HandleT = TypeVar("HandleT", Popen[Any], psutil.Process)` means:
  - `HandleT` is restricted to **one of exactly two types**:
    - `Popen[Any]` or `psutil.Process`.
- It does **not** mean:
  - "any type is allowed";
  - "subclasses of those types" (unless your checker also treats them
    specially);
  - "both types at once";
  - "a union of the two".
- At subclassing / instantiation time you pick **one** of the allowed types,
  and all uses of `HandleT` in that generic class must be consistent with that
  choice.


#### 5.5.8 Q&A: `Generic[T]`, `Service[HandleT]` and "classes taking arguments"

The questions behind this section were:

- *Is `Generic[T]` a class? Is there no plain `Generic` without `T`?*
- *If I want to use `Generic` in any project, do I always need `Generic[T]`?*
- *When we write `class Service(ABC, Generic[HandleT])` and then
  `Service[Popen[Any]]`, does that mean Python classes "accept an argument"
  like functions?*

Let's answer these explicitly.

##### 1. Is `Generic[T]` a class? Can I use just `Generic`?

Yes, `Generic` **is a real class** in `typing`.

- `Generic` by itself is an **abstract base class for generic types** (as the
  docs say).
- `Generic[T]` (or `Generic[T, U]`, etc.) is that same class **parameterised by
  one or more `TypeVar`s**.

In practice you almost always use the **parameterised form**:

- `class Box(Generic[ItemT])` – one type parameter.
- `class Dictionary(Generic[K, V])` – two type parameters.

You *could* technically write:


````python
from typing import Generic


class Weird(Generic):  # legal but not useful
    ...
````


but this does **not** declare any type parameter, so type checkers have
nothing to work with. It is effectively the same (for typing purposes) as just
inheriting from `object`.

If you want a class to be **generic**, you must:

1. Declare one or more `TypeVar`s (e.g. `HandleT = TypeVar("HandleT")`).
2. Inherit from `Generic[HandleT]` (or `Generic[K, V]`, etc.).

That is what turns `Service` / `Box` / `Dictionary` into a *template* that type
checkers understand.

##### 2. What does `class Service(ABC, Generic[HandleT])` really mean?

When you write:


````python
from abc import ABC, abstractmethod
from typing import Generic, TypeVar


HandleT = TypeVar("HandleT")


class Service(ABC, Generic[HandleT]):
    @abstractmethod
    def start(self) -> HandleT: ...

    @abstractmethod
    def stop(self, handle: HandleT) -> None: ...
````


you are doing two ordinary things at once:

- **Normal inheritance** from `ABC` → this is an abstract base class.
- **Normal inheritance** from `Generic[HandleT]` → this class has **one type
  parameter** called `HandleT`.

There is nothing “mystical” here – the parentheses list **base classes**, not
function-style *arguments*. It's the same mechanism as:

- `class Admin(User): ...`
- `class Box(Generic[ItemT]): ...`

Because of the `Generic[HandleT]` base class, type checkers treat `Service` as
**generic over `HandleT`** – everywhere you see `HandleT` in annotations, that
name can later be substituted with a concrete type.

##### 3. What does `Service[Popen[Any]]` (or `ProcessService[psutil.Process]`) mean?

This is where it is easy to think “classes are taking arguments like
functions”. But the square brackets here are **type indexing**, not a normal
function call.

- `Service[HandleT]` is a **template**.
- `Service[Popen[Any]]` is the same template with `HandleT` specialised to
  `Popen[Any]` – just like `list[int]` is “a list whose elements are `int`”.

Under the hood, classes like `list`, `dict`, and `Generic` implement
`__class_getitem__`, which lets you write `MyClass[T]` in annotations.

Important mental model:

- **This does not pass a runtime argument.**
- It creates a **specialised type** for the type system.

You then use that specialised type when defining subclasses:


````python
class PopenService(Service[Popen[Any]]):
    ...  # here HandleT is effectively Popen[Any]


class ProcessService(Service[psutil.Process]):
    ...  # here HandleT is effectively psutil.Process
````


For a type checker, this means:

- Inside `PopenService`, every `HandleT` is treated as `Popen[Any]`.
- Inside `ProcessService`, every `HandleT` is treated as `psutil.Process`.
- Calls like `PopenService().stop("oops")` become **type errors**, because
  `"oops"` is not `Popen[Any]`.

At **runtime**, however, Python does not enforce any of this; it is all extra
information for tools (type checkers, IDEs, code readers).

##### 4. Do Python classes “accept arguments” like functions?

Not in the same sense.

When you see:

- `Service[Popen[Any]]` – this is **type specialisation** (static, checked by
  tools).
- `Service[Popen[Any]](...)` – this is **two steps**:
  1. Specialise the type (`Service[HandleT]` → `Service[Popen[Any]]`).
  2. Call the class to create an instance (normal `__init__` call).

The only true *runtime* “arguments” for a class are the ones passed to
`__init__` / `__new__`, just like any other constructor. Type parameters live in
an entirely different (static) world.

##### 5. How does this relate to the “two worlds” idea?

You can think of generics as living in **two parallel worlds**:

- **Runtime world (Python interpreter):**
  - Classes, objects, methods, `__init__`, attributes.
  - Code runs even if you delete all `TypeVar` / `Generic` / annotation code.
- **Type-checker world (mypy, Pyright, IDE):**
  - `TypeVar`, `Generic[T]`, `Service[Popen[Any]]`, `Box[int]`, etc. describe
    relationships between types.
  - Tools substitute `HandleT` / `ItemT` with concrete types and warn when they
    are used inconsistently.

So:

- ✔ You can remove all generics and your program still **runs**.
- ✔ Generics add **structure, documentation, and safety** for humans and
  tools, especially in large codebases.
- ✘ They do **not** change how the code executes step-by-step.

A useful “arrow” diagram for this mental model is:

- `TypeVar` → introduces a *name for an unknown type* (e.g. `HandleT`).
- `Generic[T]` → defines a *generic blueprint* that uses that name.
- `Service[HandleT]` / `Box[ItemT]` → reusable generic classes.
- `PopenService(Service[Popen[Any]])` / `Box[int]` → **concrete
  specialisations** picked for a particular use.


---

## 6. Encapsulation with properties (`@property`)

Earlier we talked about encapsulation using naming conventions (`name`, `_name`).
A common next step in real projects is to use **properties** to control how
important attributes are read and written.

Properties let you:

- keep attribute-style access (`account.balance`),
- but still run code when that value is read or updated.

### 6.1. A small `Account` example

Example file: `oops/classes/encapsulation_property_example.py`

We model a tiny bank account:

- Real value is stored in a "private" attribute `_balance`.
- A `balance` property enforces the rule: balance cannot go negative.


````python
class Account:
    """A simple bank account with encapsulated balance."""

    def __init__(self, owner: str, balance: int = 0) -> None:
        self.owner = owner
        self._balance = 0
        self.balance = balance
````


The `balance` property controls access to `_balance`:


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


On the outside, code still just does `account.balance` and
`account.balance = 123`, but under the hood we now have a single place to
validate and protect invariants.

### 6.2. Using the `Account` class

In the `__main__` block we create an account, deposit, and try to overdraw:


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


### 6.3. Real output from the encapsulation example

From inside `oops/classes`:

```bash
python3 encapsulation_property_example.py
```

Output (also captured in the `output` variable in that file):


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


````python
class UserV1:
    def __init__(self, age: int) -> None:
        self.age = age  # direct public attribute
````


"After" – same idea, but `age` is now a property with validation. Callers still
write `user.age` and `user.age = value`:


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


In a real project you would just evolve the original `User` implementation, but
the idea is the same: callers keep using `user.age` while you add
encapsulation, validation, logging, caching, etc. behind the scenes.
