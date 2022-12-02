import json
from types import SimpleNamespace

import pytest

from ..app.utils.mongo import get_meanings_by_id


def test_get_meanings():
    result = get_meanings_by_id("read")

    assert len(result) >= 3
    assert result[0].priority == 1
