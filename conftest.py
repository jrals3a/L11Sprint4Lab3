# tests/ui/conftest.py
"""
Playwright fixtures for UI tests.

These fixtures provide a configured Chromium browser and page
for each test. They work alongside pytest-playwright's built-in
fixtures and the existing tests/conftest.py reset_tasks fixture.
"""
import pytest
from playwright.sync_api import Page, sync_playwright

BASE_URL = "http://127.0.0.1:5000"

@pytest.fixture(scope="session")
def playwright_instance():
    """Start Playwright once for the entire test session."""
    with sync_playwright() as pw:
        yield pw

@pytest.fixture
def browser(playwright_instance, request):
    """Launch a fresh Chromium browser for each test.

    Respects pytest-playwright's --headed and --slowmo CLI flags:
        uv run python -m pytest tests/ui/test_ui.py -v --headed
        uv run python -m pytest tests/ui/test_ui.py -v --headed --slowmo 2000
    """
    headed = request.config.getoption("--headed", default=False)
    slowmo = request.config.getoption("--slowmo", default=0)
    browser = playwright_instance.chromium.launch(
        headless=not headed,
        slow_mo=slowmo,
    )
    yield browser
    browser.close()

@pytest.fixture
def page(browser) -> Page:
    """Fresh browser page for each test.

    Also resets the Flask app's task state before each test
    so tests start with a clean database.
    """
    context = browser.new_context()
    page = context.new_page()

    # Reset task state before each UI test
    # Uses POST /api/tasks/reset — the reset endpoint only accepts POST
    try:
        page.request.post(f"{BASE_URL}/api/tasks/reset")
    except Exception:
        pass  # Server may not be running — test will fail naturally

    yield page
    context.close()
