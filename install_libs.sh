#!/bin/bash
python_version=$(python3 -c "import sys; print(sys.version_info.minor)")
if [ "$python_version" -lt 11 ]; then
    pip install tomli
fi
# Black is already present from depot_tools
