"""Demonstrate how `self` and other arguments are bound during object creation.

When you run:

    c = ClusterInstance()

Python internally does *something like*:

    temp_cluster_obj = ClusterInstance.__new__(ClusterInstance)
    ClusterInstance.__init__(temp_cluster_obj)

and inside `ClusterInstance.__init__` we then call:

    self.g = Service(self)

This file shows that inside `Service.__init__`, the first parameter `self`
refers to the new `Service` object, and the second parameter `val` refers to
the `ClusterInstance` that we passed in.
"""

from __future__ import annotations


class Service:
    """Service that receives a ClusterInstance in its constructor.

    The important part is the parameter binding for ``__init__``:

    - ``self`` → the *new* Service instance being created.
    - ``val``  → whatever object the caller passed in.
    """

    def __init__(self, val: "ClusterInstance") -> None:  # noqa: D401
        # At this point:
        #   self -> new Service object
        #   val  -> the ClusterInstance passed in from ClusterInstance.__init__
        print(f"Service.__init__: val.PORT = {val.PORT}")
        self.val = val


class ClusterInstance:
    """A simple class that creates a Service and passes itself into it."""

    PORT = 100

    def __init__(self) -> None:
        # Here, `self` is the new ClusterInstance object.
        # We *explicitly* pass `self` into Service.__init__ as the second argument.
        # Python automatically passes the new Service instance as the first
        # argument (its `self`).
        self.g = Service(self)


def main() -> None:
    # Creating a ClusterInstance will also create a Service and print val.PORT.
    c = ClusterInstance()

    # A few extra checks to make the relationships obvious when you run it.
    print(f"ClusterInstance.PORT = {ClusterInstance.PORT}")
    print(f"c.PORT                = {c.PORT}")
    print(f"c.g.val is c?         = {c.g.val is c}")


if __name__ == "__main__":  # pragma: no cover - manual demo
    main()

