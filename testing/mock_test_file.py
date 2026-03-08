import test_helpers
jeff_actual_base64 = test_helpers.base64_encode("actual/jeff.png")
chromium_actual_base64 = test_helpers.base64_encode("actual/chromium.png")

def run_test():
    if not (test_helpers.base64_encode("jeff.png") == jeff_actual_base64):
        return False
    if not (test_helpers.base64_encode("chromium.png") == chromium_actual_base64):
        return False
    return True
