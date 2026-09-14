from src.card_calculator import CardCalculator

def test_hex_conversion():
    res = CardCalculator.from_hex("01020304")
    assert res["Hex (MSB / Big-Endian)"] == "01020304"
    assert res["Hex (LSB / Little-Endian - Reverse)"] == "04030201"
    assert res["Decimal (MSB)"] == 16909060

def test_wiegand_26():
    # FC: 1, Card: 2 => 0x010002
    res = CardCalculator.from_wiegand26(1, 2)
    assert res["Wiegand 26-bit (H10301)"]["Facility Code (FC)"] == 1
    assert res["Wiegand 26-bit (H10301)"]["Card Number (CN)"] == 2
