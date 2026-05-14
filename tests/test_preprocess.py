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
