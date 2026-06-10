# Plan: Strengthen pytest Suite for QA Assessment Criteria

## Context

This project is a Twitch E2E automation suite using Python + pytest + Selenium.
It is being evaluated against 6 criteria:

1. Problem-solving abilities ✅ (OCR template matching already demonstrates this)
2. Knowledge of testing frameworks ⚠️ (only one test case, no parametrize/markers)
3. Knowledge on Python ✅ (inheritance, type hints, fixtures, yield)
4. **Recursivity ❌ — no recursion anywhere in the codebase**
5. Adaptability to challenge and constrain timelines ⚠️ (implicit in git history)
6. **Testing approach ❌ — only happy path, no negative/edge case tests**

## Goal

Close the two gaps (Recursivity and Testing approach) in a way that is natural,
not forced — the recursion must solve a real problem in the codebase.

## Proposed Changes

### 1. Add recursion to BasePage — retry with backoff

Problem: `find_visible()` and `dismiss_if_present()` currently fail immediately
if the element is not ready. SPAs like Twitch render asynchronously and elements
can appear/disappear multiple times.

Solution: Add a `retry(fn, retries=3, delay=1.0)` recursive method to `BasePage`
that calls `fn()` recursively, decrementing retries each time, with delay between
attempts.

```python
def retry(self, fn, retries: int = 3, delay: float = 1.0):
    try:
        return fn()
    except Exception:
        if retries <= 0:
            raise
        time.sleep(delay)
        return self.retry(fn, retries - 1, delay)
```

Use `retry()` inside `click_search()` (OCR-based, flaky) and
`select_first_streamer()` (waits for dynamic card render).

### 2. Add negative and edge case tests — new test file

Create `tests/test_search_edge_cases.py` with:

- `test_empty_search_stays_on_page` — submit empty query, assert URL unchanged
- `test_search_no_results` — search for a gibberish string unlikely to return
  streamers, assert graceful state (no crash, page still functional)
- `test_scroll_beyond_content` — scroll more than page height, assert no JS error
  and page still interactive
- `test_player_not_present_before_navigation` — assert `is_player_visible()`
  returns False before navigating to a streamer page (guards against false positive)

### 3. Update pytest markers

Add `pytest.ini` markers:
- `@pytest.mark.smoke` — critical path only (existing test)
- `@pytest.mark.edge` — edge case tests (new file)

## Files to Change

- `pages/base_page.py` — add `retry()` recursive method
- `pages/home_page.py` — wrap `click_search()` OCR call with `retry()`
- `pages/search_page.py` — wrap `select_first_streamer()` with `retry()`
- `tests/test_search_edge_cases.py` — new file, 4 edge case tests
- `pytest.ini` — add marker declarations

## Out of Scope

- Replacing Selenium with Playwright
- Adding CI/CD pipeline
- Multi-browser testing
- Performance benchmarks
