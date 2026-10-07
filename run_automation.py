from playwright.sync_api import sync_playwright


# ============================================================
# CONFIGURATION
# ============================================================

URL = (
    "https://royalenfield.operations.dynamics.com/"
    "?cmp=REIN&mi=RetailStoreTable"
)

AUTH_FILE = "auth.json"

STORE_NUMBERS = [
    "11469",
    "11470",
    "11473",
]


# ============================================================
# FILTER STORE NUMBER
# ============================================================

def filter_store(page, store_id):

    print("\n")
    print("------------------------------------------------------------")
    print(f"Filtering Store Number: {store_id}")
    print("------------------------------------------------------------")

    # --------------------------------------------------------
    # Store Number column
    # --------------------------------------------------------

    store_header = page.locator(
        '[data-dyn-columnname="RetailStoreTable_StoreNumber"].dyn-headerCell'
    ).first

    store_header.wait_for(
        state="visible",
        timeout=15000
    )

    store_header.click()

    print("✓ Store Number filter opened")

    # --------------------------------------------------------
    # Filter input
    # --------------------------------------------------------

    filter_input = page.get_by_role(
        "textbox",
        name="Filter field: Store number, operator: is one of",
        exact=True
    )

    filter_input.wait_for(
        state="visible",
        timeout=10000
    )

    filter_input.fill(store_id)

    print(f"✓ Entered store number: {store_id}")

    page.wait_for_timeout(500)

    # --------------------------------------------------------
    # FIRST APPLY
    # --------------------------------------------------------

    apply_button = page.get_by_role(
        "button",
        name="Apply",
        exact=True
    ).last

    apply_button.wait_for(
        state="visible",
        timeout=10000
    )

    if not apply_button.is_enabled():
        raise Exception("First Apply button is disabled.")

    apply_button.click()

    print("✓ First Apply clicked")

    page.wait_for_timeout(1000)

    # --------------------------------------------------------
    # SECOND APPLY
    # D365 requires Apply to be clicked twice
    # --------------------------------------------------------

    apply_button = page.get_by_role(
        "button",
        name="Apply",
        exact=True
    ).last

    try:

        apply_button.wait_for(
            state="visible",
            timeout=5000
        )

        if not apply_button.is_enabled():
            raise Exception("Second Apply button is disabled.")

        apply_button.click()

        print("✓ Second Apply clicked")

    except Exception as e:

        print("⚠ Second Apply was not available:")
        print(e)

    # --------------------------------------------------------
    # Wait for filtering
    # --------------------------------------------------------

    page.wait_for_timeout(2000)

    # --------------------------------------------------------
    # Verify filter popup closed
    # --------------------------------------------------------

    filter_input.wait_for(
        state="hidden",
        timeout=10000
    )

    print("✓ Filter popup closed")

    # --------------------------------------------------------
    # Verify store exists in Stores grid
    # --------------------------------------------------------

    stores_grid = page.get_by_role(
        "grid",
        name="Stores"
    )

    stores_grid.wait_for(
        state="visible",
        timeout=15000
    )

    store_result = stores_grid.get_by_text(
        store_id,
        exact=True
    )

    if store_result.count() == 0:

        page.screenshot(
            path=f"store_not_found_{store_id}.png",
            full_page=True
        )

        raise Exception(
            f"Store {store_id} was not found after filtering."
        )

    print(f"✓ Store {store_id} filtered successfully")

    return store_result.first


# ============================================================
# OPEN PAYMENT METHODS
# ============================================================

def open_payment_methods(page):

    print("\n")
    print("Opening Payment methods...")

    # --------------------------------------------------------
    # Confirmed D365 control name from Form Information:
    #
    # Control:
    #     Payment methods
    #
    # Control name:
    #     TenderTypesButton
    # --------------------------------------------------------

    payment_methods = page.locator(
        '[data-dyn-controlname="TenderTypesButton"]'
    ).last

    payment_methods.wait_for(
        state="visible",
        timeout=15000
    )

    print("✓ Payment methods control found")

    payment_methods.click()

    print("✓ Payment methods clicked")

    page.wait_for_timeout(2500)


