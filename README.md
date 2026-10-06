# Camel Case Splitter

Splits PascalCase and camelCase identifiers into lowercase word tokens. A second function preserves the original casing of all-caps acronym tokens.

## Usage

```python
from camel_case_splitter import split_camel_case, split_camel_case_keep_acronyms

split_camel_case("camelCase")            # -> ["camel", "case"]
split_camel_case("XMLParser")            # -> ["xml", "parser"]
split_camel_case_keep_acronyms("XMLParser")  # -> ["XML", "parser"]
```

## Why

Indexing identifiers for search or generating human-readable labels from code requires breaking camelCase apart. The obvious approach — splitting before every uppercase letter — mangles acronyms: `XMLParser` becomes `["xmlp", "arser"]`. This library inserts the boundary before the *last* uppercase letter of a run, so `XMLParser` splits into `["xml", "parser"]`.

## Edge cases

- **Digits** are treated as part of the lowercase class. `http2Client` splits into `["http2", "client"]`. In `split_camel_case_keep_acronyms`, a token containing a digit is lowercased even if the letters are uppercase, so `HTTP2Client` yields `["http2", "client"]` — acronym preservation only applies to tokens that are entirely uppercase ASCII letters.
- **Non-ASCII** is not supported. The regexes use `[A-Za-z]` explicitly. Feed the library ASCII identifiers or preprocess first.
- **Empty input** returns an empty list.

## Design notes

The window stores values eagerly rather than keeping running aggregates. Running
sums drift with floating point over long streams, and recomputing from a small
buffer is cheap enough that the drift is not worth the speed.

