from conftest_patterns import session_scope_shared as shared


def test_session_fixture_seen_in_second_module(session_fix):
    # We are in a *different* test module, but the same session fixture has
    # already been created once for the whole test run.
    assert shared.setup_calls == 1

