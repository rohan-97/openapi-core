import pytest

from openapi_core.spec.paths import SpecPath
from openapi_core.templating.media_types.exceptions import MediaTypeNotFound
from openapi_core.templating.media_types.finders import MediaTypeFinder
from openapi_core.testing import MockResponse


class TestMediaTypes:
    @pytest.fixture(scope="class")
    def spec(self):
        return {
            "application/json": {"schema": {"type": "object"}},
            "text/*": {"schema": {"type": "object"}},
        }

    @pytest.fixture(scope="class")
    def content(self, spec):
        return SpecPath.from_spec(spec)

    @pytest.fixture(scope="class")
    def finder(self, content):
        return MediaTypeFinder(content)

    def test_exact(self, finder, content):
        response = MockResponse("", mimetype="application/json")

        _, mimetype = finder.find(response)
        assert mimetype == "application/json"

    def test_match(self, finder, content):
        response = MockResponse("", mimetype="text/html")

        _, mimetype = finder.find(response)
        assert mimetype == "text/*"

    def test_not_found(self, finder, content):
        response = MockResponse("", mimetype="unknown")

        with pytest.raises(MediaTypeNotFound):
            finder.find(response)

    def test_missing(self, finder, content):
        response = MockResponse("", mimetype=None)

        with pytest.raises(MediaTypeNotFound):
            finder.find(response)
