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
