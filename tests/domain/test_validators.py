from pytest import raises

from domain.validators.hex_color import validate_hex_color
from domain.validators.revision_cycle_days import validate_revision_cycle_days

#
# - Hex Color -
#

def test_hex_color_5_digits():
    with raises(ValueError, match='The color format is not supported. Use a valid hex color format'):
        validate_hex_color('#FFFFA')

def test_hex_color_7_digits():
    with raises(ValueError, match='The color format is not supported. Use a valid hex color format'):
        validate_hex_color('#FFFFAFF')

def test_hex_color_9_digits():
    with raises(ValueError, match='The color format is not supported. Use a valid hex color format'):
        validate_hex_color('#FFFFAFFAA')

def test_hex_color_3_digits():
    h = validate_hex_color('#FFA')
    assert h == '#ffa'

def test_hex_color_4_digits():
    h = validate_hex_color('#FFA9')
    assert h == '#ffa9'

def test_hex_color_6_digits():
    h = validate_hex_color('#FFA955')
    assert h == '#ffa955'

def test_hex_color_8_digits():
    h = validate_hex_color('#FFA955AA')
    assert h == '#ffa955aa'

#
# - Revision Cycle Days - 
#

def test_validate_revision_cycle_days_zero():
    with raises(ValueError, match='The revision cycle days must be > 0.'):
        validate_revision_cycle_days(0)

def test_validate_revision_cycle_days_negative():
    with raises(ValueError, match='The revision cycle days must be > 0.'):
        validate_revision_cycle_days(-1)

def test_validate_revision_cycle_days_positive():
    assert validate_revision_cycle_days(2) == 2
