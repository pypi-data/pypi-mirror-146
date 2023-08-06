# -*- coding: utf-8 -*-

import pytest

def pytest_configure(config):
    config.addinivalue_line("markers", "unstable")

def _test_is_unstable(node):
    return any(marker.name == 'unstable' for marker in node.own_markers)

@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session: pytest.Session, exitstatus: int):
    if exitstatus == pytest.ExitCode.TESTS_FAILED:
        stats = session.config.pluginmanager.get_plugin('terminalreporter').stats
        failed_tests = [test.nodeid for test in stats.get('failed', [])]

        unstable_tests = [test.nodeid for test in session.items if _test_is_unstable(test)]

        # Remove elements from failed_tests if unstable
        non_unstable_tests = [test for test in failed_tests if test not in unstable_tests]

        if len(non_unstable_tests) == 0:
            session.exitstatus = pytest.ExitCode.OK
