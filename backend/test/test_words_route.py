import json
from types import SimpleNamespace

import pytest

from ..app.routes.words import get_meanings_by_word


def test_get_meanings():
    result = get_meanings_by_word("read")

    assert result.status >= 3
    assert result[0].priority == 1
