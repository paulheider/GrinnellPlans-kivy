import pytest

from main import PlansHTMLParser

def test_initial_plan_buffer_is_empty():
    plans_parser = PlansHTMLParser()
    assert plans_parser.plan_buffer == ''
