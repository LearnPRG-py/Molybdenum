# Fromatting guideliens

## Auto formatting

This repo uses black for auto-formatting which can be installed by running:

```bash
pip install black
```

and can be run by using

```bash
black -l 80 your_file.py
```

By default, black is already present in the chromium depot_tools.

As shown by the command, all lines are (by default) wrapped to 80 characters.

Instead of running for all files however you could use the format.sh file.

## Naming guides and Manual Formatting

All functions and variables are by default named in snake_case. For instance:

```python
# Naming example

def my_function():
    my_variable = 7
    return my_variable + 2
```

All imports not in the standard library should also be in alphabetical order and should be populated in deps.txt
