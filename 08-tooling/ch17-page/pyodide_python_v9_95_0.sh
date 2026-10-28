#!/bin/sh
# Wrapper: the interpreter the page-data builder is given as <python>. Needs env PYODIDE_NODE_PATH (the folder holding node_modules/pyodide 0.28.2).
D=$(cd "$(dirname "$0")" && pwd)
exec env NODE_PATH="$PYODIDE_NODE_PATH" node "$D/pyodide_python_v9_95_0.js" "$D/../../03-materials/ch17/assets" "$D/pywheels_v9_95_0.json" "$@"
