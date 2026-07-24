from pytest import raises

from domain.value_objects.hex_color import HexColor
from domain.value_objects.email import Email
from domain.value_objects.password import HashedPassword

#
# --- HEX COLOR --- #
#

def test_hex_color_5_digits():
    with raises(ValueError):
        HexColor('#FFFFA')

def test_hex_color_7_digits():
    with raises(ValueError):
        HexColor('#FFFFAFF')

def test_hex_color_9_digits():
    with raises(ValueError):
        HexColor('#FFFFAFFAA')

def test_hex_color_3_digits():
    h = HexColor('#FFA')
    assert h.value == '#ffa'
    assert str(h) == '#ffa'

def test_hex_color_4_digits():
    h = HexColor('#FFA9')
    assert h.value == '#ffa9'
    assert str(h) == '#ffa9'

def test_hex_color_6_digits():
    h = HexColor('#FFA955')
    assert h.value == '#ffa955'
    assert str(h) == '#ffa955'

def test_hex_color_8_digits():
    h = HexColor('#FFA955AA')
    assert h.value == '#ffa955aa'
    assert str(h) == '#ffa955aa'

#
# --- EMAIL --- #
#

def test_email_without_at():
    with raises(ValueError):
        Email('example.com.br')

def test_email_without_domain():
    with raises(ValueError):
        Email('example@com')

def test_valid_email():
    e = Email('example@com.BR')
    assert e.value == "example@com.br"
    assert str(e) == "example@com.br"

#
# --- HASHED PASSWORD --- #
#

def test_hashed_password():
    p = HashedPassword('THIS IS MY PASSWORD')
    assert p.value == "THIS IS MY PASSWORD"
    assert str(p) == "THIS IS MY PASSWORD"
