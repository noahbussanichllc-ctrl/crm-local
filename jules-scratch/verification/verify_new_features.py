from playwright.sync_api import sync_playwright, expect
import os

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.set_viewport_size({"width": 1600, "height": 1000})

    # Get the absolute path to the index.html file
    file_path = os.path.abspath('index.html')
    page.goto(f'file://{file_path}')

    # Wait for owners to load
    expect(page.locator('#ownersList')).not_to_be_empty(timeout=10000)

    # --- Test Case 1: Verify the Location dropdown ---

    # 1. Select the first owner with properties
    page.locator(".owner-item:has-text('Property')").first.click()

    # 2. Verify the location field is a dropdown (<select>)
    location_dropdown = page.locator("#centerPanel .form-group:has-text('Location') select")
    expect(location_dropdown).to_be_visible()

    # 3. Verify it has options (more than just the default "Select Location")
    option_count = location_dropdown.locator('option').count()
    assert option_count > 1, f"Expected dropdown to have more than 1 option, but found {option_count}"

    # --- Test Case 2: Verify the Delete Log button ---

    # 4. Add a new log to delete
    page.get_by_role("button", name="+ Add Log").click()
    expect(page.locator('#addLogModal')).to_be_visible()
    log_text_to_delete = "This is a test log to be deleted."
    page.locator('#newLogNotes').fill(log_text_to_delete)
    page.get_by_role("button", name="Save Log").click()

    # 5. Verify the new log appears
    log_list = page.locator('#logList')
    newest_log_entry = log_list.locator('.log-item').first
    expect(newest_log_entry).to_contain_text(log_text_to_delete)

    # 6. Click the edit button on the new log
    newest_log_entry.get_by_role("button", name="Edit").click()

    # 7. In the modal, verify the delete button is visible
    delete_button = page.locator("#editLogModal .btn-delete:has-text('Delete Log')")
    expect(delete_button).to_be_visible()

    # 8. Click the delete button and accept the confirmation dialog
    page.on("dialog", lambda dialog: dialog.accept())
    delete_button.click()

    # 9. Verify the log entry is now gone from the list
    expect(log_list.get_by_text(log_text_to_delete)).not_to_be_visible()

    # Take a final screenshot
    page.screenshot(path="jules-scratch/verification/new_features_verification.png")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)