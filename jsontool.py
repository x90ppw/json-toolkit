#!/usr/bin/env python3
"""jsontool - a tiny JSON command line toolkit (inspired by jq).

Usage:
  python3 jsontool.py format   data.json          # pretty print
  python3 jsontool.py minify   data.json          # compact output
  python3 jsontool.py get      data.json user.name  # extract a dotted path
  python3 jsontool.py keys     data.json          # list top-level keys
  python3 jsontool.py validate data.json          # check validity
Input can also come from stdin:  cat data.json | python3 jsontool.py format -
"""
import json, sys

def load(src):
    if src == "-":
        return json.load(sys.stdin)
    with open(src, encoding="utf-8") as f:
        return json.load(f)

def cmd_format(data, _arg):
    print(json.dumps(data, ensure_ascii=False, indent=2))

def cmd_minify(data, _arg):
    print(json.dumps(data, ensure_ascii=False, separators=(",", ":")))

def cmd_get(data, path):
    cur = data
    for part in path.split("."):
        if isinstance(cur, list):
            cur = cur[int(part)]
        else:
            cur = cur[part]
    print(json.dumps(cur, ensure_ascii=False) if not isinstance(cur, str) else cur)

def cmd_keys(data, _arg):
    if isinstance(data, dict):
        print("\n".join(data.keys()))
    elif isinstance(data, list):
        print(f"list of {len(data)} items")
    else:
        print(type(data).__name__)

def cmd_validate(_data, _arg):
    print("valid JSON")

COMMANDS = {"format": cmd_format, "minify": cmd_minify, "get": cmd_get,
            "keys": cmd_keys, "validate": cmd_validate}

def main(argv):
    if len(argv) < 3 or argv[1] not in COMMANDS:
        print(__doc__)
        return 2
    cmd, src = argv[1], argv[2]
    arg = argv[3] if len(argv) > 3 else ""
    if cmd == "get" and not arg:
        print("get needs a dotted path, e.g. user.name or items.0.id")
        return 2
    try:
        data = load(src)
    except (OSError, json.JSONDecodeError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    try:
        COMMANDS[cmd](data, arg)
    except (KeyError, IndexError, ValueError) as e:
        print(f"error: path not found ({e})", file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
