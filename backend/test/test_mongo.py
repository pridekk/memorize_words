import json
from types import SimpleNamespace

import pytest

from ..app.utils.mongo import get_meanings_by_id, get_words_by_query, increase_delete_count


def test_get_meanings():
    result = get_meanings_by_id("read")

    assert len(result) >= 3
    assert result[0].priority == 1


def test_get_words():
    result = get_words_by_query("R")

    assert len(result) >= 2


def test_increase_delete_count():
    increase_delete_count("read", "3b241101-e2bb-4255-8caf-4136c566a962")