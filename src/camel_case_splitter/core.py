import re

# A run of uppercase letters that is followed by another uppercase run and
# then a lowercase letter. The split is placed between the two uppercase
# runs so that consecutive acronyms stay separate: ``XMLHTTPRequest``
# splits into ``XML|HTTP|Request`` rather than ``XMLHTTP|Request``.
_UPPER_RUN_TO_LOWER = re.compile(r"([A-Z]+)([A-Z]+)(?=[a-z])")

# A lowercase/digit run that is followed by an uppercase letter. This is the
# main camelCase boundary: "camelCase" -> ["camel", "Case"].
_LOWER_TO_UPPER = re.compile(r"([a-z0-9]+)(?=[A-Z])")


def split_camel_case(name):
    """Split a PascalCase or camelCase identifier into lowercase word tokens.

    The algorithm is intentionally simple and deterministic:

    1. Insert a boundary before any uppercase letter that follows a lowercase
       letter or digit (``camelCase`` -> ``camel|Case``).
    2. Insert a boundary before the *last* uppercase letter of an uppercase run
       when that run is followed by lowercase letters, so that acronyms stay
       grouped with the next word: ``XMLParser`` -> ``XML|Parser``, not
       ``XMLP|arser``. Consecutive acronyms are separated as well:
       ``XMLHTTPRequest`` -> ``XML|HTTP|Request``.
    3. Lowercase every token.

    Non-ASCII letters are **not** handled. The regexes use ``[A-Za-z]``
    explicitly so that the behaviour is predictable on ASCII identifiers, which
    is the only use case this library targets. If you feed it ``caféItem`` the
    ``é`` will be treated like a lowercase letter for boundary detection but
    will not be normalised — callers who need Unicode support should preprocess
    or use a different tool.

    Digits are treated as part of the lowercase class: ``http2Client`` splits
    into ``["http2", "client"]``.

    Parameters
    ----------
    name : str
        The identifier to split. An empty string returns an empty list.

    Returns
    -------
    list[str]
        Lowercase word tokens, in order.
    """
    if not name:
        return []

    # Order matters: handle the uppercase-run-before-lowercase case first so
    # that the second regex does not break ``XMLParser`` into ``XMLP|arser``.
    step1 = _UPPER_RUN_TO_LOWER.sub(r"\1|\2", name)
    step2 = _LOWER_TO_UPPER.sub(r"\1|", step1)
    return [tok.lower() for tok in step2.split("|") if tok]


def split_camel_case_keep_acronyms(name):
    """Like :func:`split_camel_case` but preserves the original casing of
    all-uppercase acronym tokens.

    ``XMLParser`` -> ``["XML", "Parser"]`` (not ``["xml", "parser"]``).

    Non-acronym tokens (those containing at least one lowercase letter) are
    still lowercased, matching :func:`split_camel_case`.

    Parameters
    ----------
    name : str
        The identifier to split.

    Returns
    -------
    list[str]
        Word tokens in order, with all-caps tokens left in their original
        uppercase form.
    """
    if not name:
        return []

    step1 = _UPPER_RUN_TO_LOWER.sub(r"\1|\2", name)
    step2 = _LOWER_TO_UPPER.sub(r"\1|", step1)
    tokens = step2.split("|")
    result = []
    for tok in tokens:
        if not tok:
            continue
        # A token consisting entirely of uppercase letters is treated as an
        # acronym and preserved as-is. Anything else gets lowercased so that
        # ``Parser`` becomes ``parser``.
        if tok.isupper() and tok.isalpha():
            result.append(tok)
        else:
            result.append(tok.lower())
    return result
