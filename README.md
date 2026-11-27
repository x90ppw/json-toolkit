# json-toolkit

A tiny, zero-dependency JSON command line toolkit written in Python,
inspired by the everyday parts of `jq`.

## Usage

```bash
python3 jsontool.py format   data.json            # pretty print
python3 jsontool.py minify   data.json            # compact output
python3 jsontool.py get      data.json user.name  # extract a dotted path
python3 jsontool.py keys     data.json            # list top-level keys
python3 jsontool.py validate data.json            # check validity
cat data.json | python3 jsontool.py format -      # read from stdin
```

Requires Python 3.8+. No third-party packages.
