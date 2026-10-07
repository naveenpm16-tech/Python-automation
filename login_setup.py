from playwright.sync_api import sync_playwright

def generate_auth():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Open FinOps URL
        page.goto("https://royalenfield.operations.dynamics.com/?cmp=REIN&mi=RetailStoreTable")

        # Pause and wait for manual user input in the terminal
        input("\n--> Log in and complete MFA in the browser window.\n--> Once fully loaded on the home/store screen, press ENTER here to save session...\n")

        # Save session cookies/tokens
        context.storage_state(path="auth.json")
        print("\nSUCCESS: auth.json created successfully!")
        browser.close()

if __name__ == "__main__":
    generate_auth()