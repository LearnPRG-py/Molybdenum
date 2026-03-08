#!/bin/bash
TEST_MODE=false
OTHER_ARGS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    -t|--test)
      TEST_MODE=true
      shift
      ;;
    *)
      OTHER_ARGS+=("$1")
      shift
      ;;
  esac
done

if [ "$TEST_MODE" = true ]; then
  python3 tests.py
else
  python3 main.py "${OTHER_ARGS[@]}"
fi
