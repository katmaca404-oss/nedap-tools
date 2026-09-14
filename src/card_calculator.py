import struct
from typing import Dict, Any, Optional

class CardCalculator:
    """
    Farkli kart formatlari (Mifare CSN, Wiegand, Hex, Decimal) 
    arasinda donusum ve Nedap AEOS Identifier Type hesaplama araci.
    """

    @staticmethod
    def clean_hex(hex_str: str) -> str:
        """Hex stringi bosluk, : ve 0x gibi eklerden arindirir."""
        cleaned = hex_str.strip().replace(" ", "").replace(":", "").replace("-", "")
        if cleaned.lower().startswith("0x"):
            cleaned = cleaned[2:]
        return cleaned.upper()

    @classmethod
    def from_hex(cls, hex_input: str) -> Dict[str, Any]:
        """Ham Hex verisinden (CSN / UID) tum formatlari tureter."""
        raw_hex = cls.clean_hex(hex_input)
        
        # Cift haneli byte uzunlugu kontrolu
        if len(raw_hex) % 2 != 0:
            raw_hex = "0" + raw_hex
            
        byte_data = bytes.fromhex(raw_hex)
        
        # Big-Endian ve Little-Endian formatlari
        hex_be = raw_hex
        hex_le = byte_data[::-1].hex().upper()
        
        dec_be = int(hex_be, 16)
        dec_le = int(hex_le, 16)
        
        result = {
            "Input Hex": hex_input,
            "Hex (MSB / Big-Endian)": hex_be,
            "Hex (LSB / Little-Endian - Reverse)": hex_le,
            "Decimal (MSB)": dec_be,
            "Decimal (LSB / Reverse Dec)": dec_le,
            "Byte Length": len(byte_data),
        }
        
        # Eger 3 byte veya 4 byte ise Wiegand 26-bit olasiligi (FC + Card ID)
        if len(byte_data) in (3, 4):
            val_24 = dec_be & 0xFFFFFF
            fc = (val_24 >> 16) & 0xFF
            card_id = val_24 & 0xFFFF
            result["Wiegand 26-bit (H10301)"] = {
                "Facility Code (FC)": fc,
                "Card Number (CN)": card_id,
                "Formatted": f"FC: {fc} - CN: {card_id}"
            }
            
        return result

    @classmethod
    def from_wiegand26(cls, facility_code: int, card_number: int) -> Dict[str, Any]:
        """Wiegand 26-bit (FC + CN) degerinden Hex ve Decimal hesaplar."""
        raw_24 = ((facility_code & 0xFF) << 16) | (card_number & 0xFFFF)
        hex_val = f"{raw_24:06X}"
        return cls.from_hex(hex_val)

    @classmethod
    def from_decimal(cls, dec_val: int, byte_len: int = 4) -> Dict[str, Any]:
        """Decimal kart numarasindan Hex ve diger formatlari hesaplar."""
        hex_val = f"{dec_val:0{byte_len*2}X}"
        return cls.from_hex(hex_val)

def print_card_report(data: Dict[str, Any]):
    print("\n" + "="*50)
    print("      NEDAP AEOS IDENTIFIER HESAPLAMA RAPORU      ")
    print("="*50)
    for key, val in data.items():
        if isinstance(val, dict):
            print(f"\n[{key}]")
            for sub_k, sub_v in val.items():
                print(f"  -> {sub_k:28}: {sub_v}")
        else:
            print(f"{key:35}: {val}")
    print("="*50 + "\n")