# ============================================================
# SELECT FINANCE
# ============================================================

def select_finance(page):

    print("\n")
    print("Selecting Finance...")

    finance = page.get_by_text(
        "Finance",
        exact=True
    ).last

    finance.wait_for(
        state="visible",
        timeout=15000
    )

    finance.click()

    print("✓ Finance selected")

    page.wait_for_timeout(1500)


# ============================================================
# OPEN INFO CODES
# ============================================================

def open_info_codes(page):

    print("\n")
    print("Opening Info codes...")

    info_codes = page.locator(
        '[data-dyn-controlname="InfoCodes"]'
    ).last

    info_codes.wait_for(
        state="visible",
        timeout=15000
    )

    info_codes.click()

    print("✓ Info codes opened")

    page.wait_for_timeout(2000)


# ============================================================
# CREATE INFO CODE
# ============================================================

def create_info_code(
    page,
    info_code,
    required,
    sequence
):

    print("\n")
    print("------------------------------------------------------------")
    print(f"Creating Info Code: {info_code}")
    print(f"Required: {required}")
    print(f"Sequence: {sequence}")
    print("------------------------------------------------------------")

    # --------------------------------------------------------
    # NEW
    # --------------------------------------------------------

    new_button = page.locator(
        '[data-dyn-controlname="SystemDefinedNewButton"]'
    ).last

    new_button.wait_for(
        state="visible",
        timeout=15000
    )

    new_button.click()

    print("✓ New clicked")

    page.wait_for_timeout(1000)

    # --------------------------------------------------------
    # INFO CODE ID
    # --------------------------------------------------------

    info_code_input = page.locator(
        '[data-dyn-controlname="InfoCodeId"] input'
    ).last

    info_code_input.wait_for(
        state="visible",
        timeout=10000
    )

    info_code_input.fill(
        info_code
    )

    print(f"✓ Info Code entered: {info_code}")

    # --------------------------------------------------------
    # INPUT REQUIRED
    # --------------------------------------------------------

    input_required = page.locator(
        '[data-dyn-controlname="InputRequired"] input'
    ).last

    input_required.wait_for(
        state="visible",
        timeout=10000
    )

    if required:

        if not input_required.is_checked():

            input_required.check()

    else:

        if input_required.is_checked():

            input_required.uncheck()

    print(
        f"✓ Input Required set to: {required}"
    )

    # --------------------------------------------------------
    # SEQUENCE NUMBER
    # --------------------------------------------------------

    sequence_input = page.locator(
        '[data-dyn-controlname="SequenceNum"] input'
    ).last

    sequence_input.wait_for(
        state="visible",
        timeout=10000
    )

    sequence_input.fill(
        str(sequence)
    )

    print(
        f"✓ Sequence set to: {sequence}"
    )

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    save_button = page.locator(
        '[data-dyn-controlname="SystemDefinedSaveButton"]'
    ).last

    save_button.wait_for(
        state="visible",
        timeout=15000
    )

    save_button.click()

    print("✓ Info Code saved")

    page.wait_for_timeout(1500)


# ============================================================
# CREATE ALL THREE INFO CODES
# ============================================================

def configure_info_codes(page):

    # ========================================================
    # 1. Finance
    # Required = False
    # Sequence = 1
    # ========================================================

    create_info_code(
        page=page,
        info_code="Finance",
        required=False,
        sequence=1
    )

    # ========================================================
    # 2. REF
    # Required = True
    # Sequence = 2
    # ========================================================

    create_info_code(
        page=page,
        info_code="REF",
        required=True,
        sequence=2
    )

    # ========================================================
    # 3. auth
    # Required = True
    # Sequence = 3
    # ========================================================

    create_info_code(
        page=page,
        info_code="auth",
        required=True,
        sequence=3
    )


