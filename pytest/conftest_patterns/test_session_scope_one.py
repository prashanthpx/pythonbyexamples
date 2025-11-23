from conftest_patterns import session_scope_shared as shared


# Phase 3 – Fixtures: session scope across multiple top-level modules


def test_session_fixture_seen_in_first_module(session_fix):
    """Session fixture is shared across top-level modules.

    Even though multiple modules use the same fixture name, the underlying
    session-scoped fixture is created only once for the entire pytest run.
    """
    assert shared.setup_calls == 1

