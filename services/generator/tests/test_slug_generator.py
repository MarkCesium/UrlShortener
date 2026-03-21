import string

from src.core.services.slug import SlugGenerator

ALPHABET = set(string.ascii_letters + string.digits)


class TestSlugGenerator:
    def test_length_is_six(self) -> None:
        slug = SlugGenerator.generate()
        assert len(slug) == 6

    def test_only_alphanumeric_chars(self) -> None:
        slug = SlugGenerator.generate()
        assert all(c in ALPHABET for c in slug)

    def test_generates_unique_slugs(self) -> None:
        slugs = {SlugGenerator.generate() for _ in range(1000)}
        assert len(slugs) == 1000
