from src.preprocess import TextPreprocessor


class TestStripHtmlTags:
    def setup_method(self):
        self.tp = TextPreprocessor()

    def test_removes_simple_tags(self):
        self.tp.strip_html_tags("<p>hello</p>")
        assert self.tp.text == "hello"

    def test_removes_nested_tags(self):
        self.tp.strip_html_tags("<div><b>nested</b></div>")
        assert self.tp.text == "nested"

    def test_removes_tags_with_attributes(self):
        self.tp.strip_html_tags('<a href="link">click</a>')
        assert self.tp.text == "click"

    def test_returns_self_for_chaining(self):
        result = self.tp.strip_html_tags("<p>a</p>")
        assert result is self.tp

    def test_plain_text_unchanged(self):
        self.tp.strip_html_tags("hello world")
        assert self.tp.text == "hello world"

    def test_empty_string(self):
        self.tp.strip_html_tags("")
        assert self.tp.text == ""

    def test_only_tags(self):
        self.tp.strip_html_tags("<p></p>")
        assert self.tp.text == ""


class TestReplacePhoneNumbers:
    def setup_method(self):
        self.tp = TextPreprocessor()

    def test_us_format_with_dashes(self):
        self.tp.replace_phone_numbers("call 123-456-7890 now")
        assert "Phone Number" in self.tp.text

    def test_us_format_with_parentheses(self):
        self.tp.replace_phone_numbers("call (123) 456-7890 now")
        assert "Phone Number" in self.tp.text

    def test_with_country_code(self):
        self.tp.replace_phone_numbers("call +1-123-456-7890 now")
        assert "Phone Number" in self.tp.text

    def test_with_dots(self):
        self.tp.replace_phone_numbers("call 123.456.7890 now")
        assert "Phone Number" in self.tp.text

    def test_short_number(self):
        self.tp.replace_phone_numbers("call 555-1234 now")
        assert "Phone Number" in self.tp.text

    def test_no_phone_number(self):
        self.tp.replace_phone_numbers("hello world")
        assert self.tp.text == "hello world"

    def test_empty_string(self):
        self.tp.replace_phone_numbers("")
        assert self.tp.text == ""

    def test_returns_self_for_chaining(self):
        result = self.tp.replace_phone_numbers("123-456-7890")
        assert result is self.tp


class TestReplaceUrls:
    def setup_method(self):
        self.tp = TextPreprocessor()

    def test_http_url(self):
        self.tp.replace_urls("visit http://example.com now")
        assert "URL" in self.tp.text

    def test_https_url(self):
        self.tp.replace_urls("visit https://example.com now")
        assert "URL" in self.tp.text

    def test_url_with_path(self):
        self.tp.replace_urls("go to https://site.com/page?q=1")
        assert "URL" in self.tp.text

    def test_no_url(self):
        self.tp.replace_urls("hello world")
        assert self.tp.text == "hello world"

    def test_empty_string(self):
        self.tp.replace_urls("")
        assert self.tp.text == ""

    def test_returns_self_for_chaining(self):
        result = self.tp.replace_urls("http://example.com")
        assert result is self.tp


class TestNormalizeWhitespace:
    def setup_method(self):
        self.tp = TextPreprocessor()

    def test_multiple_spaces(self):
        self.tp.normalize_whitespace("hello    world")
        assert self.tp.text == "hello world"

    def test_tabs_and_newlines(self):
        self.tp.normalize_whitespace("hello\t\tworld\n\nfoo")
        assert self.tp.text == "hello world foo"

    def test_leading_trailing_spaces(self):
        self.tp.normalize_whitespace("   hello world   ")
        assert self.tp.text == "hello world"

    def test_single_word(self):
        self.tp.normalize_whitespace("hello")
        assert self.tp.text == "hello"

    def test_empty_string(self):
        self.tp.normalize_whitespace("")
        assert self.tp.text == ""

    def test_returns_self_for_chaining(self):
        result = self.tp.normalize_whitespace("a  b")
        assert result is self.tp


class TestToLowercase:
    def setup_method(self):
        self.tp = TextPreprocessor()

    def test_uppercase(self):
        self.tp.to_lowercase("HELLO WORLD")
        assert self.tp.text == "hello world"

    def test_mixed_case(self):
        self.tp.to_lowercase("Hello World")
        assert self.tp.text == "hello world"

    def test_already_lower(self):
        self.tp.to_lowercase("hello world")
        assert self.tp.text == "hello world"

    def test_empty_string(self):
        self.tp.to_lowercase("")
        assert self.tp.text == ""

    def test_returns_self_for_chaining(self):
        result = self.tp.to_lowercase("ABC")
        assert result is self.tp


class TestRemoveSpecialCharacters:
    def setup_method(self):
        self.tp = TextPreprocessor()

    def test_removes_listed_chars(self):
        self.tp.remove_special_characters("~[]'<>(){}\\/!#%^@+=-;.")
        assert self.tp.text == ""

    def test_preserves_dollar_and_question(self):
        self.tp.remove_special_characters("hello$world?")
        assert self.tp.text == "hello$world?"

    def test_preserves_alphanumeric(self):
        self.tp.remove_special_characters("hello123")
        assert self.tp.text == "hello123"

    def test_preserves_whitespace(self):
        self.tp.remove_special_characters("a @ b")
        assert self.tp.text == "a  b"

    def test_empty_string(self):
        self.tp.remove_special_characters("")
        assert self.tp.text == ""

    def test_returns_self_for_chaining(self):
        result = self.tp.remove_special_characters("a~b")
        assert result is self.tp


class TestReplaceEmojis:
    def setup_method(self):
        self.tp = TextPreprocessor()

    def test_replaces_money_bag(self):
        self.tp.replace_emojis("💰")
        assert ":money_bag:" in self.tp.text

    def test_replaces_multiple_emojis(self):
        self.tp.replace_emojis("😀👍")
        assert ":grinning_face:" in self.tp.text
        assert ":thumbs_up:" in self.tp.text

    def test_preserves_plain_text(self):
        self.tp.replace_emojis("hello world")
        assert self.tp.text == "hello world"

    def test_empty_string(self):
        self.tp.replace_emojis("")
        assert self.tp.text == ""

    def test_returns_self_for_chaining(self):
        result = self.tp.replace_emojis("💰")
        assert result is self.tp


class TestReplaceEmails:
    def setup_method(self):
        self.tp = TextPreprocessor()

    def test_replaces_simple_email(self):
        self.tp.replace_emails("contact user@example.com now")
        assert "EMAIL" in self.tp.text

    def test_replaces_email_with_dots(self):
        self.tp.replace_emails("user.name@sub.example.co.uk")
        assert "EMAIL" in self.tp.text

    def test_replaces_email_with_plus(self):
        self.tp.replace_emails("user+tag@example.com")
        assert "EMAIL" in self.tp.text

    def test_no_email(self):
        self.tp.replace_emails("hello world")
        assert self.tp.text == "hello world"

    def test_empty_string(self):
        self.tp.replace_emails("")
        assert self.tp.text == ""

    def test_returns_self_for_chaining(self):
        result = self.tp.replace_emails("a@b.com")
        assert result is self.tp

