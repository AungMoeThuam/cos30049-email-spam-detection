from src.preprocess import TextPreprocessor


class TestStripHtmlTags:
    def test_removes_simple_tags(self):
        tp = TextPreprocessor("<p>hello</p>")
        tp.strip_html_tags()
        assert tp.text == "hello"

    def test_removes_nested_tags(self):
        tp = TextPreprocessor("<div><b>nested</b></div>")
        tp.strip_html_tags()
        assert tp.text == "nested"

    def test_removes_tags_with_attributes(self):
        tp = TextPreprocessor('<a href="link">click</a>')
        tp.strip_html_tags()
        assert tp.text == "click"

    def test_returns_self_for_chaining(self):
        tp = TextPreprocessor("<p>a</p>")
        result = tp.strip_html_tags()
        assert result is tp

    def test_plain_text_unchanged(self):
        tp = TextPreprocessor("hello world")
        tp.strip_html_tags()
        assert tp.text == "hello world"

    def test_empty_string(self):
        tp = TextPreprocessor("")
        tp.strip_html_tags()
        assert tp.text == ""

    def test_only_tags(self):
        tp = TextPreprocessor("<p></p>")
        tp.strip_html_tags()
        assert tp.text == ""


class TestReplacePhoneNumbers:
    def test_us_format_with_dashes(self):
        tp = TextPreprocessor("call 123-456-7890 now")
        tp.replace_phone_numbers()
        assert "Phone Number" in tp.text

    def test_us_format_with_parentheses(self):
        tp = TextPreprocessor("call (123) 456-7890 now")
        tp.replace_phone_numbers()
        assert "Phone Number" in tp.text

    def test_with_country_code(self):
        tp = TextPreprocessor("call +1-123-456-7890 now")
        tp.replace_phone_numbers()
        assert "Phone Number" in tp.text

    def test_with_dots(self):
        tp = TextPreprocessor("call 123.456.7890 now")
        tp.replace_phone_numbers()
        assert "Phone Number" in tp.text

    def test_short_number(self):
        tp = TextPreprocessor("call 555-1234 now")
        tp.replace_phone_numbers()
        assert "Phone Number" in tp.text

    def test_no_phone_number(self):
        tp = TextPreprocessor("hello world")
        tp.replace_phone_numbers()
        assert tp.text == "hello world"

    def test_empty_string(self):
        tp = TextPreprocessor("")
        tp.replace_phone_numbers()
        assert tp.text == ""

    def test_returns_self_for_chaining(self):
        tp = TextPreprocessor("123-456-7890")
        result = tp.replace_phone_numbers()
        assert result is tp


class TestReplaceUrls:
    def test_http_url(self):
        tp = TextPreprocessor("visit http://example.com now")
        tp.replace_urls()
        assert "URL" in tp.text

    def test_https_url(self):
        tp = TextPreprocessor("visit https://example.com now")
        tp.replace_urls()
        assert "URL" in tp.text

    def test_url_with_path(self):
        tp = TextPreprocessor("go to https://site.com/page?q=1")
        tp.replace_urls()
        assert "URL" in tp.text

    def test_no_url(self):
        tp = TextPreprocessor("hello world")
        tp.replace_urls()
        assert tp.text == "hello world"

    def test_empty_string(self):
        tp = TextPreprocessor("")
        tp.replace_urls()
        assert tp.text == ""

    def test_returns_self_for_chaining(self):
        tp = TextPreprocessor("http://example.com")
        result = tp.replace_urls()
        assert result is tp


class TestNormalizeWhitespace:
    def test_multiple_spaces(self):
        tp = TextPreprocessor("hello    world")
        tp.normalize_whitespace()
        assert tp.text == "hello world"

    def test_tabs_and_newlines(self):
        tp = TextPreprocessor("hello\t\tworld\n\nfoo")
        tp.normalize_whitespace()
        assert tp.text == "hello world foo"

    def test_leading_trailing_spaces(self):
        tp = TextPreprocessor("   hello world   ")
        tp.normalize_whitespace()
        assert tp.text == "hello world"

    def test_single_word(self):
        tp = TextPreprocessor("hello")
        tp.normalize_whitespace()
        assert tp.text == "hello"

    def test_empty_string(self):
        tp = TextPreprocessor("")
        tp.normalize_whitespace()
        assert tp.text == ""

    def test_returns_self_for_chaining(self):
        tp = TextPreprocessor("a  b")
        result = tp.normalize_whitespace()
        assert result is tp


class TestToLowercase:
    def test_uppercase(self):
        tp = TextPreprocessor("HELLO WORLD")
        tp.to_lowercase()
        assert tp.text == "hello world"

    def test_mixed_case(self):
        tp = TextPreprocessor("Hello World")
        tp.to_lowercase()
        assert tp.text == "hello world"

    def test_already_lower(self):
        tp = TextPreprocessor("hello world")
        tp.to_lowercase()
        assert tp.text == "hello world"

    def test_empty_string(self):
        tp = TextPreprocessor("")
        tp.to_lowercase()
        assert tp.text == ""

    def test_returns_self_for_chaining(self):
        tp = TextPreprocessor("ABC")
        result = tp.to_lowercase()
        assert result is tp


