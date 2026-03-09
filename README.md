# Molybdenum

Automated expectation updater for pixel tests.

**Molybdenum** parses failing test logs, extracts base64-encoded *Actual pixel outputs* , decodes them, and writes updated expectation images directly into your repository.

No more manually copying base64 blobs or hunting through test directories.

## Why this exists

When pixel tests fail after a dependency roll, updating expectations often looks like this:

1. Run tests
2. Scroll through logs
3. Click **Actual pixels**
4. Copy base64 image
5. Decode it
6. Rename file
7. Move it into the correct expectation folder
8. Repeat dozens of times

This process is slow, repetitive, and error-prone.

**Molybdenum automates the entire workflow.**

Paste the logs once and the expectation images update automatically.

## Features

* Parses failing pixel test logs
* Extracts base64 image data
* Decodes PNG images automatically
* Writes images to the correct expectation directories
* Handles dozens or hundreds of failures instantly
* ~0.1ms per image — a 6000 image roll completes in under a second

## Example

Instead of manually updating 100+ expectation images:

```
Actual pixels (open in browser):
data:image/png;base64,iVBORw0KGgoAAAANSUhEUg...
```

Run Molybdenum and it will automatically:

```
[1/156] text_selection/hello_world_draw_find_result_0_mac.png
[2/156] caret/hello_world_caret_mac.png
...
[156/156] caret/hello_world_caret_text_selection_all_mac.png
```

All images are written directly to the repository and ready for commit.

## Usage

### 1. Install dependencies

```bash
./install.sh
```

### 2. Run your tests

Run the test suite on Chromium and locate the failing logs.

### 3. Configuration

To run the configuration wizard:

```bash
./molyb --config
```

Refer to the configuration section for more details

### 4. Start Molybdenum

```bash
./molyb
```

Or directly:

```bash
python3 main.py
```

### 5. Paste logs

Molybdenum will open `logs.txt`. Paste the failing test output and save the file.

### 6. Update expectations

Press enter and Molybdenum will automatically decode and write all updated expectation images.

### Supported Repositories

Currently supported:

* Chromium

Test suites:

* `pdf_unittests`

Support for additional repositories and test suites can be added easily, and is in progress.

In-progress additions:

* PDFium, PDFium Embeddertests

Issues can be filed to request support for any other test suites in Chromium or its sub-repos.

## Configuration

Configuration is stored in:

```
savedata.toml
```

Example:

```toml
repo = "chromium"
directory = "/path/to/chromium/src"
supervision_level = 0
```

### Supervision Levels

| Level | Behavior                                             |
| ----- | ---------------------------------------------------- |
| 0     | Automatically update all images without confirmation |
| 1     | Review each image with a visual diff before writing  |

## Why the name?

**Molybdenum (Mo, element 42)** sits directly below **Chromium (Cr, element 24)** in Group 6 of the periodic table — same group, next period down.

Molybdenum is often used as a support material in industrial chemistry — it makes other reactions work better without being the star of the show. Which is exactly what this tool does: it supports Chromium development without being part of Chromium itself.

In steel alloys, Molybdenum strengthens and stabilizes — fitting, since this tool stabilizes your test suite after a roll destabilizes it.

## Status

Beta — built to simplify expectation updates during dependency rolls.

## License

MIT
