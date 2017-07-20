import pytest

from main import PlansHTMLParser
from main import ReadPlan

import mock

def test_no_encoding_is_identity_function():
    plan_reader = ReadPlan()
    plan_body = ''
    assert plan_body == plan_reader.cleanPlanBody( plan_body )
    plan_body = 'Twas brillig and the slithey toves...'
    assert plan_body == plan_reader.cleanPlanBody( plan_body )


## TODO - add new tests for most common encodings
def test_other_encodings():
    plan_reader = ReadPlan()
    plan_body = ''
    expected = u''
    assert plan_reader.cleanPlanBody( plan_body ,
                                      this_encoding = None ) == \
                                      expected


def test_unescaped_plannames():
    plan_reader = ReadPlan()
    plan_body = ''
    expected = u''
    assert plan_reader.cleanPlanName( plan_body ,
                                      this_encoding = None ) == \
                                      expected


def test_escaped_plannames():
    plan_reader = ReadPlan()
    plan_body = ''
    expected = u''
    assert plan_reader.cleanPlanName( plan_body ,
                                      this_encoding = None ) == \
                                      expected

def test_nothing_to_do_for_guestAuth( capsys ):
    username = 'gspelvin'
    plan_reader = ReadPlan()
    plan_reader.guestAuth( username )
    out , err = capsys.readouterr()
    expected = '{} -|\n'.format( username )
    assert out == expected

