import base64
import os
import sys
import time
import main

sys.path.insert(0, "testing")
import mock_test_file

main.set_running_tests()

# Add Test Name Here
tests = ["basic_load_config()", "basic_test()"]

# Helpers
def pre_tests():
    os.system("cp savedata.toml savedatacopy.toml")
    os.system("cp -r testing testing_backup")

def cleanup(exit_code):
    os.system("mv savedatacopy.toml savedata.toml")
    os.system("mv testing_backup testing")
    quit(exit_code)
    
def base64_encode(img_path):
    with open(img_path, "rb") as i:
        contents = i.read()
    return base64.b64encode(contents)

def write_config(config_file_contents):
    with open("savedata.toml", "w") as f:
        f.write(config_file_contents)

# Tests
def basic_load_config():
    config_contents = """
    repo = "test"
    directory = "."
    supervision_level = 0
    """
    write_config(config_contents)
    config = main.load_config()
    expected = {"repo": "test", "directory": ".", "supervision_level": 0}
    if config == expected:
        return True
    else:
        return False

def basic_test():
    return False
    config_contents = """
    repo = "test"
    directory = "."
    supervision_level = 0
    """
    write_config(config_contents)
    config = main.load_config()
    expected = {"repo": "test", "directory": ".", "supervision_level": 0}
    if config != expected:
        return False
    test_passed = mock_test_file.run_test()
    if test_passed:
        # Test should not pass with no edits
        return False
    start = time.time()
    with open("testing/log.txt") as f:
        log = f.read()
    count = log.count("Actual pixels (open in browser):")
    main.update_images(log, "molybdenum_autotests", count, config)
    elapsed = time.time() - start
    print(f"Time taken: {elapsed:.4f}s")
    if elapsed > 0.1:
        print("Warning: 2 Images took > 0.1s. Consider optimising code.")
    test_passed = mock_test_file.run_test()
    if not test_passed:
        # Test should now pass after images are updated
        return False

pre_tests()
fail = False
for i in tests:
    if eval(i) == False:
        print("Test "+i+" failed!")
        fail = True

cleanup(1 if fail else 0)
