"""
  __  __     _      _        _                    
 |  \/  |___| |_  _| |__  __| |___ _ _ _  _ _ __  
 | |\/| / _ \ | || | '_ \/ _` / -_) ' \ || | '  \ 
 |_|  |_\___/_|\_, |_.__/\__,_\___|_||_\_,_|_|_|_|
               |__/                               

Molybdenum

Automated expectation updater for pixel tests.

Molybdenum parses failing test logs, extracts the "Actual pixels"
base64 images, decodes them, and writes the updated expectation PNGs
directly into the repository.

No more:
  • Copy-pasting base64 blobs
  • Manually downloading images
  • Renaming files by hand
  • Hunting through expectation folders

Just paste the logs and let Molybdenum handle the rest. 

Built for maintaining pixel tests in projects like Chromium/PDFium
where dependency rolls frequently invalidate expectation images.
"""

# --------------------- Currently supported components -------------------------
supported_repos = ["chromium"]
suite_folder_mapping = {"pdf_unittests": "pdf/test/data"}
supported_test_classes = suite_folder_mapping.keys()
# --------------------- Main Script --------------------------------------------

import base64
import os
import platform
import subprocess

try:
    # Python > 3.11
    import tomllib
except ModuleNotFoundError:
    # Python < 3.11
    import tomli as tomllib

# ------------------------------ Helpers ---------------------------------------
def configure():
    config_file = open("savedata.toml", "w")
    repo = input("Enter the name of the repo you are performing the roll in: ")
    if repo not in supported_repos:
        print(
            "Repo is currently not supported, you could try push a PR to"
            "add support, create an issue or wait till the repo is supported."
            "thank you for your patience!"
        )
    quit()
    print("\n" * 5)
    directory = input(
        "Enter the directory of your chromium checkout (src folder)."
    )
    print("\n" * 5)
    print(
        "# Supervision level determines how updates work: \
# 0. No supervision: Just writes images to your git worktree, but you can \
# revert if needed \
# 1. Confirm at the end: Confirms updates at the end of processing and prior to\
# writes \
# 2. Confirms for each individual image with a visual difference shown."
    )
    supervision_level_str = input("Enter the supervision level (0, 1, 2)")
    try:
        if int(supervision_level_str) < 0 or int(supervision_level_str) > 2:
            print("Supervision level can't be that high or low!")
            quit()
    except:
        print("Please input an integer!")
        quit()
    file = (
        '# Setting for which repo you are performing the "roll" in. \n repo = "'
        + repo
        + '"\n\n# Where that repository is present\ndirectory = "'
        + directory
        + '"\n\n# Supervision level determines how updates work:\n# 0. No \
        supervision: Just writes images to your git worktree, but you can \
        revert if needed\n# 1. Confirm at the end: Confirms updates at the end \
        of processing and prior to writes\n# 2. Confirms for each individual \
        image with a visual difference shown.\nsupervision_level = '
        + supervision_level_str
        + "\n"
    )
    config_file.write(file)
    config_file.close()


def get_logs():
    print("\n" * 20)
    print(
        "To get the error log, find the failing test suite and paste the error \
        here from the stdout section."
    )
    print(
        "The test suites currently supported are:", list(supported_test_classes)
    )
    test_suite = input("Enter the name of the test suite: ")
    print("\n" * 2)
    print("Opening logs.txt: ")
    with open("logs.txt", "w") as f:
        f.write("Paste logs here, save, and close the editor.")

    if platform.system() == "Windows":
        os.startfile("logs.txt")
    elif platform.system() == "Darwin":  # macOS
        subprocess.run(["open", "logs.txt"])
    else:  # Linux
        subprocess.run(["xdg-open", "logs.txt"])

    input("Press Enter after saving logs.txt...")

    with open("logs.txt") as f:
        error_log = f.read()

    count = error_log.count("Actual pixels (open in browser):")
    print("Found a total of", count, "immage differences.")
    print("\n" * 2)
    input("Press enter to begin updates, or control-C to exit: ")

    return error_log, test_suite, count


# ------------------------------------------------------------------------------


# ------------------------------- Main -----------------------------------------
def main():
    with open("savedata.toml", "rb") as f:
        config = tomllib.load(f)

    print(
        "  __  __     _      _        _                    \n \
  |  \/  |___| |_  _| |__  __| |___ _ _ _  _ _ __  \n \
  | |\/| / _ \ | || | '_ \/ _` / -_) ' \ || | '  \ \n \
  |_|  |_\___/_|\_, |_.__/\__,_\___|_||_\_,_|_|_|_| \n \
              |__/                               "
    )

    print("Loading Molybdenum with config: ", config)

    change_config = not (
        input("Would you like to go ahead with this configuration?").lower()
        == "y"
    )

    if change_config:
        configure()
        with open("savedata.toml", "rb") as f:
            config = tomllib.load(f)
        print("Loading Molybdenum with config: ", config)
        if input("Press enter to continue or exit to quit.") == "exit":
            quit()

    error_log, test_suite, count = get_logs()

    lines = error_log.splitlines()
    processed_count = 0
    for i, line in enumerate(lines):
        if "Actual pixels (open in browser):" in line:
            if i + 6 < len(lines):
                processed_count += 1
                base64_line = lines[i + 1]
                # Image name always remains 6 lines after the "Actual pixels"
                # line.
                img_name_line = lines[i + 6]
                img_name = img_name_line.split("(Reference: ")[1].split(")")[0]
                prefix = "data:image/png;base64,"
                base64_data = base64_line.removeprefix(prefix)
                image_bytes = base64.b64decode(base64_data)
                output = os.path.join(
                    config["directory"],
                    suite_folder_mapping[test_suite],
                    img_name,
                )
                with open(output, "wb") as f:
                    f.write(image_bytes)
                print(
                    "["
                    + str(processed_count)
                    + "/"
                    + str(count)
                    + "] - "
                    + img_name
                )

    print("Process complete with: " + str(count) + " image differences fixed!")


if __name__ == "__main__":
    main()