# ============================================================
# PROCESS ONE STORE
# ============================================================

def process_store(page, store_id):

    print("\n\n")
    print("============================================================")
    print(f"STARTING STORE: {store_id}")
    print("============================================================")

    try:

        # ====================================================
        # STEP 1
        # Filter this store
        # ====================================================

        filter_store(
            page,
            store_id
        )

        # ====================================================
        # STEP 2
        # Click Payment methods
        # ====================================================

        open_payment_methods(
            page
        )

        # ====================================================
        # STEP 3
        # Select Finance
        # ====================================================

        select_finance(
            page
        )

        # ====================================================
        # STEP 4
        # Open Info codes
        # ====================================================

        open_info_codes(
            page
        )

        # ====================================================
        # STEP 5
        # Create Finance / REF / auth
        # ====================================================

        configure_info_codes(
            page
        )

        print("\n")
        print("============================================================")
        print(f"✓ STORE {store_id} COMPLETED SUCCESSFULLY")
        print("============================================================")

        return True

    except Exception as e:

        print("\n")
        print("============================================================")
        print(f"✗ STORE {store_id} FAILED")
        print("============================================================")

        print("\nError:")
        print(e)

        # ----------------------------------------------------
        # Save screenshot
        # ----------------------------------------------------

        try:

            page.screenshot(
                path=f"error_store_{store_id}.png",
                full_page=True
            )

            print(
                f"\nScreenshot saved:"
                f" error_store_{store_id}.png"
            )

        except Exception:
            pass

        return False


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n")
    print("============================================================")
    print("D365 STORE INFO CODE AUTOMATION")
    print("============================================================")

    with sync_playwright() as p:

        # ====================================================
        # Launch browser
        # ====================================================

        browser = p.chromium.launch(
            headless=False
        )

        # ====================================================
        # Load authenticated D365 session
        # ====================================================

        context = browser.new_context(
            storage_state=AUTH_FILE
        )

        page = context.new_page()

        # ====================================================
        # Open D365 Stores page
        # ====================================================

        print("\nOpening D365...")

        page.goto(
            URL,
            wait_until="domcontentloaded",
            timeout=60000
        )

        print("✓ D365 opened")

        # Allow D365 UI to load
        page.wait_for_timeout(5000)

        # ====================================================
        # RESULTS
        # ====================================================

        successful = []
        failed = []

        # ====================================================
        # PROCESS EACH STORE
        #
        # IMPORTANT:
        #
        # Store 11469 is completely processed first.
        # Then the page is reloaded.
        # Then 11470 is processed.
        # Then 11473.
        # ====================================================

        for store_id in STORE_NUMBERS:

            result = process_store(
                page,
                store_id
            )

            if result:

                successful.append(
                    store_id
                )

            else:

                failed.append(
                    store_id
                )

            # ------------------------------------------------
            # Return to Stores page before next store
            # ------------------------------------------------

            if store_id != STORE_NUMBERS[-1]:

                print("\nReturning to Stores page...")

                page.goto(
                    URL,
                    wait_until="domcontentloaded",
                    timeout=60000
                )

                page.wait_for_timeout(4000)

                print("✓ Stores page loaded")

        # ====================================================
        # FINAL SUMMARY
        # ====================================================

        print("\n\n")
        print("============================================================")
        print("AUTOMATION COMPLETED")
        print("============================================================")

        print("\nSuccessful stores:")

        if successful:

            for store_id in successful:

                print(
                    f"  ✓ {store_id}"
                )

        else:

            print("  None")

        print("\nFailed stores:")

        if failed:

            for store_id in failed:

                print(
                    f"  ✗ {store_id}"
                )

        else:

            print("  None")

        print("\n============================================================")

        # ====================================================
        # Keep browser open
        # ====================================================

        input(
            "\nPress ENTER to close the browser..."
        )

        context.close()
        browser.close()


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()