class TestRemoveSpecialCharacters:
    def test_removes_listed_chars(self):
        tp = TextPreprocessor("~[]'<>(){}\\/!#%^@+=-;.")
        tp.remove_special_characters()
        assert tp.text == ""

    def test_preserves_dollar_and_question(self):
        tp = TextPreprocessor("hello$world?")
        tp.remove_special_characters()
        assert tp.text == "hello$world?"

    def test_preserves_alphanumeric(self):
        tp = TextPreprocessor("hello123")
        tp.remove_special_characters()
        assert tp.text == "hello123"

    def test_preserves_whitespace(self):
        tp = TextPreprocessor("a @ b")
        tp.remove_special_characters()
        assert tp.text == "a  b"

    def test_empty_string(self):
        tp = TextPreprocessor("")
        tp.remove_special_characters()
        assert tp.text == ""

    def test_returns_self_for_chaining(self):
        tp = TextPreprocessor("a~b")
        result = tp.remove_special_characters()
        assert result is tp


class TestReplaceEmojis:
    def test_replaces_money_bag(self):
        tp = TextPreprocessor("💰")
        tp.replace_emojis()
        assert ":money_bag:" in tp.text

    def test_replaces_multiple_emojis(self):
        tp = TextPreprocessor("😀👍")
        tp.replace_emojis()
        assert ":grinning_face:" in tp.text
        assert ":thumbs_up:" in tp.text

    def test_preserves_plain_text(self):
        tp = TextPreprocessor("hello world")
        tp.replace_emojis()
        assert tp.text == "hello world"

    def test_empty_string(self):
        tp = TextPreprocessor("")
        tp.replace_emojis()
        assert tp.text == ""

    def test_returns_self_for_chaining(self):
        tp = TextPreprocessor("💰")
        result = tp.replace_emojis()
        assert result is tp


class TestReplaceEmails:
    def test_replaces_simple_email(self):
        tp = TextPreprocessor("contact user@example.com now")
        tp.replace_emails()
        assert "EMAIL" in tp.text

    def test_replaces_email_with_dots(self):
        tp = TextPreprocessor("user.name@sub.example.co.uk")
        tp.replace_emails()
        assert "EMAIL" in tp.text

    def test_replaces_email_with_plus(self):
        tp = TextPreprocessor("user+tag@example.com")
        tp.replace_emails()
        assert "EMAIL" in tp.text

    def test_no_email(self):
        tp = TextPreprocessor("hello world")
        tp.replace_emails()
        assert tp.text == "hello world"

    def test_empty_string(self):
        tp = TextPreprocessor("")
        tp.replace_emails()
        assert tp.text == ""

    def test_returns_self_for_chaining(self):
        tp = TextPreprocessor("a@b.com")
        result = tp.replace_emails()
        assert result is tp


class TestReplacePercentages:
    def test_percentage_without_space(self):
        tp = TextPreprocessor("increase 50%")
        tp.replace_percentages()
        assert "PERCENTAGE" in tp.text

    def test_percentage_with_space(self):
        tp = TextPreprocessor("increase 50 %")
        tp.replace_percentages()
        assert "PERCENTAGE" in tp.text

    def test_decimal_percentage(self):
        tp = TextPreprocessor("rate 12.5%")
        tp.replace_percentages()
        assert "PERCENTAGE" in tp.text

    def test_no_percentage(self):
        tp = TextPreprocessor("hello world")
        tp.replace_percentages()
        assert tp.text == "hello world"

    def test_empty_string(self):
        tp = TextPreprocessor("")
        tp.replace_percentages()
        assert tp.text == ""

    def test_returns_self_for_chaining(self):
        tp = TextPreprocessor("50%")
        result = tp.replace_percentages()
        assert result is tp


class TestReplaceNumbers:
    def test_replaces_number(self):
        tp = TextPreprocessor("count 42")
        tp.replace_numbers()
        assert "NUMBER" in tp.text

    def test_replaces_multiple_numbers(self):
        tp = TextPreprocessor("10 items cost 25 dollars")
        tp.replace_numbers()
        assert "NUMBER" in tp.text
        assert tp.text.count("NUMBER") == 2

    def test_no_number(self):
        tp = TextPreprocessor("hello world")
        tp.replace_numbers()
        assert tp.text == "hello world"

    def test_empty_string(self):
        tp = TextPreprocessor("")
        tp.replace_numbers()
        assert tp.text == ""

    def test_returns_self_for_chaining(self):
        tp = TextPreprocessor("42")
        result = tp.replace_numbers()
        assert result is tp
