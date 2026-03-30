from textwrap import dedent
import pytest

def test_import() -> None:
    import amzn_awesome_trustworthy_mars  # type: ignore # noqa: F401
