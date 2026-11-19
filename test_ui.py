# tests/ui/test_ui.py
"""
Playwright UI tests for Task Tracker web interface.

These tests drive a real Chromium browser — every click, form fill,
and navigation is executed in an actual browser instance against the
running Flask application.

Requirements:
    - Flask server must be running: uv run python -m app
    - Chromium installed: uv run python setup_browsers.py

Run headless (default / CI):
    uv run python -m pytest tests/ui/test_ui.py -v

Run headed (see the browser):
    uv run python -m pytest tests/ui/test_ui.py -v --headed

Run with slow motion (for learning):
    uv run python -m pytest tests/ui/test_ui.py -v --headed --slowmo 2000
"""
import pytest

BASE_URL = "http://127.0.0.1:5000"

# ── S4_3: Task UI Tests ───────────────────────────────────────────────────────

@pytest.mark.ui
def test_add_task(page):
    """TC-RF014-001: Add a task through the web UI.

    Verifies the complete add-task workflow:
    1. Navigate to the add task form
    2. Fill in title and description
    3. Submit the form
    4. Verify redirect to task list
    5. Verify task appears in the list
    """
    # Navigate to the add task form
    page.goto(f"{BASE_URL}/tasks/new")

    # Fill in the form fields
    page.fill('input[name="title"]', "Playwright Test Task")
    page.fill('input[name="description"]', "Added by Playwright automation")

    # Submit the form
    page.click('button[type="submit"]')

    # Wait for the redirect to the task list
    page.wait_for_url(lambda url: url.endswith("/tasks"), timeout=10000)

    # Verify the task appears in the list
    content = page.content()
    assert "Playwright Test Task" in content, "Task title should appear in task list"
    assert "Added by Playwright automation" in content, "Task description should appear"

@pytest.mark.ui
def test_form_validation_empty_title(page):
    """TC-RF014-002: Empty title shows validation error in the UI.

    Verifies server-side validation by bypassing HTML5 required attribute.
    HTML5 'required' prevents browser form submission — we use JavaScript
    to submit directly, bypassing front-end validation to reach the
    server-side check in ui.py.
    """
    # Navigate to the add task form
    page.goto(f"{BASE_URL}/tasks/new")

    # Fill description only — leave title empty
    page.fill('input[name="description"]', "No title provided")

    # Bypass HTML5 required attribute and submit directly via JavaScript
    # This simulates what happens when front-end validation is bypassed
    page.evaluate("document.querySelector('form').submit()")

    # Wait for the error message to appear before asserting
    # page.evaluate() is near-instant — without this wait the assertion
    # runs before the server response renders the error on the page
    page.wait_for_selector(".alert-error", timeout=5000)

    # Verify we stay on /tasks/new (not redirected to /tasks)
    assert "/tasks/new" in page.url, "Should stay on form when title is empty"

    # Verify server-side error message is shown
    error = page.locator(".alert-error")
    assert error.count() > 0, "Error message element should be present"
    message = error.inner_text().lower()
    assert "required" in message or "title" in message, \
        "Error message should mention title or required"

@pytest.mark.ui
def test_complete_task(page):
    """TC-RF014-003: Complete a task through the web UI.

    Verifies the task completion workflow:
    1. Add a task
    2. Navigate to task list
    3. Click the Complete button
    4. Verify the task shows as completed (strikethrough styling)
    """
    # Step 1: Add a task to complete
    page.goto(f"{BASE_URL}/tasks/new")
    page.fill('input[name="title"]', "Task to Complete")
    page.fill('input[name="description"]', "Will be marked done")
    page.click('button[type="submit"]')

    # Wait for redirect to task list
    page.wait_for_url(lambda url: url.endswith("/tasks"), timeout=10000)

    # Verify task was added
    assert "Task to Complete" in page.content()

    # Click the Complete button
    page.locator(".btn-complete").first.click()

    # Wait for the page to reload after completion
    page.wait_for_url(lambda url: url.endswith("/tasks"), timeout=10000)

    # Verify task is now marked as completed
    # The <li> element gets class="task-item task-completed" after completion
    completed = page.locator(".task-completed")
    assert completed.count() > 0, "At least one task should show as completed"
    assert "Task to Complete" in completed.first.inner_text(), \
        "The completed task should be 'Task to Complete'"

@pytest.mark.ui
def test_delete_task(page):
    """TC-RF014-004: Delete a task through the web UI.

    Verifies the task deletion workflow:
    1. Add a task
    2. Navigate to task list
    3. Click the Delete button
    4. Verify the task is removed from the list
    """
    # Step 1: Add a task to delete
    page.goto(f"{BASE_URL}/tasks/new")
    page.fill('input[name="title"]', "Task to Delete")
    page.fill('input[name="description"]', "Will be removed")
    page.click('button[type="submit"]')

    # Wait for redirect to task list
    page.wait_for_url(lambda url: url.endswith("/tasks"), timeout=10000)

    # Verify task was added
    assert "Task to Delete" in page.content()

    # Click the Delete button
    page.locator(".btn-delete").first.click()

    # Wait for the page to reload after deletion
    page.wait_for_url(lambda url: url.endswith("/tasks"), timeout=10000)

    # Verify task is no longer in the list
    assert "Task to Delete" not in page.content(), \
        "Deleted task should not appear in the task list"

@pytest.mark.ui
def test_end_to_end_workflow(page):
    """TC-RF014-005: Complete end-to-end task workflow.

    Chains add → complete → delete in one test session,
    mirroring a real user's complete interaction with the app.

    Student exercise: Use DevTools to find the Complete button selector.
    All other steps are provided.
    """
    # ── Step 1: Add a task ───────────────────────────────────────────────
    page.goto(f"{BASE_URL}/tasks/new")
    page.fill('input[name="title"]', "E2E Workflow Task")
    page.fill('input[name="description"]', "This task will be completed then deleted")
    page.click('button[type="submit"]')

    # Wait for redirect to task list
    page.wait_for_url(lambda url: url.endswith("/tasks"), timeout=10000)

    # ── Step 2: Verify task appears ──────────────────────────────────────
    assert "E2E Workflow Task" in page.content(), \
        "Task should appear in the list after adding"

    # ── Step 3: Complete the task ────────────────────────────────────────
    # STUDENT EXERCISE: Find the Complete button selector using DevTools
    # See detailed instructions below this test.
    # TODO: Replace YOUR_SELECTOR_HERE with the correct selector for the Complete button
    page.locator(".btn-complete").first.click()

    # Wait for page to reload
    page.wait_for_url(lambda url: url.endswith("/tasks"), timeout=10000)

    # ── Step 4: Verify task shows as completed ───────────────────────────
    completed = page.locator(".task-completed")
    assert completed.count() > 0, "Task should show completed styling"

    # ── Step 5: Delete the task ──────────────────────────────────────────
    page.locator(".btn-delete").first.click()

    # Wait for page to reload
    page.wait_for_url(lambda url: url.endswith("/tasks"), timeout=10000)

    # ── Step 6: Verify task is gone ──────────────────────────────────────
    assert "E2E Workflow Task" not in page.content(), \
        "Task should be gone after deletion"
