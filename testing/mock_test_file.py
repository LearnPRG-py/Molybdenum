import test_helpers

jeff_actual_base64 = test_helpers.base64_encode("testing/actual/jeff.png")
chromium_actual_base64 = test_helpers.base64_encode(
    "testing/actual/chromium.png"
)


def run_test():
    if not (
        test_helpers.base64_encode("testing/jeff.png") == jeff_actual_base64
    ):
        return False
    if not (
        test_helpers.base64_encode("testing/chromium.png")
        == chromium_actual_base64
    ):
        return False
    return True
