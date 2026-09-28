import unittest

from camel_case_splitter import split_camel_case, split_camel_case_keep_acronyms


class TestSplitCamelCase(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual(split_camel_case(""), [])

    def test_single_lowercase_word(self):
        self.assertEqual(split_camel_case("hello"), ["hello"])

    def test_single_uppercase_word(self):
        self.assertEqual(split_camel_case("HELLO"), ["hello"])

    def test_camel_case(self):
        self.assertEqual(split_camel_case("camelCase"), ["camel", "case"])

    def test_pascal_case(self):
        self.assertEqual(split_camel_case("PascalCase"), ["pascal", "case"])

    def test_acronym_followed_by_word(self):
        # The key edge case: XMLParser should not become ["xmlp", "arser"].
        self.assertEqual(split_camel_case("XMLParser"), ["xml", "parser"])

    def test_multiple_acronyms(self):
        self.assertEqual(
            split_camel_case("XMLHTTPRequest"), ["xmlhttp", "request"]
        )

    def test_digit_followed_by_uppercase(self):
        self.assertEqual(split_camel_case("http2Client"), ["http2", "client"])

    def test_uppercase_followed_by_digit(self):
        self.assertEqual(split_camel_case("Version2Update"), ["version2", "update"])

    def test_single_character_tokens(self):
        self.assertEqual(split_camel_case("aB"), ["a", "b"])

    def test_all_uppercase_single_word(self):
        self.assertEqual(split_camel_case("URL"), ["url"])

    def test_consecutive_uppercase_at_end(self):
        self.assertEqual(split_camel_case("myURL"), ["my", "url"])


class TestSplitCamelCaseKeepAcronyms(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual(split_camel_case_keep_acronyms(""), [])

    def test_acronym_preserved(self):
        self.assertEqual(
            split_camel_case_keep_acronyms("XMLParser"), ["XML", "parser"]
        )

    def test_multiple_acronyms_preserved(self):
        self.assertEqual(
            split_camel_case_keep_acronyms("XMLHTTPRequest"),
            ["XMLHTTP", "request"],
        )

    def test_trailing_acronym_preserved(self):
        self.assertEqual(
            split_camel_case_keep_acronyms("myURL"), ["my", "URL"]
        )

    def test_no_acronyms_lowercases_everything(self):
        self.assertEqual(
            split_camel_case_keep_acronyms("camelCase"), ["camel", "case"]
        )

    def test_single_uppercase_word_preserved(self):
        self.assertEqual(split_camel_case_keep_acronyms("URL"), ["URL"])

    def test_digit_in_token(self):
        # "HTTP2" contains a digit so it is not all-alpha-uppercase; it gets
        # lowercased. This documents the chosen behaviour rather than claiming
        # acronym detection for alphanumeric tokens.
        self.assertEqual(
            split_camel_case_keep_acronyms("HTTP2Client"), ["http2", "client"]
        )


if __name__ == "__main__":
    unittest.main()
