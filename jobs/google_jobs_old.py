from playwright.sync_api import sync_playwright


class GoogleJobs:

    def search_jobs(self):

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=False
            )

            page = browser.new_page()

            page.goto("https://www.google.com")

            page.wait_for_load_state("networkidle")

            # Search Box
            page.locator("textarea[name='q']").fill(
                "Azure DevOps Jobs Gurgaon"
            )

            # Press Enter
            page.keyboard.press("Enter")

            page.wait_for_load_state("networkidle")

            print("✅ Search Completed")

            page.wait_for_timeout(5000)

            browser.close()